from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from typing import Dict, List
from selenium.common.exceptions import NoSuchElementException
import datetime
import re
import queue


url = "https://smart-lab.ru/q/shares_fundamental/"  # parser's target


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
        display.start()
        driver.get(url)
        body(driver, *args, **kwargs)
        driver.close()
        display.stop()

    return selenium_and_display_settings


def remove_trash(string) -> str:
    """Remove % ₽ млрд spases and replace , to ."""
    string = str(string)
    string = (
        string.replace(",", ".")
        .replace(" ", "")
        .replace("%", "")
        .replace("₽", "")
        .replace("млрд", "")
    )
    return string


def floating(share_stats):
    for key, value in share_stats.items():
        if value is not None:
            if (
                key == "pe"
                or key == "ps"
                or key == "pb"
                or key == "env"
                or key == "net_worth"
                or key == "debt_eq"
                or key == "net_income"
                or key == "income_after_taxes"
                or key == "roe"
                or key == "roi"
                or key == "roa"
                or key == "price"
                or key == "ebitda"
                or key == "last_divident"
            ):
                try:
                    float_value = float(value)
                    share_stats[key] = float_value
                except ValueError:
                    share_stats[key] = None
    return share_stats


def send_list(shares: List[Dict], q) -> List[Dict]:
    """get value from queue, append to list and send to serialaizer"""
    while not q.empty():
        shares.append(q.get())
    # bulk_update(shares)
    print(shares)  # print for test
    shares.clear()
    return shares


def from_shares_banks(column_num, i, driver) -> str:
    """Take some text from shares fundamental"""
    l = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["
        + str(i)
        + "]/td["
        + str(column_num)
        + "]"
    ).text
    if len(l) < 1:
        return None
    return l


def date_check_banks(i, driver) -> bool:
    """remove share if last report more than 3 years"""
    report = str(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr["
            + str(i)
            + "]/td[17]"
        ).text
    )
    current_year = datetime.datetime.now().year
    suitable_year = current_year - 2
    if int(report[: report.rfind("-")]) < suitable_year:
        return False
    return True


def end_of_banks_table(i, driver) -> bool:
    try:
        element = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr["
            + str(i)
            + "]/td[1]"
        ).text
    except NoSuchElementException:
        return True
    return False


def share_from_page(share_stats, driver, price_div) -> Dict:
    link = "window.open('https://smart-lab.ru/forum/" + str(ticket) + "', '_blank')"
    driver.execute_script(link)
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://smart-lab.ru/forum/" + ticket)
    driver.find_element_by_xpath(
        "/html/body/div[2]/div[3]/div[1]"
    ).click()  # serch grath button
    ao = "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[3]/tbody/tr[4]/td[2]"
    ap = "/html/body/div[2]/div[3]/div[3]/div[2]/span/i"
    ao_with_ap = "/html/body/div[2]/div[3]/div[3]/div[2]/span[1]/i"
    ap_with_ao = "/html/body/div[2]/div[3]/div[3]/div[2]/span[2]/i"
    if price_div == "ao":
        price_d = ao
    elif price_div == "ao_with_ap":
        price_d = ao_with_ap
    elif price_div == "ap_with_ao":
        price_d = ap_with_ao
    elif price_div == "ap":
        price_d = ap
    try:
        share_stats["price"] = driver.find_element_by_xpath(price_d).text
    except Exception:
        share_stats["price"] = None
    share_stats["price"] = remove_trash(share_stats["price"])
    if share_stats["price"] != None:
        pattern = r"^[0-9.]+$"
        match = re.match(pattern, share_stats["price"])
        if not match:
            share_stats["price"] = None
    try:
        share_stats["ebitda"] = str(
            remove_trash(
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[2]/tbody/tr[3]/td[2]"
                ).text
            )
        )
    except Exception:
        share_stats["ebitda"] = None
    if share_stats["ebitda"] != None:
        pattern = r"^[0-9.]+$"
        match = re.match(pattern, share_stats["ebitda"])
        if not match:
            share_stats["ebitda"] = None
    if price_div == "ao" or price_div == "ao_with_ap":
        try:
            share_stats["last_divident"] = str(
                remove_trash(
                    driver.find_element_by_xpath(
                        "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[3]/tbody/tr[5]/td[2]"
                    ).text
                )
            )
        except Exception:
            share_stats["last_divident"] = None
    elif price_div == "ap_with_ao" or price_div == "ap":
        try:
            share_stats["last_divident"] = str(
                remove_trash(
                    driver.find_element_by_xpath(
                        "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[3]/tbody/tr[6]/td[2]"
                    ).text
                )
            )
        except Exception:
            share_stats["last_divident"] = None
        price_d = ao_with_ap
    try:
        share_stats["ps"] = str(
            remove_trash(
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[3]/tbody/tr[2]/td[2]"
                ).text
            )
        )
    except Exception:
        pass
    try:
        share_stats["pb"] = str(
            remove_trash(
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[3]/tbody/tr[3]/td[2]"
                ).text
            )
        )
    except Exception:
        pass
    try:
        share_stats["pe"] = str(
            remove_trash(
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[3]/tbody/tr[1]/td[2]"
                ).text
            )
        )
    except Exception:
        pass
    try:
        share_stats["net_income"] = str(
            remove_trash(
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[2]/tbody/tr[2]/td[2]"
                ).text
            )
        )
    except Exception:
        pass
    try:
        share_stats["income_after_taxes"] = str(
            remove_trash(
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[2]/tbody/tr[4]/td[2]"
                ).text
            )
        )
    except Exception:
        pass
    share_stats["ticket"] = ticket
    if price_div == "ap_with_ao" or price_div == "ap":
        share_stats["ticket"]
        try:
            share_stats["ticket"] = str(
                remove_trash(
                    driver.find_element_by_xpath(
                        "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[1]/tbody/tr[6]/td[2]/ul/li"
                    ).text
                )
            )
        except Exception:
            share_stats["price"] = None
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return share_stats


def share_banks(i, q, shares, driver) -> Dict:
    """take some shares"""
    share_stats: Dict = {}
    share_stats["name"] = str(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr[2"
            + str(i)
            + "]/td[2]"
        ).text
    )
    share_stats["pe"] = str(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr["
            + str(i)
            + "]/td[12]"
        ).text
    )
    share_stats["ps"] = None
    share_stats["pb"] = str(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr[2"
            + str(i)
            + "]/td[13]"
        ).text
    )
    share_stats["env"] = str(
        driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr[2"
            + str(i)
            + "]/td[2]"
        ).text
    )
    share_stats["net_worth"] = remove_trash(
        str(
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr[2"
                + str(i)
                + "]/td[2]"
            ).text
        )
    )
    share_stats["debt_eq"] = remove_trash(
        str(
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr[2"
                + str(i)
                + "]/td[2]"
            ).text
        )
    )
    share_stats["net_income"] = remove_trash(
        str(
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr[2"
                + str(i)
                + "]/td[2]"
            ).text
        )
    )
    share_stats["income_after_taxes"] = remove_trash(
        str(
            driver.find_element_by_xpath(
                "/html/body/div[1]/div/div[6]/div/div/table[2]/tbody/tr[2"
                + str(i)
                + "]/td[2]"
            ).text
        )
    )
    share_stats["country"] = "ru"
    share_stats["roe"] = None
    share_stats["roi"] = None
    share_stats["roa"] = None
    if from_shares(10, i, driver) != None and from_shares(11, i, driver) == None:
        price_div = "ao"
        share_from_page(share_stats, driver, price_div)
    elif from_shares(10, i, driver) != None and from_shares(11, i, driver) != None:
        price_div = "ao_with_ap"
        share_from_page(share_stats, driver, price_div)
        floating(share_stats)
        q.put(share_stats)
        price_div = "ap_with_ao"
        share_from_page(share_stats, driver, price_div)
    elif from_shares(10, i, driver) == None and from_shares(11, i, driver) != None:
        price_div = "ap"
        share_from_page(share_stats, driver, price_div)
    floating(share_stats)
    q.put(share_stats)
    if (i - 1) % 20 == 0:
        send_list(shares, q)
    return share_stats


@initiate_display
def switch_page(driver):
    shares: List[Dict] = []
    q = queue.SimpleQueue()
    i = 2
    while True:
        if end_of_banks_table(i, driver) == True:
            send_list(shares, q)
            break  # exit in the end of table
        elif date_check_banks(i, driver) == False:
            pass
        else:
            print(i)
            share_banks(i, q, shares, driver)
        i += 1


if __name__ == "__main__":
    switch_page()
