# Farfetch: Understanding the Customer

![Touch-Driven Recommender Engines](/Plots/Touch_Driven_Recommender_Engines.png)

## How to Navigate This Repository

Browse the pitch deck about Touch-Driven Recommender Engines:
https://github.com/acdick/farfetch_understanding_the_customer/blob/master/Farfetch_Understanding_the_Customer.pdf

Read the full story on Medium about Touch-Driven Recommender Engines:

## The Project Data Stack

* Business Understanding:                 Brand Management, Consumer Journeys
* Data Mining & Cleaning:                 Requests, BeautifulSoup, HTML
* Data Warehousing:                       MongoDB, NoSQL, JSON, Pickle
* Data Exploration & Feature Engineering: Python, Numpy, Pandas
* Predictive Modeling:                    Surprise
* Data Visualization:                     Selenium Webdriver, Seaborn, Matplotlib

## Data Product Inputs and Outputs

**Farfetch Customer Reviews**<br>
https://www.farfetch.com/reviews

* Pieces Bought
* Product URL
* Rating
* Reviewed By

**Farfetch Product Details**
* Original Price
* Discount
* Designer
* Gender
* Made In
* Category

**Consumer Journey**
* Touch-Driven Recommender Engine
* Live Checkpoint for Inventory Stockouts
* Non-Repeating Rolling Recommendations
* Synchronization with NoSQL Database

![Understanding the Customer: Who They Are](/Plots/Who_They_Are.png)

## A Touch-Driven Recommender Engine

**Unpersonalized: The Most-Rated Individual Products**
* 3x recommendations

![The Most-Rated Individual Products](/Plots/The_Most_Rated_Individual_Products.png)

**Unpersonalized: The "Best One" Most-Rated Subcategory**
* 3x recommendations

![The Best One Most-Rated Subcategory](/Plots/The_Best_One_Most_Rated_Subcategory.png)

**Unpersonalized: The "Best Nine" Most-Rated Subcategories**
* 9x recommendations

![The Best Nine Most-Rated Subcategories](/Plots/The_Best_Nine_Most_Rated_Subcategories.png)

**Content-Based Filtering: Product Similarity via Pearson Correlation**
* 3x recommendations

![Content-Based Similarity: Pearson Correlation](/Plots/Content_Based_Similarity_Pearson_Correlation.png)

**Collaborative Filtering: Matrix Factorization via Singular Value Decomposition**
* Nx recommendations