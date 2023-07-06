import requests
#import fileinput
from urllib.request import urlopen,Request
from urllib.request import urlretrieve
from urllib.parse import quote
from bs4 import BeautifulSoup
#from bs4 import BeautifulSoup
#from lxml.html.soupparser import fromstring


#url= "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=T&type=price-sales&statement=price-ratios&freq=Q"
url= "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=AAPL&type=price-sales&statement=price-ratios&freq=Q"

#table= Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = requests.get(url)
soup = BeautifulSoup(response.text)
#table = urlopen(table).read()
data = soup.body.find("var")





print(soup)


"""
def geturl():
    table= Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    table = urlopen(table).read()
    bs= BeautifulSoup(table, features = "lxml")
    table=bs.findAll("a")
    for i in table:
        if i.get_text() =='Следующая глава':
            refs=i["href"]
            a='https://tl.rulate.ru'+str(refs)
    return a


for charapter in range(1, 20000):
    response = requests.get(url)
    #add err response.status_code 404
    our_content = response.content
    our_file = open('{0}.txt'.format(book_name), 'a+')
    if charapter == 1:
        our_file.write('{0}\n'.format(book_name)+'\n')
    our_soup = BeautifulSoup(our_content, 'lxml')
    for tag in our_soup.find_all('p'):
            our_file.write(tag.text + '\n')
    print(url +  ' %d download' % (charapter))
    trash_list()
    try:
        url = geturl()
    except UnboundLocalError:
        break

"""
