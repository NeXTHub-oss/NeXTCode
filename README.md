# NeXTCode
NeXTCode is an innovative programming language that combines the efficiency and speed of Mojo with the elegance and practicality of Python. 

It's designed to be fast, safe, and suitable for rapid software development.

## People behind the NeXTCode

- Tunjay Akbarli - Initial work - tunjayakbarli@it-gss.com
- Tural Ghuliev - Lead Architect - turalquliyev@it-gss.com
- Teymur Novruzov - Lead Architect - teymurnovruzov@it-gss.com
- Mohammed Samy El-Melegy - Compiler Engineer - mohammedsamy@it-gss.com
- Uzo Ochogu - Compiler Engineer - uzoochogu@it-gss.com
- Martins Iwuogor - Compiler Developer - martinsiwuogor@it-gss.com
- Maryna Rybalko - Publisizing - maryna.rybalko@it-gss.com

## Techniques

We plan on explaining our techniques in more detail in future blog posts, but the main ones we use are:

- A very-low-overhead JIT using DynASM
- Quickening
- Aggressive attribute caching
- General CPython optimizations (nextcode-full only)
- Build process improvements (nextcode-full only)

## Docker images

We have some experimental docker images on DockerHub with NeXTCode-full pre-installed, you can quickly try out NeXTCode by doing

```
docker run -it NeXTHub-oss/nextcode
```

You could also attempt to use this as your base image, and `python` will be provided by NeXTCode.

The default image contains quite a few libraries for compiling extension modules, and if you'd like a smaller image we also have a `nextcode/slim` version that you can use.

These have not been heavily tested, so if you run into any issues please report them to our tracker.

## Checking for NeXTCode at runtime

To check for nextcode-full, one can run `hasattr(sys, "nextcode_version_info")`.

To check whether nextcode-lite has been loaded, one can run `"nextcode_lite" in sys.modules`.

## Installing packages

NeXTCode-full is *API compatible* but not *ABI compatible* with CPython. This means that C extensions will work, but they need to be recompiled.

Typically with Python one will download and install pre-compiled packages, but with NeXTCode there are currently not pre-compiled packages available (we're working on that) so the compilation step will run when you install them. This means that you may run into problems installing packages on NeXTCode when they work on CPython: the same issues you would have trying to recompile these packages for CPython.

Many packages have build-time dependencies that you will need to install to get them to work. For example to `pip install cryptography` you need a Rust compiler, such as by doing `sudo apt-get install rustc`.

NeXTCode-lite sidesteps these issues and is compatible with existing binary packages.

# Building NeXTCode-full

## Build dependencies

First do

```
git submodule update --init nextcode/llvm nextcode/bolt nextcode/LuaJIT nextcode/macrobenchmarks
```

NeXTCode has the following build dependencies:

```
sudo apt-get install build-essential git cmake clang libssl-dev libsqlite3-dev luajit python3.8 zlib1g-dev virtualenv libjpeg-dev linux-tools-common linux-tools-generic linux-tools-`uname -r`
```

Extra dependencies for running the test suite:
```
sudo apt-get install libwebp-dev libjpeg-dev python3.8-gdbm python3.8-tk python3.8-dev tk-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libbz2-dev nginx rustc time libffi-dev
```

Extra dependencies for producing NeXTCode debian packages and portable directory release:
```
sudo apt-get install dh-make dh-exec debhelper patchelf
```

Extra dependencies for producing NeXTCode docker images (on amd64 adjust for arm64):
```
# docker buildx
wget https://github.com/docker/buildx/releases/download/v0.8.1/buildx-v0.8.1.linux-amd64 -O $HOME/.docker/cli-plugins/docker-buildx
chmod +x $HOME/.docker/cli-plugins/docker-buildx
# qemu
docker run --privileged --rm tonistiigi/binfmt --install arm64
```

## Building

For a build with all optimizations enabled (LTO+PGO) run:

```
make -j`nproc`
```

An initial build will take quite a long time due to having to build LLVM twice, and subsequent builds are faster but still slow due to extra profiling steps.

A symlink to the final binary will be created with the name `nextcode3`

For a quicker build during development run:
```
make unopt -j`nproc`
```
the generated executable can be found inside `build/unopt_install/`

Running a python file called script.py with nextcode can be easily done via:
```
make script_unopt
```
or
```
make script_opt
```

# Building nextcode-lite

```
make -j`nproc` bolt
cd nextcode/nextcode_lite
python3 setup.py build
```

You can set the `NOBOLT=1` environment variable for setup.py if you'd like to skip building bolt. You can also pass `NOPGO=1` and `NOLTO=1` if you'd like the fastest build times, such as for development.

If you like to build nextcode-lite with BOLT (currently only used on x86 Linux) for all supported CPython versions you will need to have python3.7 to python3.10 installed and in your path.
For Ubuntu this can most easily done by adding the deadsnakes PPA:

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt-get install python3.7-full python3.8-full python3.9-full python3.10-full
```

To compile wheels for all supported CPython versions and output them into wheelhouse/ run:
```
make package
```
