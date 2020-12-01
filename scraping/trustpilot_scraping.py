import pandas as pd
import os
import sys
import lxml.html as html
import math
import csv
import time
import requests
import json

cwd = os.path.join(os.getcwd())
sys.path.append(cwd + "/..")
import constants as cst


def clean_urls(row):
    if "?" in row['url']:
        row['url'] = row['url'].split("?")[0]
    return row


def get_urls_list():
    df_reviews = pd.read_json(cst.TRAIN_REVIEWS1)
    df_reviews_clean_url = df_reviews.apply(clean_urls, axis=1)
    return list(df_reviews_clean_url['url'].unique())


urls = get_urls_list()
results_per_page = 20
for i, url in enumerate(urls):
    print('Scraper set for ' + url + ' - saving result to ' + cst.TRAIN_REVIEWS2)
    ## Count amount of pages to scrape
    # Get page, skipping HTTPS as it gives certificate errors
    page = requests.get(url, verify=False)
    tree = html.fromstring(page.content)

    # Total amount of ratings
    ratingCount = tree.xpath('//span[@class="headline__review-count"]')
    ratingCount = int(ratingCount[0].text.replace(',', ''))

    # Amount of chunks to consider for displaying processing output
    # For ex. 10 means output progress for every 10th of the data
    tot_chunks = 20

    # Throttling to avoid spamming page with requests
    # With sleepTime seconds between every page request
    throttle = False
    sleepTime = 2

    # Total pages to scrape
    pages = math.ceil(ratingCount / results_per_page)
    print('Found total of ' + str(pages) + ' pages to scrape')

    with open(cst.TRAIN_REVIEWS2, 'a', newline='', encoding='utf8') as csvfile:

        # Tab delimited to allow for special characters
        datawriter = csv.writer(csvfile, delimiter='\t')
        if i == 0:
            datawriter.writerow(['date', 'title', 'text', 'url', 'stars'])
        print('Processing..')
        for i in range(1, pages + 1):

            # Sleep if throttle enabled
            if (throttle): time.sleep(sleepTime)

            page = requests.get(url + '?page=' + str(i))
            tree = html.fromstring(page.content)

            # Each item below scrapes a pages review titles, bodies, ratings and dates.
            titles = tree.xpath('//h2[@class="review-content__title"]')
            bodies = tree.xpath('//p[@class="review-content__text"]')
            ratings = tree.xpath('//div[@class="star-rating star-rating--medium"]/img/@alt')
            dates = tree.xpath('//div[@class="review-content-header__dates"]')

            for idx, e in enumerate(bodies):

                # Progress counting, outputs for every processed chunk
                reviewNumber = idx + 20 * (i - 1) + 1
                chunk = int(ratingCount / tot_chunks)
                if (reviewNumber % chunk == 0):
                    print('Processed ' + str(reviewNumber) + '/' + str(ratingCount) + ' ratings')

                # Title of comment
                title = titles[idx].text_content().strip()

                # Body of comment
                text = e.text_content().strip()

                # The rating is the 5th from last element
                stars = ratings[idx][0]

                # Date of comment
                temp_dic = dates[0].text_content().strip()
                date = json.loads(temp_dic)["publishedDate"]

                datawriter.writerow([date, title, text, url, stars])
        print('Processed ' + str(ratingCount) + '/' + str(ratingCount) + ' ratings.. Finished!')
