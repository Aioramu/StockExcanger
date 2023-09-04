from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from typing import Dict, List
from selenium.common.exceptions import NoSuchElementException
import datetime

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


def new_page(parse):
    def wrapper_function(driver, ticket):
        driver.execute_script(
            "window.open('https://smart-lab.ru/forum/GAZP', '_blank')"
        )
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://smart-lab.ru/forum/" + ticket)
        driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div[1]"
        ).click()  # serch grath button
        parse()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return wrapper_function


@new_page
def share_ao(share_stats, driver) -> Dict:
    try:
        share_stats["price"] = driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div[3]/div[2]/span/i"
        ).text.replace("₽", "")
    except Exception as e:
        print(e)
        print("Missing ao price")
    print(share_stats)
    return share_stats


@new_page
def share_ap():
    return None


def share(i, driver) -> Dict:
    """take some shares"""
    share_stats: Dict = {}
    share_stats["name"] = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr[" + str(i) + "]/td[2]/a"
    ).text
    share_stats["pe"] = from_shares(13, i, driver)
    share_stats["ps"] = from_shares(14, i, driver)
    share_stats["pb"] = from_shares(15, i, driver)
    share_stats["env"] = from_shares(16, i, driver)
    share_stats["net_worth"] = remove_trash(from_shares(6, i, driver))
    share_stats["roe"] = remove_trash(from_shares(17, i, driver))
    share_stats["debt_eq"] = remove_trash(from_shares(18, i, driver))
    share_stats["country"] = "ru"
    if from_shares(10, i, driver) != None and from_shares(11, i, driver) == None:
        share_ao(share_stats, driver)
    return share_stats


""" ticket=models.CharField(max_length=256,unique=True)
    price=models.FloatField(null=True)
    pe=models.FloatField(null=True)
    ps=models.FloatField(null=True)
    pb=models.FloatField(null=True)
    ebitda=models.FloatField(null=True)
    env=models.FloatField(null=True)
    net_worth=models.FloatField(null=True)
    roe=models.FloatField(null=True)
    debt_eq=models.FloatField(null=True)
    roa=models.FloatField(null=True)
    roi=models.FloatField(null=True)
    last_divident=models.FloatField(null=True)"""


def from_shares(column_num, i, driver) -> str:
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


def date_check(i, driver) -> bool:
    """remove share if last report more than 3 years"""
    report = from_shares(19, i, driver)
    current_year = datetime.datetime.now().year
    suitable_year = current_year - 2
    if int(report[: report.rfind("-")]) < suitable_year:
        return False
    return True


def ticket_href_check(i, driver) -> bool:
    """remove share if ticket too long"""
    ticket_href = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr[" + str(i) + "]/td[2]/a"
    ).get_attribute("href")
    ticket = ticket_href[ticket_href.rfind("/") + 1 :]
    if len(ticket) > 10:
        print(ticket_href)
        return False
    return True


def end_of_table(i, driver) -> bool:
    try:
        element = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["
            + str(i)
            + "]/td[1]"
        ).text
    except NoSuchElementException:
        return True
    return False


@initiate_display
def switch_page(driver):
    shares = []
    i = 2
    while True:
        if end_of_table(i, driver) == True:
            break  # exit in the end of table
        elif date_check(i, driver) == False or ticket_href_check(i, driver) == False:
            pass
        else:
            share(i, driver)
        i += 1


if __name__ == "__main__":
    switch_page()
