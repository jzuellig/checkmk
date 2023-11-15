#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import SNMPTree

from cmk.plugins.lib.steelhead import DETECT_STEELHEAD


def inventory_steelhead_status(info):
    if len(info) == 1:
        yield None, {}


def check_steelhead_status(item, params, info):
    health, status = info[0]
    if health == "Healthy" and status == "running":
        return (0, "Healthy and running")
    return (2, f"Status is {health} and {status}")


check_info["steelhead_status"] = LegacyCheckDefinition(
    detect=DETECT_STEELHEAD,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.17163.1.1.2",
        oids=["2", "3"],
    ),
    service_name="Status",
    discovery_function=inventory_steelhead_status,
    check_function=check_steelhead_status,
)
