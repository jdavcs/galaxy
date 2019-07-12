"""
Unit test utilities.
"""
import textwrap
from contextlib import contextmanager
from os import environ


def clean_multiline_string(multiline_string, sep='\n'):
    """
    Dedent, split, remove first and last empty lines, rejoin.
    """
    multiline_string = textwrap.dedent(multiline_string)
    string_list = multiline_string.split(sep)
    if not string_list[0]:
        string_list = string_list[1:]
    if not string_list[-1]:
        string_list = string_list[:-1]
    # return '\n'.join( docstrings )
    return ''.join([(s + '\n') for s in string_list])

@contextmanager
def modify_environ(values, keys_to_remove=[]):
    """
    Modify the environment for a test, adding/updating values in dict `values` and
    removing any environment variables mentioned in list `keys_to_remove`.
    """
    new_keys = set(values.keys()) - set(environ.keys())
    old_environ = environ.copy()
    try:
        environ.update(values)
        for key in keys_to_remove:
            try:
                del environ[key]
                new_keys.remove(key)  # Because key no longer exists
            except KeyError:
                pass
        yield
    finally:
        for key in new_keys:
            del environ[key]
        environ.update(old_environ)


#@contextmanager
#def modify_environ():
#    pass
#
#def __environ(values, keys_to_remove=[]):
#    """
#    Modify the environment for a test, adding/updating values in dict `values` and
#    removing any environment variables mentioned in list `keys_to_remove`.
#    """
#
## https://github.com/pypa/virtualenv/blob/28839085ff8a5a770bb4a8c52158d763760c89c1/virtualenv.py#L897
#    if values or keys_to_remove: # only do stuff if we want to modify the env.
#
#
#
#
#
#    old_environ = environ.copy()  # Save current environment
#    new_keys = set(values.keys()) - set(environ.keys())
#
#    environ.update(values)
#    for key in keys_to_remove:
#        if key in environ:
#            del environ[key]
#            new_keys.remove(key)  # Because key no longer exists
#
#    print('exec 1')
#    yield
#    print('exec 2')
#
#
#    environ.clear()
#    environ.update(old_environ)
#




__all__ = (
    "clean_multiline_string",
)
