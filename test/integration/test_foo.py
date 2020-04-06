import os
from collections import namedtuple
from datetime import timedelta

import pytest

from galaxy.util import listify
from galaxy_test.driver.driver_util import GalaxyConfigTestDriver


def get_config():
    driver = GalaxyConfigTestDriver()
    driver.setup()
    return driver.app.config

def test_one():
#     config = get_config()
# sanity check; must be triggered by keyword 'foo'
    assert True
