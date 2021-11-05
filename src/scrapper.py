import time
from datetime import datetime

import bs4
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
today = datetime.today().strftime("%B %d, %Y")


class Scraper:
    def __init__(self, resource: str = "facebook") -> None:
        self.resource = resource

    def __str__(self) -> str:
        print(f"Scraper object for {self.resource}")

    def __scrap_facebook(self) -> list:
        fb_todays_posts = []
        url = "https://ai.facebook.com/blog/"
        driver.get(url)
        try:
            time.sleep(10)
            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
            top_post = soup.find_all("div", {"class": "_8x7i _8x8q _8x92"})
            other_posts = soup.find_all("div", {"class": "_8wpt"})
            all_posts = top_post + other_posts
            for post in all_posts:
                elements = [s for s in post.strings]
                title, descr, date = elements[-3:]
                domen = "|".join(elements[:-3])

                if date == today:
                    link = post.find("a", href=True)["href"]
                    org = "Facebook AI"
                    p = (org, domen, date, title, descr, link)
                    fb_todays_posts.append(p)
                else:
                    break
        except:
            raise TimeoutError(f"{url} is not responding on time.")

        return fb_todays_posts

    # def __scrap_google(self) -> list:
    #     pass

    # def __scrap_openai(self) -> list:
    #     pass

    # def __scrap_stanford(self) -> list:
    #     pass

    def scrap_all(self) -> list:
        all_todays_posts = []
        all_todays_posts.append(self.__scrap_facebook())
        # all_todays_posts.append(self.__scrap_google())
        # all_todays_posts.append(self.__scrap_openai())
        # all_todays_posts.append(self.__scrap_stanford())
        return all_todays_posts
