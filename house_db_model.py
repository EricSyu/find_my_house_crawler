from datetime import datetime
from peewee import *
from sentry_sdk import capture_exception
from dotenv import load_dotenv
import os

load_dotenv()
mysql_db = MySQLDatabase(os.getenv('MYSQL_DB_NAME'), user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PWD'),
                        host=os.getenv('MYSQL_HOST'), port=int(os.getenv('MYSQL_PORT')), autoconnect=False)

house_table_name = os.getenv('HOUSE_TABLE_NAME')

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
    other = CharField(null=True)
    data_from = CharField()
    record_time = DateTimeField(default = datetime.now)
    rank = IntegerField()
    comment = CharField(null=True)
    discard = BooleanField()

    class Meta:
        database = mysql_db
        table_name = house_table_name

class HouseDbWriter:

    @staticmethod
    def insert(houses):
        mysql_db.connect()
        if not mysql_db.table_exists(house_table_name):
            mysql_db.create_tables([HouseDbModel])
        
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
                        carport = h.carport,
                        room = h.room,
                        floor = h.floor,
                        area = h.area,
                        house_age = h.house_age,
                        unit_price = h.unit_price,
                        price = h.price,
                        link = h.link,
                        other = h.other,
                        rank = h.rank,
                        data_from = h.data_from,
                        record_time = h.record_time,
                        comment = h.comment
                    )
            except Exception as ex:
                capture_exception(ex)

        mysql_db.close()