# Rust implementation of the substitute logic
## Using Rust from Python

PyO3 can be used to generate a native Python module. The easiest way to try this out for the first time is to use maturin. maturin is a tool for building and publishing Rust-based Python packages with minimal configuration. The following steps install maturin, use it to generate and build a new Python package, and then launch Python to import and execute a function from the package.

First, follow the commands below to create a new directory containing a new Python virtualenv, and install maturin into the virtualenv using Python's package manager, pip:

```
$ mkdir rssubstitute
$ cd rssubstitute
$ python -m venv .env
$ source .env/bin/activate
$ pip install maturin
$ maturin init
```

## Compile and test
The toolchain uses Maturinn to create a Pythonn wheel. For more information about Maturin see the guide: https://www.maturin.rs/

To compile the Rust binding execute
```
$ maturin develop
```
Or just use the Makefile
```
$ make dev
```

This can take a while. When finished, you can test it from python:
```
$ python
$ >>> import rssubstitute
$ >>> rssubstitute.substitute("#{1 + 1}", {})
```
The unit test can be executed with 
```
$ make test
```

## Troubleshooting
#### Library not loaded: /usr/local/opt/z3/lib/libz3.4.12.dylib

Either install via Homebrew:
```
$ brew install z3
$ brew install zstd
````

If error persists, download a version for your platform from https://github.com/Z3Prover/z3/releases and copy it to /usr/local/lib/.

#### Testing: Linker issue like "Symbol not found"

Run the test without features:

`cargo test --no-default-features`