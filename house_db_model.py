from datetime import datetime
from house import House
from peewee import *
from sentry_sdk import capture_exception
from dotenv import load_dotenv
import os

class HouseDbModel(Model):
    id = CharField(primary_key = True)
    type = CharField()
    kind = CharField()
    shape = CharField()
    region = CharField()
    section = CharField()
    title = CharField()
    status = CharField()
    carport = CharField()
    room = CharField()
    floor = CharField()
    area = FloatField()
    house_age = IntegerField()
    unit_price = FloatField()
    price = IntegerField()
    link = CharField()
    data_from = CharField()
    record_time = DateTimeField(default = datetime.now)
    favorite_ranking = IntegerField()
    comment = CharField(null=True)

    class Meta:
        database = None
        table_name = None

class DbHelper:

    def __init__(self):
        load_dotenv()
        self.db = MySQLDatabase(os.getenv('MYSQL_DB_NAME'), user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PWD'),
                                host=os.getenv('MYSQL_HOST'), port=int(os.getenv('MYSQL_PORT')), autoconnect=True, charset='utf8mb4')
        self.house_table_name = os.getenv('HOUSE_TABLE_NAME')
        HouseDbModel._meta.database = self.db
        HouseDbModel._meta.table_name = self.house_table_name

    def create_house_table(self):
        if not self.db.table_exists(self.house_table_name):
            self.db.create_tables([HouseDbModel])

    def insert(self, houses):
        for h in houses:
            try:
                query = HouseDbModel.select().where(HouseDbModel.id == h.id)
                if not query.exists():
                    HouseDbModel.create(
                        id = h.id,
                        type = h.type,
                        kind = h.kind,
                        shape = h.shape,
                        region = h.region,
                        section = h.section,
                        title = h.title,
                        status = h.status,
                        carport = h.carport,
                        room = h.room,
                        floor = h.floor,
                        area = h.area,
                        house_age = h.house_age,
                        unit_price = h.unit_price,
                        price = h.price,
                        link = h.link,
                        favorite_ranking = h.favorite_ranking,
                        data_from = h.data_from,
                        record_time = h.record_time,
                        comment = h.comment
                    )
            except Exception as ex:
                capture_exception(ex)

    def get_active_house_link_pairs(self):
        query = HouseDbModel.select().where(HouseDbModel.status == "Active")
        houseLinkPairs = [{'id': h.id, 'link': h.link} for h in query]
        return houseLinkPairs

    def close_house(self, id):
        query = HouseDbModel.update(status = "Close").where(HouseDbModel.id == id)
        query.execute()

    def __del__(self):
        self.db.close()