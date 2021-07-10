import logging
import os, sentry_sdk, seqlog
from time import sleep
from house_db_model import DbHelper
from fno_crawler import FiveNineOneCrawler
from dotenv import load_dotenv
from sentry_sdk import capture_exception

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

    try:
        crawler = FiveNineOneCrawler()
        dbhelper = DbHelper()

        # get houses 
        fno_url = os.getenv('FNO_SEARCH_URL')
        houses = crawler.get_houses(fno_url)

        # insert db 
        dbhelper.create_house_table()
        dbhelper.insert(houses)

        # close house if it is sunset 
        houseLinks = dbhelper.get_active_house_link_pairs()
        for h in houseLinks:
            if not crawler.is_active(h['link']):
                dbhelper.close_house(h['id'])
                logging.info("close house_id:{id}", id=h['id'])

        logging.info("house-crawlers run finish. house_count:{cnt}", cnt=len(houses))
        sleep(2)
    except Exception as ex:
        capture_exception(ex)
    