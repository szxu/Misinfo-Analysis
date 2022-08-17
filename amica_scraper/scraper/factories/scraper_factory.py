from scraper.util.io import Input

from scraper.forum_scraper.wxc_scraper import WxcScraper
from scraper.forum_scraper.mit_scraper import MitScraper
from scraper.forum_scraper.hr_scraper import HrScraper

from scraper.news_scraper.wxc_news_scraper import WxcNewsScraper
from scraper.news_scraper.pyb_news_scraper import PybNewsScraper

from scraper.user_scraper.mit_user_scraper import MitUserScraper

from scraper.fact_scraper.pyb_fact_scraper import PybFactScraper



class ScraperFactory():

    @staticmethod
    def create_forum_scraper(target):
        target["web_name"] = input("Please enter web name from (WXC, HR, MIT): ").upper()
        target = Input.get_date(target)
        if target["web_name"] == 'WXC':
            scraper = WxcScraper()
        elif target["web_name"] == 'MIT':
            scraper = MitScraper()
        elif target["web_name"] == 'HR':
            scraper = HrScraper()
        else:
            scraper = None
            print("This website does not support FORUM-based scraping.")
        return scraper.init(target)

    @staticmethod
    def create_news_scraper(target):
        target["web_name"] = input("Please enter web name from (WXC or PYB): ").upper()
        if target["web_name"] == 'WXC':
            target = Input.get_date(target)
            scraper = WxcNewsScraper()
        elif target["web_name"] == 'PYB':
            scraper = PybNewsScraper()
        else:
            scraper = None
            print("This website does not support NEWS-based scraping.")

        return scraper.init(target)

    @staticmethod
    def create_user_scraper(target):
        target["web_name"] = input("Please enter web name from (MIT): ").upper()
        if target["web_name"] == 'MIT':
            scraper = MitUserScraper()
        else:
            scraper = None
            print("This website does not support USER-based scraping.")

        return scraper.init(target)

    @staticmethod
    def create_fact_scraper(target):
        target["web_name"] = input("Please enter web name from (PYB): ").upper()
        if target["web_name"] == 'PYB':
            scraper = PybFactScraper()
        else:
            scraper = None
            print("This website does not support Fact-based scraping.")

        return scraper.init(target)