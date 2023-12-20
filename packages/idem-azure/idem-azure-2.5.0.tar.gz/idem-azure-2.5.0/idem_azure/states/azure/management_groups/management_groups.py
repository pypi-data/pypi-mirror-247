"""State module for managing Management Group."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]
__reconcile_wait__ = {"static": {"wait_in_seconds": 20}}


async def present(
    hub,
    ctx,
    name: str,
    management_group_name: str,
    resource_id: str = None,
    display_name: str = None,
    parent_id: str = None,
) -> Dict:
    r"""Create or update Management Groups.

    Args:
        name(str): The identifier for this state.
        management_group_name(str): The name of the management group to create or update. Can include alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters that match the allowed characters.Regex pattern: ^[-\w\._\(\)]+$.
        display_name(str, Optional): The management group name to be displayed
        parent_id(str, Optional): creates management group under this id
        resource_id(str, Optional): Management group resource id on Azure

    Returns:
        Dict

    Examples:
        .. code-block:: sls

            my-management-group:
              azure.management_groups.management_groups.present:
                - name: my-management-group
                - management_group_name: my-management-group-1
                - display_name: my-management-group-1
                - parent_id: /providers/Microsoft.Management/managementGroups/parent-management-group

    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": [],
    }
    if resource_id is None:
        resource_id = (
            f"/providers/Microsoft.Management/managementGroups/{management_group_name}"
        )

    response_get = await hub.exec.azure.management_groups.management_groups.get(
        ctx, resource_id=resource_id, raw=True
    )
    if response_get["result"]:
        if response_get["ret"] is None:
            if ctx.get("test", False):
                # Return a proposed state by Idem state --test
                result[
                    "new_state"
                ] = hub.tool.azure.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "management_group_name": management_group_name,
                        "resource_id": resource_id,
                        "display_name": display_name,
                        "parent_id": parent_id,
                    },
                )
                result["comment"].append(
                    f"Would create azure.management_groups.management_groups '{name}'"
                )
                return result
            else:
                # PUT operation to create a resource
                payload = hub.tool.azure.management_groups.management_groups.convert_present_to_raw_management_group(
                    display_name=display_name, parent_id=parent_id
                )

                response_put = await hub.exec.request.json.put(
                    ctx,
                    url=f"{ctx.acct.endpoint_url}{resource_id}?api-version=2020-05-01",
                    success_codes=[200, 201, 202],
                    json=payload,
                )

                if not response_put["result"]:
                    hub.log.error(
                        f"Could not create Management Group {response_put['comment']} {response_put['ret']}"
                    )
                    result["comment"].extend(
                        hub.tool.azure.result_utils.extract_error_comments(response_put)
                    )
                    result["result"] = False
                    return result

                result[
                    "new_state"
                ] = hub.tool.azure.management_groups.management_groups.convert_raw_management_group_to_present(
                    resource=response_put,
                    idem_resource_name=name,
                    management_group_name=management_group_name,
                    resource_id=resource_id,
                )
                result["comment"].append(
                    f"Created azure.management_groups.management_groups '{name}'"
                )
                return result

        else:
            existing_resource = response_get["ret"]
            result[
                "old_state"
            ] = hub.tool.azure.management_groups.management_groups.convert_raw_management_group_to_present(
                resource=existing_resource,
                idem_resource_name=name,
                management_group_name=management_group_name,
                resource_id=resource_id,
            )
            # Generate a new PUT operation payload with new values
            new_payload = hub.tool.azure.management_groups.management_groups.update_management_groups_payload(
                existing_resource,
                {"display_name": display_name, "parent_id": parent_id},
            )
            if ctx.get("test", False):
                if new_payload["ret"] is None:
                    result["new_state"] = copy.deepcopy(result["old_state"])
                    result["comment"].append(
                        f"azure.management_groups.management_groups '{name}' has no property need to be updated."
                    )
                else:
                    result[
                        "new_state"
                    ] = hub.tool.azure.management_groups.management_groups.convert_raw_management_group_to_present(
                        resource=new_payload["ret"],
                        idem_resource_name=name,
                        management_group_name=management_group_name,
                        resource_id=resource_id,
                    )
                    result["comment"].append(
                        f"Would update azure.management_groups.management_groups '{name}'"
                    )
                return result
            # PUT operation to update a resource
            if new_payload["ret"] is None:
                result["new_state"] = copy.deepcopy(result["old_state"])
                result["comment"].append(
                    f"azure.management_groups.management_groups '{name}' has no property need to be updated."
                )
                return result
            result["comment"].extend(new_payload["comment"])
            response_put = await hub.exec.request.json.put(
                ctx,
                url=f"{ctx.acct.endpoint_url}{resource_id}?api-version=2020-05-01",
                success_codes=[200],
                json=new_payload["ret"],
            )

            if not response_put["result"]:
                hub.log.debug(
                    f"Could not update azure.management_groups.management_groups {response_put['comment']} {response_put['ret']}"
                )
                result["result"] = False
                result["comment"].extend(
                    hub.tool.azure.result_utils.extract_error_comments(response_put)
                )
                return result

            result[
                "new_state"
            ] = hub.tool.azure.management_groups.management_groups.convert_raw_management_group_to_present(
                resource=response_put["ret"],
                idem_resource_name=name,
                management_group_name=management_group_name,
                resource_id=resource_id,
            )
            result["comment"].append(
                f"Updated azure.management_groups.management_groups '{name}'"
            )
            return result

    else:
        hub.log.debug(
            f"Could not get azure.management_groups.management_groups {response_get['comment']} {response_get['ret']}"
        )
        result["result"] = False
        result["comment"].extend(
            hub.tool.azure.result_utils.extract_error_comments(response_get)
        )
        return result


async def absent(hub, ctx, name: str, management_group_name: str) -> Dict:
    r"""Delete Management Groups.

    Args:
        name(str): The identifier for this state.
        management_group_name(str): The name of the resource group to delete. The name is case insensitive.Regex pattern: ^[-\w\._\(\)]+$.

    Returns:
        Dict

    Examples:
        .. code-block:: sls

            resource_is_absent:
              azure.management_groups.management_groups.absent:
                - name: value
                - management_group_name: value
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": [],
    }
    resource_id = (
        f"/providers/Microsoft.Management/managementGroups/{management_group_name}"
    )
    response_get = await hub.exec.azure.management_groups.management_groups.get(
        ctx, resource_id=resource_id, raw=True
    )

    if response_get["result"]:
        if response_get["ret"]:
            result[
                "old_state"
            ] = hub.tool.azure.management_groups.management_groups.convert_raw_management_group_to_present(
                resource=response_get["ret"],
                idem_resource_name=name,
                management_group_name=management_group_name,
                resource_id=resource_id,
            )
            if ctx.get("test", False):
                result["comment"].append(
                    f"Would delete azure.management_groups.management_groups '{name}'"
                )
                return result

            response_delete = await hub.exec.request.raw.delete(
                ctx,
                url=f"{ctx.acct.endpoint_url}{resource_id}?api-version=2020-05-01",
                success_codes=[200, 202, 204],
            )

            if not response_delete["result"]:
                hub.log.debug(
                    f"Could not delete azure.management_groups.management_groups {response_delete['comment']} {response_delete['ret']}"
                )
                result["result"] = False
                result["comment"].extend(
                    hub.tool.azure.result_utils.extract_error_comments(response_delete)
                )
                return result

            result["comment"].append(
                f"Deleted azure.management_groups.management_groups '{name}'"
            )
            return result

        else:
            # If Azure returns 'Not Found' error, it means the resource has been absent.
            result["comment"].append(
                f"azure.management_groups.management_groups '{name}' already absent"
            )
            return result
    else:
        hub.log.debug(
            f"Could not get azure.management_groups.management_groups '{name}' {response_get['comment']} {response_get['ret']}"
        )
        result["result"] = False
        result["comment"].extend(
            hub.tool.azure.result_utils.extract_error_comments(response_get)
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Lists all Management Groups.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe azure.management_groups.management_groups
    """
    result = {}
    ret_list = await hub.exec.azure.management_groups.management_groups.list(ctx)
    if not ret_list["ret"]:
        hub.log.debug(f"Could not describe management_groups {ret_list['comment']}")
        return result

    for resource in ret_list["ret"]:
        resource_id = resource["resource_id"]
        result[resource_id] = {
            "azure.management_groups.management_groups.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
