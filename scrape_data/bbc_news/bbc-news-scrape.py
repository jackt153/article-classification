# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import pandas as pd
import time

from urllib.request import urlopen
from bs4 import BeautifulSoup


# -

# ### BBC News Main Page

def getAndParseURL(url:str) -> BeautifulSoup:
    """Gets all the tags from the pages
    
    
    """
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return(soup)


main_pages = [
'https://www.bbc.co.uk/news',
'https://www.bbc.co.uk/news/coronavirus',
'https://www.bbc.co.uk/news/uk',
'https://www.bbc.co.uk/news/world',
'https://www.bbc.co.uk/news/business'
]

bbc_main_page = getAndParseURL('https://www.bbc.co.uk/news')

# +
links = bbc_main_page.find_all('a', { 'class': 'gs-c-promo-heading' })


bbc_home_page_str = 'https://www.bbc.co.uk'
bbc_news_links_list = list(set([
    bbc_home_page_str + str(link['href']) for link in links
]))
bbc_news_links_list
# -

time.sleep(5)

# ### Once one article Page

trial_url = 'https://www.bbc.co.uk/news/uk-52264145'
print(trial_url)

# +

try:
    page = urlopen(bbc_news_links_list[0])
except:
    print('Could not load page')
# -

soup = BeautifulSoup(page, 'html.parser')

# The BBC news section:

section = soup.findAll('span',{'class': "primary-nav__link-text"})
for sect in section:
    print(sect)

# This retrivies the article title.

headline = soup.find('h1', {"class": "story-body__h1"})
print(f'Type: {type(headline)}')
print(headline.text)

# Obtain the main body of the article

content = soup.find('div', {"class": "story-body__inner"})

article = ''
for i in content.findAll('p'):
    article = article + ' ' +  i.text.replace('"','')
    #article = article  + " ".join([ word.replace('"', '') for word in i.text.split()])

print(i.text.replace('"',''))

print(" ".join([word for word in article.split()]))

# ### Loop to go through the articles

# +
full_list = []

for link in bbc_news_links_list[0:6]:
    temp_list = []
    try:
        soup = getAndParseURL(link)
        temp_list.append(link)
        time.sleep(5)
        
        headline = soup.find('h1', {"class": "story-body__h1"})
        print(headline.text)
        temp_list.append(headline.text)
        
        content = soup.find('div', {"class": "story-body__inner"})
        article = ''
        for i in content.findAll('p'):
            article = article + ' ' +  i.text.replace('"','')

        temp_list.append(" ".join([word for word in article.split()]))
        full_list.append(temp_list)
    except:
        print('Could not load page')
        

# -

df = pd.DataFrame(full_list, columns=['link','title', 'article'])
df['link']
