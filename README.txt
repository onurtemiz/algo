# Descriptions

## File descriptions

- **sales.csv** - Train data. Daily sales data covering 2017-2019.
- **product_hierarchy.csv** - Data containing the hierarchy of the products.
- **store_cities.csv** - Data containing the city information of the stores.
- **test.csv** - Test data.
- **sample_submission.csv** - Sample submission file.
- **product_values.csv** - Data containing the profit values of the products sold.

## Column descriptions

- **store_id** - The unique identifier of a store.
- **product_id** - The unique identifier of a product.
- **date** - Sales date (YYYY-MM-DD)
- **sales_quantity** - Sales quantity.
- **is_promo** - Promo exists (1) or not (0)
- **hierarchy_id_1** - The first level hierarchy id of the product.
- **hierarchy_id_2** - The second level hierarchy id of the product.
- **hierarchy_id_3** - The third level hierarchy id of the product.
- **city_id** - The id of the city where the store is located.
- **city_name** - The name of the city where the store is located.
- **prediction** - The prediction for question 1.
- **order_quantity** - The order quantity for question 2.
- **value** - The profit value of the product.


## Rules

### Q1 - Demand Forecast

- **Objective:** To make the most accurate demand prediction for each product, store, date in `test.csv` data.
- The final assessment will be made by comparing the actual demand with the predicted demand.
**RMSLE** (Root Mean Squared Log Error) will be used as the error metric.
- The `prediction` column in the` sample_submission.csv` file must be filled for demand prediction.


### Q2 - Store Allocation

- **Objective:** To make the most profitable order decision without exceeding the specified number of orders.
- For order quantites, the `order_quantity` column in `sample_submission.csv` file must be filled.
- The `order_quantity` column must be an integer. If it's not an integer, **it will be rounded down.**
- Minimum of the `order_quantity` and actual sales quantity will be used for evaluation.
- The total number of orders can be up to 3,000,000. **If the total of order_quantity column is more than 3,000,000 shared result will not be accepted!**
- The profitability values of the products are included in the `product_values.csv` file.

### Q3 - Guess Product Groups
- **Objective** To guess given product groups correctly
- 1-1-2 
- 1-2-3 
- 8-17-1 
- 7-8-18 
- 9-11-13 

### Result Sharing Format

- The format in the file `sample_submission.csv` should be used.
- The file format should be csv.
- Columns should be separated by pipe (|).
- The dot (.) Should be used as a decimal point.
- Columns that should be included in the output:
  - store_id
  - product_id
  - date
  - prediction
  - order_quantity
- File name should be *GROUPNAME.csv.* **Otherwise it will not be accepted!**