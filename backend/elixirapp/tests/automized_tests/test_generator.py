from .value_factory import ValueFactory
from elixir.tool_helper import ToolHelper
from .constants import VALID, INVALID
from elixirapp.tests.test_baseobject import BaseTestObject
from rest_framework import status
import json


class TestGenerator(BaseTestObject):

    def build(self):
        self.value_factory = ValueFactory()
        self.value_factory.create_values_by_level()  # create valid and invalid values

    def test_all(self):
        """
        Description:    Method for automized testing based on restrictions parsed from the schema.
        """
        self.build()

        print(f"ARRVALS: {self.value_factory.array_values}")

        self.test_string_or_object(self.value_factory.string_values)
        self.test_string_or_object(self.value_factory.object_values)
        self.test_array(self.value_factory.array_values)

    def test_string_or_object(self, test_dict: dict):
        """
        Description:    Method for testing attributes in the tool based on schema restrictions.
        """
        input_tool = ToolHelper.get_input_tool()

        for path, constraints in test_dict.items():

            if path not in self.value_factory.array_restrictions:  # only test real strings
                constraints = test_dict[path]
                path_list = path.split('/')

                value_before = self._test_valid_values(constraints, input_tool, path_list)  # extract original
                self._test_invalid_values(constraints, input_tool, path_list)

                # change back to original
                self.value_factory.alter_tool(input_tool, path_list, value_before)

    def test_array(self, test_dict: dict):
        """
        Description:    Method for testing attributes in the tool based on schema restrictions.
        """
        input_tool = ToolHelper.get_input_tool()

        for path, constraints in test_dict.items():
            constraints = test_dict[path]
            path_list = path.split('/')

            value_before = self._test_valid_values(constraints, input_tool, path_list)  # extract original
            self._test_invalid_values(constraints, input_tool, path_list)

            # change back to original
            self.value_factory.alter_tool(input_tool, path_list, value_before)

    def _test_valid_values(self, values: dict, input_tool: object, path_list: list):
        """
        Description:    Alters tool based on path using the valid values specified for the attribute.
        Returns:        Value at the specified path for the input tool before replacement.
        """
        original_value = self._get_tool_value(input_tool, path_list)

        if isinstance(values[VALID], list):
            for valid_value in values[VALID]:
                if valid_value:
                    if isinstance(original_value, list) and not isinstance(valid_value, list):
                        valid_value = [valid_value]
                    original_value = self.value_factory.alter_tool(input_tool, path_list, valid_value)
                    self.__test_post_valid_tool(input_tool)
        else:
            original_value = self.value_factory.alter_tool(input_tool, path_list, values[VALID])
            self.__test_post_valid_tool(input_tool)

        self.value_factory.alter_tool(input_tool, path_list, original_value)  # change back

        return original_value

    def __test_post_valid_tool(self, valid_tool):
        for url in self.put_post_urls:
            with self.subTest(url=url):
                tool = json.loads(json.dumps(valid_tool))
                response = self.post_tool(url, tool)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_201_CREATED,
                    msg=f"Tool creation failed for URL {url}. Response code: {response.status_code}, body: {response.content}"
                )

    def _test_invalid_values(self, constraints: dict, input_tool: object, path_list: list):
        """
        Description:    Alters tool based on path using the invalid values specified for the attribute.
        Returns:        Value at the specified path for the input tool before replacement.
        """
        original_value = self._get_tool_value(input_tool, path_list)

        for invalid_value in constraints[INVALID]:
            if isinstance(original_value, list) and not isinstance(invalid_value, list):
                invalid_value = [invalid_value]  # wrap into list

            original_value = self.value_factory.alter_tool(input_tool, path_list, invalid_value)  # alter tool
            self.__test_post_invalid_tool(input_tool)

        self.value_factory.alter_tool(input_tool, path_list, original_value)  # change back

        return original_value

    def __test_post_invalid_tool(self, valid_tool):
        for url in self.put_post_urls:
            with self.subTest(url=url):
                tool = json.loads(json.dumps(valid_tool))
                response = self.post_tool(url, tool)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                    msg=f"Tool creation unexpectedly worked for URL {url}."
                )

    def _get_tool_value(self, parsing_object, path):
        if not path:
            return parsing_object

        key = path[0]

        if isinstance(parsing_object, list):
            if not parsing_object:
                return None
            next_obj = parsing_object[0].get(key)
        else:
            next_obj = parsing_object.get(key)

        return self._get_tool_value(next_obj, path[1:]) if next_obj is not None else None
