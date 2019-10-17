import os
import pytest
from base.driver_util import GalaxyTestDriver
from collections import namedtuple


OptionData = namedtuple('OptionData', 'expected, loaded')


@pytest.fixture(scope='module')
def driver(request):
    request.addfinalizer(DRIVER.tear_down)
    return DRIVER


def create_driver():
    global DRIVER
    DRIVER = GalaxyTestDriver()
    DRIVER.setup()


def get_config_data():
    create_driver()
    parent_dirs = load_parent_dirs()

    for key, data in DRIVER.app.config.appschema.items():
        expected_value = get_expected(key, data, parent_dirs)
        loaded_value = getattr(DRIVER.app.config, key)

        data = OptionData(expected=expected_value, loaded=loaded_value)

        #data = (expected_value, loaded_value)
        yield pytest.param(data)


def load_parent_dirs():
    parent_dirs = {
        'root_dir': DRIVER.app.config.root,
        'config_dir': DRIVER.app.config.config_dir,
        'data_dir': DRIVER.app.config.data_dir,
        'tool_data_path': DRIVER.app.config.tool_data_path,
    }
    return parent_dirs


def get_expected(key, data, parent_dirs):
    value = data.get('default')

    parent = data.get('path_resolves_to')
    if parent:
        value = parent_dirs[parent]

    return value


@pytest.mark.parametrize('data', get_config_data())
def test_config_option(data, driver):
    print(data)
    assert data.expected == data.loaded
