from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import requests
import ast
import json


url = "https://smart-lab.ru/q/shares_fundamental/"
django_url = "http://web:8000"
shares = []
i=1

#selenium and display settings
display = Display(visible=0, size=(800, 600))
options = webdriver.FirefoxOptions()
service = Service(executable_path = "/usr/local/bin/geckodriver")
service_log_path = "/dev/null"
options.add_argument('--headless') #turn off display for docker
driver = webdriver.Firefox(options=options, service=service, service_log_path=service_log_path)


class Share(object):

    def __init__(self, url):
        self.url = url
    """Take some Share's stats"""

    def from_shares(self, tdnum):
        """Take some text from shares fundamental"""
        l=driver.find_element_by_xpath(
         "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td["+str(tdnum)+"]").text
        return(l)

    def remove_trash(string):
        """Remove % ₽ млрд spases and replace , to ."""
        string=str(string)
        string=string.replace(",", ".").replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "")
        return string

    def share_body(self):
        report = self.from_shares(19)
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
                share_stats["pe"]=self.from_shares(13)
                share_stats["ps"]=self.from_shares(14)
                share_stats["pb"]=self.from_shares(15)
                share_stats["env"]=self.from_shares(16)
                share_stats["net_worth"]=self.from_shares(6)
                share_stats["net_worth"]=share_stats["net_worth"].replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "").replace(",", ".")
                share_stats["roe"]=self.from_shares(17)
                share_stats["roe"]=share_stats["roe"].replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "").replace(",", ".")
                share_stats["debt_eq"]=self.from_shares(18)
                share_stats["country"]="ru"
                share_stats=self.ao(ticket, share_stats)
                #shares.append(share_stats)
                return share_stats

    def ao(self, ticket, share_stats):
        driver.execute_script("window.open('https://smart-lab.ru/forum/GAZP', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://smart-lab.ru/forum/"+ticket)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]").click() #serch grath button 
        try:
            share_stats["price"]=driver.find_element_by_xpath(
                                "/html/body/div[2]/div[3]/div[3]/div[2]/span/i").text.replace("₽", "")
        except Exception as e:
            print(e)
            print("Missing ao price")
            #return None
        try:
            share_stats["ebitda"]=driver.find_element_by_xpath(
                                 "/html/body/div[2]/div[3]/div[2]/div[2]/div/table[2]/tbody/tr[3]/td[2]").text #.replace(" млрд", "")
            share_stats["ebitda"]=share_stats["ebitda"].replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "").replace(",", ".")
        except Exception as e:
            print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return share_stats

    def ap(self, share_stats):
        driver.execute_script("window.open('https://smart-lab.ru/forum/GAZP', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://smart-lab.ru/forum/"+ticket_for_url)
        driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]").click()
        try:
            share_stats["ticket"]=driver.find_element_by_xpath(
                                  "/html/body/div[2]/div[2]/div[2]/div[2]/div/table[1]/tbody/tr[6]/td[2]/ul/li").text
        except Exception as e:
            print(e)
            share_stats["ticket"]=share_stats["ticket"
                                  ].replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "").replace(",", ".")
        try:
            share_stats["price"]=driver.find_element_by_xpath(
                                 "/html/body/div[2]/div[2]/div[3]/div[2]/span[2]/i").text.replace("₽", "")
        except Exception as e:
            print(e)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return share_stats

def post_to_django(shares, django_url):
    #stock_dict = ast.literal_eval(data)
    stock_post = requests.post(django_url, json=shares)
    print(stock_post.status_code)
    print(stock_post.text)

if __name__ == "__main__":
    display.start()
    driver.get(url)
    gas = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr[2]/td[11]").text #Empty ap"
    while(True):
        try:
            i+=1
            tr = str(i+1)
            stock = Share("https://smart-lab.ru/q/shares_fundamental/")
            t = stock.share_body()
            shares.clear()
            shares.append(t)
            if driver.find_element_by_xpath(
                     "/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(tr)+"]/td[11]").text == gas:
                #post_to_django(shares, django_url)
                print(shares)
            else:
                stock_ao = stock.share_body()
                if stock_ao!=None:
                    #ost_to_django(stock_ao, django_url)
                    print(stock_ao)
                    ticket_for_url = stock_ao["ticket"]
                    stock_ap = stock.ap(stock_ao)
                    #post_to_django(stock_ap, django_url)
                    print(stock_ap)
        except Exception as e:
            #driver.quit()
            #display.stop()
            print(e)
            break
