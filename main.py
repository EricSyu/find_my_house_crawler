import logging
import os, sentry_sdk, seqlog
from time import sleep
from house_db_model import DbHelper
from fno_crawler import FiveNineOneCrawler
from sinyi_crawler import SinYiCrawler
from dotenv import load_dotenv
from sentry_sdk import capture_exception
from datetime import datetime

def parse(search_str:str):
    search_composes = search_str.split(';')
    return [(c.split('|')[0], c.split('|')[1]) for c in search_composes]

def create_crawler(crawler_type:str):
    if crawler_type == '591':
        return FiveNineOneCrawler()
    elif crawler_type.upper() == 'SINYI':
        return SinYiCrawler()

    raise Exception('Could not support type:' + crawler_type)

def crawl_houses_into_db():
    search_str = os.getenv('SEARCH_HOUSE_STR')
    search_tuples = parse(search_str)
    houses = []
    for s in search_tuples:
        crawler = create_crawler(s[0])
        h = crawler.get_houses(s[1])
        houses.extend(h)
    
    dbhelper = DbHelper()
    dbhelper.create_house_table()
    dbhelper.insert(houses)
    logging.info("house-crawlers run finish. house_count:{cnt}", cnt=len(houses))

def close_house_if_not_exists():
    dbhelper = DbHelper()
    link_dict = dbhelper.get_active_link_dict()
    for id, link in link_dict.items():
        crawler_type = id.split('_')[0]
        crawler = create_crawler(crawler_type)
        if not crawler.is_active(link):
            dbhelper.close_house(id)
            logging.info("close house_id:{i}", i=id)

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
        start_time = datetime.now()
        mode = os.getenv('MODE')
        if mode == '1':
            crawl_houses_into_db()
        elif mode == '2':
            close_house_if_not_exists()
        else: 
            raise Exception("not support mode:" + mode)
        end_time = datetime.now()

        time_format = '%Y/%m/%d %H:%M:%S'
        run_time = round((end_time - start_time).total_seconds(), 0)
        logging.info("start_time:{st}, end_time:{et}, run_time:{rt}sec", st = start_time.strftime(time_format), et = end_time.strftime(time_format), rt = run_time)
        sleep(2)
    except Exception as ex:
        capture_exception(ex)
    
if __name__ == '__main__':
    main()
        