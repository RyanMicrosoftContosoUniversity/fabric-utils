"""
Utilities for creating and working with shortcuts in Microsoft Fabric Lakehouse
"""
import json
from azure.identity import ClientSecretCredential
import requests



class ShortcutUtils:

    @staticmethod
    def build_shortcut_create_payload(name:str, target_type:str, target_connection:str, target_location:str, target_subpath:str, shortcut_location:str):
        """
        This is a function to create the payload which will be used by the create_shortcut function to create a shortcut in a lakehouse

        name:str
        target_type:str
        target_connection:str,
        target_location:str
        target_subpath:str,
        shortcut_location:str
        """
        

        return {
        "name": f"{name}",
        "path": f"/{shortcut_location}",
        "target": {
        "type": f"{target_type}",
        "adlsGen2": {
            "connectionId": f"{target_connection}",
            "location": f"{target_location}",
            "subpath": f"{target_subpath}"
        }
        }
    }

    @staticmethod
    def create_shortcut(workspace_id:str, item_id:str, target:str, api_token:str):
        """
        https://learn.microsoft.com/en-us/rest/api/fabric/core/onelake-shortcuts/create-shortcut?tabs=HTTP

        Create a new shortcut

        workspace_id:str: The uuid of the workspace where the shortcut is to be created
        item_id:str: The uuid of the item to be created
        api_token:str: The API Token used for authentication with the endpoiont
        """
        url = f'https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{item_id}/shortcuts?shortcutConflictPolicy=CreateOrOverwrite'

        headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers,json=target)

        if response.status_code >=200 and response.status_code <300:
            print(f'Shortcut Request Successful: {response.content}')

            return response
        else:
            print(f'Error in creating shortcut: {response.content}')

            return response
