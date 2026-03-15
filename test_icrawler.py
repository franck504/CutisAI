from icrawler.builtin import BingImageCrawler
import os

if __name__ == "__main__":
    crawler = BingImageCrawler(storage={"root_dir": "./test_bing"}, downloader_threads=2)
    crawler.crawl(keyword="Buruli ulcer lesion", max_num=10)
    print("Files:", os.listdir("./test_bing"))
