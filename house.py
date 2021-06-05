from datetime import datetime

class House:
    def __init__(self):
        self.id = ''
        self.type = ''
        self.kind = ''
        self.shape = ''
        self.region = ''
        self.section = ''
        self.title = ''
        self.carport = ''
        self.room = ''
        self.floor = ''
        self.area = 0
        self.house_age = 0
        self.unit_price = 0
        self.price = 0
        self.link = ''
        self.other = ''
        self.data_from = ''
        self.record_time = datetime.now()
        self.rank = 99
        self.comment = ''
        self.discard = False