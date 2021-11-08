import time
from datetime import datetime

import bs4
from selenium import webdriver
from telegram.utils.helpers import escape_markdown
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
today = datetime.today().strftime("%B %d, %Y")


class Scraper:
    def __init__(self, resource: str = "facebook") -> None:
        self.resource = resource

    def __str__(self) -> str:
        print(f"Scraper object for {self.resource}")

    def __scrape_facebook(self) -> list:
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
                domain = "|".join(elements[:-3])

                if date == today:
                    link = post.find("a", href=True)["href"]
                    org = "Facebook AI"
                    p = (org, domain, date, title, descr, link)
                    (org, domain, date, title, descr, link) = [
                        escape_markdown(el, version=2) for el in p
                    ]
                    message = f"{domain}\n{org} \\- {date}\n\n*{title}*\n_{descr}_\n[Go to blog post]({link})"
                    fb_todays_posts.append(message)
                else:
                    break
        except:
            raise TimeoutError(f"{url} is not responding on time.")

        return fb_todays_posts

    def __scrape_google(self) -> list:
        google_todays_posts = []
        url = "https://ai.googleblog.com/"
        driver.get(url)
        try:
            time.sleep(10)
            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
            posts = soup.find_all("div", {"class": "post"})
            for post in posts:
                title = post.find("a")["title"]
                date = post.find("span", {"class": "publishdate"}).text
                date = date.strip().split(",")[1:]
                date = ",".join(date).strip()

                if date == today:
                    link = post.find("a", href=True)["href"]
                    org = "Google AI"
                    p = (org, date, title, link)
                    (org, date, title, link) = [escape_markdown(el, version=2) for el in p]
                    message = f"{org} \\- {date}\n\n*{title}*\n[Go to blog post]({link})"
                    google_todays_posts.append(message)
                else:
                    break
        except:
            raise TimeoutError(f"{url} is not responding on time.")

        return google_todays_posts

    def __scrape_openai(self) -> list:
        openai_todays_posts = []
        url = "https://openai.com/blog/"
        driver.get(url)
        try:
            time.sleep(10)
            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
            posts = soup.find_all("div", {"class": "post-card-full medium-xsmall-copy"})
            for post in posts:
                title = post.find("a", href=True).text
                date = post.find("time").text

                if date == today:
                    link = post.find("a", href=True)["href"].replace("/blog", "")
                    link = url + link
                    descr = self.__scrape_openai_post_descr(link)
                    org = "OpenAI"
                    p = (org, date, title, descr, link)
                    (org, date, title, descr, link) = [escape_markdown(el, version=2) for el in p]
                    message = f"{org} \\- {date}\n\n*{title}*\n_{descr}_\n[Go to blog post]({link})"
                    openai_todays_posts.append(message)
                else:
                    break
        except:
            raise TimeoutError(f"{url} is not responding on time.")

        return openai_todays_posts

    def __scrape_openai_post_descr(self, link):
        driver.get(link)
        try:
            time.sleep(10)
            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
            descr = soup.find("meta", property="og:description")
            descr = descr.get("content")
        except:
            raise TimeoutError(f"{url} is not responding on time.")

        return descr

    # def __scrape_stanford(self) -> list:
    #     pass

    def scrape_all(self) -> list:
        all_todays_posts = []
        all_todays_posts.extend(self.__scrape_facebook())
        all_todays_posts.extend(self.__scrape_google())
        all_todays_posts.extend(self.__scrape_openai())
        # all_todays_posts.extend(self.__scrape_stanford())
        return all_todays_posts
