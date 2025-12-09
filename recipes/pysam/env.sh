export CIBW_BEFORE_ALL_LINUX='yum install -y libcurl-devel zlib-devel bzip2-devel xz-devel && pip install cython'
export CIBW_BEFORE_ALL_MACOS='brew install -q samtools bcftools'
export CIBW_BUILD='cp314-*'
# Test files are not currently included in the sdist
export CIBW_TEST_COMMAND=
export CIBW_TEST_REQUIRES=
