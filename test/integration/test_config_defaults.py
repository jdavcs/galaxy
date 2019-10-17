import pytest
from base.driver_util import GalaxyTestDriver
from collections import namedtuple


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

    for key, data in DRIVER.app.config.appschema.items():
        expected_value = get_expected(key, data)
        loaded_value = getattr(DRIVER.app.config, key)
        data = (expected_value, loaded_value)
        yield pytest.param(data)



def get_expected(key, data):
    return data.get('default')  #fix this




@pytest.mark.parametrize('data', get_config_data())
def test_config_option(data, driver):
    print(data)
    assert True
