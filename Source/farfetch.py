from   recommender import Recommender
from   selenium    import webdriver
from   bs4         import BeautifulSoup as BS
import pandas      as     pd
import requests
import pymongo
import time
import json

class Farfetch():
    
    # initiates Mongo NoSQL database and creates document stores
    def __init__(self):
        self.client             = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        self.database           = self.client['farfetch']
        self.review_collection  = self.database['customer_reviews']
        self.product_collection = self.database['product_details']
        self.recommender_system = self.init_recommender_system()
        self.driver             = None
        
    ################################################################################
    # DATA GATHERING: CUSTOMER REVIEWS
    ################################################################################
    
    # deletes all documents from the collection of customer reviews
    def clear_review_collection(self):
        self.review_collection.delete_many({})
        return self.review_collection

    # parses a single review from HTML soup
    def parse_review(self, soup):
        
        # create the review to be returned
        customer_review = {}
    
        # top module of review card
        top = soup.find('div', class_ = 'baseline col12 cards top-module')

        # date of the review
        date = top.find('p', class_ = 'color-medium-grey col-xs-5 alpha omega review-flex-item-1')
        customer_review['Date'] = date.get_text().strip()
    
        # rating of the review
        stars     = top.findAll('span', class_ = 'rateit-selected float-left svg')
        halfstars = top.findAll('span', class_ = 'rateit-halfselected float-left svg')
        customer_review['Rating'] = len(stars) + (len(halfstars) * 0.5)
    
        # pieces bought
        pieces  = []
        details = top.findAll('a')
        for detail in details:
            piece                = {}
            piece['Description'] = detail.get_text()
            piece['URL']         = 'https://www.farfetch.com' + detail['href']
            pieces.append(piece)
        
        customer_review['Pieces'] = pieces
    
        # ordered from & reviewed by
        tag = top.find('p', class_ = 'review-pieces-bought')
    
        while tag is not None:
            try:
                tag = tag.find_next_sibling()
                customer_review[tag.get_text().split(':')[0].strip()] = tag.get_text().split(':')[1].strip()
                
            except:
                break
        
        # bottom module of review card
        bot = soup.find('div', class_ = 'baseline col12 overflow cards bottom-module')
    
        # review comments
        if bot:
            review = bot.findAll('div', class_ = 'baseline col12 alpha omega')
            customer_review['Review'] = review[1].get_text().strip()
    
        return customer_review

    # collects all reviews from one HTML page
    def parse_page_reviews(self, html):
        
        # the reviews to be inserted into the collection
        reviews = []
        soup    = BS(html, 'html.parser')
    
        # find and parse all review containers
        page_reviews = soup.findAll('div', class_ = 'font-M baseline col12 mt10 alpha omega boutique-module')
        for page_review in page_reviews:
            reviews.append(self.parse_review(page_review))
    
        # insert page reviews into Mongo collection
        self.review_collection.insert_many(reviews)
    
        return self.review_collection
    
    # collects the specified number of reviews from the site
    def parse_site_reviews(self, n_reviews):
        
        sleep_time = 3
        
        # load first page of 10 reviews
        url             = 'https://www.farfetch.com/reviews'
        driver          = webdriver.Chrome('/Users/flatironschool/Downloads/chromedriver')
        driver.get(url)
        html            = driver.page_source
        self.parse_page_reviews(html)
        
        # load second page of 10 reviews
        time.sleep(sleep_time)
        elem         = driver.find_element_by_xpath("//div[@id='reviewsWrapper']/div[13]/div/span[2]")
        elem.click()
        html         = driver.page_source
        self.parse_page_reviews(html)

        # load subsequent pages of 10 reviews per page
        while self.review_collection.count_documents({}) < n_reviews:
            clicked = False
            
            while not clicked:
                try:
                    time.sleep(sleep_time)
                    elem         = driver.find_element_by_xpath("//div[@id='reviewsWrapper']/div[13]/div/span[3]")
                    elem.click()
                    clicked      = True
                    
                except:
                    pass
            
            html = driver.page_source
            self.parse_page_reviews(html)
            
        # close the Selenium webdriver
        driver.close()
        
        return self.review_collection
    
    # saves the documents in the customer review collection to a json file
    def save_reviews_to_json(self, path):
        with open(path, 'w') as f:
            json.dump(list(self.review_collection.find({}, {'_id': 0})), f)
        
        return self.review_collection