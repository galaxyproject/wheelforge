export CIBW_SKIP='*-musllinux_* *-macosx_* *_i686'
export CIBW_BEFORE_ALL_LINUX='yum install -y openssl11 openssl11-devel && cp /usr/lib64/pkgconfig/openssl11.pc /usr/lib64/pkgconfig/openssl.pc && curl https://sh.rustup.rs -sSf | sh -s -- -y'
export CIBW_ENVIRONMENT_LINUX='PATH=$PATH:$HOME/.cargo/bin'
