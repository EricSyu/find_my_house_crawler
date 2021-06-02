from datetime import datetime
from peewee import *

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


mysql_db = MySQLDatabase('house', user='root', password='root',
                        host='127.0.0.1', port=3306)

class HouseDbModel(Model):
    id = CharField(primary_key = True)
    type = CharField()
    kind = CharField()
    shape = CharField()
    region = CharField()
    section = CharField()
    title = CharField()
    carport = CharField()
    room = CharField()
    floor = CharField()
    area = FloatField()
    house_age = IntegerField()
    unit_price = FloatField()
    price = IntegerField()
    link = CharField()
    other = CharField()
    data_from = CharField()
    record_time = DateTimeField(default = datetime.now)
    rank = IntegerField()
    comment = CharField()
    discard = BooleanField()

    class Meta:
        database = mysql_db
        table_name = "house_sale_table"
