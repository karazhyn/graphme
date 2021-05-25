import logging
import links_crawler.config 
from links_crawler.crawler import Crawler
import argparse


def main_crawler(initial_link, initial_thread=2, initial_depth=1):
    logging.basicConfig(
        format=links_crawler.config.LOGGING_FORMAT,
        level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--initial_url', default=initial_link, help="The url from which the crawler will begin")
    parser.add_argument('-c', '--thread_count', default=initial_thread, type=int,
                        help="The amount of concurrent threads the crawler will run")
    parser.add_argument('-d', '--crawling_depth', default=initial_depth, type=int,
                        help="how deep the crawler will recursively look for links")
    args = parser.parse_args()
    crawler = Crawler(args.initial_url, args.thread_count, args.crawling_depth)
    links_depth_report, broken_links = crawler.run()
    for link, depth in links_depth_report.items():
        print(f"url: {link}, depth: {depth}")

    print("\n Broken links:\n")
    for link in broken_links:
        print(link)
    print('ALL DICT:')
    print(crawler.all_links)
    print('\n\nALL EXTERNAL DICTS: ')
    print(crawler.external_links)


    return crawler.all_links, crawler.external_links

#debug block
# if __name__ == '__main__':
#     main_crawler('https://support.unity3d.com/hc/en-us', 20)
