from house_db_model import HouseDbWriter
from fno_crawler import FiveNineOneCrawler
import sentry_sdk
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    sentry_sdk.init(
        "https://4834efea1ee74da5ab0602b7454dd30b@o796183.ingest.sentry.io/5802006",
        traces_sample_rate=1.0
    )

    crawler = FiveNineOneCrawler()
    fno_url = os.getenv('FNO_SEARCH_URL')
    houses = crawler.get_houses(fno_url)

    HouseDbWriter.insert(houses)
    