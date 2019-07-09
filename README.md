RECOMMENDER SYSTEMS
# Touch-Driven Recommender Engines
UNDERSTANDING THE CUSTOMER

[Browse the pitch deck...](Farfetch_Understanding_the_Customer.pdf)

In the digital age, the internet connects billions of people to countless products around the world, providing consumers with more choices than ever before. In 2016, 185,000 sellers carried over 353 million products in the Amazon Marketplace alone. While savvy choosers may find exactly what they want, many consumers can be paralyzed by the decision-making process.

The Jam Experiment, published by Sheena Sethi Iyengar and Mark Lepper in 2001, studied how choice influences consumer behavior. An assortment of 24 jams attracted more customers (60%) than six jams (40%). But only 3% of shoppers purchased from the large set, while 30% bought from the small one. Shoppers felt confident in choosing the best jam when offered fewer options.

Recommender systems assist consumers in the search and discovery of new products and services, selectively reducing the option set presented to them. Demonstrating their business value, Netflix attributes $1 billion in annual cost savings to its AI recommender system. These systems filter options through several approaches involving varying levels of personalization.

Personalized recommender systems suffer from the “cold start” problem, in which they require some initial data about customer preferences to make targeted recommendations. To address this issue, demographic data mining approaches can pre-populate assumptions about a new consumer, while ensemble techniques can aggregate multiple recommender systems.

But perhaps we can leverage simple unpersonalized recommender systems to follow the touch points of the consumer journey. We can tackle the cold start problem by recommending popular products to new customers and then progressively switching to more personalized recommendations. So let’s try to implement a touch-driven recommender engine for an e-commerce platform.

[Continue reading the full story curated by The Startup, a Medium publication...](https://medium.com/swlh/touch-driven-recommender-engines-85b6c722a7d9?source=friends_link&sk=436886dcec00e828fffdeb6c23ed56a5)

## Repository Contents

* [Project Features](#project-features)
* [Data Products](#data-products)
* [Source Code](#source-code)
* [Output Results](#output-results)
* [Collaboration](#collaboration)

## Project Features
ADTECH | DIGITAL MARKETING | BRAND MANAGEMENT | CONSUMER JOURNEYS | RECOMMENDER SYSTEMS

![Touch-Driven Recommender Engines](/img/Touch_Driven_Recommender_Engines.png)

- [x] **Touch-Driven Recommender Engine**<br>
A system that records the touch points for each customer and their responses to adaptive recommendations.

- [x] **Live Checkpoint for Inventory Stockout**<br>
A check that each recommended product is in-stock, querying the status of the product webpage or database.

- [x] **Non-Repeating Rolling Recommendations**<br>
A check that each product recommended to the customer is novel based on the recommendation history.

- [ ] **Synchronization with NoSQL Database**<br>
Database feedback of the customer response for each recommendation prior to issuing the next recommendation.

## Data Products
SELENIUM | REQUESTS | BEAUTIFULSOUP | HTML

**[Farfetch Customer Reviews](https://www.farfetch.com/reviews)**
* Date
* Rating
* Pieces Bought
* Product URLs
* Ordered From
* Reviewed By
* Review

**[Farfetch Product Details](https://www.farfetch.com/shopping/women/gucci-leather-belt-with-double-g-buckle-item-12132461.aspx)**
* Product URL
* In-Stock / Sold Out
* Original Price
* Discount %
* Sale Price
* Designer
* Product
* Gender
* Category
* Subcategory
* Style
* Color
* Made In

**[Data Mining](/src/01_Data_Gathering.ipynb)**
* 100,000 Customer Reviews
* 21,641 Product Ratings
* 16,105 In-Stock Product Ratings
* 9,667 Unique Customers
* 13,518 Unique Products

**[Exploratory Data Analysis](/src/02_Exploratory_Data_Analysis.ipynb)**
* 3 Genders (Women, Men, Kids)
* 5 Made In Locations
* 16 Discount Levels
* 1,184 Designers
* 29 Categories
* 374 Subcategories
* 7,788 Colors
* 12,596 Styles

## Source Code
PYTHON | MONGODB | NOSQL | JSON | PICKLE | PANDAS | NUMPY | SURPRISE | SINGULAR VALUE DECOMPOSITION

**[The Farfetch Class](/src/farfetch.py)**
* Object and NoSQL MongoDB database initialization
* Data gathering and cleaning of customer reviews and product information
* Feature engineering of product similarity
* Adaptor wrapping of Recommender class
* Live demonstration of Touch-Driven Recommender Engine

**[The Recommender Class](/src/recommender.py)**
* Object and customer history initialization
* Unpersonalized recommenders
* Content-based recommender
* Collaborative filtering recommender

**[Recommender Engine Unit Tests](/src/03_Recommender_Systems.ipynb)**
* The Most-Rated Individual Products
* The “Best One” Most-Rated Subcategory
* The “Best Nine” Most-Rated Subcategories
* Content-Based Product Similarity via Pearson Correlation
* User-to-User Collaborative Filtering via Singular Value Decomposition

## Output Results
SEABORN / MATPLOTLIB

**[Recommender Engine Live Demo](/src/04_Live_Demo.ipynb)**
1. Instantiate Farfetch object
2. Load product similarity matrix
3. Start live demo
4. Create new user, display recommended product webpages and collect customer ratings
5. End live demo

**Unpersonalized Recommender**
* The Most-Rated Individual Products
* 3x Recommendations

![The Most-Rated Individual Products](/img/The_Most_Rated_Individual_Products.png)
![The Most-Rated Individual Products Farfetch](/img/The_Most_Rated_Individual_Products_Farfetch.png)

**Unpersonalized Recommender**
* The "Best One" Most-Rated Subcategory: Adidas Shoes
* 3x Recommendations

![The Best One Most-Rated Subcategory](/img/The_Best_One_Most_Rated_Subcategory.png)
![The Best One Most-Rated Subcategory Farfetch](/img/The_Best_One_Most_Rated_Subcategory_Farfetch.png)

**Unpersonalized Recommender**
* The "Best Nine" Most-Rated Subcategories
* Designers: Adidas, Dolce & Gabbana, Gucci
* Categories: Shoes, Clothing, Bags
* 9x Recommendations

![The Best Nine Most-Rated Subcategories](/img/The_Best_Nine_Most_Rated_Subcategories.png)
![The Best Nine Most-Rated Subcategories Farfetch](/img/The_Best_Nine_Most_Rated_Subcategories_Farfetch.png)

**Content-Based Filtering Recommender**
* Product Similarity via Pearson Correlation
* 3x Recommendations

![Content-Based Similarity: Pearson Correlation](/img/Content_Based_Similarity_Pearson_Correlation.png)
![Content-Based Similarity: Pearson Correlation Farfetch](/img/Content_Based_Similarity_Pearson_Correlation_Farfetch.png)

**User-to-User Collaborative Filtering Recommender**
* Matrix Factorization via Singular Value Decomposition
* Unlimited Recommendations
* 99.988% Customer-Product Matrix Sparsity

![Collaborative Filtering: Singular Value Decomposition](/img/Collaborative_Filtering_SVD.png)
![Collaborative Filtering: Customer-Product Utility Matrix](/img/Customer_Product_Utility_Matrix.png)

## Collaboration

**Contact:** Adam C Dick
* [Email](mailto:adam.c.dick@gmail.com)
* [LinkedIn](https://www.linkedin.com/in/adamcdick/)
* [Medium](https://medium.com/@adam.c.dick)
* [Scholar](https://scholar.google.com/citations?user=eMO88ogAAAAJ&hl=en)

**License**
* [MIT License](https://github.com/acdick/touch_driven_recommender_engines/blob/master/LICENSE)