#!/usr/bin/python3
import os
import subprocess
import sys

import yaml
import requests

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
    sdist_file = sdist_url_dicts[0]["filename"]
    sdist_url = sdist_url_dicts[0]["url"]

    # Download the sdist
    print(f"Downloading {sdist_url} ... ", end="", flush=True)
    with requests.get(sdist_url, stream=True) as response:
        response.raise_for_status()
        with open(sdist_file, "wb") as f:
            for chunk in response.iter_content():
                f.write(chunk)
    print("Done")

    # Generate the commands to run
    commands = []
    env_file = os.path.join(folder, "env.sh")
    if os.path.exists(env_file):
        commands.append(f". {env_file}")
    commands.append(f"cibuildwheel --output-dir wheelhouse {sdist_file}")
    full_command = " && ".join(commands)

    try:
        print(f"Executing: {full_command}")
        subprocess.run(full_command, shell=True, check=True)
    finally:
        # Clean up
        os.remove(sdist_file)
