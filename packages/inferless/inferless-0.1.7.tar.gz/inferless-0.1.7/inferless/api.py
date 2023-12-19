import os
from typing import Optional
import json
import threading


def call(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None, callback=None):
    """
    Call Inferless API
    :param url: Inferless Model API URL
    :param workspace_api_key: Inferless Workspace API Key
    :param data: Model Input Data
    :param callback: Callback function to be called after the response is received
    :return: Response from the API call
    """
    try:
        import requests
        if workspace_api_key is None:
            workspace_api_key = os.environ.get("INFERLESS_API_KEY")
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {workspace_api_key}"}
        if data is None:
            data = {}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to call {url} with status code {response.status_code} and response {response.text}")
        if callback is not None:
            callback(None, response.json())
        return response.json()
    except Exception as e:
        if callback is not None:
            callback(e, None)
        else:
            raise e


def call_async(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None, callback=None):
    """
    Call Inferless API
    :param url: Inferless Model API URL
    :param workspace_api_key: Inferless Workspace API Key
    :param data: Model Input Data
    :param callback: Callback function to be called after the response is received
    :return: Response from the API call
    """
    thread = threading.Thread(target=call, args=(url, workspace_api_key, data, callback))
    thread.start()
    return thread
