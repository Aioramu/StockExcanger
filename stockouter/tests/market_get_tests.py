import pytest
from stockouter.macrotrends import get_net_worth


def test_get_networth():
    tickets = ["QCOM", "NKE", "MMC"]
    for ticket in tickets:
        net_worth = get_net_worth(ticket)

        assert net_worth != None
        assert type(net_worth) == type(str())
