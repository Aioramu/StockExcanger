import requests
import re
from urllib.request import urlopen,Request
from urllib.request import urlretrieve
from urllib.parse import quote
from bs4 import BeautifulSoup


url= "https://www.macrotrends.net/assets/php/fundamental_iframe.php?t=AAPL&type=price-sales&statement=price-ratios&freq=Q"


response = requests.get(url)
soup = BeautifulSoup(response.text)
string_soup = str(soup)
data = re.search("var chartData.*}]", string_soup)



print(data[0])

