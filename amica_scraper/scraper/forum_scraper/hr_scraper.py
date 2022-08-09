# selenium 4
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, datetime

from util.df_handler import DfHandler
from util.comment import Comment
from util.chrome_option_setter import ChromeOptionSetter

from scraper.util.text_segmenter import TextSegmenter
from scraper.util.time_retriever import Date_retriever

class HrScraper():
    def get_comment_content(self, df, id, target):
        os = ChromeOptionSetter()
        chrome_options = os.set_options2()
        c_driver = webdriver.Chrome(options=chrome_options)
        c_driver.set_page_load_timeout(10)
        c_driver.get("https://huaren.us/showtopic.html?topicid=" + str(id) + "&fid=" + str(target['cat_num']))
        c_driver.implicitly_wait(0.5)


        comment_list = c_driver.find_element(By.CLASS_NAME, "post-list")
        comments = comment_list.find_elements(By.CLASS_NAME, "post-item")
        parent_title = ""
        parent_id = 0

        for i in range(len(comments)):
            comment = comments[i]

            id = int(comment.get_attribute("id"))
            user_id = comment.find_element(By.CLASS_NAME, "post-user").find_element(By.CLASS_NAME, "avatar-wrap").get_attribute('href').replace("https://huaren.us/userinfo.html?uid=", "")
            content = comment.find_element(By.CLASS_NAME, "post-content").text
            time = comment.find_element(By.CLASS_NAME, "post-top-action").text.split("发表于：")[1].split("|只看")[0]

            if i == 0:
                parent_id = id
                is_article = True
                parent_title = comment.find_element(By.CLASS_NAME, "post-content").find_element(By.CLASS_NAME, "topic-title").text
                text = content.split(parent_title)[-1]
            else:
                is_article = False
                text = content

            title = parent_title
            segmented_text = TextSegmenter.seg(title + text)

            parent_text = ""
            parent_user_id = ""
            website = "HR"
            category = target["cat_name"]
            read_count = 0
            reply_count = 0

            cur_comment = Comment(id, website, category, is_article, title, text, user_id, parent_id,
                                  parent_title, parent_text, parent_user_id, time, segmented_text, read_count,
                                  reply_count)
            cur_comment.print_comment()
            df = cur_comment.add_row(df)

            return df

    def get_article_content(self, post, df, target, isend):
        article_url = post.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
        id = article_url.replace("https://huaren.us/showtopic.html?topicid=", "").replace("&fid=" + str(target["cat_num"]), "")
        time = post.find_element(By.XPATH, "div[2]/div[1]/span").text
        timestamp = Date_retriever.retrieve_date(time, "HR")
        start_timestamp = datetime.combine(target["start_date"], datetime.min.time())
        end_timestamp = datetime.combine(target["end_date"], datetime.max.time())

        if timestamp > end_timestamp:
            print("Skip because program " + str(timestamp) + " hasn't reached the target datetime " + str(
                end_timestamp))
            isend = False
            return df, isend
        elif timestamp <= end_timestamp and timestamp >= start_timestamp:
            df = self.get_comment_content(df, id, target)
            isend = False
            return df, isend
        else:
            print("Ending because current time (" + str(timestamp) + ") earlier than target datetime " + str(end_timestamp))
            isend = True
            return df, isend




    def get_page_content(self, driver, df, page_num, target):
        # if the page has all posts, eariler than target date, then end
        isend = True
        driver.get("https://huaren.us/showforum.html?forumid=" + str(target["cat_num"]) + "&order=tid&page=" + str(page_num))
        driver.implicitly_wait(0.5)

        posts = driver.find_element(By.XPATH, "//*[@class='hr-expansion-panel topic-list gray expanded']").find_elements(By.CLASS_NAME, "hr-topic")

        for post in posts:
            try:
                df, isend = self.get_article_content(post, df, target, isend)
                if isend == True:
                    print("Ending program because page has all posts eariler than target date")
                    break
            except :
                print(traceback.format_exc())
        return df, isend


    def init(self, target):
        target["cat_name"] = input("Please enter category name (Chats): ")

        os = ChromeOptionSetter()
        df = DfHandler.make_comment_df()

        if target["cat_name"] == "Chats":
            target["cat_num"] = 398
        else:
            target["cat_num"] = 0

        for i in range(1, 10000):
            chrome_options = os.set_options()
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(10)
            driver.refresh()
            try:
                df, isend = self.get_page_content(driver, df, i, target)
                if isend == True:
                    print("Ending program because page has all posts eariler than target date")
                    break
            except Exception as ex:
                print(traceback.format_exc())
            driver.quit()

        return df

# if __name__ == '__main__':
#     target = {}
#     target["start_date"] = date(2022, 8, 5)
#     target["end_date"] = date(2022, 8, 5)
#
#     s = HrScraper()
#     _df = s.init(target)
#     _df.to_csv("/home/ktonxu/project/AMICA/AMICA-scraper/files/test/out.csv", index=False)