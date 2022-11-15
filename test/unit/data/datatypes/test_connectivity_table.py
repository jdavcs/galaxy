import os

import pytest

from galaxy.datatypes.tabular import ConnectivityTable
from galaxy.util import galaxy_directory


@pytest.fixture
def dataset():
    class MockDataset:
        file_name = os.path.join(galaxy_directory(), "test-data/1.ct")

    return MockDataset()


@pytest.fixture
def make_trans():
    class Stub:
        pass

    class StubTransaction:
        def __init__(self, chunk_size):
            self.app = Stub()
            self.app.config = Stub()
            self.app.config.display_chunk_size = chunk_size

    return StubTransaction


def test_get_chunk__chunk_size_greater_than_file(dataset, make_trans):
    dt = ConnectivityTable()
    chunk_size = 1000
    trans = make_trans(chunk_size)
    chunk = dt.get_chunk(trans, dataset, 0)
    assert chunk == '{"ck_data": "363\\ttmRNA\\n1\\tG\\t0\\t2\\t359\\t1\\n2\\tG\\t1\\t3\\t358\\t2\\n", "ck_index": 1}'


def test_get_chunk__chunk_size_less_than_line(dataset, make_trans):
    dt = ConnectivityTable()
    chunk_size = 9
    trans = make_trans(chunk_size)

    # reads line 1
    chunk = dt.get_chunk(trans, dataset, 0)
    assert chunk == '{"ck_data": "363\\ttmRNA\\n", "ck_index": 1}'

    # reads line 2
    chunk = dt.get_chunk(trans, dataset, 1)
    assert chunk == '{"ck_data": "1\\tG\\t0\\t2\\t359\\t1\\n", "ck_index": 2}'

    # reads line 3
    chunk = dt.get_chunk(trans, dataset, 2)
    assert chunk == '{"ck_data": "2\\tG\\t1\\t3\\t358\\t2\\n", "ck_index": 3}'
