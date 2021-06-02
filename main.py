from house import *
from fno_crawler import FiveNineOneCrawler

if __name__ == '__main__':
    crawler = FiveNineOneCrawler()
    fno_url = f"https://sale.591.com.tw/home/search/list?type=2&shType=list&regionid=8&price=$_1400$&shape=2&houseage=1$_10$&section=104&pattern=3"
    houses = crawler.get_houses(fno_url)

    mysql_db.connect()
    if not mysql_db.table_exists('house_sale_table'):
        mysql_db.create_tables([HouseDbModel])
    
    for h in houses:
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

    mysql_db.close()
