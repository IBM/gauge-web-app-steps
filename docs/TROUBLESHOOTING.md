# Troubleshooting

Find Error messages in the terminal output, or in `\$GAUGE\_PROJECT\_ROOT/logs/gauge.log.`

## Windows Users

This module also works on Windows, but it was developed on Mac/Linux.\
It is recommended to use a Unix Shell, like [Git Bash](https://gitforwindows.org/).\
It is also recommended to install [Python from the Windows App Store](https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5).

## Issues with GRPCIO

**Error message:**

```
ImportError: dlopen(/\<installation-path>/site-packages/grpc/_cython/cygrpc.cpython-310-darwin.so, 0x0002): tried: ‘/\<installation-path>/site-packages/grpc/_cython/cygrpc.cpython-310-darwin.so’ (mach-o file, but is an incompatible architecture (have ‘x86_64’, need ‘arm64e’)), ‘/usr/local/lib/cygrpc.cpython-310-darwin.so’ (no such file), ‘/usr/lib/cygrpc.cpython-310-darwin.so’ (no such file)
```

Type the following:

```shell
pip install --no-binary :all: grpcio --ignore-installed
```

**Error message:**

```
WARNING: Ignoring invalid distribution -rpcio (/\<installation-path>/site-packages)
```

Type the following, one after the other:

```shell
pip install --upgrade pip
python -m pip install --upgrade setuptools
pip install --no-cache-dir --force-reinstall -Iv grpcio==1.68.1
```

## Issues with Protobuf

**Error message:**

```
08-07-2022 13:11:53.441 [python] [ERROR] TypeError: Descriptors cannot not be created directly.
08-07-2022 13:11:53.441 [python] [ERROR] If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
08-07-2022 13:11:53.441 [python] [ERROR] If you cannot immediately regenerate your protos, some other possible workarounds are: > > 08-07-2022 13:11:53.441 [python] [ERROR] 1. Downgrade the protobuf package to 3.20.x or lower.
```

Type the following:

```shell
pip install protobuf==3.20.1
```

## Windows and Appium / Selenium

On Windows machines, the installation of the Selenium or Appium dependencies might fail.
The Appium tar package must be downloaded from here:

**https://pypi.org/project/Appium-Python-Client/**

Check the required version from the file requirements.txt
Download the Appium-Python-Client-x.x.x.tar.gz

Untar it:

```shell
tar -xvf Appium-Python-Client*
```

Install it:

```shell
python setup.py install
```

Then, try again to install this module.
