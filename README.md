**Vimet**

Adrià Ferrer

DAFT, Barcelona 2019

Kanban: https://app.asana.com/0/1119190122556879/board

### Introduction
We have all tried to follow a diet. In fact if you quickly look online you'll find hundreds of miracle solutions and none of them actually work. We are looking for the best possible diet but, for us, it's right in front of our eyes: The Mediterranean Diet.

Although the mediterranean diet is well known, there is still a lot of confusion regarding what is it really composed of and it is not easy to find clear steps to follow it.

On the other hand, although it is not a miracle diet, the results have been medicaly proven numerous times and having professional assistance to follow its eating principles always is a good help.

   **Food items and proportions included in the Mediterranean Diet**
![Alter text](https://cdn.shopify.com/s/files/1/0018/5312/8748/files/alimentos-dieta-mediterranea_1024x1024.png?v=1549193784)
Source: www.casavimet.com

Vimet (https://casavimet.com/) brings the Mediterranean Diet to your kitchen assessed by the most relevant medical doctors and nutricionists in the field. Vimet plans your weekly diet for you, so that you only have to buy the groceries and prepare the delicious yet healthy meals. It also comes with the weekly plan so you can plan ahead and follow the guidelines.

### Overview
Vimet has been up and running for almost a year now and after around 200 orders and 50 clients, they would like to answer some questions with the data collected during this time.

* Is there any item combination that maximises sales?

* If we run out of an item, what should be the substitute?

All of these questions can be answered with the available data. The main potential issue will be the low amount of data as we only have around 200 orders and 50 clients.

Success will be defined if both models can provide significant answer and/or a decision-making tool can be defined (e.g. descriptive data on best combinations of products)

### Data Preparation
We will work with 2 datasets:
* Oders register:
(General description of the dataset such as the size, complexity, data types, etc.)
* Items Register: 
(General description of the dataset such as the size, complexity, data types, etc.)

Both Datasets were provided by Vimet

### Data Ingestion & Database
During the ETL process we will transform the data so it can be properly saved in an SQL database. The tables' structure is the following.

**Database structure**
![Alter text](https://github.com/adriaferrer/Vimet/blob/master/DBstructure.png)

The customers table was not provided by Vimet to comply with GDPR as the data contains personal information of the customers. However some information directly linked to the clients has been included in the schema and with the implementation of the rest of the client information, it can be used in the future.
The DataBase is hosted by Google Cloud.

#### Database description
**Orders**
* Name: Identifier of the order (str)
* Customer: Customer Id (int)
* Financial status: describes whether the order has been paid, refunded or not paid (str)
* Fulfillment status: describes whether the order has been fulfilled or not (str)
* Total: Total amount of the order (float)
* Discount Amount: amount of discount applied to the order (float)
* Shipping method: Describes the shipping method of the order (str)
* Shipping Zip: Postal code where the order was sent to (str)
* Payment method: identifies the payment method (str)
* Refunded amount: total amount refunded to customer in that order (float)
* Discount code: Identifies whether the client used a discount code or not (int)
* Notes: Notes provided by the customer to be applied in the order (str)

**Items**
* Name: Order Id (str)
* Lineitem quatity: Quantity of the item in the order (int)
* Lineitem name: description of the item (str)
* Lineitem price: price of the item (float)
* Lineitem requires shipping: identifies whether the item requires shipping (int)
* Lineitem taxable: defines whether the item is taxable (int)
* Lineitem fulfillment status: defines whether the item was finally included in the order (str)

**Customers**
* Customer: customer id (int)
* Accepts marketing: describes whether the client has agreed to receive marketing (int)
* Shipping City: Described the city the order was sent to (str)
* Customer_class: artificial variable created from the number of orders a client has made (str)


### Data Wrangling and Cleaning
We start with the ETL process. The data is obtained via a csv provided by Vimet that includes all the information from the Shopify server. This process could be automatized in future steps. Once the data is obtained, we run a first script to transform and load the data to our SQL database.This transformation includes dividing the whole database into the corresponding tables.
After this, each of the tables are transformed to enable analysing the data. From this step on, we will have data we can work with.

Three main steps will follow in paralel:
* Descriptive study of the data.
* Creation of a ML model.

**Data Flow**
![Alter text](https://github.com/adriaferrer/Vimet/blob/master/DataFlow.png)

1) **Descriptive statistics**: In order to provide context for the analysis, a descriptive study will be performed on the data to identify the best-selling products, evolution of sales, etc.

2) **Recommender**: Two recommender models will be designed to recommend new products to customers and substitute products for orders.

### Data Analysis

#### Descriptive statistics
We have described the items and the orders separately first and then the combined data.
* **Items:** we checked the distribution of the numerical features, identified the main providers and items bought and checked that, generally, the customers follow a mediterranean food distribution.
* **Orders:** we also checked the distribution and the (non)correlation of the numerical features. We also described the percentages of paid and fulfilled orders. Additionally we mapped where the orders are delivered.

#### Recommender
**Similar customers:** We defined the similarity of customers based on the items bought historically based on a defined cosine distance matrix. This allowed to identify potential items a customer could buy that have never bought before.
**Substitutive items:** We identified items that never go toghether in an order (thus, substitutive) using a cosine distance matrix between items. We can now provide items that can potentially substitute others that are in the same food group (e.g. vegetables).

### Evaluation
The evaluation of the model will be done in next steps using real customers to validate the recommendations. Also the group of nutricionists of Vimet will validate the recommendations for substitutive items.

### Conclusion
* This analysis provided the first steps to implement data analytics in Vimet.
* When (and if) the company grows the potential for more effective decision-making is significant as it can automatize several processes and minimize costs as delivery areas can be predicted and expensive product can be substituted by cheaper products.

### What are the next steps?
* Validation with real customers
* Scriptd to production
* Further automatization of ETL
* Auto shopping list: from nutricionist "menu" to list of items to buy in the market.
* Demand forecast
* Trying Vimet!
