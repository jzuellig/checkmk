#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# Example output from agent:
# <<<citrix_hostsystem>>>
# VMName rz1css01
# CitrixPoolName RZ1XenPool01 - Cisco UCS


# Note(1): The pool name is the same for all VMs on one host system
# Note(2): for the same host and vm this section can appear
# several times (with the same content).


# mypy: disable-error-code="attr-defined"

from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.config import check_info


def parse_citrix_hostsystem(string_table):
    parsed = {"vms": [], "pool": ""}
    for line in string_table:
        if line[0] == "VMName":
            vm = " ".join(line[1:])
            if vm not in parsed["vms"]:
                parsed["vms"].append(vm)
        elif line[0] == "CitrixPoolName":
            pool = " ".join(line[1:])
            if not parsed["pool"]:
                parsed["pool"] = pool
    return parsed


#   .--Host VMs------------------------------------------------------------.
#   |              _   _           _    __     ____  __                    |
#   |             | | | | ___  ___| |_  \ \   / /  \/  |___                |
#   |             | |_| |/ _ \/ __| __|  \ \ / /| |\/| / __|               |
#   |             |  _  | (_) \__ \ |_    \ V / | |  | \__ \               |
#   |             |_| |_|\___/|___/\__|    \_/  |_|  |_|___/               |
#   |                                                                      |
#   '----------------------------------------------------------------------'


def inventory_citrix_hostsystem_vms(parsed):
    if parsed["vms"]:
        return [(None, None)]
    return []


def check_citrix_hostsystem_vms(_no_item, _no_params, parsed):
    vmlist = parsed["vms"]
    return 0, "%d VMs running: %s" % (len(vmlist), ", ".join(vmlist))


check_info["citrix_hostsystem.vms"] = LegacyCheckDefinition(
    service_name="Citrix VMs",
    sections=["citrix_hostsystem"],
    discovery_function=inventory_citrix_hostsystem_vms,
    check_function=check_citrix_hostsystem_vms,
)

# .
#   .--Host Info-----------------------------------------------------------.
#   |              _   _           _     ___        __                     |
#   |             | | | | ___  ___| |_  |_ _|_ __  / _| ___                |
#   |             | |_| |/ _ \/ __| __|  | || '_ \| |_ / _ \               |
#   |             |  _  | (_) \__ \ |_   | || | | |  _| (_) |              |
#   |             |_| |_|\___/|___/\__| |___|_| |_|_|  \___/               |
#   |                                                                      |
#   '----------------------------------------------------------------------'


def inventory_citrix_hostsystem(parsed):
    if parsed["pool"]:
        return [(None, None)]
    return []


def check_citrix_hostsystem(_no_item, _no_params, parsed):
    return 0, "Citrix Pool Name: %s" % parsed["pool"]


check_info["citrix_hostsystem"] = LegacyCheckDefinition(
    parse_function=parse_citrix_hostsystem,
    service_name="Citrix Host Info",
    discovery_function=inventory_citrix_hostsystem,
    check_function=check_citrix_hostsystem,
)
