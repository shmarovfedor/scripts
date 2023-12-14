# !/bin/bash

# Author: Fedor Shmarov
# Email: fedor.shmarov@newcastle.ac.uk

# This installs all necessary dependencies for Ubuntu
setup_ubuntu() {
sudo apt-get update
sudo apt-get install \
  build-essential git gperf libgmp-dev cmake bison curl flex g++-multilib \
  linux-libc-dev libboost-all-dev libtinfo-dev ninja-build python3-setuptools \
  unzip wget python3-pip openjdk-8-jre
}

# This downloads and locally installs Clang/LLVM into CLANG_LLVM_ESBMC_ROOT_DIR
setup_clang_llvm() {
wget ${CLANG_LLVM_SRC_URL} -O ${CLANG_LLVM_DOWNLOAD_PATH}
mkdir -p ${CLANG_LLVM_DEST_DIR}
tar xfJ ${CLANG_LLVM_DOWNLOAD_PATH} --strip-components=1 -C ${CLANG_LLVM_DEST_DIR}
rm ${CLANG_LLVM_DOWNLOAD_PATH}
}

# This downloads and sets up Boolector
setup_boolector() {
git clone --depth=1 --branch=3.2.2 https://github.com/boolector/boolector ${BOOLECTOR_SRC_DIR}
cd ${BOOLECTOR_SRC_DIR}
./contrib/setup-lingeling.sh 
./contrib/setup-btor2tools.sh
./configure.sh --prefix ${BOOLECTOR_RELEASE_DIR}
cd build
make -j9
make install
}

# This downloads and builds ESBMC
setup_esbmc() {
rm -rf ${ESBMC_REPO_DIR}
git clone --branch=${ESBMC_REPO_BRANCH} ${ESBMC_REPO_URL} ${ESBMC_REPO_DIR}
mkdir -p ${ESBMC_REPO_DIR}/build
cmake -B${ESBMC_REPO_DIR}/build ${ESBMC_REPO_DIR} -GNinja \
  -DBUILD_TESTING=On -DENABLE_REGRESSION=On \
  -DClang_DIR=${CLANG_LLVM_DEST_DIR} \
  -DLLVM_DIR=${CLANG_LLVM_DEST_DIR} \
  -DBoolector_DIR=${BOOLECTOR_RELEASE_DIR} \
  -DCMAKE_INSTALL_PREFIX:PATH=${ESBMC_INSTALL_DIR}
cmake --build ${ESBMC_REPO_DIR}/build
ninja install -C ${ESBMC_REPO_DIR}/build
}

# This generates a "quick build" script inside the ESBMC build directory
generate_quick_build_script() {
echo \
"# !/bin/bash
cmake -B${ESBMC_REPO_DIR}/build ${ESBMC_REPO_DIR} -GNinja \
-DBUILD_TESTING=On -DENABLE_REGRESSION=On \
-DClang_DIR=${CLANG_LLVM_DEST_DIR} \
-DLLVM_DIR=${CLANG_LLVM_DEST_DIR} \
-DBoolector_DIR=${BOOLECTOR_RELEASE_DIR} \
-DCMAKE_INSTALL_PREFIX:PATH=${ESBMC_INSTALL_DIR}
cmake --build ${ESBMC_REPO_DIR}/build
ninja install -C ${ESBMC_REPO_DIR}/build" > ${ESBMC_REPO_DIR}/build/quick_build.sh
chmod +x ${ESBMC_REPO_DIR}/build/quick_build.sh
}

print_usage() {
echo \
"Usage: ./build.sh -i <esbmc-repo-url> -b <esbmc-branch-to-checkout> -d <esbmc-destination-directory>

  -b   ESBMC branch to checkout (default: ${ESBMC_REPO_BRANCH})
  -d   path to the directory where ESBMC and all its dependencies will be built (default: ${ESBMC_ROOT_DIR})
  -h   prints this message
  -i   URL for the ESBMC Git repository (default: ${ESBMC_REPO_URL})
"
}


# The execution flow starts here

# Setting some default values
CLANG_LLVM_SRC_URL="https://github.com/llvm/llvm-project/releases/download/llvmorg-11.0.0/clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04.tar.xz"
ESBMC_ROOT_DIR=$(realpath esbmc)
ESBMC_REPO_URL="https://github.com/esbmc/esbmc"
ESBMC_REPO_BRANCH="master"

# Parsing command line options
while getopts d:b:i:h flag
do
    case "${flag}" in
    i) ESBMC_REPO_URL=${OPTARG};;
    b) ESBMC_REPO_BRANCH=${OPTARG};;
    d) ESBMC_ROOT_DIR=${OPTARG};;
    h) print_usage; exit 0;;
    *) exit 1;;
    esac
done

# Setting up the rest of the paths
ESBMC_ROOT_DIR=$(realpath ${ESBMC_ROOT_DIR})
ESBMC_REPO_DIR="${ESBMC_ROOT_DIR}/esbmc"
ESBMC_INSTALL_DIR="${ESBMC_ROOT_DIR}/release"
CLANG_LLVM_DEST_DIR="${ESBMC_ROOT_DIR}/clang"
CLANG_LLVM_DOWNLOAD_PATH="${ESBMC_ROOT_DIR}/clang_llvm_download.tar.xz"
BOOLECTOR_SRC_DIR="${ESBMC_ROOT_DIR}/boolector"
BOOLECTOR_RELEASE_DIR="${ESBMC_ROOT_DIR}/boolector-release"

# Installing dependencies for Ubuntu
setup_ubuntu

# Remove the ESBMC root directory in it exists
rm -rf ${ESBMC_ROOT_DIR}

# Creating the destination folder
mkdir -p ${ESBMC_ROOT_DIR}

# Setting up Clang/LLVM
setup_clang_llvm

# Setting up Boolector
setup_boolector

# Setting up ESBMC
setup_esbmc

# Generating the "quick build" script
generate_quick_build_script

