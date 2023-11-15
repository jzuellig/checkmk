#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


# mypy: disable-error-code="arg-type"

from cmk.base.check_api import get_bytes_human_readable, LegacyCheckDefinition, savefloat
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import SNMPTree

from cmk.plugins.lib.juniper import DETECT_JUNIPER_TRPZ


def inventory_juniper_trpz_flash(info):
    yield None, {}


def check_juniper_trpz_flash(_no_item, params, info):
    warn, crit = params["levels"]
    used, total = map(savefloat, info[0])
    message = f"Used: {get_bytes_human_readable(used)} of {get_bytes_human_readable(total)} "
    perc_used = (used / total) * 100  # fixed: true-division
    if isinstance(crit, float):
        a_warn = (warn / 100.0) * total
        a_crit = (crit / 100.0) * total
        perf = [("used", used, a_warn, a_crit, 0, total)]
        levels = f"Levels Warn/Crit are ({warn:.2f}%, {crit:.2f}%)"
        if perc_used > crit:
            return 2, message + levels, perf
        if perc_used > warn:
            return 1, message + levels, perf
    else:
        perf = [("used", used, warn, crit, 0, total)]
        levels = "Levels Warn/Crit are ({}, {})".format(
            get_bytes_human_readable(warn),
            get_bytes_human_readable(crit),
        )
        if used > crit:
            return 2, message + levels, perf
        if used > warn:
            return 1, message + levels, perf
    return 0, message, perf


check_info["juniper_trpz_flash"] = LegacyCheckDefinition(
    detect=DETECT_JUNIPER_TRPZ,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.14525.4.8.1.1",
        oids=["3", "4"],
    ),
    service_name="Flash",
    discovery_function=inventory_juniper_trpz_flash,
    check_function=check_juniper_trpz_flash,
    check_ruleset_name="general_flash_usage",
    check_default_parameters={"levels": (90.0, 95.0)},
)
