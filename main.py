import logging
import os, sentry_sdk, seqlog
from time import sleep
from house_db_model import HouseDbWriter
from fno_crawler import FiveNineOneCrawler
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    sentry_sdk.init(
        "https://4834efea1ee74da5ab0602b7454dd30b@o796183.ingest.sentry.io/5802006",
        traces_sample_rate=1.0
    )
    seqlog.log_to_seq(
        server_url="http://192.168.80.200:5341/", 
        level=logging.NOTSET,
        batch_size=1,
        auto_flush_timeout=1,  # seconds
        override_root_logger=True
    )

    crawler = FiveNineOneCrawler()
    fno_url = os.getenv('FNO_SEARCH_URL')
    houses = crawler.get_houses(fno_url)

    HouseDbWriter.insert(houses)
    logging.info("house-crawlers run finish. house_count:{cnt}", cnt=len(houses))
    sleep(2)