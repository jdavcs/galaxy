import os

import pytest

from galaxy.datatypes.tabular import ConnectivityTable
from galaxy.util import galaxy_directory


@pytest.fixture
def test_file_path():
    return os.path.join(galaxy_directory(), "test-data/1.ct")


@pytest.fixture
def test_file_length(test_file_path):
    with open(test_file_path) as f:
        return len(f.read())


@pytest.fixture
def dataset(test_file_path):
    class MockDataset:
        file_name = test_file_path

    return MockDataset()


@pytest.fixture
def make_trans():
    class Stub:
        pass

    class StubTransaction:
        def __init__(self, chunk_size):
            self.app = Stub()
            self.app.config = Stub()  # type: ignore[attr-defined]
            self.app.config.display_chunk_size = chunk_size  # type: ignore[attr-defined]

    return StubTransaction


def test_get_chunk__chunk_size_greater_than_file(dataset, make_trans, test_file_length):
    dt = ConnectivityTable()
    chunk_size = 1000
    trans = make_trans(chunk_size)
    chunk = dt.get_chunk(trans, dataset)
    assert (
        chunk
        == f'{{"ck_data": "363\\ttmRNA\\n1\\tG\\t0\\t2\\t359\\t1\\n2\\tG\\t1\\t3\\t358\\t2\\n", "offset": {test_file_length}}}'
    )

    # no more data
    chunk = dt.get_chunk(trans, dataset, test_file_length)
    assert chunk == f'{{"ck_data": "\\n", "offset": {test_file_length}}}'


def test_get_chunk__chunk_size_less_than_line(dataset, make_trans, test_file_length):
    dt = ConnectivityTable()
    chunk_size = 9  # length of line 1, less than length of lines 2 and 3
    trans = make_trans(chunk_size)

    # reads line 1: start at 0
    chunk = dt.get_chunk(trans, dataset, 0)
    assert chunk == '{"ck_data": "363\\ttmRNA\\n", "offset": 10}'

    # reads line 2: start anywhere on line 1
    chunk = dt.get_chunk(trans, dataset, 5)
    assert chunk == '{"ck_data": "1\\tG\\t0\\t2\\t359\\t1\\n", "offset": 24}'

    # reads line 3: start anywhere on line 2
    chunk = dt.get_chunk(trans, dataset, 20)
    assert chunk == '{"ck_data": "2\\tG\\t1\\t3\\t358\\t2\\n", "offset": 38}'

    # no more data: start anywhere on line 3
    chunk = dt.get_chunk(trans, dataset, 30)
    assert chunk == f'{{"ck_data": "\\n", "offset": {test_file_length}}}'
