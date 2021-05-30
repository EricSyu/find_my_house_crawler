from fno_crawler import FiveNineOneCrawler
from peewee import *

if __name__ == '__main__':
    url = f"https://sale.591.com.tw/home/search/list?type=2&shType=list&regionid=8&price=$_1400$&shape=2&houseage=1$_10$&section=104&pattern=3"
    
    crawler = FiveNineOneCrawler()
    houses = crawler.get_houses(url)
    print(len(houses))
