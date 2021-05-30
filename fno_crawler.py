import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import time

class FiveNineOneCrawler:
    SALE_URL = 'https://sale.591.com.tw'

    def __init__(self):
        self.user_agent = generate_user_agent()
        self.session = requests.session()
        self.csrf_token = None;

    def get_houses(self, search_url):
        if self.csrf_token == None:
            self.csrf_token = self.__get_csrf_tag()

        req_url = search_url
        houses = []
        total = 0
        exists_next = True
        while exists_next == True:
            timestamp = int(round(time.time() * 1000))
            req_url = req_url + f"&timestamp={timestamp}"
            response = self.session.get(req_url, headers={
                'X-CSRF-TOKEN': self.csrf_token,
                "User-Agent": self.user_agent
            })
            resp_json = response.json()
            houses.extend(resp_json['data']['house_list'])
            
            total = resp_json['data']['total']
            exists_next = len(houses) != total

            if exists_next:
                page = resp_json['data']['page']
                soup = BeautifulSoup(page, "html.parser")
                a_tags = soup.find('a', attrs={ 'class': 'pageNext' })
                data_first = a_tags['data-first']
                req_url = search_url + f"&firstRow={data_first}&totalRows={total}"
        
        return houses

    def __get_csrf_tag(self):
        sale_html = self.session.get(FiveNineOneCrawler.SALE_URL, headers={
            "User-Agent": self.user_agent
        });
        soup = BeautifulSoup(sale_html.text, "html.parser")
        csrf_tag = soup.find('meta', { 'name': 'csrf-token' })
        return csrf_tag['content']