export CIBW_SKIP='*-musllinux_* *-macosx_*'
export CIBW_ARCHS_LINUX='auto64'
export CIBW_BEFORE_ALL_LINUX='curl https://sh.rustup.rs -sSf | sh -s -- -y'
export CIBW_ENVIRONMENT_LINUX='PATH=$PATH:$HOME/.cargo/bin'
