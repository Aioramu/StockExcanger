import queue
import re
import threading
from time import sleep
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# from .crud import bulk_update

thread_count = 4


# def initiate_display() -> None:
#    switch_page(driver)


def share(stock_count, driver) -> Dict:
    """take some shares"""
    share_stats: Dict = {}
    ticket = driver.find_element_by_xpath(
        "/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["
        + str(stock_count)
        + "]/div[2]/div"
    ).text
    share_stats["ticket"] = ticket
    share_stats["name"] = driver.find_element_by_xpath(
        "/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["
        + str(stock_count)
        + "]/div[1]/div/div/a"
    ).text
    share_stats["price"] = float(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["
            + str(stock_count)
            + "]/div[5]/div"
        ).text.replace(",", "")
    )
    share_stats["last_divident"] = float(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["
            + str(stock_count)
            + "]/div[8]/div"
        ).text.replace("%", "")
    )
    share_stats["pe"] = float(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["
            + str(stock_count)
            + "]/div[7]/div"
        ).text
    )
    share_stats["ps"] = get_ratio(
        ticket, "&type=price-sales&statement=price-ratios&freq=Q"
    )
    share_stats["pb"] = get_ratio(
        ticket, "&type=price-book&statement=price-ratios&freq=Q"
    )
    share_stats["env"] = get_ratio(
        ticket, "&type=price-fcf&statement=price-ratios&freq=Q"
    )
    share_stats["net_worth"] = get_net_worth(ticket)
    share_stats["roe"] = get_roe(ticket, "&type=roe&statement=ratios&freq=Q")
    share_stats["roa"] = get_roe(ticket, "&type=roa&statement=ratios&freq=Q")
    share_stats["roi"] = get_roe(ticket, "&type=roi&statement=ratios&freq=Q")
    share_stats["debt_eq"] = get_roe(
        ticket, "&type=debt-equity-ratio&statement=ratios&freq=Q"
    )
    share_stats["country"] = "us"
    return share_stats


def get_ratio(ticket: str, req_fragment: str) -> float:
    """for ps, pb or env"""
    ratio_url = (
        "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t="
        + ticket
        + req_fragment
    )
    try:
        last_vals = (
            get_graph_var(ratio_url)[::-1].replace('"v3":', "").replace("}]", "")
        )
    except TypeError:
        return None
    split_vals = last_vals.split(",")
    f_split_vals = float(split_vals[1])
    return f_split_vals


def get_net_worth(ticket: str) -> float:
    """return net worth in billions"""
    ratio_url = "https://www.macrotrends.net/assets/php/market_cap.php?t=" + ticket
    try:
        last_vals = float(get_graph_var(ratio_url)[::-1].replace("}]", ""))
    except TypeError:
        return None
    return last_vals


def get_roe(ticket: str, req_fragment: str) -> float:
    """for roe, roa, roi or debt_eq"""
    ratio_url = (
        "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t="
        + ticket
        + req_fragment
    )
    try:
        last_vals = (
            get_graph_var(ratio_url)[::-1]
            .replace('"v2":', "")
            .replace('"v3":', "")
            .replace("}]", "")
        )
    except TypeError:
        return None
    split_vals = last_vals.split(",")
    if split_vals[2] == "null":
        return None
    else:
        f_split_vals = float(split_vals[2])
        return f_split_vals


def get_graph_var(ratio_url: str) -> str:
    """helper func for get_ratio, get_net_worth, get_roe"""
    response = requests.get(
        ratio_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        },
    )
    soup = BeautifulSoup(response.text)
    string_soup = str(soup)
    find_var = re.search("var chartData.*}]", string_soup)
    save_var = str(find_var[0])[::-1]
    cut_last_vals = save_var.split(':"1v')[0]
    return cut_last_vals


def total_shares(driver) -> int:
    """ "total_shares count plus one"""
    page_num = driver.find_element_by_xpath(
        "/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[10]/div/div[6]"
    ).text
    count: int = int(page_num.split(" ")[-1]) + 1  # plus one
    return count


def view_page(stock_count: int, driver, q) -> None:
    """parse and add one dict to queue"""
    try:
        q.put(share(stock_count, driver))
    except Exception as e:
        print(e)
    return None


def send_list(shares: List[Dict], q) -> List[Dict]:
    """get value from queue, append to list and send to serialaizer"""
    while not q.empty():
        shares.append(q.get())
    # bulk_update(shares)
    print(shares)
    return shares


def initiate_display(body):
    def selenium_and_display_settings(*args, **kwargs):
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
        body(driver, *args, **kwargs)
        driver.close()
        display.stop()

    return selenium_and_display_settings


@initiate_display
def switch_page(driver) -> None:
    """switch to next page"""
    stock_count: int = 1
    shares: List[Dict] = []
    q = queue.SimpleQueue()
    for stock in range(1, total_shares(driver)):
        if stock_count % 21 == 0:
            while threading.active_count() > 1:
                sleep(0.1)
            driver.find_element_by_xpath(
                "/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[10]/div/div[4]/div"
            ).click()
            stock_count = 1
            send_list(shares, q)
            shares.clear()
        while threading.active_count() >= thread_count:
            sleep(0.25)
        th = threading.Thread(
            target=view_page, args=(stock_count, driver, q), daemon=True
        )
        th.start()
        stock_count += 1
    sleep(10)
    send_list(shares, q)
    return None
