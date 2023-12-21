from typing import Any
import os

__version__ = '1.1.0'


def _strtobool(val) -> bool:
    """
    Copied from the `distutils.util` module, due to python 3.12 not including `distutils` in
    standard library anymore.

    Convert a string representation of truth to True or False.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))


def bool_value(value: Any):
    """
    Does our best to get the 'bool' value from any other value.
    If you pass in a string, we use the built-in `distutils.util.strtobool` function to parse bool
    values from strings/text.
    (ie: string `'false'` would return `False`)

    Generally, if the value passed in is one of these, it's considered `True`:

    - For Strings (after stripping any leading/training white-space):
        - "t"
        - "True"
        - "T"
        - "1"
        - "true"
        - "on"
    - For `bool`:
        - We simply return whatever the passed-in bool is.
    - Other Types Of Objects:
        - If object is True-like (where object's `__bool__()` value is True).

    Otherwise, a `False` will be returned (ie: if string contains 'false', we return False).

    If any `ValueError` is raised while trying to get bool-value from any object,
    will return `False`.

    Examples:

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

    """
    try:
        if value is None:
            return False

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            # Ensure we have a string and strip left/right sides of any white space.
            value = value.strip().lower()
            if len(value) == 0:
                return False
            return _strtobool(value)

        # If we get to this point we just ask the object for it's bool value.
        return bool(value)
    except ValueError:
        return False


def bool_env(env_var_name: str):
    """
    Given an environmental variable name, will get env-var value and run it though `bool_value`,
    returning a bool-representative value from the environmental variable.

    If the en-var is set to one of these values
    (after stripping any leading/trailing whitespace), we will consider the env-var `True`:

    - "t"
    - "True"
    - "T"
    - "1"
    - "true"

    Otherwise, the env-var is False,

    If the env-var does not exist, will return `False`.

    ```python
    from xbool import bool_env
    import os

    os.environ['SOME_ENV_VAR'] = "False"
    assert bool_env('SOME_ENV_VAR') is False


    os.environ['SOME_OTHER_ENV_VAR'] = "True"
    assert bool_env('SOME_OTHER_ENV_VAR') is True
    ```

    Args:
        env_var_name: Environmental variable name to convert to a bool-value.

    Returns:
        bool: Boolean representative value of the environmental variable.
    """
    return bool_value(os.environ.get(env_var_name))
