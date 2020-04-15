import os
from collections import namedtuple
from datetime import timedelta

import pytest

from galaxy.util import listify
from galaxy_test.driver.driver_util import GalaxyConfigTestDriver

OptionData = namedtuple('OptionData', ('key', 'expected', 'loaded'))


@pytest.fixture(scope='module')
def driver(request):
    request.addfinalizer(DRIVER.tear_down)
    return DRIVER


def create_driver():
    global DRIVER
    DRIVER = GalaxyConfigTestDriver()
    DRIVER.setup()


def get_config_data():
    create_driver()  # create + setup DRIVER
    items = ((k, v) for k, v in DRIVER.app.config.schema.app_schema.items())
    for key, data in items:
        data = OptionData(key=key, expected='42', loaded='42')
        yield pytest.param(data)


def get_key(option_data):
    return option_data.key

@pytest.mark.parametrize('data', get_config_data(), ids=get_key)
def test_config_option(data, driver):
    assert data.expected == data.loaded
