import streamlit as st
#import pyodbc
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Data Page",
    page_icon="🗄️",
    layout="wide"
)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, authentication_status, username =authenticator.login(location="sidebar")

if st.session_state["authentication_status"]:
    authenticator.logout(location="sidebar") 
    st.title("Telcos Database🗄️")

    df = pd.read_csv('Data/clean_df.csv')

    st.markdown("<h2 style='font-size:24px;'>Full Dataset</h2>", unsafe_allow_html=True)
    # Main script to display the data
    #df = get_all_column()
    #st.write(df)
    selection = st.selectbox("Select...", options=["All columns", "Numerical columns", "Categorical columns"])

    # Define numerical and categorical columns
    numerical_columns = ["tenure", "MonthlyCharges", "TotalCharges"]
    categorical_columns = ["gender", "Partner", "SeniorCitizen","Dependents", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
                        "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", 
                        "PaymentMethod", "Churn"]

    # Filter the DataFrame based on user selection
    if selection == "Numerical columns":
        df_filtered = df[numerical_columns]
    elif selection == "Categorical columns":
        df_filtered = df[categorical_columns]
    else:
        df_filtered = df


    st.write(df_filtered)

    # Create a section header
    st.markdown("<h2 style='font-size:24px;'>Upload csv file here</h2>", unsafe_allow_html=True)

    # Allow users to upload a CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    # If a file is uploaded
    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Display the DataFrame
        st.write("Uploaded Data:")
        st.write(df)

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: emmanuel")
    st.write("password: 00000")