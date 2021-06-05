from house_db_model import HouseDbWriter
from fno_crawler import FiveNineOneCrawler
import sentry_sdk

if __name__ == '__main__':
    sentry_sdk.init(
        "https://4834efea1ee74da5ab0602b7454dd30b@o796183.ingest.sentry.io/5802006",
        traces_sample_rate=1.0
    )

    crawler = FiveNineOneCrawler()
    fno_url = f"https://sale.591.com.tw/home/search/list?type=2&shType=list&regionid=8&kind=9&shape=2&pattern=3&houseage=1$_10$&order=unitprice_asc&area=0&section=104&price=$_1300$&label=7"
    houses = crawler.get_houses(fno_url)

    HouseDbWriter.insert(houses)
    