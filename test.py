from selenium import webdriver


class Share(object):

    def __init__(self, url):
        self.url = url
    """Take some Share's stats"""

    def share_body(self):
        report = driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[18]").text
        if int(report[:report.rfind('-')]) <= 2019:
            print("Too old")
            return
        else:
            ticket_href = driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[2]/a").get_attribute("href")
            ticket = ticket_href[ticket_href.rfind('/')+1:]
            if len(ticket) > 10:
                print("Too scam")
                return
            else:
                share_stats = {}
                share_stats["name"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[2]/a").text
                share_stats["ticket"]=ticket
                share_stats["pe"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[12]").text
                share_stats["ps"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[13]").text
                share_stats["pb"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[14]").text
                share_stats["env"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[15]").text
                share_stats["net_worth"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[5]").text.replace(" ", "")
                share_stats["roe"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[16]").text.replace("%", "")
                share_stats["debt_eq"]=driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[17]").text
                share_stats=self.ao(ticket, share_stats)
                return share_stats

    def ao(self, ticket, share_stats):
        driver.execute_script("window.open('https://smart-lab.ru/forum/GAZP', '_blank')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://smart-lab.ru/forum/"+ticket)
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]").click()
        try:
            share_stats["price"]=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[2]/span/i").text.replace("₽", "")
        except Exception as e:
            print(e)
            print("Missing ao price")
            return
        try:
            share_stats["ebitda"]=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div/table[2]/tbody/tr[3]/td[2]").text #.replace(" млрд", "")
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
            share_stats["ticket"]=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[2]/div/table[1]/tbody/tr[6]/td[2]/ul/li").text
        except Exception as e:
            print(e)
        try:
            share_stats["price"]=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[2]/span[2]/i").text.replace("₽", "")
        except Exception as e:
            print(e)
            share_stats["price"]=share_stats["price"]+"p"
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return share_stats

def remove_trash(string):
    """Remove % ₽ млрд spases and replace , to ."""
    string=str(string)
    string=string.replace(",", ".").replace(" ", "").replace("%", "").replace("₽", "").replace("млрд", "")
    return string

shares = []
driver = webdriver.Firefox(executable_path = './geckodriver')
url = "https://smart-lab.ru/q/shares_fundamental/"
driver.get(url)
gas = driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr[2]/td[10]").text
i = 1

while(i<400):
    i+=1
    if __name__ == "__main__":
        stock = Share("https://smart-lab.ru/q/shares_fundamental/")
        if driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[10]").text == gas:
            print(stock.share_body())
#        elif driver.find_element_by_xpath("/html/body/div[1]/div/div[6]/div/div/table[1]/tbody/tr["+str(i)+"]/td[9]").text == "0.0%":
    #        continue
        else:
            stock_ao = stock.share_body()
            print(stock_ao)
            ticket_for_url = stock_ao["ticket"]
            stock_ap = stock.ap(stock_ao)
            print(stock_ap)
