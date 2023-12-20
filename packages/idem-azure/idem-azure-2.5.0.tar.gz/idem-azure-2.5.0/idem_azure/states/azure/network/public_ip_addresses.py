"""State module for managing Public IP Address."""
import copy
import uuid
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


RESOURCE_TYPE_FULL = "azure.network.public_ip_addresses"


async def present(
    hub,
    ctx,
    name: str,
    resource_group_name: str,
    public_ip_address_name: str,
    location: str,
    allocation_method: str,
    zones: List[str] = None,
    ddos_protection_mode: str = None,
    ddos_protection_plan_id: str = None,
    domain_name_label: str = None,
    edge_zone: str = None,
    idle_timeout_in_minutes: int = None,
    ip_address: str = None,
    ip_tags: Dict[str, str] = None,
    ip_version: str = None,
    public_ip_prefix_id: str = None,
    reverse_fqdn: str = None,
    linked_public_ip_address_id: str = None,
    service_public_ip_address_id: str = None,
    migration_phase: str = None,
    sku: str = None,
    sku_tier: str = None,
    tags: Dict[str, str] = None,
    extended_location: Dict[str, str] = None,
    subscription_id: str = None,
    resource_id: str = None,
) -> Dict:
    r"""Create or update Public IP Addresses.

    Args:
        name(str): The identifier for this state.
        resource_group_name(str): The name of the resource group.
        public_ip_address_name(str): The name of the public IP address.
        location(str): Resource location.
        allocation_method(str): Defines the allocation method for this IP address.
        zones(list[str], Optional): A collection containing the availability zone to allocate the Public IP in.
        ddos_protection_mode(str, Optional): The DDoS protection mode of the public IP.
        ddos_protection_plan_id(str, Optional): The ID of DDoS protection plan associated with the public IP.
        domain_name_label(str, Optional): Label for the Domain Name.
        edge_zone(str, Optional): Specifies the Edge Zone within the Azure Region where this Public IP should exist.
        idle_timeout_in_minutes(int, Optional): Specifies the timeout for the TCP idle connection.
        ip_address(str, Optional): The IP address associated with the public IP address resource.
        ip_tags(dict, Optional): A mapping of IP tags to assign to the public IP.
        ip_version(str, Optional): The IP Version to use.
        public_ip_prefix_id(str, Optional): If specified then public IP address allocated will be provided from the public IP prefix resource.
        reverse_fqdn(str, Optional): A fully qualified domain name that resolves to this public IP address.
        migration_phase(str, Optional): Migration phase of Public IP Address.
        service_public_ip_address_id(str, Optional): The service public IP address ID of the public IP address resource.
        linked_public_ip_address_id(str, Optional): The linked public IP address ID of the public IP address resource.
        sku(str, Optional): The SKU of the Public IP.
        sku_tier(str, Optional): The SKU Tier that should be used for the Public IP.
        tags(dict, Optional): Resource tags.
        extended_location(Dict[str,str], Optional): The extended location of the public ip address.

            * name(str, Optional):
                The name of the extended location.
            * type(str, Optional):
                The type of the extended location.
        subscription_id(str, Optional): Subscription Unique id.
        resource_id(str, Optional): Management group resource id on Azure.

    Returns:
        dict

    Examples:
        .. code-block:: sls

            resource_is_present:
              azure.network.public_ip_addresses.present:
                - name: value
                - resource_group_name: value
                - public_ip_address_name: value
    """
    result = ctx.get("wrapper_result")

    if ctx.get("skip_present"):
        return result

    if not result:
        error_message = hub.tool.azure.comment_utils.no_result_from_wrapper(
            RESOURCE_TYPE_FULL, name
        )
        hub.log.error(error_message)
        return {
            "result": True,
            "old_state": None,
            "new_state": None,
            "name": name,
            "comment": [error_message],
        }

    computed = ctx.get("computed")
    computed_resource_id = computed.get("resource_id")
    computed_resource_url = computed.get("resource_url")
    existing_resource = result["old_state"]

    if not existing_resource:
        if ctx.get("test", False):
            # Return a proposed state by Idem state --test
            result["new_state"] = hub.tool.azure.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_group_name": resource_group_name,
                    "public_ip_address_name": public_ip_address_name,
                    "location": location,
                    "allocation_method": allocation_method,
                    "zones": zones,
                    "ddos_protection_mode": ddos_protection_mode,
                    "ddos_protection_plan_id": ddos_protection_plan_id,
                    "domain_name_label": domain_name_label,
                    "edge_zone": edge_zone,
                    "idle_timeout_in_minutes": idle_timeout_in_minutes,
                    "ip_address": ip_address,
                    "ip_tags": ip_tags,
                    "ip_version": ip_version,
                    "public_ip_prefix_id": public_ip_prefix_id,
                    "reverse_fqdn": reverse_fqdn,
                    "sku": sku,
                    "sku_tier": sku_tier,
                    "tags": tags,
                    "extended_location": extended_location,
                    "linked_public_ip_address_id": linked_public_ip_address_id,
                    "service_public_ip_address_id": service_public_ip_address_id,
                    "migration_phase": migration_phase,
                    "resource_id": computed_resource_id,
                    "subscription_id": subscription_id,
                },
            )
            result["comment"].append(
                hub.tool.azure.comment_utils.would_create_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            return result

        else:
            # PUT operation to create a resource
            payload = hub.tool.azure.network.public_ip_addresses.convert_present_to_raw_public_ip_addresses(
                location=location,
                allocation_method=allocation_method,
                zones=zones,
                ddos_protection_mode=ddos_protection_mode,
                ddos_protection_plan_id=ddos_protection_plan_id,
                domain_name_label=domain_name_label,
                edge_zone=edge_zone,
                idle_timeout_in_minutes=idle_timeout_in_minutes,
                ip_address=ip_address,
                ip_tags=ip_tags,
                ip_version=ip_version,
                public_ip_prefix_id=public_ip_prefix_id,
                reverse_fqdn=reverse_fqdn,
                sku=sku,
                sku_tier=sku_tier,
                tags=tags,
                extended_location=extended_location,
                linked_public_ip_address_id=linked_public_ip_address_id,
                service_public_ip_address_id=service_public_ip_address_id,
                migration_phase=migration_phase,
            )
            response_put = await hub.exec.request.json.put(
                ctx,
                url=computed_resource_url,
                success_codes=[200, 201],
                json=payload,
            )

            if not response_put["result"]:
                hub.log.debug(
                    hub.tool.azure.comment_utils.could_not_create_comment(
                        RESOURCE_TYPE_FULL, name
                    )
                )
                result["comment"].extend(
                    hub.tool.azure.result_utils.extract_error_comments(response_put)
                )
                result["result"] = False
                return result

            result[
                "new_state"
            ] = hub.tool.azure.network.public_ip_addresses.convert_raw_public_ip_addresses_to_present(
                resource=response_put["ret"],
                idem_resource_name=name,
                resource_group_name=resource_group_name,
                public_ip_address_name=public_ip_address_name,
                resource_id=computed_resource_id,
                subscription_id=subscription_id,
            )
            result["comment"].append(
                hub.tool.azure.comment_utils.create_comment(RESOURCE_TYPE_FULL, name)
            )

            # We want to make another get when resource creation is completed
            # to populate the new_state with properties present after the completion and not earlier.
            if (
                response_put["ret"]
                and (
                    response_put["ret"].get("properties")
                    and response_put["ret"]["properties"].get(
                        "publicIPAllocationMethod"
                    )
                )
                == "Static"
                and response_put["ret"]["properties"].get("provisioningState")
                == "Updating"
            ):
                result["rerun_data"] = {
                    "get_resource_on_completion": True,
                    "operation_id": str(uuid.uuid4()),
                    "operation_headers": dict(response_put.get("headers")),
                    "resource_id": f"{computed_resource_id}",
                    "resource_url": f"{computed_resource_url}",
                    "old_state": result["old_state"],
                }

            return result

    else:
        raw_existing_resource = hub.tool.azure.network.public_ip_addresses.convert_present_to_raw_public_ip_addresses(
            **existing_resource
        )
        # Generate a new PUT operation payload with new values
        new_payload = hub.tool.azure.network.public_ip_addresses.update_public_ip_addresses_payload(
            raw_existing_resource,
            {
                "allocation_method": allocation_method,
                "zones": zones,
                "ddos_protection_mode": ddos_protection_mode,
                "ddos_protection_plan_id": ddos_protection_plan_id,
                "domain_name_label": domain_name_label,
                "edge_zone": edge_zone,
                "idle_timeout_in_minutes": idle_timeout_in_minutes,
                "ip_address": ip_address,
                "ip_tags": ip_tags,
                "ip_version": ip_version,
                "public_ip_prefix_id": public_ip_prefix_id,
                "reverse_fqdn": reverse_fqdn,
                "sku": sku,
                "sku_tier": sku_tier,
                "tags": tags,
                "extended_location": extended_location,
                "linked_public_ip_address_id": linked_public_ip_address_id,
                "service_public_ip_address_id": service_public_ip_address_id,
                "migration_phase": migration_phase,
            },
        )

        if ctx.get("test", False):
            if new_payload["ret"] is None:
                result["new_state"] = copy.deepcopy(result["old_state"])
                result["comment"].append(
                    hub.tool.azure.comment_utils.no_property_to_be_updated_comment(
                        RESOURCE_TYPE_FULL, name
                    )
                )
            else:
                result[
                    "new_state"
                ] = hub.tool.azure.network.public_ip_addresses.convert_raw_public_ip_addresses_to_present(
                    resource=new_payload["ret"],
                    idem_resource_name=name,
                    resource_group_name=resource_group_name,
                    public_ip_address_name=public_ip_address_name,
                    resource_id=computed_resource_id,
                    subscription_id=subscription_id,
                )
                result["comment"].append(
                    hub.tool.azure.comment_utils.would_update_comment(
                        RESOURCE_TYPE_FULL, name
                    )
                )
            return result
        # PUT operation to update a resource
        if new_payload["ret"] is None:
            result["new_state"] = copy.deepcopy(result["old_state"])
            result["comment"].append(
                hub.tool.azure.comment_utils.no_property_to_be_updated_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            return result
        result["comment"].extend(new_payload["comment"])
        response_put = await hub.exec.request.json.put(
            ctx,
            url=computed_resource_url,
            success_codes=[200],
            json=new_payload["ret"],
        )
        if not response_put["result"]:
            hub.log.debug(
                hub.tool.azure.comment_utils.could_not_update_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            result["result"] = False
            result["comment"].extend(
                hub.tool.azure.result_utils.extract_error_comments(response_put)
            )
            return result

        result[
            "new_state"
        ] = hub.tool.azure.network.public_ip_addresses.convert_raw_public_ip_addresses_to_present(
            resource=response_put["ret"],
            idem_resource_name=name,
            resource_group_name=resource_group_name,
            public_ip_address_name=public_ip_address_name,
            resource_id=computed_resource_id,
            subscription_id=subscription_id,
        )
        result["comment"].append(
            hub.tool.azure.comment_utils.update_comment(RESOURCE_TYPE_FULL, name)
        )
        return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_group_name: str = None,
    public_ip_address_name: str = None,
    subscription_id: str = None,
    resource_id: str = None,
) -> dict:
    r"""Delete Public IP Addresses.

    Args:
        name(str): The identifier for this state.
        resource_group_name(str, Optional): The name of the resource group.
        public_ip_address_name(str, Optional): The name of the public IP address.
        subscription_id(str, Optional): Subscription Unique id.
        resource_id(str, Optional): Resource Group resource id in Azure.

    Returns:
        Dict

    Examples:
        .. code-block:: sls

            resource_is_absent:
              azure.network.public_ip_addresses.absent:
                - name: value
                - resource_group_name: value
                - public_ip_address_name: value
    """
    return hub.tool.azure.result_utils.absent_implemented_through_wrapper_result(
        RESOURCE_TYPE_FULL, name
    )


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Lists all Public IP Addresses under the same subscription.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe azure_auto.network.public_ip_addresses
    """
    result = {}
    ret_list = await hub.exec.azure.network.public_ip_addresses.list(ctx)
    if not ret_list["ret"]:
        hub.log.debug(f"Could not describe public ip addresses {ret_list['comment']}")
        return result

    for resource in ret_list["ret"]:
        resource_id = resource["resource_id"]
        result[resource_id] = {
            "azure.network.public_ip_addresses.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.azure.resource_utils.is_pending(
        ret=ret, state=state, **pending_kwargs
    )
