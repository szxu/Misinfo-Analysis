# selenium 4
import traceback
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, datetime

from util.df_handler import DfHandler
from util.chrome_option_setter import ChromeOptionSetter
from scraper.util.text_segmenter import TextSegmenter
from util.comment import Comment

from scraper.util.time_retriever import Date_retriever

class WxcScraper():
    def get_comment_content(self, id, target):
        os = ChromeOptionSetter()
        chrome_options = os.set_options2()
        c_driver = webdriver.Chrome(options=chrome_options)
        c_driver.set_page_load_timeout(10)
        c_driver.get("https://bbs.wenxuecity.com/" + str(target["cat_name"]) + "/" + str(id) + ".html")
        c_driver.implicitly_wait(0.5)

        text = c_driver.find_elements(By.XPATH, "//div[@id='postbody']")[0].text

        c_driver.close()
        return text

    def get_article_content(self, post, df, target, isend):
        comments = post.find_elements(By.TAG_NAME, 'p')
        parent_id = ""
        for i in range(len(comments)):
            print("+" * 20)
            comment = comments[i]
            print(comment.text)
            links = comment.find_elements(By.TAG_NAME, 'a')
            title = str(links[0].text)
            commentUrl = links[0].get_attribute('href')
            id = commentUrl.replace("https://bbs.wenxuecity.com/" + str(target["cat_name"]) + "/", "").replace(".html",
                                                                                                               "")
            user_id = str(links[1].text)
            commentAtrTxt = comment.find_element(By.TAG_NAME, 'small').text
            commentAtrTxtList = commentAtrTxt.split(")")
            byte_num = commentAtrTxtList[0].replace("(", "").replace(" bytes", "")
            read_count = commentAtrTxtList[1].replace("(", "").replace(" reads", "")
            time_and_like_list = commentAtrTxtList[2].split("(")
            time = time_and_like_list[0]
            like = time_and_like_list[1] if len(time_and_like_list) > 1 else "0"
            timestamp = Date_retriever.retrieve_date(time, "WXC")
            start_timestamp = datetime.combine(target["start_date"], datetime.min.time())
            end_timestamp = datetime.combine(target["end_date"], datetime.max.time())
            # print(timestamp, start_timestamp, end_timestamp)

            if i == 0:
                parent_id = id
                is_article = True
            else:
                is_article = False

            if timestamp <= end_timestamp and timestamp >= start_timestamp:
                text = self.get_comment_content(id, target)
                segmented_text = ""  # TextSegmenter.seg(title + text)
                reply_count = 0

                parent_title = ""
                parent_text = ""
                parent_user_id = ""
                website = "WXC"
                category = target["cat_name"]

                cur_comment = Comment(id, website, category, is_article, title, text, user_id, parent_id,
                                      parent_title, parent_text, parent_user_id, time, segmented_text, read_count,
                                      reply_count)
                cur_comment.print_comment()
                df = cur_comment.add_row(df)
                isend = False

            elif timestamp > end_timestamp:
                print("Continue because program " + str(timestamp) + " hasn't reached the target datetime " + str(
                    start_timestamp))
                isend = False

            print("=" * 20)

        return df, isend


    def get_page_content(self, driver, df, page_num, target):
        # if the page has all posts, eariler than target date, then end
        isend = True
        driver.get("https://bbs.wenxuecity.com/" + str(target["cat_name"]) + "/?page=" + str(page_num))
        driver.implicitly_wait(0.5)

        posts = driver.find_elements(By.CLASS_NAME, "odd") + driver.find_elements(By.CLASS_NAME, "even")
        for post in posts:
            try:
                df, isend = self.get_article_content(post, df, target, isend)
            except :
                print(traceback.format_exc())
        return df, isend

    def init(self, target):
        target["cat_name"] = input("Please enter category name from (currentevent or military): ")

        os = ChromeOptionSetter()
        df = DfHandler.make_comment_df()

        for i in range(1, 1000000):
            chrome_options = os.set_options()
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(10)
            driver.refresh()
            try:
                df, isend = self.get_page_content(driver, df, i, target)
                print("Finish Scraping Page " + str(i))
                if isend == True:
                    print("Ending program because page has all posts eariler than target date")
                    break
            except Exception as ex:
                print(traceback.format_exc())
            driver.quit()

        return df



# if __name__ == '__main__':
#     target = {}
#     target["start_date"] = date(2022, 7, 15)
#     target["end_date"] = date(2022, 7, 17)
#
#     s = WxcScraper()
#     _df = s.init(target)
#     _df.to_csv("/home/ktonxu/project/AMICA/AMICA-scraper/files/test/out.csv", index=False)