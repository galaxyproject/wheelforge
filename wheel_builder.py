#!/usr/bin/python3
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import requests
import yaml

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("The script requires exactly one argument")
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        raise Exception(f"{folder} is not a directory")

    # Load the package metadata from meta.y(a)ml
    meta_file = os.path.join(folder, "meta.yaml")
    if not os.path.exists(meta_file):
        alternative_meta_file = os.path.join(folder, "meta.yml")
        if not os.path.exists(alternative_meta_file):
            raise Exception(f"Missing {meta_file} file")
        else:
            meta_file = alternative_meta_file
    with open(meta_file) as f:
        meta = yaml.safe_load(f)
    package_name = meta["name"]
    package_version = meta["version"]
    is_package_pure = meta.get("purepy", False)

    # Find the sdist url using the PyPI warehouse API https://warehouse.pypa.io/api-reference/json.html
    pypi_url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
    response = requests.get(pypi_url)
    response.raise_for_status()
    pypi_metadata = response.json()
    sdist_url_dicts = [url_dict for url_dict in pypi_metadata["urls"] if url_dict["packagetype"] == "sdist"]
    if not sdist_url_dicts:
        raise Exception(f"Missing sdist url in response from {pypi_url}")
    if len(sdist_url_dicts) > 1:
        raise Exception(f"Multiple sdist urls in response from {pypi_url}")
    sdist_filename = sdist_url_dicts[0]["filename"]
    sdist_url = sdist_url_dicts[0]["url"]

    # Download the sdist
    print(f"Downloading {sdist_url} ... ", end="", flush=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        sdist_filepath = os.path.join(temp_dir, sdist_filename)
        with requests.get(sdist_url, stream=True) as response:
            response.raise_for_status()
            with open(sdist_filepath, "wb") as f:
                for chunk in response.iter_content():
                    f.write(chunk)
        print("Done", flush=True)

        # Generate the commands to run
        check_commands = []
        commands = []
        env_file = os.path.join(folder, "env.sh")
        if os.path.exists(env_file):
            commands.append(f". '{env_file}'")
        if is_package_pure:
            tar_temp_dir = Path(tempfile.mkdtemp(dir=temp_dir))
            with tarfile.open(sdist_filepath) as tar:
                tar.extractall(path=tar_temp_dir)

            try:
                (extracted_sdist_dir,) = tar_temp_dir.iterdir()
            except ValueError:
                raise Exception("Invalid sdist: didn't contain a single directory")

            commands.append(f"python3 -m build --wheel --outdir wheelhouse '{extracted_sdist_dir}'")
        else:
            check_commands = commands.copy()
            check_commands.append("cibuildwheel --print-build-identifiers")
            commands.append(f"cibuildwheel --output-dir wheelhouse '{sdist_filepath}'")
        joined_command = " && ".join(commands)
        joined_check_command = " && ".join(check_commands)

        # Run builder check commands
        if check_commands:
            try:
                check_cp = subprocess.run(
                    joined_check_command,
                    shell=True,
                    check=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
            except subprocess.CalledProcessError as exc:
                raise Exception(f"Build platform check command failed: {exc.stdout}")
            if not check_cp.stdout:
                print("No platforms to build for on this builder, exiting...")
                sys.exit(0)

        # Run the commands
        print(f"Executing: {joined_command}")
        subprocess.run(joined_command, shell=True, check=True)
