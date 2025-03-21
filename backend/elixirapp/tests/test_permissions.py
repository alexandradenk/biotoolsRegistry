from rest_framework import status
from elixir.serializers import *
from backend.elixirapp.tests.test_baseobject import BaseTestObject
from elixir.test_datastructure_json import inputTool, inputToolInvalid
import unittest


class TestPermissions(BaseTestObject):
    test_superuser_name = BaseTestObject.superuser_registration_data['username']
    test_user_name = BaseTestObject.valid_user_registration_data['username']
    test_other_user_1_name = BaseTestObject.other_valid_user_1_login_data['username']
    test_other_user_2_name = BaseTestObject.other_valid_user_2_login_data['username']

    editPermission_field = 'editPermission'
    editPermission_private = 'private'
    editPermission_public = 'public'

    editingRights_private = {
        "type": editPermission_private
    }
    editingRights_public = {
        "type": editPermission_public
    }
    editingRights_group = {
        "type": editPermission_private,
        "authors": [test_user_name, test_other_user_1_name]
    }

    # BASE -------------------------------------------------------------------------------------------------------------

    def post_tool_with_permissions(self, data, permissions):
        data[self.editPermission_field] = permissions
        self.post_tool_checked(data)

    # PRIVATE ----------------------------------------------------------------------------------------------------------

    # --- UPDATE -------------------------------------------------------------------------------------------------------
    def test_update_private_tool_creator(self):
        """
        Test updating a private tool as its creator
        Info:
            - Post executed as normal user
            - Update executed as normal user (creator)
        Expected: Successful update (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_private)

        # update tool
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.json()['name'], new_name)

    def test_update_private_tool_other_user(self):
        """
        Test updating a private tool as another user
        Info:
            - Post executed as superuser
            - Update executed as normal user (not the creator)
        Expected: No update (403 Forbidden)
        """
        data = inputTool()
        self.switch_user(self.superuser_registration_data, self.superuser_login_data, True)
        self.post_tool_with_permissions(data, self.editingRights_private)

        # try to update tool as other user
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)

        # ensure resource was not updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertNotEquals(get_response.json()['name'], new_name)

    def test_update_private_tool_superuser(self):
        """
        Test updating a private tool as a superuser
        Info:
            - Post executed as normal user
            - Update executed as superuser (not the creator)
        Expected: Successful update (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_private)

        # try to update tool as superuser
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, True)
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.json()['name'], new_name)

    # --- DELETE -------------------------------------------------------------------------------------------------------
    def test_delete_private_tool_creator(self):
        """
        Test deleting a private tool as its creator
        Info:
            - Post executed as normal user
            - Deletion executed as normal user (creator)
        Expected: Successful deletion (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_private)

        # delete tool
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

        # ensure resource was deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_private_tool_other_user(self):
        """
        Test deleting a private tool as another user
        Info:
            - Post executed as superuser
            - Deletion executed as normal user (not the creator)
        Expected: No deletion (403 Forbidden)
        """

        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_private)

        # try to delete tool as other user
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

        # ensure resource was not deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_delete_private_tool_superuser(self):
        """
        Test deleting a private tool as a superuser
        Info:
            - Post executed as normal user
            - Deletion executed as superuser (not the creator)
        Expected: Successful deletion (200 OK)
        """

        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_private)

        # delete tool as superuser
        self.switch_user(self.superuser_registration_data, self.superuser_login_data, True)
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

        # ensure resource was deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    # PUBLIC -----------------------------------------------------------------------------------------------------------

    # --- UPDATE -------------------------------------------------------------------------------------------------------

    def test_update_public_tool_creator(self):
        """
        Test updating a public tool as its creator
        Info:
            - Post executed as normal user
            - Update executed as normal user (creator)
        Expected: Successful update (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # update tool
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.json()['name'], new_name)

    def test_update_public_tool_other_user(self):
        """
        Test updating a public tool as another user
        Info:
            - Post executed as superuser
            - Update executed as normal user (not the creator)
        Expected: Successful update (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # try to update tool as other user
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEquals(get_response.json()['name'], new_name)

    def test_update_public_tool_superuser(self):
        """
        Test updating a public tool as a superuser
        Info:
            - Post executed as normal user
            - Update executed as superuser (not the creator)
        Expected: Successful update (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # try to update tool as superuser
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, True)
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.json()['name'], new_name)

    # --- DELETE -------------------------------------------------------------------------------------------------------

    def test_delete_public_tool_creator(self):
        """
        Test deleting a public tool as its creator
        Info:
            - Post executed as normal user
            - Deletion executed as normal user (creator)
        Expected: Successful deletion (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # delete tool
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

        # ensure resource was deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_public_tool_other_user(self):
        """
        Test deleting a public tool as another user
        Info:
            - Post executed as superuser
            - Deletion executed as normal user (not the creator)
        Expected: No deletion (403 Forbidden)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # try to delete tool as other user
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

        # ensure resource was not deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_delete_public_tool_superuser(self):
        """
        Test deleting a public tool as a superuser
        Info:
            - Post executed as normal user
            - Deletion executed as superuser (not the creator)
        Expected: Successful deletion (200 OK)
        """

        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # delete tool as superuser
        self.switch_user(self.superuser_registration_data, self.superuser_login_data, True)
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

        # ensure resource was deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    # GROUP ------------------------------------------------------------------------------------------------------------

    # --- UPDATE -------------------------------------------------------------------------------------------------------

    def test_update_group_permission_tool_creator(self):
        """
        Test updating a group tool as its creator
        Info:
            - Post executed as normal user
            - Update executed as normal user (creator)
        Expected: Successful update (200 OK)
        """
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_group)

        # update tool
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.json()['name'], new_name)

    def test_update_group_permission_tool_other_user_in_group(self):
        """
        Test updating a group tool as another user in the group
        Info:
            - Post executed as superuser
            - Update executed as normal user (not the creator)
        Expected: Successful update (200 OK)
        """
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # try to update tool as a user of the specified group
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEquals(get_response.json()['name'], new_name)

    def test_update_group_permission_tool_other_user_not_in_group(self):
        """
        Test updating a group tool as another user that is not in the group
        Info:
            - Post executed as normal user
            - Update executed as normal user (not the creator) TODO adapt
        Expected: No update (403 Forbidden)
        """
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_group)

        # try to update tool as a user that is not in the specified group
        self.switch_user(self.other_valid_user_2_registration_data, self.other_valid_user_2_login_data, False)
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)

        # ensure resource was not updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertNotEqual(get_response.json()['name'], new_name)

    def test_update_group_permission_tool_superuser(self):
        """
        Test updating a group tool as the superuser
        Info:
            - Post executed as a normal user
            - Update executed as superuser (not in the group)
        Expected: Successful update (200 OK)
        """
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_group)

        # try to update tool as a superuser
        self.switch_user(self.superuser_registration_data, self.superuser_login_data, True)
        new_name = 'Updated Tool Name'
        data['name'] = new_name
        put_response = self.put_tool(self.base_url, data)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.json()['name'], new_name)

    # --- DELETE -------------------------------------------------------------------------------------------------------

    def test_delete_group_permission_tool_creator(self):
        """
        Test deleting a group tool as its creator
        Info:
            - Post executed as normal user
            - Deletion executed as normal user (creator) TODO adapt
        Expected: Successful deletion (200 OK)
        """
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_group)

        # update tool
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN) # TODO why

        # ensure resource was updated
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_delete_group_permission_tool_other_user_in_group(self):
        """
        Test deleting a group tool as another user in the group
        Info:
            - Post executed as superuser
            - Deletion executed as normal user (not the creator)
        Expected: No deletion (403 Forbidden)
        """
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_public)

        # try to update tool as a user of the specified group
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_delete_group_permission_tool_other_user_not_in_group(self):
        """
        Test deleting a group tool as another user that is not in the group
        Info:
            - Post executed as normal user
            - Deletion executed as normal user (not in the group)
        Expected: No deletion (403 Forbidden)
        """
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_group)

        # try to delete tool as a user that is not in the specified group
        self.switch_user(self.other_valid_user_2_registration_data, self.other_valid_user_2_login_data, False)
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

        # ensure resource was not deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_delete_group_permission_tool_superuser(self):
        """
        Test deleting a group tool as the superuser
        Info:
            - Post executed as a normal user
            - Deletion executed as superuser (not in the group)
        Expected: Successful deletion (200 OK)
        """
        self.switch_user(self.other_valid_user_1_registration_data, self.other_valid_user_1_login_data, False)
        self.switch_user(self.valid_user_registration_data, self.valid_user_login_data, False)
        data = inputTool()
        self.post_tool_with_permissions(data, self.editingRights_group)

        # try to delete tool as a superuser
        self.switch_user(self.superuser_registration_data, self.superuser_login_data, True)
        print(f"CHECK USER BEFORE DELETE: {self.user.username}, is superuser: {self.user.is_superuser}")
        print('NEW USER BLUB', self.user.username, self.user.is_superuser)
        delete_response = self.remove_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

        # ensure resource was deleted
        get_response = self.get_tool(self.base_url, data['biotoolsID'])
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
