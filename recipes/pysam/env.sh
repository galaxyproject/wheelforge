export CIBW_BEFORE_ALL_LINUX='yum install -y libcurl-devel zlib-devel bzip2-devel xz-devel && pip install cython'
export CIBW_SKIP='*-musllinux_* *-macosx_*'
