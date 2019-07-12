from os import environ

from .utility import modify_environ


def test_modify_environ__restore():
    key0, val0 = 'foo_678363', 'to preserve'
    environ[key0] = val0

    with modify_environ({}):
        pass
    assert environ[key0] == val0  # existing key/val unchanged

    del environ[key0]


def test_modify_environ__add_and_restore():
    key0, val0 = 'foo_678363', 'to preserve'
    environ[key0] = val0

    key1, val1 = 'foo_542644', 'to add'
    values = {key1: val1}

    assert key1 not in environ  # ensure key to add does not exist
    with modify_environ(values):
        assert environ[key0] == val0  # key/val unchanged
        assert environ[key1] == val1  # new key/val added
    assert key1 not in environ  # new key removed
    assert environ[key0] == val0  # existing key/val unchanged

    del environ[key0]


def test_modify_environ__update_and_restore():
    key0, val0 = 'foo_678363', 'to preserve'
    environ[key0] = val0

    val_update = 'value to update'
    values = {key0: val_update}

    with modify_environ(values):
        assert environ[key0] == val_update  # value updated
    assert environ[key0] == val0  # value restored

    del environ[key0]


def test_modify_environ__remove_and_restore():
    key0, val0 = 'foo_678363', 'to preserve'
    key1, val1 = 'foo_542644', 'to remove'
    environ[key0] = val0
    environ[key1] = val1

    values = {}
    remove = [key1]

    with modify_environ(values, remove):
        assert environ[key0] == val0  # key/val unchanged
        assert key1 not in environ  # key removed

    assert environ[key0] == val0  # value restored
    assert environ[key1] == val1  # value restored

    del environ[key0]
    del environ[key1]



#def test_modify_environ__update_and_restore():
#
#    key, val = 'foo_678363', '42'
#    environ[key] = val  # Preload to test updating
#    val_updated = 'dodo'
#
#    values = {key: val_updated}
#    remove = []
#
#    assert key1 not in environ
#    assert key2 in environ
#    with modify_environ(values, remove):
#        assert environ[key1] == val1
#        assert environ[key2] == val2_updated
#    assert key1 not in environ  # key1 should be removed
#    assert environ[key2] == val2  # key2 should be restored to old value
#
#    del environ[key2]  # cleanup
#
#
#def test_modify_environ_remove_and_restore():
#    pass
#
#
#def test_modify_environ_add_remove_and_restore():
#    pass


#def test_environ_contextmanager_env_restored():
#    """ os.environ must be preserved across calls to __environ """
#    key, val = 'foo_test_678363', '42'
#    os.environ[key] = val
#    with __environ({}, []):
#        pass
#    assert os.environ[key] == val
#    del os.environ[key]
