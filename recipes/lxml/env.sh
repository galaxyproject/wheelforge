# lxml 6.1.3 still supports Python 3.8 but doesn't ship CPython 3.8 wheels on PyPI
export CIBW_BUILD='cp38-*'
# lxml's pyproject.toml lists all Linux archs (incl. ppc64le and riscv64), only build the native one
export CIBW_ARCHS_LINUX='auto64'
# lxml's macOS wheels for CPython 3.8 are not universal2, see https://bugs.launchpad.net/lxml/+bug/2055404
export CIBW_ARCHS_MACOS='x86_64'
