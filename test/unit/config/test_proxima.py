import pytest

#from proxima.demo import sample

from galaxy import config
from galaxy.config import BaseAppConfiguration
from galaxy.config import GalaxyAppConfiguration
from galaxy.config.schema import AppSchema


@pytest.fixture(scope="module")
def appconfig():
    return config.GalaxyAppConfiguration(override_tempdir=False)


def test_attribute(appconfig):
    assert not hasattr(appconfig, 'foo')
    appconfig._proximaconfig.foo = 42  # makes foo available on appconfig
    assert hasattr(appconfig, 'foo')
    assert appconfig.foo == 42
