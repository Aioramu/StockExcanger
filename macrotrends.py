from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import requests
import ast


#global variables
django_url = "http://172.21.0.1:8000"
url = "https://www.macrotrends.net/stocks/stock-screener"
stock_count=1 #on curr page, takes 1-20 values

#selenium and display settings
display = Display(visible=0, size=(800, 600))
options = webdriver.FirefoxOptions()
service = Service(executable_path = "/usr/local/bin/geckodriver")
#options.add_argument('--headless') #turn off display for docker
driver = webdriver.Firefox(options=options, service=service)


def switch_page(i):
    global stock_count
    if i%20==0: #switch to next page
        driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[10]/div/div[4]/div").click()
        sleep(1)
        stock_count=1
    else:
        stock_count+=1

def share(stock_count):
    share_stats = {}
    print(stock_count)
    share_stats["name"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[1]/div/div/a").text
    share_stats["ticket"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[2]/div").text
    share_stats["pe"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[7]/div").text
    return share_stats
"""
    share_stats["ps"]=from_shares(14)
    share_stats["pb"]=from_shares(15)
    share_stats["env"]=from_shares(16)
    share_stats["net_worth"]=remove_trash(from_shares(6))
    share_stats["roe"]=remove_trash(from_shares(17))
    share_stats["debt_eq"]=from_shares(18)
"""
def post_to_django(data, django_url):
    stock_dict = ast.literal_eval(data)
    stock_post = requests.post(django_url, stock_dict)
    print(stock_post.status_code)
    print(stock_post.text)

if __name__ == "__main__":
    display.start()
    driver.get(url)
    while(True):
        try:
            switch_page(stock_count)
            #stock = Share(url)
            #stock_str = stock.share_body()
            stock = share(stock_count)
            post_to_django(stock, django_url)
        except Exception as e:
            print(e)




"""

def from_shares(tdnum):
    l=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td["+str(tdnum)+"]").text
    return(l)

def remove_trash(string):
    string=str(string)
    string=string.replace(",", ".").replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "")
    return string
class Share(object):

    def __init__(self, url):
        self.url = url


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
"""
"""
        try:
            i+=1

            stock_ao = ast.literal_eval(stock.share_body())
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
"""
