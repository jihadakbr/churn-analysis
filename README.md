# Churn Analysis
This dataset contains detailed information on customers, including demographic data, transaction behaviors, and interaction history. It focuses on identifying patterns that may indicate customer churn, such as frequent purchases, service engagement, and other relevant behaviors. By analyzing this data, we aim to predict which customers are at risk of leaving, enabling the development of targeted retention strategies to reduce churn and improve customer loyalty.

---

## Table of Contents

1. [Dataset Overview](#dataset-overview)
2. [Main Objective](#main-objective)
3. [Data Understanding](#data-understanding)
4. [Data Preprocessing](#data-preprocessing)
5. [Results](#results)
   1. [The Best Model](#the-best-model)
   2. [Key Insights](#key-insights)
6. [Business Recommendations](#business-recommendations)
7. [Deployment](#dashboard)
8. [License](#license)
9. [Contact](#contact)

---

## Dataset Overview

| No. | Column Name                | Description                                                                 |
|-----|----------------------------|-----------------------------------------------------------------------------|
| 1   | user_id                    | Customer account number.                                                    |
| 2   | attrition_flag             | Customer status (Existing and Attrited).                                    |
| 3   | customer_age               | Age of the customer.                                                        |
| 4   | gender                     | Gender of customer (M for male and F for female).                           |
| 5   | dependent_count            | Number of dependents of customers.                                          |
| 6   | education_level            | Customer education level (Uneducated, High School, Graduate, College, Post-Graduate, Doctorate, Unknown). |
| 7   | marital_status             | Customer's marital status (Single, Married, Divorced, and Unknown).         |
| 8   | income_category            | Customer income interval category (Less than \$40K, \$40K-\$60K, \$60K-\$80K, \$80K-\$120K, \$120K+, Unknown). |
| 9   | card_category              | Type of card used (Blue, Silver, Gold, and Platinum).                      |
| 10  | months_on_book             | Period of being a customer (in months).                                     |
| 11  | total_relationship_count   | The number of products used by customers in the bank.                       |
| 12  | months_inactive_12_mon     | Period of inactivity for the last 12 months.                                |
| 13  | contacts_count_12_mon      | The number of interactions between the bank and the customer in the last 12 months. |
| 14  | credit_limit               | Credit card transaction nominal limit in one period.                        |
| 15  | total_revolving_bal        | Total funds used in one period.                                             |
| 16  | avg_open_to_buy            | The difference between the credit limit set for the cardholder's account and the current balance. |
| 17  | total_amt_chng_q4_q1       | Increase in customer transaction nominal between quarter 4 and quarter 1.  |
| 18  | total_trans_amt            | Total nominal transaction in the last 12 months.                           |
| 19  | total_trans_ct             | The number of transactions in the last 12 months.                          |
| 20  | total_ct_chng_q4_q1        | The number of customer transactions increased between quarter 4 and quarter 1. |
| 21  | avg_utilization_ratio      | Percentage of credit card usage.                                           |


---

## Main Objective

The goal of this project is to develop a machine learning model to predict customer churn and provide insights into the reasons for churn using feature importance analysis.

---

## Data Understanding

There are 10,127 rows with 21 features. In the training set, the target distribution is imbalanced, with 83.9% existing customers and 16.1% attrited customers, representing a ratio of 5.2:1.

![pie-chart](https://raw.githubusercontent.com/jihadakbr/churn-analysis/refs/heads/main/img/pie-chart.png)

---

## Data Preprocessing

1. **Removing Duplicates**: No duplicate data found.
2. **Handling Missing Values**: No missing data found.
3. **Data Type Conversion**: 
   - Converted `user_id` from integer to string.
4. **Error Detection**: No errors were found in the dataset.
5. **Outlier Detection**: There are no extreme outliers. The data appears valid and natural.

---

## Results

### The Best Model

**Best Model: XGBoost**

![metrics](https://raw.githubusercontent.com/jihadakbr/churn-analysis/refs/heads/main/img/the-best-model.png)

![confusion-matrix](https://raw.githubusercontent.com/jihadakbr/churn-analysis/refs/heads/main/img/confusion_matrix.png)

![pr-curve](https://raw.githubusercontent.com/jihadakbr/churn-analysis/refs/heads/main/img/pr-curve.png)

---

### Key Insights

![feature-importance](https://raw.githubusercontent.com/jihadakbr/churn-analysis/refs/heads/main/img/feature-importance.png)

**Insights for Permutation Feature Importance and the Partial Dependence Plots**

1. Key Predictors of Churn (Most Important Features):
  - `total_trans_ct` (Total number of transactions)
    - This feature is the most important predictor in the model, suggesting that customers with a higher number of transactions are less likely to churn.
    - Customers with a total transaction count (`total_trans_ct`) of less than or equal to 20 are more likely to churn, as indicated by the predicted probability of > 0.499 (with our threshold set at 0.4501). Since `total_trans_ct` is the strongest predictor, improving transaction frequency could help reduce churn.

2. Moderately Important Features:
  - `total_revolving_bal` (Total revolving balance)
    - Although this feature is important, it does not strongly predict churn as compared to `total_trans_ct`.
    - As the total revolving balance increases, the likelihood of churn decreases, but the maximum prediction for this feature is 0.406, which is below the threshold of 0.4501. Therefore, it's not a strong predictor for churn.
  - `total_relationship_count` (Number of products used)
    - This feature is relatively important, but its impact on churn prediction is lower than `total_trans_ct`.
    - As the number of products used increases, the likelihood of churn decreases. However, the maximum prediction for this feature is 0.360, which is below the threshold of 0.4501, indicating that this is not a strong predictor for churn.
  - `total_amt_chng_q4_q1` (Transaction amount change between Q4 and Q1)
    - This feature has moderate importance but is not a dominant predictor for churn.
    - A significant increase in the amount of transactions between the quarters correlates with a reduced likelihood of churn, but the maximum prediction for this feature is 0.350. Since it is below the threshold of 0.4501, it is not a strong predictor for churn.
  - `total_ct_chng_q4_q1` (Change in transaction count between Q4 and Q1)
    - Like the previous feature, this one also plays a role but is not highly predictive.
    - An increase in the transaction count between the quarters correlates with a lower probability of churn. However, the maximum prediction for this feature is 0.270, which is below the threshold of 0.4501, indicating it is not a strong predictor.

3. Less Important Features:
  - `months_inactive_12_mon` (Months inactive in the past 12 months)
    - This feature is important but shows a relatively flat relationship in the PDP, suggesting less predictive power.
    - The plot shows a stable or constant line as the number of inactive months increases. The maximum prediction for this feature is 0.216, which is below the threshold of 0.4501, suggesting that inactivity is not a strong predictor for churn in this case.
  - `avg_utilization_ratio` (Average credit card utilization ratio)
    - This feature is of low to moderate importance, but its impact on churn prediction is weak.
    - High credit utilization indicates potential financial stress and could be linked to churn. However, the maximum prediction for this feature is 0.231, which is below the threshold, making it a weak predictor for churn.
  - `months_on_book` (Time as a customer)
    - While this feature is likely to be a weak predictor, it does carry some information about customer longevity.
    - The PDP for this feature shows a relatively stable line, indicating that the duration of the customer relationship does not have a strong effect on churn. The maximum prediction for this feature is 0.189, which is also below the threshold of 0.4501, confirming that it is not a strong predictor for churn.

---

## Business Recommendations

1. Incentivize More Transactions for High-Risk Customers
  - Since `total_trans_ct` (Total number of transactions) is the most significant predictor of churn, focus on increasing transaction frequency, especially for customers who have a transaction count of 20 or fewer. Consider launching targeted campaigns or promotional offers (e.g., cashbacks, loyalty points, or discounts) to encourage these customers to engage more frequently with the service. This approach will directly help in reducing churn.
2. Target Customers with Low Product Usage
  - `total_relationship_count` (Number of products used) plays a moderately significant role in churn. Customers who use fewer products are more likely to churn. Therefore, proactively offer additional products or cross-sell services to existing customers with fewer products. This could include personalized offers for credit cards, loans, or investment products based on the customer's profile, increasing the chances of retaining them.
3. Focus on Increasing Transaction Amounts for Engaged Customers
  - `total_amt_chng_q4_q1` (Transaction amount change between Q4 and Q1) suggests that an increase in transaction amounts correlates with a reduced likelihood of churn. Target customers with increased spending potential by offering higher credit limits, promotional offers on purchases, or rewards for spending more. Encouraging higher transaction amounts will keep these customers engaged and loyal.
4. Engage Inactive Customers with Personalized Campaigns
  - While `months_inactive_12_mon` (Months inactive in the last 12 months) is not a strong predictor on its own, it still offers valuable insight into potential churn. Develop re-engagement campaigns specifically designed for inactive customers. Personalized reminders, exclusive offers, or reconnect campaigns (such as special incentives for reactivation) can help revive interest in your products or services. A customer who has been inactive for a while might still be persuaded to re-engage.
5. Provide Financial Relief or Support for High Utilization Customers
  - Although `avg_utilization_ratio` (Average credit card utilization ratio) is not a strong predictor, high credit utilization can signal financial stress and increase the likelihood of churn. To reduce churn, offer financial relief options such as flexible payment plans, lower interest rates, or debt management programs. This could help reduce stress for high-utilization customers and increase their loyalty to the service.

---

## Deployment

- Streamlit Link: https://churn-analysis-jihadakbar.streamlit.app

![streamlit-dashboard](https://raw.githubusercontent.com/jihadakbr/churn-analysis/refs/heads/main/img/streamlit_dashboard.png)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact
For questions or collaborations, feel free to reach out:

- Email: [jihadakbr@gmail.com](mailto:jihadakbr@gmail.com)
- LinkedIn: [linkedin.com/in/jihadakbr](https://www.linkedin.com/in/jihadakbr)
- Portfolio: [jihadakbr.github.io](https://jihadakbr.github.io/)
