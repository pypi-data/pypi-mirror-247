![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.10|%203.11|%203.12&color=blue?style=flat-square&logo=python)
![PyPI version](https://badge.fury.io/py/xbool.svg?)

- [Introduction](#introduction)
- [Documentation](#documentation)
- [Install](#install)
- [Quick Start](#quick-start)
    * [bool_value](#bool_value)
    * [bool_env](#bool_env)
- [Licensing](#licensing)

# Introduction

General purpose bool/boolean utilities, extracting bools from strings.

Only two so far:

- `bool_value`, see **[bool_value docs](https://xyngular.github.io/py-xbool/latest/)**.
- `bool_env`, see **[bool_env docs](https://xyngular.github.io/py-xbool/latest/)**.

# Documentation

**[📄 Detailed Documentation](https://xyngular.github.io/py-xbool/latest/)** | **[🐍 PyPi](https://pypi.org/project/xbool/)**

# Install

```bash
# via pip
pip install xbool

# via poetry
poetry add xbool
```

# Quick Start

## bool_value

Generally converts objects to bool-values, special-casing strings
to use the built-in `distutils.util.strtobool` function to convert the string value
to a bool.

```python
from xbool import bool_value

# Convert string to bool
assert bool_value('true') is True
assert bool_value('false') is False

assert bool_value('y') is True
assert bool_value('n') is False

assert bool_value('on') is True
assert bool_value('off') is False

assert bool_value('t') is True
assert bool_value('f') is False

assert bool_value('yes') is True
assert bool_value('no') is False

assert bool_value('1') is True
assert bool_value('0') is False

# Any other string is generally considered False:
assert bool_value("some-other-string") is False

# Convert bools to bools:
assert bool_value(True) is True
assert bool_value(False) is False

# Generally, for non-strings, True-like objects return True:
some_object = object()
assert bool_value(some_object) is True

# And False-like objects return False:
assert bool_value(None) is False
```

## bool_env

Looks up environmental variable with passed in name.

Runs the env-var value though `bool_value` for you and returns the result.

Useful to easily get a bool-value from an environmental variable.

```python
from xbool import bool_env
import os

os.environ['SOME_ENV_VAR'] = "False"
assert bool_env('SOME_ENV_VAR') is False


os.environ['SOME_OTHER_ENV_VAR'] = "True"
assert bool_env('SOME_OTHER_ENV_VAR') is True
```


# Licensing

This library is licensed under the MIT-0 License. See the LICENSE file.
