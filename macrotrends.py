from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import requests
import ast


#global variables
django_url = "http://web:8000"
url = "https://www.macrotrends.net/stocks/stock-screener" #parser's target
stock_count=1 #on curr page, takes 1-20 values
shares = [] # list of dictionaries that flashing on each iteration

#selenium and display settings
display = Display(visible=0, size=(800, 600))
options = webdriver.FirefoxOptions()
service = Service(executable_path = "/usr/local/bin/geckodriver")
service_log_path = "/dev/null"
#options.add_argument('--headless') #turn off display for docker
driver = webdriver.Firefox(options=options, service=service, service_log_path=service_log_path)


def switch_page(i):
    """switch to next page"""
    global stock_count
    if i%20==0:
        driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[10]/div/div[4]/div").click()
        sleep(1)
        stock_count=1
    else:
        stock_count+=1

def share(stock_count):
    """take some shares from main page"""
    share_stats = {}
    share_stats["name"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[1]/div/div/a").text
    share_stats["ticket"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[2]/div").text
    share_stats["pe"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[7]/div").text
    return share_stats
"""
    share_stats["ps"]
    share_stats["pb"]
    share_stats["env"]
    share_stats["net_worth"]
    share_stats["roe"]
    share_stats["debt_eq"]
"""
def post_to_django(data, django_url):
    #stock_dict = ast.literal_eval(data)
    stock_post = requests.post(django_url, json=data)
    print(stock_post.status_code)
    print(stock_post.text)


if __name__ == "__main__":
    display.start()
    driver.get(url)
    while(True):
        try:
            switch_page(stock_count)
            shares.clear()
            shares.append(share(stock_count))
            print(shares) #print for test
            #post_to_django(stock, django_url)
            
        except Exception as e:
            print(e)
