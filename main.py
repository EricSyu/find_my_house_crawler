import logging
import os, sentry_sdk, seqlog
from time import sleep
from house_db_model import DbHelper
from fno_crawler import FiveNineOneCrawler
from sinyi_crawler import SinYiCrawler
from dotenv import load_dotenv
from sentry_sdk import capture_exception

def parse(search_str:str):
    search_composes = search_str.split(';')
    return [(c.split('|')[0], c.split('|')[1]) for c in search_composes]

def create_crawler(crawler_type:str):
    if crawler_type == '591':
        return FiveNineOneCrawler()
    elif crawler_type == 'sinyi':
        return SinYiCrawler()

    raise Exception('Could not support type:' + crawler_type)

def main():
    load_dotenv()
    sentry_sdk.init(
        os.getenv('SENTRY_URL'),
        traces_sample_rate=1.0
    )
    seqlog.log_to_seq(
        server_url=os.getenv('SEQ_SERVER_URL'), 
        level=logging.NOTSET,
        batch_size=1,
        auto_flush_timeout=1,
        override_root_logger=True
    )

    try:
        # get houses 
        search_str = os.getenv('SEARCH_HOUSE_STR')
        search_tuples = parse(search_str)
        houses = []
        for s in search_tuples:
            crawler = create_crawler(s[0])
            h = crawler.get_houses(s[1])
            houses.extend(h)

        # insert db 
        dbhelper = DbHelper()
        dbhelper.create_house_table()
        dbhelper.insert(houses)

        # close house if it is sunset 
        # houseLinks = dbhelper.get_active_house_link_pairs()
        # for h in houseLinks:
        #     if not crawler.is_active(h['link']):
        #         dbhelper.close_house(h['id'])
        #         logging.info("close house_id:{id}", id=h['id'])

        logging.info("house-crawlers run finish. house_count:{cnt}", cnt=len(houses))
        sleep(2)
    except Exception as ex:
        capture_exception(ex)
    
if __name__ == '__main__':
    main()
        