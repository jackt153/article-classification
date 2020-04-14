import pandas as pd
import time

from urllib.request import urlopen
from bs4 import BeautifulSoup
from pathlib import Path
import datetime

from utils.logging_config import get_logger

logger = get_logger()

HOME_PATH = Path.home()
PATH_TO_SCRAPED_DATA = 'art_data/scraped_data'
# ### BBC News Main Page


def getAndParseURL(url: str) -> BeautifulSoup:
    """Gets all the tags from the pages


    """
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    return soup


main_pages = [
    "https://www.bbc.co.uk/news",
    "https://www.bbc.co.uk/news/coronavirus",
    "https://www.bbc.co.uk/news/uk",
    "https://www.bbc.co.uk/news/world",
    "https://www.bbc.co.uk/news/business",
    "https://www.bbc.co.uk/news/politics",
    "https://www.bbc.co.uk/news/technology",
    "https://www.bbc.co.uk/news/science_and_environment",
    "https://www.bbc.co.uk/news/health",
    "https://www.bbc.co.uk/news/education",
    "https://www.bbc.co.uk/news/entertainment_and_arts",
]

full_list = []
for main_page in main_pages:

    try:
        logger.info(f"Re retrieve page: {main_page}")
        bbc_main_page = getAndParseURL(main_page)
        logger.info(f"retrieved page: {main_page}")

        links = bbc_main_page.find_all("a", {"class": "gs-c-promo-heading"})

        bbc_home_page_str = "https://www.bbc.co.uk"
        bbc_news_links_list = list(
            set([bbc_home_page_str + str(link["href"]) for link in links])
        )
        bbc_news_links_list

        # ### Loop to go through the articles
        for link in bbc_news_links_list:
            temp_list = []
            try:
                logger.info("Trying link")
                soup = getAndParseURL(link)
                logger.info(f"Successfuly got soup for: {link}")
                temp_list.append(link)
                time.sleep(5)

                headline = soup.find("h1", {"class": "story-body__h1"})
                logger.info("Get headline")

                temp_list.append(headline.text)

                content = soup.find("div", {"class": "story-body__inner"})
                logger.info("Get Article content")
                article = ""
                for i in content.findAll("p"):
                    article = article + " " + i.text.replace('"', "")

                temp_list.append(" ".join([word for word in article.split()]))
                logger.info("Append all items to main list")
                full_list.append(temp_list)
                logger.info(f"Current number of article in main list: {len(full_list)}")

            except Exception as e:
                logger.error(f"could not load article: {e}")
    except Exception as e:
        logger.error(f"{e}")

if len(full_list) > 0:
    df = pd.DataFrame(full_list, columns=["link", "title", "article"])

    df["create_date"] = pd.to_datetime("today")
    df["create_date"] = df["create_date"].dt.strftime("%m-%d-%Y %H:%M:%S")
    df["create_date"] = pd.to_datetime(df["create_date"])

    df.to_csv(HOME_PATH/PATH_TO_SCRAPED_DATA/ f'bbc_scrape_{str(datetime.date.today())}.csv', index=False)
