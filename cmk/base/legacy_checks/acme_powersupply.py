#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.check_legacy_includes.acme import acme_environment_states
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import SNMPTree

from cmk.plugins.lib.acme import DETECT_ACME

# .1.3.6.1.4.1.9148.3.3.1.5.1.1.3.1 Power Supply A --> ACMEPACKET-ENVMON-MIB::apEnvMonPowerSupplyStatusDescr.1
# .1.3.6.1.4.1.9148.3.3.1.5.1.1.3.2 Power Supply B --> ACMEPACKET-ENVMON-MIB::apEnvMonPowerSupplyStatusDescr.2
# .1.3.6.1.4.1.9148.3.3.1.5.1.1.4.1 2 --> ACMEPACKET-ENVMON-MIB::apEnvMonPowerSupplyState.1
# .1.3.6.1.4.1.9148.3.3.1.5.1.1.4.2 2 --> ACMEPACKET-ENVMON-MIB::apEnvMonPowerSupplyState.2


def inventory_acme_powersupply(info):
    return [(descr, None) for descr, state in info if state != "7"]


def check_acme_powersupply(item, _no_params, info):
    for descr, state in info:
        if item == descr:
            dev_state, dev_state_readable = acme_environment_states[state]
            return dev_state, "Status: %s" % dev_state_readable
    return None


check_info["acme_powersupply"] = LegacyCheckDefinition(
    detect=DETECT_ACME,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9148.3.3.1.5.1.1",
        oids=["3", "4"],
    ),
    service_name="Power supply %s",
    discovery_function=inventory_acme_powersupply,
    check_function=check_acme_powersupply,
)
