#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import json
from collections.abc import Mapping

from cmk.base.plugins.agent_based.agent_based_api.v1 import register
from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import CheckResult, StringTable
from cmk.base.plugins.agent_based.utils import netapp_api
from cmk.base.plugins.agent_based.utils import netapp_ontap_models as models

Section = Mapping[str, models.ShelfFanModel]

# <<<netapp_ontap_fan:sep(0)>>>
# {
#     "fans": [
#         {"id": 1, "rpm": 3030, "state": "ok"},
#         {"id": 2, "rpm": 2970, "state": "ok"},
#         {"id": 3, "rpm": 3030, "state": "ok"},
#         {"id": 4, "rpm": 3000, "state": "ok"},
#     ],
#     "id": "10",
# }
# {
#     "fans": [
#         {"id": 1, "rpm": 2970, "state": "ok"},
#         {"id": 2, "rpm": 3030, "state": "ok"},
#         {"id": 3, "rpm": 3000, "state": "ok"},
#         {"id": 4, "rpm": 3060, "state": "ok"},
#     ],
#     "id": "20",
# }


def _get_section_single_instance(section: Section) -> netapp_api.SectionSingleInstance:
    # see netapp_api._DEV_KEYS["fan"]
    error_key = "cooling-element-is-error"
    number_key = "cooling-element-number"

    return {
        key: {error_key: str(val.state == "error").lower(), number_key: key}
        for key, val in section.items()
    }


def parse_netapp_ontap_fan(string_table: StringTable) -> Section:
    """
    It should be parsed/discoverd evaluating with "installed"/"not installed" but the API is not
    responding with this information
    """

    return {
        fan.item_name(): fan
        for line in string_table
        if (fan := models.ShelfFanModel(**json.loads(line[0])))
    }


register.agent_section(
    name="netapp_ontap_fan",
    parse_function=parse_netapp_ontap_fan,
)


def check_netapp_ontap_fan(item: str, section: Section) -> CheckResult:
    yield from netapp_api.get_single_check("fan")(item, _get_section_single_instance(section))


register.check_plugin(
    name="netapp_ontap_fan",
    service_name="Fan Shelf %s",
    sections=["netapp_ontap_fan"],
    discovery_function=netapp_api.discover_single,
    discovery_ruleset_name="discovery_netapp_api_fan_rules",
    discovery_default_parameters={"mode": "single"},
    check_function=check_netapp_ontap_fan,
)


def check_netapp_ontap_fan_summary(
    item: str,
    section: Section,
) -> CheckResult:
    yield from netapp_api.get_summary_check("fan")(item, _get_section_single_instance(section))


register.check_plugin(
    name="netapp_ontap_fan_summary",
    service_name="Fan Shelf %s",
    sections=["netapp_ontap_fan"],
    discovery_function=netapp_api.discover_summary,
    discovery_ruleset_name="discovery_netapp_api_fan_rules",
    discovery_default_parameters={"mode": "single"},
    check_function=check_netapp_ontap_fan_summary,
)
