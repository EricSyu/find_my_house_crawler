import requests
from user_agent import generate_user_agent
from house import House
import json

class SinYiCrawler:
    SALE_URL = 'https://www.sinyi.com.tw/'

    def __init__(self):
        self.user_agent = generate_user_agent()
        self.session = requests.session()
        self.sid = '20210516215347082'
        self.sat = '730282'

    def get_houses(self, search_arg):
        postData = search_arg
        req_url = 'https://sinyiwebapi.sinyi.com.tw/searchObject.php'
        house_list = []
        total = 0
        exists_next = True
        while exists_next == True:
            response = self.session.post(req_url, headers={
                "sid": self.sid,
                "sat": self.sat,
                "code": "0",
                "User-Agent": self.user_agent
            }, data=postData)
            resp_json = response.json()

            for h in resp_json['content']['object']:
                house_list.append(h)

            total = resp_json['content']['totalCnt']
            exists_next = (len(house_list) != total)
            if exists_next:
                current_page = resp_json['content']['page']
                next_page = current_page + 1
                postDataObj = json.loads(postData)
                postDataObj['page'] = next_page
                postData = json.dumps(postDataObj)
        return self.__to_houses(house_list)

    def __to_houses(self, data_list):
        houses = []
        shape_dict = {
            'L': '大樓'
        }
        for d in data_list:
            h = House()
            h.id = 'SinYi_' + str(d['houseNo'])
            h.type = '預售屋' if d['age'] == '預售' else '中古屋'
            h.kind = '住宅'
            h.shape = "|".join([(shape_dict[t] if t in shape_dict else '') for t in d['houselandtype']])
            h.region = d['address'][0:3]
            h.section = d['address'][3:6]
            h.title = d['name']
            h.carport = '有' if d['isParking'] else '無'
            h.room = d['layout']
            h.floor = d['floor'] + 'F/' + d['totalfloor'] + 'F'
            h.area = d['pingUsed']
            h.house_age = float(d['age'][:-1]) if d['age'] != '預售' else 0
            h.unit_price = round(d['totalPrice']/d['pingUsed'], 2)
            h.price = d['totalPrice']
            h.link = d['shareURL']
            h.data_from = "信義房屋"
            houses.append(h)
        return houses

    def is_active(self, link):
        response_html = self.session.get(link, headers={
            "User-Agent": self.user_agent
        })
        return "抱歉！找不到這一頁" not in response_html.text
    