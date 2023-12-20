"""Functions related to the Cloud Meta Data API."""
import os
from uuid import UUID

import requests

from piscada_cloud.mappings import Tag


def _check_credentials(host: str | None = None, token: str | None = None, env_var: str | None = None) -> tuple[str, str]:
    if isinstance(host, str) and isinstance(token, str):
        return host, token
    if (host is None and token is not None) or (host is not None and token is None):
        raise RuntimeError("Both `host` and `token` must be provided when used as parameters.")
    host = os.getenv(f"{env_var}_HOST")
    token = os.getenv(f"{env_var}_TOKEN")
    if not host or not token:
        raise RuntimeError(f"Both environment variables {env_var}_HOST and {env_var}_TOKEN need to be defined when host and token are not provided as parameters.")
    return host, token


def get_controllers(host: str | None = None, token: str | None = None) -> list[dict]:
    """Get list of accessible controllers.

    Returns
    -------
    list[dict]
        List of accessible controllers.

    Parameters
    ----------
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['CLOUD_META_DATA_HOST'].
    token: str, optional
        Access token associated with the host. Overrides the default, which is os.environ['CLOUD_META_DATA_TOKEN'].

    Raises
    ------
    RuntimeError
        If credentials are not provided or response status from Cloud Meta Data API is not 200.
    """
    host, token = _check_credentials(host, token, env_var="CLOUD_META_DATA")
    response = requests.request("GET", f"https://{host}/v0/controllers", headers={"Authorization": f"Bearer {token}"}, timeout=(5, 30))
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    return response.json()


def get_tags(  # pylint: disable=too-many-arguments
    controller_uuid: UUID | None = None,
    name: str | None = None,
    path: str | None = None,
    uuid: UUID | None = None,
    host: str | None = None,
    token: str | None = None,
    controller_version: str | None = None,
) -> list[Tag]:
    """
    List accessible tags with filtering.

    Parameters
    ----------
    controller_uuid: UUID | None
        UUID of the controller the tag(s) are associated with
    name: str | None
        Tag name
    path: str | None
        Tag path
    uuid: UUID | None
        Tag UUID
    host: str, optional
        Endpoint to send get request.
    token: str, optional
        Access token associated with the host.
    controller_version: str | None
        Version of the controller. Valid values: 'v3' or 'v4'. None if not provided.
    """
    if controller_version == "v4":
        return get_tags_ver4(controller_uuid, name, path, uuid, host, token)
    if controller_version == "v3":
        return get_tags_ver3(controller_uuid, host, token)

    tags = get_tags_ver4(controller_uuid, name, path, uuid, host, token)
    if tags:
        return tags
    tags = get_tags_ver3(controller_uuid, host, token)
    if tags:
        return tags

    raise ValueError(f"Controller {controller_uuid} is neither version 3 nor version 4.")


def get_tags_ver4(  # pylint: disable=too-many-arguments
    controller_uuid: UUID | None = None, name: str | None = None, path: str | None = None, uuid: UUID | None = None, host: str | None = None, token: str | None = None
) -> list[Tag]:
    """List accessible tags from V4 controller with filtering.

    Parameters
    ----------
    controller_uuid: UUID | None
        UUID of the controller the tag(s) are associated with
    name: str | None
        Tag name
    path: str | None
        Tag path
    uuid: UUID | None
        Tag UUID
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['CLOUD_META_DATA_HOST'].
    token: str, optional
        Access token associated with the host. Overrides the default, which is os.environ['CLOUD_META_DATA_TOKEN'].

    Returns
    -------
    list[Tag]
        Tags matching provided filter

    Raises
    ------
    RuntimeError
        if Cloud Meta Data API does not respond with status 200
    """
    host, token = _check_credentials(host, token, env_var="CLOUD_META_DATA")
    if not (controller_uuid is None or isinstance(controller_uuid, UUID)):
        raise ValueError("controller_uuid must be of type UUID")
    if not (uuid is None or isinstance(uuid, UUID)):
        raise ValueError("uuid must be of type UUID")
    query_params = [f"{key}={value}" for key, value in {"controller-uuid": controller_uuid, "name": name, "path": path, "uuid": uuid}.items() if value is not None]
    url = f"https://{host}/v0/tags"
    if len(query_params) > 0:
        url += "?" + "&".join(query_params)
    response = requests.request("GET", url, headers={"Authorization": f"Bearer {token}"}, timeout=(5, 30))
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    return [Tag(controller_id=meta_data["controller-uuid"], uuid=meta_data["uuid"], name=meta_data["name"], path=meta_data["path"]) for meta_data in response.json()]


def get_tags_ver3(  # pylint: disable=too-many-arguments
    controller_uuid: UUID | None = None,
    host: str | None = None,
    token: str | None = None,
) -> list[Tag]:
    """List accessible tags from V3 controller with filtering.

    Get tags from V3 controller.

    Parameters
    ----------
    controller_uuid: UUID | None
        UUID of the controller the tag(s) are associated with
    host: str, optional
        Endpoint to send get request. Overrides the default, which is os.environ['WRITEAPI_HOST'].
    token: str, optional
        Access token associated with the host. Overrides the default, which is os.environ['WRITEAPI_TOKEN'].

    Returns
    -------
    list[Tag]
        Tags matching provided filter

    Raises
    ------
    RuntimeError
        if Cloud Meta Data API does not respond with status 200
    """
    host, token = _check_credentials(host, token, env_var="WRITEAPI")
    url = f"https://{host}/v1/controllers/{controller_uuid}/tags"
    url += "?fields=description%2Cname%2Cid%2Ctype"

    response = requests.request("GET", url, headers={"Authorization": f"Bearer {token}"}, timeout=(10, 30))
    if response.status_code != 200:
        raise RuntimeError(f"Cloud Meta Data API gave response: {response.status_code}: {response.text}")
    return [
        Tag(
            controller_id=controller_uuid,  # type: ignore
            name=meta_data[1]["name"],
            uuid=None,
            path="",
        )
        for meta_data in response.json()
    ]
