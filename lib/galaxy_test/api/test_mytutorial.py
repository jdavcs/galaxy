from galaxy_test.base.populators import DatasetPopulator
from ._framework import ApiTestCase

NUMBER_OF_DATATYPES = 446

class MyTutorialApiTestCase(ApiTestCase):

    #def test_version_is_current(self):
    #    response = self._get("version")
    #    response.raise_for_status()
    #    data = response.json()
    #    assert data["version_major"] == "22.09"


    #def test_list_datatypes(self):
    #    response = self._get("datatypes")
    #    response.raise_for_status()
    #    data = response.json()
    #    assert len(data) == NUMBER_OF_DATATYPES
    #    assert 'fasta' in data
    #    assert 'totally invalid' not in data

    #def BAD_test_create_role(self):
    #    ROLE_COUNT = 1
    #    # verify no roles except 1
    #    response = self._get("roles")
    #    response.raise_for_status()
    #    data = response.json()
    #    assert len(data) == ROLE_COUNT

    #    # create role
    #    name = 'my cool name'
    #    description = 'description of this cool role'
    #    payload = {
    #        "name": name,
    #        "description": description,
    #    }
    #    response = self._post("roles", payload, admin=True, json=True)
    #    response.raise_for_status()
    #    role = response.json()
    #    assert role["name"] == name
    #    assert role["description"] == description

    #    # verify role has been added
    #    response = self._get("roles")
    #    response.raise_for_status()
    #    data = response.json()
    #    assert len(data) == ROLE_COUNT + 1

    def setUp(self):
        super().setUp()
        self.dataset_populator = DatasetPopulator(self.galaxy_interactor)

    def test_create_role(self):
        
        # create role
        name = self.dataset_populator.get_random_name()
        description = 'description of this cool role'
        payload = {
            "name": name,
            "description": description,
        }

        # verify role not in roles
        response = self._get("roles")
        response.raise_for_status()
        data = response.json()
        assert not any(role["name"] == name for role in data)

        # TODO do i need these params???
        response = self._post("roles", payload, admin=True, json=True)
        response.raise_for_status()
        role = response.json()
        assert role["name"] == name
        assert role["description"] == description

        # verify role has been added
        response = self._get("roles")
        response.raise_for_status()
        data = response.json()
        assert any(role["name"] == name for role in data)



