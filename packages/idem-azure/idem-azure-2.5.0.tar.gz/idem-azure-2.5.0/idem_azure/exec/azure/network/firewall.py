"""Exec module for managing Network Firewall"""

__func_alias__ = {"list_": "list"}

from typing import Dict
from collections import OrderedDict


async def get(hub, ctx, resource_id: str, name: str = None, raw: bool = False) -> Dict:
    """Gets network Firewall from azure account.

    Args:
        resource_id(str):
            The resource id of the Firewall.
        name(str, Optional):
            The name of the resource
        raw(bool, Optional):
            Returns raw response if True. Defaults to False

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec azure.network.firewall.get resource_id="value" raw="False"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path:  azure.network.firewall.get
                - kwargs:
                    resource_id: "/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/azureFirewalls/{firewall_name}"
                    raw: False
    """

    result = dict(comment=[], ret=None, result=True)
    response_get = await hub.exec.request.json.get(
        ctx,
        url=f"{ctx.acct.endpoint_url}{resource_id}?api-version=2022-07-01",
        success_codes=[200],
    )
    if not response_get["result"]:
        if response_get["status"] != 404:
            result["result"] = False
        result["comment"].extend(
            hub.tool.azure.result_utils.extract_error_comments(response_get)
        )
        return result
    uri_parameters = OrderedDict(
        {
            "subscriptions": "subscription_id",
            "resourceGroups": "resource_group_name",
            "azureFirewalls": "firewall_name",
        }
    )
    uri_parameter_values = hub.tool.azure.uri.get_parameter_value_in_dict(
        resource_id, uri_parameters
    )
    if raw:
        result["ret"] = response_get["ret"]
    else:
        result["ret"] = hub.tool.azure.network.firewall.convert_raw_firewall_to_present(
            idem_resource_name=resource_id,
            resource=response_get["ret"],
            resource_id=resource_id,
            **uri_parameter_values,
        )
    return result


async def list_(
    hub,
    ctx,
) -> Dict:
    """Lists all Network Firewall.

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec azure.network.firewall.list

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: azure.network.firewall.list

    """

    result = dict(comment=[], ret=[], result=True)
    subscription_id = ctx.acct.subscription_id
    uri_parameters = OrderedDict(
        {
            "subscriptions": "subscription_id",
            "resourceGroups": "resource_group_name",
            "azureFirewalls": "firewall_name",
        }
    )
    async for page_result in hub.tool.azure.request.paginate(
        ctx,
        url=f"{ctx.acct.endpoint_url}/subscriptions/{subscription_id}/providers/Microsoft.Network/azureFirewalls?api-version=2022-07-01",
        success_codes=[200],
    ):
        resource_list = page_result.get("value", None)
        if resource_list:
            for resource in resource_list:
                resource_id = resource["id"]
                uri_parameter_values = hub.tool.azure.uri.get_parameter_value_in_dict(
                    resource_id, uri_parameters
                )
                result["ret"].append(
                    hub.tool.azure.network.firewall.convert_raw_firewall_to_present(
                        resource=resource,
                        idem_resource_name=resource_id,
                        resource_id=resource_id,
                        **uri_parameter_values,
                    )
                )
    return result
