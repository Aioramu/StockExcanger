import pytest
from stockouter.macrotrends import get_net_worth
from stockouter.macrotrends import get_ratio
from stockouter.macrotrends import get_roe
from stockouter.macrotrends import total_shares
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def test_get_networth():
    tickets = ["QCOM", "NKE", "MMC"]
    for ticket in tickets:
        net_worth = get_net_worth(ticket)
        assert net_worth != None
        assert type(net_worth) == type(float())


def test_get_ratio():
    tickets = ["V", "MA", "META"]
    req_fragments = [
        "&type=price-sales&statement=price-ratios&freq=Q",
        "&type=price-book&statement=price-ratios&freq=Q",
        "&type=price-fcf&statement=price-ratios&freq=Q",
    ]
    for req_fragment in req_fragments:
        for ticket in tickets:
            ratio = get_ratio(ticket, req_fragment)
            assert ratio != None
            assert type(ratio) == type(float())


def test_get_roe():
    tickets = ["NKE", "MSFT"]
    req_fragments = [
        "&type=roe&statement=ratios&freq=Q",
        "&type=roa&statement=ratios&freq=Q",
        "&type=roi&statement=ratios&freq=Q",
        "&type=debt-equity-ratio&statement=ratios&freq=Q",
    ]
    for req_fragment in req_fragments:
        for ticket in tickets:
            value = get_roe(ticket, req_fragment)
            assert value != None
            assert type(value) == type(float())


def test_total_shares():
    display = Display(visible=0, size=(800, 600))
    options = webdriver.FirefoxOptions()
    service = Service(executable_path="/usr/local/bin/geckodriver")
    service_log_path = "/dev/null"
    options.add_argument("--headless")  # turn off display for docker
    driver = webdriver.Firefox(
        options=options, service=service, service_log_path=service_log_path
    )
    url = "https://www.macrotrends.net/stocks/stock-screener"  # parser's target
    display.start()
    driver.get(url)
    value = total_shares(driver)
    driver.close()
    display.stop()
    assert value != None
    assert type(value) == type(int())
