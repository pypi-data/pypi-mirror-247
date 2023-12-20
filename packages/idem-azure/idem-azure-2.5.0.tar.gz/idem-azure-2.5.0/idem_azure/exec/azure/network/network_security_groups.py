"""Exec module for managing network security groups."""
from collections import OrderedDict
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}

RESOURCE_TYPE = "network.network_security_groups"


async def get(
    hub, ctx, resource_id: str, name: str = None, raw: bool = False
) -> Dict[str, Any]:
    """Get network security group resource from resource_id.

    Args:
        resource_id(str):
            The resource_id of network security group
        name(str, Optional):
            The name of the resource
        raw(bool, Optional):
            Returns raw response if True. Defaults to False

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id:

        .. code-block:: bash

            idem exec azure.network.network_security_groups.get resource_id="value"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path:  azure.network.network_security_groups.get
                - kwargs:
                    resource_id: "/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkSecurityGroups/{network_security_group_name}"

    """
    result = dict(comment=[], result=True, ret=None)
    api_version = hub.tool.azure.api_versions.get_api_version(RESOURCE_TYPE)
    uri_parameters = OrderedDict(
        {
            "resourceGroups": "resource_group_name",
            "networkSecurityGroups": "network_security_group_name",
            "subscriptions": "subscription_id",
        }
    )

    response_get = await hub.exec.request.json.get(
        ctx,
        url=f"{ctx.acct.endpoint_url}{resource_id}?api-version={api_version}",
        success_codes=[200],
    )
    if not response_get["result"]:
        if response_get["status"] != 404:
            result["result"] = False
        result["comment"].extend(
            hub.tool.azure.result_utils.extract_error_comments(response_get)
        )
        return result
    elif response_get["result"] and response_get["ret"]:
        if raw:
            result["ret"] = response_get["ret"]
        else:
            uri_parameter_values = hub.tool.azure.uri.get_parameter_value_in_dict(
                resource_id, uri_parameters
            )

            result[
                "ret"
            ] = hub.tool.azure.network.network_security_groups.convert_raw_network_security_groups_to_present(
                resource=response_get["ret"],
                idem_resource_name=resource_id,
                resource_id=resource_id,
                **uri_parameter_values,
            )

    return result


async def list_(hub, ctx) -> Dict:
    """List of network security groups

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id:

        .. code-block:: bash

            idem exec azure.network.network_security_groups.list

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: azure.network.network_security_groups.list


    """
    result = dict(comment=[], result=True, ret=[])
    api_version = hub.tool.azure.api_versions.get_api_version(RESOURCE_TYPE)
    subscription_id = ctx.acct.subscription_id
    uri_parameters = OrderedDict(
        {
            "resourceGroups": "resource_group_name",
            "networkSecurityGroups": "network_security_group_name",
            "subscriptions": "subscription_id",
        }
    )
    async for page_result in hub.tool.azure.request.paginate(
        ctx,
        url=f"{ctx.acct.endpoint_url}/subscriptions/{subscription_id}/providers/Microsoft.Network/networkSecurityGroups?api-version={api_version}",
        success_codes=[200],
    ):
        resource_list = page_result.get("value")
        if resource_list:
            for resource in resource_list:
                resource_id = resource["id"]
                uri_parameter_values = hub.tool.azure.uri.get_parameter_value_in_dict(
                    resource["id"], uri_parameters
                )
                result["ret"].append(
                    hub.tool.azure.network.network_security_groups.convert_raw_network_security_groups_to_present(
                        resource=resource,
                        idem_resource_name=resource_id,
                        resource_id=resource_id,
                        **uri_parameter_values,
                    )
                )
    return result
