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