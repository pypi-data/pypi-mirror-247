import copy
from typing import Any
from typing import Dict
from typing import List


def update_public_ip_addresses_payload(
    hub, existing_payload: Dict[str, Any], new_values: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate an updated payload, which can be used by
     PUT operation to update a resource on Azure.

    Args:
        hub: The redistributed pop central hub.
        existing_payload: An existing resource state from Azure. This is usually a GET operation response.
        new_values: A dictionary of desired state values. If any property's value is None,
         this property will be ignored. This is to match the behavior when a present() input is a None, Idem does not
         do an update.

    Returns:
        A result dict.
        result: True if no error occurs during the operation.
        ret: An updated payload that can be used to call PUT operation to update the resource. None if no update on all values.
        comment: A messages tuple.
    """
    result = {"result": True, "ret": None, "comment": []}
    need_update = False
    new_payload = copy.deepcopy(existing_payload)

    if (
        (new_values.get("allocation_method") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            new_values["allocation_method"]
            != existing_payload.get("properties").get("publicIPAllocationMethod")
        )
    ):
        new_payload["properties"]["publicIPAllocationMethod"] = new_values.get(
            "allocation_method"
        )
        need_update = True

    if (new_values.get("zones") is not None) and (
        set(new_values["zones"]) != set(existing_payload.get("zones"))
    ):
        new_payload["zones"] = new_values.get("zones")
        need_update = True

    if (
        (new_values.get("ddos_protection_mode") is not None)
        and (existing_payload.get("properties") is not None)
        and (existing_payload.get("properties").get("ddosSettings") is not None)
        and (
            new_values["ddos_protection_mode"]
            != existing_payload.get("properties")
            .get("ddosSettings")
            .get("protectionMode")
        )
    ):
        new_payload["properties"]["ddosSettings"]["protectionMode"] = new_values.get(
            "ddos_protection_mode"
        )
        need_update = True

    if (
        (new_values.get("ddos_protection_plan_id") is not None)
        and (existing_payload.get("properties") is not None)
        and (existing_payload.get("properties").get("ddosSettings") is not None)
        and (
            new_values["ddos_protection_plan_id"]
            != existing_payload.get("properties")
            .get("ddosSettings")
            .get("ddosProtectionPlan")
        )
    ):
        new_payload["properties"]["ddosSettings"][
            "ddosProtectionPlan"
        ] = new_values.get("ddos_protection_plan_id")
        need_update = True

    if (
        (new_values.get("domain_name_label") is not None)
        and (existing_payload.get("properties") is not None)
        and (existing_payload.get("properties").get("dnsSettings") is not None)
        and (
            new_values["domain_name_label"]
            != existing_payload.get("properties")
            .get("dnsSettings")
            .get("domainNameLabel")
        )
    ):
        new_payload["properties"]["dnsSettings"]["domainNameLabel"] = new_values.get(
            "domain_name_label"
        )
        need_update = True

    # TODO [DA]: Look into the reason for extendedLocation being a part of "properties"
    #  when it seems like it is not, by the documentation:
    #  https://learn.microsoft.com/en-us/rest/api/virtualnetwork/public-ip-addresses/create-or-update?view=rest-virtualnetwork-2023-05-01&tabs=HTTP
    if (
        (new_values.get("edge_zone") is not None)
        and (existing_payload.get("extendedLocation") is not None)
        and (
            new_values["edge_zone"]
            != existing_payload.get("extendedLocation").get("type")
        )
    ):
        new_payload["extendedLocation"]["type"] = new_values.get("edge_zone")
        need_update = True

    if (
        (new_values.get("idle_timeout_in_minutes") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            new_values["idle_timeout_in_minutes"]
            != existing_payload.get("properties").get("idleTimeoutInMinutes")
        )
    ):
        new_payload["properties"]["idleTimeoutInMinutes"] = new_values.get(
            "idle_timeout_in_minutes"
        )
        need_update = True

    if (
        (new_values.get("ip_address") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            new_values["ip_address"]
            != existing_payload.get("properties").get("ipAddress")
        )
    ):
        new_payload["properties"]["ipAddress"] = new_values.get("ip_address")
        need_update = True

    if (
        (new_values.get("ip_tags") is not None)
        and (existing_payload.get("properties") is not None)
        and (new_values["ip_tags"] != existing_payload.get("properties").get("ipTags"))
    ):
        new_payload["properties"]["ipTags"] = new_values.get("ip_tags")
        need_update = True

    if (
        (new_values.get("ip_version") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            new_values["ip_version"]
            != existing_payload.get("properties").get("publicIPAddressVersion")
        )
    ):
        new_payload["properties"]["publicIPAddressVersion"] = new_values.get(
            "ip_version"
        )
        need_update = True

    if (
        (new_values.get("public_ip_prefix_id") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            new_values["public_ip_prefix_id"]
            != existing_payload.get("properties").get("publicIPPrefix")
        )
    ):
        new_payload["properties"]["publicIPPrefix"] = new_values.get(
            "public_ip_prefix_id"
        )
        need_update = True

    if (
        (new_values.get("reverse_fqdn") is not None)
        and (existing_payload.get("properties") is not None)
        and (existing_payload.get("properties").get("dnsSettings") is not None)
        and (
            new_values["reverse_fqdn"]
            != existing_payload.get("properties").get("dnsSettings").get("reverseFqdn")
        )
    ):
        new_payload["properties"]["dnsSettings"]["reverseFqdn"] = new_values.get(
            "reverse_fqdn"
        )
        need_update = True

    if (
        (new_values.get("linked_public_ip_address_id") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            existing_payload.get("properties").get("linkedPublicIPAddress") is not None
        )
        and (
            new_values["linked_public_ip_address_id"]
            != existing_payload.get("properties")["linkedPublicIPAddress"].get("id")
        )
    ):
        new_payload["properties"]["linkedPublicIPAddress"] = {
            "id": new_values.get("linked_public_ip_address_id")
        }
        need_update = True

    if (
        (new_values.get("service_public_ip_address_id") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            existing_payload.get("properties").get("servicePublicIPAddress") is not None
        )
        and (
            new_values["service_public_ip_address_id"]
            != existing_payload.get("properties")["servicePublicIPAddress"].get("id")
        )
    ):
        new_payload["properties"]["servicePublicIPAddress"] = {
            "id": new_values.get("service_public_ip_address_id")
        }
        need_update = True

    if (
        (new_values.get("migration_phase") is not None)
        and (existing_payload.get("properties") is not None)
        and (
            new_values["migration_phase"]
            != existing_payload.get("properties").get("migrationPhase")
        )
    ):
        new_payload["properties"]["migrationPhase"] = new_values.get("migration_phase")
        need_update = True

    if (
        (new_values.get("sku") is not None)
        and (existing_payload.get("sku") is not None)
        and (new_values["sku"] != existing_payload.get("sku").get("name"))
    ):
        new_payload["sku"]["name"] = new_values.get("sku")
        need_update = True

    if (
        (new_values.get("sku_tier") is not None)
        and (existing_payload.get("sku") is not None)
        and (new_values["sku_tier"] != existing_payload.get("sku").get("tier"))
    ):
        new_payload["sku"]["tier"] = new_values.get("sku_tier")
        need_update = True

    if (new_values.get("tags") is not None) and (
        new_values["tags"] != existing_payload.get("tags")
    ):
        new_payload["tags"] = new_values.get("tags")
        need_update = True

    if (new_values.get("extended_location") is not None) and (
        new_values["extended_location"] != existing_payload.get("extendedLocation")
    ):
        new_payload["extendedLocation"] = {
            "name": new_values["extended_location"].get("name"),
            "type": new_values["extended_location"].get("type"),
        }
        need_update = True

    if need_update:
        result["ret"] = new_payload
    return result


def convert_raw_public_ip_addresses_to_present(
    hub,
    resource: Dict,
    idem_resource_name: str,
    resource_group_name: str,
    public_ip_address_name: str,
    resource_id: str,
    subscription_id: str,
) -> Dict[str, Any]:
    """
    Giving an existing resource state and desired state inputs, generate a dict that match the format of
     present input parameters.

    Args:
        hub: The redistributed pop central hub.
        resource: An existing resource state from Azure. This is usually a GET operation response.
        resource_group_name: Azure Resource Group name.
        idem_resource_name: The Idem name of the resource.
        public_ip_address_name: Azure Resource Group name.
        resource_id: Azure public ip address resource id.
        subscription_id: The Microsoft Azure subscription ID.

    Returns:
        A dict that contains the parameters that match the present function's input format.
    """
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "resource_group_name": resource_group_name,
        "public_ip_address_name": public_ip_address_name,
        "location": resource["location"],
        "subscription_id": subscription_id,
    }
    if "tags" in resource:
        resource_translated["tags"] = resource["tags"]
    if "zones" in resource:
        resource_translated["zones"] = resource["zones"]
    if resource.get("sku") and resource.get("sku").get("name"):
        resource_translated["sku"] = resource["sku"]["name"]
    if resource.get("sku") and resource.get("sku").get("tier"):
        resource_translated["sku_tier"] = resource["sku"]["tier"]
    if "extendedLocation" in resource:
        resource_translated["extended_location"] = {
            "name": resource["extendedLocation"].get("name"),
            "type": resource["extendedLocation"].get("type"),
        }

    properties = resource.get("properties")
    if properties:
        if "publicIPAllocationMethod" in properties:
            resource_translated["allocation_method"] = properties[
                "publicIPAllocationMethod"
            ]
        if "ddosSettings" in properties:
            resource_translated["ddos_protection_mode"] = properties["ddosSettings"][
                "protectionMode"
            ]
        if "ddosSettings" in properties:
            resource_translated["ddos_protection_plan_id"] = properties["ddosSettings"][
                "ddosProtectionPlan"
            ]
        if "dnsSettings" in properties:
            resource_translated["domain_name_label"] = properties["dnsSettings"][
                "domainNameLabel"
            ]
        # TODO [DA]: Look into the reason for extendedLocation being a part of "properties"
        #  when it seems like it is not, by the documentation:
        #  https://learn.microsoft.com/en-us/rest/api/virtualnetwork/public-ip-addresses/create-or-update?view=rest-virtualnetwork-2023-05-01&tabs=HTTP
        if "extendedLocation" in properties:
            resource_translated["edge_zone"] = properties["extendedLocation"]["type"]
        if "idleTimeoutInMinutes" in properties:
            resource_translated["idle_timeout_in_minutes"] = properties[
                "idleTimeoutInMinutes"
            ]
        if "ipAddress" in properties:
            resource_translated["ip_address"] = properties["ipAddress"]
        if "ipTags" in properties:
            resource_translated["ip_tags"] = properties["ipTags"]
        if "publicIPAddressVersion" in properties:
            resource_translated["ip_version"] = properties["publicIPAddressVersion"]
        if "publicIPPrefix" in properties:
            resource_translated["public_ip_prefix_id"] = properties["publicIPPrefix"]
        if "dnsSettings" in properties:
            resource_translated["reverse_fqdn"] = properties["dnsSettings"][
                "reverseFqdn"
            ]
        if "linkedPublicIPAddress" in properties:
            resource_translated["linked_public_ip_address_id"] = properties[
                "linkedPublicIPAddress"
            ].get("id")
        if "servicePublicIPAddress" in properties:
            resource_translated["service_public_ip_address_id"] = properties[
                "linkedPublicIPAddress"
            ].get("id")
        if "migrationPhase" in properties:
            resource_translated["migration_phase"] = properties["migrationPhase"]

    return resource_translated


def convert_present_to_raw_public_ip_addresses(
    hub,
    location: str,
    allocation_method: str = None,
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
    sku: str = None,
    sku_tier: str = None,
    tags: Dict[str, str] = None,
    extended_location: Dict[str, str] = None,
    linked_public_ip_address_id: str = None,
    service_public_ip_address_id: str = None,
    migration_phase: str = None,
    **kwargs
):
    """
    Giving some present function inputs, generate a payload that can be used during PUT operation to Azure. Any None
    value input will be ignored, unless this parameter is a required input parameter.

    Args:
        hub: The redistributed pop central hub.
        location: Resource location.
        allocation_method: Defines the allocation method for this IP address.
        zones: A collection containing the availability zone to allocate the Public IP in.
        ddos_protection_mode: The DDoS protection mode of the public IP.
        ddos_protection_plan_id: The ID of DDoS protection plan associated with the public IP.
        domain_name_label: Label for the Domain Name.
        edge_zone: Specifies the Edge Zone within the Azure Region where this Public IP should exist.
        idle_timeout_in_minutes: Specifies the timeout for the TCP idle connection.
        ip_address: The IP address associated with the public IP address resource.
        ip_tags: A mapping of IP tags to assign to the public IP.
        ip_version: The IP Version to use.
        public_ip_prefix_id: If specified then public IP address allocated will be provided from the public IP prefix resource.
        reverse_fqdn: A fully qualified domain name that resolves to this public IP address.
        sku: The SKU of the Public IP.
        sku_tier: The SKU Tier that should be used for the Public IP.
        tags: Resource tags.
        extended_location: The extended location of the public ip address.
        migration_phase: Migration phase of Public IP Address.
        linked_public_ip_address_id: The linked public IP address ID of the public IP address resource.
        service_public_ip_address_id: The service public IP address ID of the public IP address resource.

    Returns:
        A dict in the format of an Azure PUT operation payload.
    """
    payload = {"location": location}
    if tags is not None:
        payload["tags"] = tags
    if zones is not None:
        payload["zones"] = zones
    if (sku is not None) or (sku_tier is not None):
        payload["sku"] = {}
    if sku is not None:
        payload["sku"]["name"] = sku
    if sku_tier is not None:
        payload["sku"]["tier"] = sku_tier
    if extended_location is not None:
        payload["extended_location"] = {}
        if extended_location["name"] is not None:
            payload["extended_location"]["name"] = extended_location["name"]
        if extended_location["name"] is not None:
            payload["extended_location"]["type"] = extended_location["type"]
    if (
        (allocation_method is not None)
        or (ddos_protection_mode is not None)
        or (ddos_protection_plan_id is not None)
        or (domain_name_label is not None)
        or (edge_zone is not None)
        or (idle_timeout_in_minutes is not None)
        or (ip_address is not None)
        or (ip_tags is not None)
        or (ip_version is not None)
        or (public_ip_prefix_id is not None)
        or (reverse_fqdn is not None)
    ):
        payload["properties"] = {}
    if allocation_method is not None:
        payload["properties"]["publicIPAllocationMethod"] = allocation_method
    if (ddos_protection_mode is not None) or (ddos_protection_plan_id is not None):
        payload["properties"]["ddosSettings"] = {}
    if ddos_protection_mode is not None:
        payload["properties"]["ddosSettings"]["protectionMode"] = ddos_protection_mode
    if ddos_protection_plan_id is not None:
        payload["properties"]["ddosSettings"][
            "ddosProtectionPlan"
        ] = ddos_protection_plan_id
    if (domain_name_label is not None) or (reverse_fqdn is not None):
        payload["properties"]["dnsSettings"] = {}
    if domain_name_label is not None:
        payload["properties"]["dnsSettings"]["domainNameLabel"] = domain_name_label
    # TODO [DA]: Look into the reason for extendedLocation being a part of "properties"
    #  when it seems like it is not, by the documentation:
    #  https://learn.microsoft.com/en-us/rest/api/virtualnetwork/public-ip-addresses/create-or-update?view=rest-virtualnetwork-2023-05-01&tabs=HTTP
    if edge_zone is not None:
        payload["properties"]["extendedLocation"] = {}
        payload["properties"]["extendedLocation"]["type"] = edge_zone
    if idle_timeout_in_minutes is not None:
        payload["properties"]["idleTimeoutInMinutes"] = idle_timeout_in_minutes
    if ip_address is not None:
        payload["properties"]["ipAddress"] = ip_address
    if ip_tags is not None:
        payload["properties"]["ipTags"] = ip_tags
    if ip_version is not None:
        payload["properties"]["publicIPAddressVersion"] = ip_version
    if public_ip_prefix_id is not None:
        payload["properties"]["publicIPPrefix"] = public_ip_prefix_id
    if reverse_fqdn is not None:
        payload["properties"]["dnsSettings"]["reverseFqdn"] = reverse_fqdn
    if linked_public_ip_address_id is not None:
        payload["properties"]["linkedPublicIPAddress"] = {
            "id": linked_public_ip_address_id
        }
    if service_public_ip_address_id is not None:
        payload["properties"]["servicePublicIPAddress"] = {
            "id": service_public_ip_address_id
        }
    if migration_phase is not None:
        payload["properties"]["migrationPhase"] = migration_phase

    return payload
