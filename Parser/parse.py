import settings
import csv
import time
import json
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from seleniumwire.utils import decode

query = input('Enter a search query: ')


class ReviewParser:
    reviews_count = 0

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-encoding')

    driver = webdriver.Chrome(options=options)
    driver.scopes = ['.*google.com/maps/preview/review.*']
    base_url = 'https://www.google.com/search'

    def __init__(self, query):
        self.driver.get(f'{self.base_url}?q={query}')
        self.find_map()

    def find_map(self):
        print('Finding maps location')
        self.driver.find_element('xpath', "//*[@id='lu_map']").click()
        time.sleep(5)

        try:
            reviews = self.driver.find_element(
                'xpath', "//div[@jsaction='pane.rating.moreReviews']")
        except NoSuchElementException:
            time.sleep(50)

        if reviews:
            print('Found reviews')
            reviews.click()
            time.sleep(5)
            self.write_headers()
            self.get_reviews()

        else:
            print('No reviews found')
            time.sleep(50)
            self.driver.quit()

    def get_reviews(self):
        for request in self.driver.requests:
            if request.response:
                response = request.response
                data = decode(response.body, response.headers.get(
                    'Content-Encoding', 'identity'))
                # drop first line as it does not have any useful data
                data = data.splitlines()[1]
                self.write_file(data)

        del self.driver.requests

        scroll = self.driver.find_element(
            'xpath', "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]")
        scroll.send_keys(Keys.END)

        time.sleep(2)

        if len(self.driver.requests) > 0:
            self.get_reviews()

        else:
            print('No more reviews')
            self.driver.quit()

    def write_headers(self):
        with open('reviews.csv', 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(settings.headers)

    def write_file(self, data):
        print('Writing to file')
        data = json.loads(data)

        with open('reviews.csv', "a", newline='', encoding="utf-8") as f:
            for review in data[settings.reviews_index]:
                writer = csv.writer(f)
                writer.writerow(self.get_review_data(review))

    def get_review_data(self, review):
        review_data = []
        did_owner_reply = False
        self.reviews_count += 1
        print(f'Getting review {self.reviews_count}')
        for key, value in settings.review_format.items():
            # Reply text is dependent on this
            if key == 'didOwnerReply':
                did_owner_reply = review[value[0]] is not None
                if did_owner_reply:
                    review_data.append('Yes')
                else:
                    review_data.append('No')
                continue  # skip the rest of the loop

            # Dependent on didOwnerReply
            if key == 'replyTextFromOwner':
                if did_owner_reply:
                    review_data.append(
                        review[value[0]][value[1]])
                else:
                    review_data.append('No reply')

                continue  # skip the rest of the loop

            # Needs to be converted to string
            if key == 'rating':
                review_data.append(str(review[value[0]]))
                continue

            if len(value) == 1:
                review_data.append(review[value[0]])
            else:
                review_data.append(review[value[0]][value[1]])

        return review_data


ReviewParser(query)
