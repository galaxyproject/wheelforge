export CIBW_SKIP='*-macosx_*'
export CIBW_BEFORE_ALL_LINUX='yum install -y openssl-devel && curl https://sh.rustup.rs -sSf | sh -s -- -y'
export CIBW_ENVIRONMENT_LINUX="PATH=$PATH:$HOME/.cargo/bin"
