import pytest
from galaxy_test.driver.driver_util import GalaxyConfigTestDriver
from galaxy_test.driver.driver_util import GalaxyTestDriver

from collections import namedtuple

OptionData = namedtuple('OptionData', ('key', 'expected', 'loaded'))


@pytest.fixture(scope='module')
def driver(request):
    request.addfinalizer(DRIVER.tear_down)
    return DRIVER


def create_driver():
    # Same approach as in functional/test_toolbox_pytest.py:
    # We setup a global driver, so that the driver fixture can tear down the driver.
    # Ideally `create_driver` would be a fixture and clean up after the yield,
    # but that's not compatible with the use use of pytest.mark.parametrize:
    # a fixture is not directly callable, so it cannot be used in place of get_config_data.
    global DRIVER
    DRIVER = GalaxyConfigTestDriver()
    #DRIVER = GalaxyTestDriver()
    DRIVER.setup()


def get_config_data():
    create_driver()
    items = ((k, v) for k, v in DRIVER.app.config.schema.app_schema.items())
    for key, data in items:
        expected_value = data.get('default')
        loaded_value = getattr(DRIVER.app.config, key)
        data = OptionData(key=key, expected=expected_value, loaded=loaded_value)
        yield pytest.param(data)


@pytest.mark.parametrize('data', get_config_data())
def test_foo(data, driver):  # 'data' is the OptionData NamedTuple with expected/loaded/key members
    assert True
    #print(data.key, data.expected)
    #print('\t' + str(data.loaded))
    #assert data.expected == data.loaded
