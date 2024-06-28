## Using Rust from Python


PyO3 can be used to generate a native Python module. The easiest way to try this out for the first time is to use maturin. maturin is a tool for building and publishing Rust-based Python packages with minimal configuration. The following steps install maturin, use it to generate and build a new Python package, and then launch Python to import and execute a function from the package.

First, follow the commands below to create a new directory containing a new Python virtualenv, and install maturin into the virtualenv using Python's package manager, pip:

```
$ mkdir native
$ cd native
$ python -m venv .env
$ source .env/bin/activate
$ pip install maturin
$ maturin init
```

## Compile and test
To compile the Rust binding just execute
```
$ maturin develop
```
This can take a while. When finished, you can test it from python:
```
$ python
$ >>> import native
$ >>> native.substitute(1, 2)
```

## Troubleshooting
#### Library not loaded: /usr/local/opt/z3/lib/libz3.4.12.dylib

Either install via Homebrew:
```
$ brew install z3
$ brew install zstd
````

If error persists, download a version for your platform from https://github.com/Z3Prover/z3/releases and copy it to /usr/local/lib/.