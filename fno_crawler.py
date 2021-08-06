from bs4.builder import HTML
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import time
from house import House

class FiveNineOneCrawler:
    SALE_URL = 'https://sale.591.com.tw'

    def __init__(self):
        self.user_agent = generate_user_agent()
        self.session = requests.session()
        self.csrf_token = None

    def get_houses(self, search_arg):
        if self.csrf_token == None:
            self.csrf_token = self.__get_csrf_tag()

        search_url = 'https://sale.591.com.tw/home/search/list?' + search_arg
        req_url = search_url
        house_list = []
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
            for h in resp_json['data']['house_list']:
                if 'is_newhouse' not in h:
                    house_list.append(h)
            
            total = int(resp_json['data']['total'])
            exists_next = (len(house_list) != total)

            if exists_next:
                page = resp_json['data']['page']
                soup = BeautifulSoup(page, "html.parser")
                a_tags = soup.find('a', attrs={ 'class': 'pageNext' })
                data_first = a_tags['data-first']
                req_url = search_url + f"&firstRow={data_first}&totalRows={total}"
        
        return self.__to_houses(house_list)

    def __get_csrf_tag(self):
        sale_html = self.session.get(FiveNineOneCrawler.SALE_URL, headers={
            "User-Agent": self.user_agent
        });
        soup = BeautifulSoup(sale_html.text, "html.parser")
        csrf_tag = soup.find('meta', { 'name': 'csrf-token' })
        return csrf_tag['content']

    def __to_houses(self, data_list):
        houses = []
        type_dict = {
            "2": "中古屋"
        }
        carport_dict = {
            1: "有",
            0: "無"
        }
        for d in data_list:
            h = House()
            h.id = '591_' + str(d['houseid'])
            h.type = type_dict[d['type']] if d['type'] in type_dict else d['type']
            h.kind = d['kind_name']
            h.shape = d['shape_name']
            h.region = d['region_name']
            h.section = d['section_name']
            h.title = d['title']
            h.carport = carport_dict[d['has_carport']] if d['has_carport'] in carport_dict else d['has_carport']
            h.room = d['room']
            h.floor = d['floor']
            h.area = d['area']
            h.house_age = d['houseage']
            h.unit_price = d['unitprice']
            h.price = d['price']
            h.link = f"https://sale.591.com.tw/home/house/detail/{d['type']}/{d['houseid']}.html"
            h.data_from = "591"
            houses.append(h)
        return houses
    
    def is_active(self, link):
        response_html = self.session.get(link, headers={
            "User-Agent": self.user_agent
        });
        return "您查詢的物件找不到了" not in response_html.text
    