from galaxy_test.base.populators import (
    DatasetPopulator,
)
from ._framework import ApiTestCase
from galaxy_test.driver.driver_util import log


class FooTestCase(ApiTestCase):

    def setUp(self):
        super(FooTestCase, self).setUp()
        self.dataset_populator = DatasetPopulator(self.galaxy_interactor)


    def test_create(self):
        with self.dataset_populator.test_history() as history_id:
            payload = self.dataset_populator.run_tool_payload(
                tool_id="create_2",
                inputs={},
                history_id=history_id,
            )
            create_response = self._post("tools", data=payload)
            self._assert_status_code_is(create_response, 200)
            create_object = create_response.json()
            self._assert_has_keys(create_object, "outputs")
            assert len(create_object["outputs"]) == 2

            output = create_object["outputs"][0]
            self.dataset_populator.wait_for_history(history_id, assert_ok=True)
            output_content = self.dataset_populator.get_history_dataset_content(history_id, dataset=output)
            output_details = self.dataset_populator.get_history_dataset_details(history_id, dataset=output)

            # we need output_details
            

    #def test_index(self):
    #    tool_ids = self.__tool_ids()
    #    assert "create_10" in tool_ids

    #def __tool_ids(self):
    #    index = self._get("tools")
    #    tools_index = index.json()
    #    # In panels by default, so flatten out sections...
    #    tools = []
    #    for tool_or_section in tools_index:
    #        if "elems" in tool_or_section:
    #            tools.extend(tool_or_section["elems"])
    #        else:
    #            tools.append(tool_or_section)

    #    tool_ids = [_["id"] for _ in tools]
    #    return tool_ids


