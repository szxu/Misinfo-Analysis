import traceback

# selenium 4
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date

from util.chrome_option_setter import ChromeOptionSetter
from scraper.util.text_segmenter import TextSegmenter
from util.news import News
from util.comment import Comment
from util.df_handler import DfHandler


class PybNewsScraper():
    def get_post_content(self, df, url, target):
        p_driver = webdriver.Chrome()
        p_driver.refresh()
        p_driver.get(url)
        p_driver.implicitly_wait(1)

        body = p_driver.find_element(By.CLASS_NAME, "feature-single-main-left")
        title = body.find_elements(By.TAG_NAME, "h1")[0].text
        time = body.find_elements(By.CLASS_NAME, "feature-single-first-col-left")[0].text
        text = body.find_elements(By.CLASS_NAME, "feature-single-second-sec")[0].text
        segmented_text = ""

        website = target["web_name"]
        category = target["cat_name"]
        source = ""
        read_count = 0
        cur_news = News(id, website, category, title, text, source, time, read_count, segmented_text)
        cur_news.print_news()
        df = cur_news.add_row(df)

        p_driver.close()
        return df

    def get_page_content(self, driver, df, target):
        isend = False
        driver.get("https://www.piyaoba.org/category/feature/" + target["cat_name"] + "/")
        driver.implicitly_wait(10)

        posts = driver.find_element(By.CLASS_NAME, "feature-cat-second-inner").find_elements(By.CLASS_NAME, "feature-cat-second-cols")
        for post in posts:
            url = post.find_elements(By.TAG_NAME, "a")[0].get_attribute('href')
            try:
                df = self.get_post_content(df, url, target)
                break
            except Exception as ex:
                print(traceback.format_exc())

        isend = True
        return df, isend

    def init(self, target):
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

        df = DfHandler.make_news_df()
        cdf = DfHandler.make_comment_df()

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
                print(traceback.format_exc())
            print("Finish Scraping Category " + cat)
        return df, cdf

if __name__ == '__main__':
    target = {}
    target["web_name"] = "PYB"
    target["start_date"] = date(2022, 8, 5)
    target["end_date"] = date(2022, 8, 5)

    s = PybNewsScraper()
    _df = s.init(target)
    _df.to_csv("/home/ktonxu/project/AMICA/AMICA-scraper/files/test/out.csv", index=False)