import pytest
from stockouter.macrotrends import get_net_worth
from stockouter.macrotrends import get_ratio
from stockouter.macrotrends import get_roe
from stockouter.macrotrends import total_shares
from stockouter.macrotrends import initiate_display

tickets = ["NKE", "MSFT", "SHEL"]


def test_get_ps():
    req_fragment = "&type=price-sales&statement=price-ratios&freq=Q"
    for ticket in tickets:
        ratio = get_ratio(ticket, req_fragment)
        assert ratio != None
        assert type(ratio) == type(float())


def test_get_pb():
    req_fragment = "&type=price-book&statement=price-ratios&freq=Q"
    for ticket in tickets:
        ratio = get_ratio(ticket, req_fragment)
        assert ratio != None
        assert type(ratio) == type(float())


def test_get_env():
    req_fragment = "&type=price-fcf&statement=price-ratios&freq=Q"
    for ticket in tickets:
        ratio = get_ratio(ticket, req_fragment)
        assert ratio != None
        assert type(ratio) == type(float())


def test_get_networth():
    for ticket in tickets:
        net_worth = get_net_worth(ticket)
        assert net_worth != None
        assert type(net_worth) == type(float())


def test_get_roe():
    req_fragment = "&type=roe&statement=ratios&freq=Q"
    for ticket in tickets:
        value = get_roe(ticket, req_fragment)
        assert value != None
        assert type(value) == type(float())


def test_get_roa():
    req_fragment = "&type=roa&statement=ratios&freq=Q"
    for ticket in tickets:
        value = get_roe(ticket, req_fragment)
        assert value != None
        assert type(value) == type(float())


def test_get_roi():
    req_fragment = "&type=roi&statement=ratios&freq=Q"
    for ticket in tickets:
        value = get_roe(ticket, req_fragment)
        assert value != None
        assert type(value) == type(float())


@initiate_display
def test_total_shares(driver):
    value = total_shares(driver)
    assert value != None
    assert type(value) == type(int())
