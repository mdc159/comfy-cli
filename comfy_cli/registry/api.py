import requests
import json
from comfy_cli import constants
from comfy_cli.registry.types import PyProjectConfig


def publish_node_version(node_config: PyProjectConfig, token: str):
    """
    Publishes a new version of a node.

    Args:
    node_config (PyProjectConfig): The node configuration.
    token (str): Personal access token for authentication.

    Returns:
    dict: JSON response from the API server.
    """
    url = f"{constants.COMFY_REGISTRY_URL_ROOT}/publishers/{node_config.tool_comfy.publisher_id}/nodes/{node_config.project.name}/versions"
    headers = {"Content-Type": "application/json"}
    body = {
        "personal_access_token": token,
        "node": {
            "id": node_config.project.name,
            "description": node_config.project.description,
            "name": node_config.tool_comfy.display_name,
            "license": node_config.project.license,
            "repository": node_config.project.urls.repository,
        },
        "node_version": {
            "version": node_config.project.version,
            "dependencies": node_config.project.dependencies,
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    # print the json of response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to publish node version: {response.status_code} {response.text}"
        )