# selenium 4
import traceback

from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from datetime import date, datetime

from util.df_handler import DfHandler
from util.comment import Comment
from util.chrome_option_setter import ChromeOptionSetter

from scraper.util.text_segmenter import TextSegmenter
from scraper.util.time_retriever import Date_retriever

class MitScraper():
    def get_read_count(self, id, target):
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)
        driver.get("https://www.mitbbs.com/article_t/"+ target["cat_name"] +"/"+ str(id) +".html")
        driver.implicitly_wait(0.5)
        news_bg = driver.find_elements(By.CLASS_NAME, "news-bg")[0]
        attributes = news_bg.find_elements(By.XPATH, "table/tbody/tr[2]/td")[0]
        attri_array = attributes.text.split(",")
        read_count = attri_array[-2].replace("次阅读", "")
        reply_count = attri_array[-1].replace("次回复", "")

        return read_count, reply_count

    def get_comment_content(self, driver, df, comment_num, target):
        isend = False
        #print(commentNum)

        driver.get("https://www.mitbbs.com/article/" + str(target["cat_name"]) + "/" + str(comment_num) + "_3.html")
        driver.implicitly_wait(0.5)

        id = comment_num
        news_bg_td = driver.find_element(By.XPATH, "//td[@class='news-bg']")
        center_td = news_bg_td.find_elements(By.TAG_NAME, "td")[-1]
        center_td_texts = center_td.text.split(",")
        time = center_td_texts[-1]

        timestamp = Date_retriever.retrieve_date(time, "MIT")
        start_timestamp = datetime.combine(target["start_date"], datetime.min.time())
        end_timestamp = datetime.combine(target["end_date"], datetime.max.time())
        #print(timestamp, start_timestamp, end_timestamp)

        if timestamp <= end_timestamp and timestamp >= start_timestamp:
            #print("="*20)
            urls = center_td.find_elements(By.XPATH, "//a[@class='news' ]")
            comment_parent_url = urls[0].get_attribute('href')
            parent_id = int(
                comment_parent_url.replace("https://www.mitbbs.com/article_t/" + str(target["cat_name"]) + "/",
                                           "").replace(".html", ""))
            user_id = urls[2].text
            content = driver.find_element(By.XPATH, "//td[@class='jiawenzhang-type']")
            title = content.text.split("美东)")[0].split("标  题:")[-1].split("发信站:")[0]
            text = content.text.split("美东)")[-1].split("※ 来源")[0].replace("\n", "")
            segmented_text = TextSegmenter.seg(title + text)

            if parent_id == id:
                is_article = True
            else:
                is_article = False

            parent_title = ""
            parent_text = ""
            parent_user_id = 0
            website = "MIT"
            category = target["cat_name"]
            read_count = 0
            reply_count = 0

            if is_article == True:
                read_count, reply_count = self.get_read_count(id, target)

            cur_comment = Comment(id, website, category, is_article, title, text, user_id, parent_id,
                                  parent_title, parent_text, parent_user_id, str(timestamp), segmented_text, read_count, reply_count)
            cur_comment.print_comment()
            df = cur_comment.add_row(df)

        elif timestamp < start_timestamp:
            print("Ending because current month earlier than target month")
            isend = True

        # if abs(34710143 - int(comment_num)) > 1:
        #     isend = True

        return df, isend

    def init(self, target):
        target["cat_name"] = input("Please enter category name from (USANews or Military): ")

        os = ChromeOptionSetter()
        global chrome_options

        df = DfHandler.make_comment_df()

        for i in range(34715667, 1, -2):
            chrome_options = os.set_options()
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(10)
            driver.refresh()
            try:
                df, is_end = self.get_comment_content(driver, df, i, target)
                print("Finish Scraping Comment " + str(i))
                if is_end == True:
                    break
            except Exception as ex:
                print(traceback.format_exc())
            driver.quit()

        return df

# if __name__ == '__main__':
#     target = {}
#     target["user_id"] = 'hhcare'
#     target["start_date"] = date(2022, 7, 14)
#     target["end_date"] = date(2022, 7, 14)
#     #for i in range(65091579, 1, -2):
#
#     ms = MitScraper()
#     _df = ms.init(target)
#     _df.to_csv("/home/ktonxu/project/AMICA/AMICA-scraper/files/test/out.csv", index=False)