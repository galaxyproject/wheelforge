Recipes and continuous integration (CI) to build [wheels](https://pythonwheels.com/)
for Python packages that don't provide them on [PyPI](https://pypi.org/).

A package recipe is a simple `meta.yaml` file (in [YAML](https://yaml.org) format), contained in a
dedicated subdirectory of `recipes/` , specifying the package name and version,
e.g. the recipe for Mercurial 6.1.1 would be in the file `recipes/mercurial/meta.yaml`
containing:

```yaml
---
name: mercurial
version: 6.1.1
```

When a recipe is added to this repository or updated, a CI job downloads from
PyPI the sdist archive for the specified package, and then builds the wheels
using either [cibuildwheel](https://cibuildwheel.readthedocs.io) (default) or
[build](https://pypa-build.readthedocs.io) (if it is a pure Python package
specified with `purepy: true` in the recipe).

At the end of the CI job, the wheels are uploaded to https://wheels.galaxyproject.org ,
a Python Package Repository used by the [Galaxy Project](https://galaxyproject.org).
