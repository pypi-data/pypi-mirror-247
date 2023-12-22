LiteSync for Python3
====================

This is a wrapper library to use [LiteSync](http://litesync.io) on Python 3

It is based on [pysqlite3](https://github.com/coleifer/pysqlite3)


### Additional features:  (compared to Python's sqlite3 module)

* User-defined window functions (requires SQLite >= 3.25)
* Flags and VFS an be specified when opening connection
* Incremental BLOB I/O, [bpo-24905](https://github.com/python/cpython/pull/271)
* Improved error messages, [bpo-16379](https://github.com/python/cpython/pull/1108)
* Simplified detection of DML statements via `sqlite3_stmt_readonly`.
* Sqlite native backup API (also present in standard library 3.7 and newer).


Installation
------------

You must install some LiteSync library for this one to work. It can be either
pre-compiled binaries or you can compile it by yourself. You can start with
the [free version](http://litesync.io/en/download.html).


## Installing with pip

```
pip install litesync
```


## Cloning and Building

Optionally you can clone the repo and build it:

```
git clone --depth=1 https://gitlab.com/litesync/litesync-python3
cd litesync-python3
python setup.py build
```
