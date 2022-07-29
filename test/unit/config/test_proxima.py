import pytest

import proxima

from galaxy import config
from galaxy.config import BaseAppConfiguration
from galaxy.config import GalaxyAppConfiguration
from galaxy.config.schema import AppSchema


@pytest.fixture(scope="module")
def appconfig():
    pm = proxima.Proxima()
    pm.config.foo = 42
    return config.GalaxyAppConfiguration(proxima_manager=pm, override_tempdir=False)


def test_attribute(appconfig):
    assert appconfig.foo == 42
