#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#

from ocean_lib.ocean.util import to_base_18
from ocean_lib.web3_internal.event_filter import EventFilter


def test_transfer_event_filter(alice_ocean, alice_wallet, alice_address, bob_address):
    token = alice_ocean.create_data_token(
        "DataToken1", "DT1", from_wallet=alice_wallet, blob="foo_blob"
    )

    token.mint(alice_address, to_base_18(100.0), from_wallet=alice_wallet)
    token.approve(bob_address, to_base_18(1.0), from_wallet=alice_wallet)
    token.transfer(bob_address, to_base_18(5.0), from_wallet=alice_wallet)

    block = alice_ocean.web3.eth.blockNumber
    event = getattr(token.events, "Transfer")
    event_filter = EventFilter("Transfer", event, None, block, block)

    assert event_filter.filter_id

    event_filter.uninstall()
    event_filter.recreate_filter()

    assert event_filter.get_new_entries() == []
