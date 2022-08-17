# selenium 4
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date

from util.chrome_option_setter import ChromeOptionSetter
from scraper.util.text_segmenter import TextSegmenter
from util.news import News
from util.comment import Comment
from util.df_handler import DfHandler


class PybFactScraper():
    def get_post_content(self, url, cur_news):
        p_driver = webdriver.Chrome()
        p_driver.refresh()
        p_driver.get(url)
        p_driver.implicitly_wait(0.5)

        source = p_driver.find_elements(By.ID, "postmeta")[0].find_elements(By.TAG_NAME, "span")[0].text
        text = p_driver.find_elements(By.ID, "articleContent")[0].text
        read_count = p_driver.find_elements(By.ID, "countnum")[0].text

        other_posts = p_driver.find_elements(By.CLASS_NAME, "otherposts")[0]

        divs = other_posts.find_elements(By.TAG_NAME, "div")
        div_count = len(divs)

        for i in range(4, div_count-4, 3):
            div = divs[i]
            p_driver.execute_script("arguments[0].style.display = 'block';", div)
            id = cur_news.id + '/' + div.get_attribute("id")
            website = cur_news.web
            category = cur_news.cat
            is_article = False
            title = ""
            parentid = cur_news.id
            parent_title = cur_news.title
            parent_text = ""
            parent_userid = source
            segmented_text = ""

            reply = div.find_elements(By.CLASS_NAME, "reply")[0].text.split(" 发表评论于 ")
            userid = reply[0]
            time = reply[1]

            comment_text = div.find_elements(By.CLASS_NAME, "summary")[0].text.replace("\n", " ")

            cur_comment = Comment(id, website, category, is_article, title, comment_text, userid, parentid,
                                 parent_title, parent_text, parent_userid, time, segmented_text)
            #curComment.print_comment()
            cdf = cur_comment.add_row(cdf)


        p_driver.close()
        return source, text, read_count, cdf

    def get_page_content(self, driver, df, target):
        isend = False
        driver.get("https://www.piyaoba.org/category/feature/" + target["cat_name"] + "/")
        driver.implicitly_wait(10)

        posts = driver.find_element(By.CLASS_NAME, "feature-cat-second-inner").find_elements(By.CLASS_NAME, "feature-cat-second-cols")
        print(posts[0].text)

        # for i in range(len(posts)):
        #     isend = False
        #     post = posts[i]
        #     post_url = post.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
        #     title = post.find_elements(By.TAG_NAME, 'a')[0].text
        #     time = post.find_elements(By.TAG_NAME, 'span')[0].text
        #     id = post_url.split("/news/")[-1].replace(".html", "")
        #     year, month, day = time.split("-")
        #     comment_date = date(int(year), int(month), int(day))
        #
        #     if comment_date <= target["end_date"] and comment_date >= target["start_date"]:
        #         website = "WXC"
        #         category = target["cat_name"]
        #         cur_news = News(id, website, category, title, "", "", time, "", "")
        #
        #         source, text, read_count, cdf = self.get_post_content(post_url, cur_news)
        #         text = text.replace("\n", " ")
        #         segmented_text = TextSegmenter.seg(title + text)
        #
        #         cur_news = News(id, website, category, title, text, source, time, read_count, segmented_text)
        #         df = cur_news.add_row(df)
        #
        #     if comment_date < target["start_date"]:
        #         print("Ending because current month earlier than target month")
        #         isend = True
        #         break
        #
        #     # if i >= 5:
        #     #     print("Ending because i >= 5")
        #     #     isend = True
        #     #     break
        #     print("Finish Scraping Post " + str(id))
        return df, isend

    def init(self, target):
        #

        os = ChromeOptionSetter()
        global chromeOptions
        chromeOptions = os.set_options()

        cats = ["disinformation-affirmative-action",
                "covid-19-and-vaccination-disinformation",
                "disinformation-about-biden-democrats",
                "disinformation-about-crt",
                "disinformation-about-political-engagement-and-election",
                "anti-immigration-disinformation",
                "disinformation-about-community-safety-and-anti-asian-hate"
                ]

        df = DfHandler.make_fact_df()

        for cat in cats:
            try:
                target["cat_name"] = cat
                driver = webdriver.Chrome(options=chromeOptions)
                driver.set_page_load_timeout(10)
                driver.refresh()
                df, isend = self.get_page_content(driver, df, target)
                driver.quit()
                if isend == True:
                    break
            except Exception as ex:
                print(ex)
            print("Finish Scraping Category " + cat)



        return df

if __name__ == '__main__':
    target = {}
    target["start_date"] = date(2022, 8, 5)
    target["end_date"] = date(2022, 8, 5)

    s = PybFactScraper()
    _df = s.init(target)
    _df.to_csv("/home/ktonxu/project/AMICA/AMICA-scraper/files/test/out.csv", index=False)