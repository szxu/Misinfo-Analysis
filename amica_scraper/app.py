# selenium 4
import os
import pandas as pd
import json
import chromedriver_autoinstaller as chromedriver

from util.df_handler import DfHandler
from scraper.factories.scraper_factory import ScraperFactory

from datetime import date, datetime

class App():
    @staticmethod
    def scrap_news(target):
        df, cdf = ScraperFactory.create_news_scraper(target)
        df = DfHandler.update_link(df)
        cdf = DfHandler.update_link(cdf)

        filename = target["web_name"] + "_" + target["cat_name"] + "_" + str(target["start_date"]) + "_" + str(target["end_date"])
        news_path = BASE_PATH + '/files/news/' + target["web_name"] + '/'

        if target["file_type"] == "csv":
            path = news_path + filename + '.csv'
            df.to_csv(path, index=False)
            c_path = news_path + filename + '_comments' + '.csv'
            cdf.to_csv(c_path, index=False)
        elif target["file_type"] == "json":
            path = news_path + filename + '.json'
            df.to_json(path, orient='records')
            c_path = news_path + filename + '_comments' + '.json'
            cdf.to_json(c_path, orient='records')
        else:
            print("error")

    @staticmethod
    def scrap_forum(target):
        df = ScraperFactory.create_forum_scraper(target)
        df = DfHandler.update(df)

        filename = target["web_name"] + "_" + target["cat_name"] + "_" + str(target["start_date"]) + "_" + str(target["end_date"])
        forum_path = BASE_PATH + '/files/forum/' + target["web_name"] + '/'

        if target["file_type"] == "csv":
            path = forum_path + filename + '.csv'
            df.to_csv(path, index=False)
        elif target["file_type"] == "json":
            path = forum_path + filename + '.json'
            df.to_json(path, orient='records')

    @staticmethod
    def scrap_user(target):
        df = ScraperFactory.create_user_scraper(target)
        df = DfHandler.update(df)

        filename = target["web_name"] + "_" + target["user_id"] + "_" + str(datetime.today())
        forum_path = BASE_PATH + '/files/user/' + target["web_name"] + '/'

        if target["file_type"] == "csv":
            path = forum_path + filename + '.csv'
            df.to_csv(path, index=False)
        elif target["file_type"] == "json":
            path = forum_path + filename + '.json'
            df.to_json(path, orient='records')

    @staticmethod
    def get_date(start_or_end):
        date_entry = input('Enter a ' + start_or_end + ' date in YYYY-MM-DD numerical format: ')
        year, month, day = map(int, date_entry.split('-'))
        date1 = date(year, month, day)
        return date1

    def get_user_input(self):
        target = {}
        global BASE_PATH
        BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'

        target["source_type_input"] = input("Please enter the type of source(News or Forum or User): ").lower()
        target["web_name"] = input("Please enter web name from (WXC, HR or MIT): ").upper()
        target["file_type"] = input("Please enter the export file type (csv or json): ")

        if target["source_type_input"] == "user":
            target["user_id"] = input("Please enter the user id: ")
            self.scrap_user(target)
        else:
            target["start_date"] = self.get_date('start')
            target["end_date"] = self.get_date('end')
            print("This program scraps from " + str(target["start_date"]) + ' to ' + str(target["end_date"]))
            if target["source_type_input"] == "news":
                self.scrap_news(target)
            elif target["source_type_input"] == "forum":
                self.scrap_forum(target)
            else:
                print("Please enter a valid source type!")

    # def fake_user_input(self):
    #     target = {}
    #     global BASE_PATH
    #     BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../'
    #
    #     target["source_type_input"] = "forum".lower()
    #     target["web_name"] = "MIT"
    #     target["file_type"] = "csv"
    #
    #     if target["source_type_input"] == "user":
    #         target["user_id"] = "beijingren3"
    #         self.scrap_user(target)
    #     else:
    #         target["cat_name"] = "USANews"
    #         target["start_date"] = date(2022, 7, 7)
    #         target["end_date"] = date(2022, 7, 7)
    #         print("This program scraps from " + str(target["start_date"]) + ' to ' + str(target["end_date"]))
    #         if target["source_type_input"] == "news":
    #             self.scrap_news(target)
    #         elif target["source_type_input"] == "forum":
    #             self.scrap_forum(target)
    #         else:
    #             print("Please enter a valid source type!")


    def init(self):
        chromedriver.install()
        self.get_user_input()
        #self.fake_user_input()


