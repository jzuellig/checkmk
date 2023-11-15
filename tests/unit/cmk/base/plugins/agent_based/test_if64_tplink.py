#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.base.plugins.agent_based.if64_tplink import parse_if64_tplink

from cmk.plugins.lib import interfaces


def test_parse_if64_tplink() -> None:
    assert parse_if64_tplink(
        [
            [
                "1",
                "Vlan-interface1",
                "6",
                "0",
                "1",
                "377138653",
                "0",
                "322566",
                "0",
                "0",
                "0",
                "833158925",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "",
                [172, 132, 198, 175, 52, 255],
                "",
            ],
            [
                "49153",
                "gigabitEthernet 1/0/1 : copper",
                "6",
                "1000",
                "1",
                "304751823764",
                "273677445",
                "622053",
                "471593",
                "0",
                "0",
                "28059984507",
                "146316671",
                "2292666",
                "221224",
                "0",
                "0",
                "0",
                "",
                [172, 132, 198, 175, 52, 255],
                "ifAlias",
            ],
        ]
    ) == [
        interfaces.InterfaceWithCounters(
            interfaces.Attributes(
                index="1",
                descr="Vlan-interface1",
                alias="",
                type="6",
                speed=0,
                oper_status="1",
                out_qlen=0,
                phys_address=[172, 132, 198, 175, 52, 255],
                oper_status_name="up",
                speed_as_text="",
                group=None,
                node=None,
                admin_status=None,
            ),
            interfaces.Counters(
                in_octets=377138653,
                in_ucast=0,
                in_mcast=322566,
                in_bcast=0,
                in_disc=0,
                in_err=0,
                out_octets=833158925,
                out_ucast=0,
                out_mcast=0,
                out_bcast=0,
                out_disc=0,
                out_err=0,
            ),
        ),
        interfaces.InterfaceWithCounters(
            interfaces.Attributes(
                index="49153",
                descr="gigabitEthernet 1/0/1 : copper",
                alias="ifAlias",
                type="6",
                speed=1000000000,
                oper_status="1",
                out_qlen=0,
                phys_address=[172, 132, 198, 175, 52, 255],
                oper_status_name="up",
                speed_as_text="",
                group=None,
                node=None,
                admin_status=None,
            ),
            interfaces.Counters(
                in_octets=304751823764,
                in_ucast=273677445,
                in_mcast=622053,
                in_bcast=471593,
                in_disc=0,
                in_err=0,
                out_octets=28059984507,
                out_ucast=146316671,
                out_mcast=2292666,
                out_bcast=221224,
                out_disc=0,
                out_err=0,
            ),
        ),
    ]
