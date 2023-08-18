import re
import requests
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def initiate_display():
    #selenium, and display settings
    display = Display(visible=0, size=(800, 600))
    options = webdriver.FirefoxOptions()
    service = Service(executable_path = "/usr/local/bin/geckodriver")
    service_log_path = "/dev/null"
    options.add_argument('--headless') #turn off display for docker
    driver = webdriver.Firefox(options=options, service=service, service_log_path=service_log_path)
    url = "https://www.macrotrends.net/stocks/stock-screener" #parser's target
    display.start()
    driver.get(url)
    switch_page(driver)
    driver.close()
    display.stop()
        
def switch_page(driver):
    """switch to next page"""
    stock_count=int(1)
    shares = []
    for stock_count in range(1, 22):
        if stock_count%21!=0:
            view_page(shares, stock_count, driver)
            stock_count=stock_count+1
        else:
            driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[10]/div/div[4]/div").click()
            stock_count=1
            send_list(shares)
            shares.clear() 
            
def view_page(shares, stock_count, driver):
    try:
        shares.append(share(stock_count, driver))
    except Exception as e:
        print(e)
    #print(shares[-1]) #print for test

def send_list(shares):
    print(shares)     #print for test
    return shares
    
def share(stock_count, driver):
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
    last_vals = get_graph_var(ratio_url)[::-1].replace('"v3":', '').replace("}]", "")
    split_vals = last_vals.split(",")
    return(split_vals[1])
 
def get_net_worth(ticket):
    """return net worth in B"""
    ratio_url= "https://www.macrotrends.net/assets/php/market_cap.php?t="+ticket
    last_vals = get_graph_var(ratio_url)[::-1].replace('}]', '')
    return(last_vals)
 
def get_roe(ticket, req_fragment):
    ratio_url= "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t="+ticket+req_fragment
    last_vals = get_graph_var(ratio_url)[::-1].replace('"v2":', '').replace('"v3":', '').replace('}]', '')
    split_vals = last_vals.split(",")
    return(split_vals[2])

def get_graph_var(ratio_url):
    response = requests.get(ratio_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    soup = BeautifulSoup(response.text)
    string_soup = str(soup)
    find_var = re.search("var chartData.*}]", string_soup)
    try:
        save_var = str(find_var[0])[::-1]
    except TypeError:
        pass
    cut_last_vals = save_var.split(':"1v')[0]
    return cut_last_vals