# Churn-Prediction-Deployment-APP

## Overview
Welcome to my project repository, where I explore the Telco customer churn prediction using machine learning techniques. This project aims to provide valuable insights into the factors influencing customer churn and build a predictive model to help businesses identify customers at risk of churning. Leveraging streamlit for the website design for stakeholders to interact with the top two models. 

## Comprehensive Churn Prediction and Data Analytics Platform
- Data page : Gives stakeholders the opportunity to view categorical and numerical data and their structure
- Dashboard page : Provides stakeholders the opportunity to visualize EDA and related information on metrics
- Predict page: Gives stakeholders the opportunity to select various combination of features and models to predict whether a customer will churn or not with the probability churning or not churning
- History page : Provides stakeholders the historic data on old predictions made.
- Bulk prediction : This page gives a bulk prediction option, allowing stakholders to upload their data sets and obtain predictions of the entire dataset. To use bulk prediction, make sure your dataset has the same structure as the dataframe on the data page. You can use the demo_df.csv file in the data folder in my repository just for demonstration purposes.

## Key Insights
### Data Exploration
- Senior citizens are less likely to churn compared to non-senior citizens.
- Customers with phone services are more likely to churn.
- Customers with paperless billing are more likely to churn.
- Customers who pay with electronic checks are more likely to churn.

### Modeling
- XGBoost outperformed other models in terms of overall accuracy.
- Random Forest and Logistic Regression also showed promising results.
- Balancing the dataset using SMOTE improved the models' performance, especially in terms of predicting churn (True Positives).

### Recommendations
- Use XGBoost, Random Forest, or Logistic Regression for predicting churn.
- Focus on improving services for customers with phone services and paperless billing.
- Offer incentives for customers to switch to longer contract terms.
- Encourage customers to use alternative payment methods to electronic checks.
- Taking into consideration the threshold during churn predictions can also assist in identifying more customers likely to churn
- It is also key to note that in an attempt to ensure “customers who have been predicted to likely churn” do not churn, by probably intruding some discounts for such customers, there is a likelihood the model might have selected a few or some customers who are not likely to churn. This might cause financial constraint. To reduce this type of burden on the company, a good threshold which has a good balance of both true positives and false negative is essential.



## Getting Started
To get a local copy up and running, follow these steps:

1. Clone this repository to your desired folder:

   ```bash
   cd my-folder
   git clone https://github.com/tettehosabutey49/Churn-Prediction-Deployment-APP

Change into the cloned repository:
```sh
cd CustomerChurnPrediction
```
Create a virtual environment:
```sh
python -m venv env
```
Activate the virtual environment:
On Windows:
```sh
env\Scripts\activate
```
On macOS/Linux:
```sh
source env/bin/activate
```

2. Create Render and connect your github repo to render
3. Deploy the churn prediction app as a webservice on render

### License
This project is [MIT](./LICENSE) licensed.

## Author
 Author: Emmanuel Osabutey
