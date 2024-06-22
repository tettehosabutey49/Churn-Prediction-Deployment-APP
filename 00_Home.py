import streamlit as st

st.set_page_config(
    page_title = "Home Page",
    page_icon="🏠",
    layout="wide"
)

st.title("Telecom Churn Prediction Application")
st.image("others\Customer-Churn.png", caption="", use_column_width=True)

# Set up three columns
col1, col2, col3 = st.columns(3)

# About column
with col1:
    st.write("##### About")
    st.write("This Telco Churn Prediction App is designed to help telecom companies reduce churn and improve customer retention. By leveraging advanced machine learning algorithms, the app provides valuable insights into customer behavior, allowing companies to implement targeted retention strategies.")

# Key Features column
with col2:
    st.write("##### Key Features")
    st.write("- Extraction of data from a SQL Server database")
    st.write("- Option to upload and use external data files")
    st.write("- Predicting Churn based on customer data provided")
    st.write("- Data Visualization for EDA and KPIs")
    st.write("- History page for recording previous predictions made")
    st.write("- Bulk Prediction page for prediction of large data sets")


# Using columns
with col3:
    st.write("##### How to Use")
    st.write("1. **Input Data**: Provide customer data such as demographics and usage.")
    st.write("2. **Run the Prediction Model**: Click on the 'Submit' button to generate churn predictions.")
    st.write("3. **Interpret Results**: Review the churn predictions and take appropriate action to retain customers.")

st.write("##### Benefits to Telecom Companies")
st.write("- **Churn Prediction**: Predict which customers are likely to churn.")
st.write("- **Customer Segmentation**: Segment customers based on churn likelihood for targeted retention strategies.")
st.write("- **Retention Strategies**: Offer personalized discounts, upgrades, or better service to retain customers.")
st.write("- **Cost Savings**: Save on acquiring new customers by retaining existing ones.")
st.write("- **Improved Customer Satisfaction**: Increase satisfaction by addressing customer needs.")
st.write("- **Competitive Advantage**: Stand out by offering better service and personalized offerings.")
st.write("- **Data-Driven Decision Making**: Make informed decisions based on customer behavior and preferences.")
st.write(" ")
st.write(" ")
st.write(" ")

st.write("##### Useful Links and Information")
st.link_button(label="Link to my GitHub repository to access the Telcos Churn ML Deployment Application", url="https://github.com/tettehosabutey49/Churn-Prediction-Deployment-APP")
st.link_button(label="Link to my GitHub repository to access the Telcos Churn ML Project from scratch", url="https://github.com/tettehosabutey49/Telco-Customer-Churn-Prediction-using-Machine-Learning")