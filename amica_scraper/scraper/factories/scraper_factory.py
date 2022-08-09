from scraper.forum_scraper.wxc_scraper import WxcScraper
from scraper.forum_scraper.mit_scraper import MitScraper
from scraper.forum_scraper.hr_scraper import HrScraper
from scraper.news_scraper.wxc_news_scraper import WxcNewsScraper
from scraper.user_scraper.mit_user_scraper import MitUserScraper


class ScraperFactory():

    @staticmethod
    def create_forum_scraper(target):
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
        if target["web_name"] == 'WXC':
            scraper = WxcNewsScraper()
        else:
            scraper = None
            print("This website does not support NEWS-based scraping.")

        return scraper.init(target)

    @staticmethod
    def create_user_scraper(target):
        if target["web_name"] == 'MIT':
            scraper = MitUserScraper()
        else:
            scraper = None
            print("This website does not support USER-based scraping.")

        return scraper.init(target)