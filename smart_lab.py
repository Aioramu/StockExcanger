from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import requests
import ast
import json


display = Display(visible=0, size=(800, 600))
options = webdriver.FirefoxOptions()
service = Service(executable_path = "/usr/local/bin/geckodriver")
options.add_argument('--headless') #turn off display for docker
driver = webdriver.Firefox(options=options, service=service)

django_url = "http://172.21.0.1:8000"
display.start()
url = "https://smart-lab.ru/q/shares_fundamental/"
driver.get(url)
gas = driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr[2]/td[11]").text
#"I am the godness of recursion. On the river this sheep code one row above to the saint"
i=1

def from_shares(tdnum):
    """Take some text from shares fundamental"""
    l=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td["+str(tdnum)+"]").text
    return(l)

def remove_trash(string):
    """Remove % ₽ млрд spases and replace , to ."""
    string=str(string)
    string=string.replace(",", ".").replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "")
    return string

class Share(object):

    def __init__(self, url):
        self.url = url
    """Take some Share's stats"""

    def share_body(self):
        report = from_shares(19)
        if int(report[:report.rfind('-')]) <= 2019:
            print("Too old")
            return None
        else:
            ticket_href = driver.find_element_by_xpath(
                        "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[2]/a").get_attribute("href")
            ticket = ticket_href[ticket_href.rfind('/')+1:]
            if len(ticket) > 10:
                print("Too scam")
                return None
            else:
                share_stats = {}
                share_stats["name"]=driver.find_element_by_xpath(
                                   "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[2]/a").text
                share_stats["ticket"]=ticket
                share_stats["pe"]=from_shares(13)
                share_stats["ps"]=from_shares(14)
                share_stats["pb"]=from_shares(15)
                share_stats["env"]=from_shares(16)
                share_stats["net_worth"]=remove_trash(from_shares(6))
                share_stats["roe"]=remove_trash(from_shares(17))
                share_stats["debt_eq"]=from_shares(18)
                share_stats=self.ao(ticket, share_stats)
                return share_stats

    def ao(self, ticket, share_stats):
        driver.execute_script("window.open('https://smart-lab.ru/forum/GAZP', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://smart-lab.ru/forum/"+ticket)
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]").click()
        try:
            share_stats["price"]=driver.find_element_by_xpath(
                                "/html/body/div[2]/div[2]/div[3]/div[2]/span/i").text.replace("₽", "")
        except Exception as e:
            print(e)
            print("Missing ao price")
            #return None
        try:
            share_stats["ebitda"]=driver.find_element_by_xpath(
                                 "/html/body/div[2]/div[2]/div[2]/div[2]/div/table[2]/tbody/tr[3]/td[2]").text #.replace(" млрд", "")
            share_stats["ebitda"]=remove_trash(share_stats["ebitda"])
        except Exception as e:
            print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return share_stats

    def ap(self, share_stats):
        driver.execute_script("window.open('https://smart-lab.ru/forum/GAZP', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://smart-lab.ru/forum/"+ticket_for_url)
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]").click()
        try:
            share_stats["ticket"]=driver.find_element_by_xpath(
                                 "/html/body/div[2]/div[2]/div[2]/div[2]/div/table[1]/tbody/tr[6]/td[2]/ul/li").text
        except Exception as e:
            print(e)
            share_stats["ticket"]=share_stats["ticket"]
        try:
            share_stats["price"]=driver.find_element_by_xpath(
                                 "/html/body/div[2]/div[2]/div[3]/div[2]/span[2]/i").text.replace("₽", "")
        except Exception as e:
            print(e)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return share_stats



while(True):
    try:
        i+=1
        if __name__ == "__main__":
            stock = Share("https://smart-lab.ru/q/shares_fundamental/")
            shares = []
            d = shares.append(stock.share_body())
            if driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[11]").text == gas:
                r = requests.post(django_url, data=d)
                print(r.status_code)
                print(r.text)
                #print(stock.share_body())
    #        elif driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[9]").text == "0.0%":
        #        continue
            else:
                stock_ao = d
                if stock_ao!=None:
                    #print(stock_ao)
                    r = requests.post(django_url, data=stock_ao)
                    print(r.status_code)
                    print(r.text)
                    ticket_for_url = stock_ao["ticket"]
                    stock_ap = stock.ap(stock_ao)
                    print(stock_ap)
                    #requests.post("172.18.0.4:8000", data=stock_ap)
    except Exception as e:
        #driver.quit()
        #display.stop()
        print(e)
