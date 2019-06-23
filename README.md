# Farfetch: Understanding the Customer

## How to Navigate This Repository

**Touch-Driven Recommender Engines**

Browse the [pitch deck](../blob/master/Farfetch_Understanding_the_Customer.pdf)
Read the [full story](https://medium.com/@adam.c.dick/touch-driven-recommender-engines-85b6c722a7d9) on Medium:

**Explore the Data**

* [Data Gathering](../blob/master/Source/01_Data_Gathering.ipynb)
* [Exploratory Data Analysis](../blob/master/Source/02_Exploratory_Data_Analysis.ipynb)
* [Recommender Engine Unit Tests](../blob/master/Source/03_Recommender_Systems.ipynb)
* [Recommender Engine Live Demo](../blob/master/Source/04_Live_Demo.ipynb)

**Review the Source Code**

* [The Recommender System class](../blob/master/Source/recommender.py)
* [The Farfetch class](../blob/master/Source/farfetch.py)

## The Project Data Stack

**Business Understanding**
* Brand Management
* Consumer Journeys

**Programming Languages**
* Python

**Data Mining & Cleaning**
* Selenium Webdriver
* Requests
* BeautifulSoup / HTML

**Data Warehousing**
* MongoDB / NoSQL
* JSON
* Pickle

**Data Exploration & Feature Engineering**
* Pandas
* Numpy

**Predictive Modeling**
* Surprise / Singular Value Decomposition

**Data Visualization**
* Seaborn
* Matplotlib

## Data Product Inputs and Outputs

![Understanding the Customer: Who They Are](/Plots/Who_They_Are.png)

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

## A Touch-Driven Recommender Engine

![Touch-Driven Recommender Engines](/Plots/Touch_Driven_Recommender_Engines.png)

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

**User-to-User Collaborative Filtering: Matrix Factorization via Singular Value Decomposition**
* Nx recommendations

![Collaborative Filtering: Singular Value Decomposition](/Plots/Collaborative_Filtering_SVD.png)

![Collaborative Filtering: Customer-Product Utility Matrix](/Plots/Customer_Product_Utility_Matrix.png)