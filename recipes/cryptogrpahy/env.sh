export CIBW_SKIP='*-musllinux_* *-macosx_*'
export CIBW_BEFORE_ALL_LINUX='yum install -y openssl11 openssl11-devel && curl https://sh.rustup.rs -sSf | sh -s -- -y'
export CIBW_ENVIRONMENT_LINUX='PATH=$PATH:$HOME/.cargo/bin'
export CIBW_BEFORE_BUILD_LINUX='export CFLAGS="$CFLAGS $(pkg-config --cflags openssl11)" && export LDFLAGS="$LDFLAGS $(pkg-config --libs openssl11)"'
