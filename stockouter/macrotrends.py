from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import requests
import ast
from bs4 import BeautifulSoup
import re
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


#selenium, and display settings


def switch_page(i,driver):
    """switch to next page"""
    stock_count=i
    if i%20==0:
        driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[10]/div/div[4]/div").click()
        sleep(1)
        stock_count=1
    else:
        stock_count+=1

def share(stock_count,driver):
    """take some shares"""
    share_stats = {}
    share_stats["name"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[1]/div/div/a").text
    ticket = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[2]/div").text
    share_stats["ticket"]=ticket
    share_stats["pe"]=driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[4]/div[2]/div/div["+str(stock_count)+"]/div[7]/div").text
    share_stats["ps"]=get_ratio(ticket, "&type=price-sales&statement=price-ratios&freq=Q")
    share_stats["pb"]=get_ratio(ticket, "&type=price-book&statement=price-ratios&freq=Q")
    share_stats["env"]=get_ratio(ticket, "&type=price-fcf&statement=price-ratios&freq=Q")
    share_stats["net_worth"]=get_net_worth(ticket)
    share_stats["roe"]=get_roe(ticket, "&type=roe&statement=ratios&freq=Q")
    share_stats["debt_eq"]=get_roe(ticket, "&type=debt-equity-ratio&statement=ratios&freq=Q")
    return share_stats


def get_ratio(ticket, req_fragment):
    """for ps, pb or env"""
    ratio_url= "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t="+ticket+req_fragment
    response = requests.get(ratio_url, headers=headers)
    soup = BeautifulSoup(response.text)
    string_soup = str(soup)
    find_var = re.search("var chartData.*}]", string_soup)
    save_var = str(find_var[0])[::-1]
    cut_last_vals = save_var.split(':"1v')[0]
    last_vals = cut_last_vals[::-1].replace('"v3":', '').replace("}]", "")
    split_vals = last_vals.split(",")
    return(split_vals[1])

def get_net_worth(ticket):
    """return net worth in B"""
    pb_ratio= "https://www.macrotrends.net/assets/php/market_cap.php?t="+ticket
    pb_response = requests.get(pb_ratio, headers=headers)
    pb_soup = BeautifulSoup(pb_response.text)
    string_soup = str(pb_soup)
    find_var = re.search("var chartData.*}]", string_soup)
    save_var = str(find_var[0])[::-1]
    cut_last_val = save_var.split(':"1v')[0]
    last_val = cut_last_val[::-1].replace('}]', '')
    return(last_val)

def get_roe(ticket, req_fragment):
    pb_ratio= "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t="+ticket+req_fragment
    pb_response = requests.get(pb_ratio, headers=headers)
    pb_soup = BeautifulSoup(pb_response.text)
    string_soup = str(pb_soup)
    find_var = re.search("var chartData.*}]", string_soup)
    save_var = str(find_var[0])[::-1]
    cut_last_vals = save_var.split(':"1v')[0]
    last_vals = cut_last_vals[::-1].replace('"v2":', '').replace('"v3":', '').replace('}]', '')
    split_vals = last_vals.split(",")
    return(split_vals[2])


def pages_get_info(shares,driver):
    stock_count=1
    while(True):
        switch_page(stock_count,driver)
        shares.clear()
        try:
            shares.append(share(stock_count,driver))
        except Exception as e:
            print(e)
    return shares

def initiate_display():
    url = "https://www.macrotrends.net/stocks/stock-screener" #parser's target
     #on curr page, takes 1-20 values
    shares = [] # list of dictionaries that flashing on each iteration
    ticket = str
    display = Display(visible=0, size=(800, 600))
    options = webdriver.FirefoxOptions()
    service = Service(executable_path = "/usr/local/bin/geckodriver")
    service_log_path = "/dev/null"
    options.add_argument('--headless') #turn off display for docker
    driver = webdriver.Firefox(options=options, service=service, service_log_path=service_log_path)
    display.start()
    driver.get(url)
    pages_get_info(shares,driver)
    driver.close()
    display.stop()
    return shares
