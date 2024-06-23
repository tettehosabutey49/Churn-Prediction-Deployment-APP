import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Dashboard Page",
    page_icon="📊",
    layout="wide"
)

# st.title("Churn Prediction Dashboard📊")
# st.write("Welcome to the Telcos Dataset Dashboard! 🚀 Explore insightful visualizations and uncover trends in customer churn and behavior. Use the filters to dive deeper into contract types, gender distribution, and more. Let's discover valuable insights together! 📊")

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
    # Load your data
    df = pd.read_csv('Data/clean_df.csv')
    df.dropna(inplace=True)

    # Create sidebar filters
    dashboard_selection = st.sidebar.selectbox("Select Dashboard", ['EDA Dashboard', 'KPI Dashboard'])

    selected_gender = st.sidebar.selectbox("Select Gender", ['All'] + df['gender'].unique().tolist())
    selected_churn = st.sidebar.selectbox("Select Churn Status", ['All'] + df['Churn'].unique().tolist())
    selected_contract = st.sidebar.selectbox("Select Contract Type", ['All'] + df['Contract'].unique().tolist())

    # Filter data based on selections
    filtered_df = df.copy()
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
    if selected_churn != 'All':
        filtered_df = filtered_df[filtered_df['Churn'] == selected_churn]
    if selected_contract != 'All':
        filtered_df = filtered_df[filtered_df['Contract'] == selected_contract]

    # Define palette dictionary
    palette_dict = {False: "grey", True: "brown", "Yes": "brown", "No": "grey"}

    if dashboard_selection == 'EDA Dashboard':
        
        # EDA Dashboard
        st.subheader("Exploratory Data Analysis (EDA) Dashboard")
        st.write("Welcome to the Telcos Dataset Dashboard! 🚀 Explore insightful visualizations and uncover trends in customer churn and behavior. Use the filters to dive deeper into contract types, gender distribution, and more. Let's discover valuable insights together! 📊")
        
        # Plot Contract Type by Churn
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.countplot(data=filtered_df, x="Contract", hue="Churn", palette=palette_dict, ax=ax)
        ax.set_title('Contract Type by Churn', fontsize=8)
        ax.set_xlabel('Contract Type', fontsize=6)
        st.pyplot(fig)
        st.write(" ")
        st.write(" ")

        # Create two columns for visuals
        col1, col2 = st.columns(2)

        # Create a pie chart in the first column
        with col1:
            fig1, ax1 = plt.subplots()
            churn_counts = filtered_df['Churn'].value_counts()
            explode = tuple([0.05] * len(churn_counts))  # Explode each slice by 0.05
            ax1.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', explode=explode, colors=['brown', 'grey'])
            ax1.set_title('Churn Distribution')
            st.pyplot(fig1)

            st.write(" ")
            fig4, ax4 = plt.subplots()
            sns.countplot(data=df, x="SeniorCitizen", hue="Churn", palette={"No": "grey", "Yes": "Brown"})
            ax4.set_title('Churn by SeniorCitizen')
            plt.xticks(rotation=50)
            st.pyplot(fig4)

        # Create a bar chart in the second column
        with col2:
            fig2, ax2 = plt.subplots()
            gender_churn_counts = filtered_df.groupby("gender")["Churn"].value_counts().unstack().fillna(0)
            gender_churn_counts.plot(kind='bar', stacked=True, ax=ax2, color=['brown','grey'])
            ax2.set_title('Churn Distribution by Gender')
            st.pyplot(fig2)

            fig3, ax3 = plt.subplots()
            sns.countplot(data=df, x="PaymentMethod", hue="Churn", palette={"No": "grey", "Yes": "brown"})
            ax3.set_title('Payment Method Distribution by Churn')
            plt.xticks(rotation=50)
            st.pyplot(fig3)

            ## Creating numeric columns and categorical columns
        # Create heatmap for numeric columns
            numeric_cols = df.select_dtypes(include=["int", "float"])
            corr_matrix = numeric_cols.corr()
            colors = ["#8B0000", "#DC143C", "#CD5C5C", "#FF4500", "#FF6347", "#FFC0CB", "#A9A9A9"]
            fig5, ax5 = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap=colors, square=True, ax=ax5)
            ax5.set_title("Correlation of numerical columns")
            st.pyplot(fig5)


    else:
        # KPI Dashboard
        st.subheader("Key Performance Indicators (KPI) Dashboard")
        st.write("This KPI Dashboard provides a comprehensive overview of the model's performance. It includes confusion matrices, ROC curves, and analyses of threshold effects. By fine-tuning these thresholds, we aim to enhance the model's ability to accurately predict the number of customers likely to churn, thereby improving overall prediction accuracy and business decision-making.")
        col3, col4, col5, col6 = st.columns(4)
        with col3: 
            st.write("###### XGBoost Metrics🎯✨")
            st.metric(label= "Precision🎯✨", value="81%" )
        with col4:
            st.write("")
            st.write("")
            st.metric(label="f1_score", value="77%")
        with col5:
            st.write("##### Forest Metrics✨")
            st.metric(label= "Precision🎯✨", value="82.4%" )
        with col6:
            st.write("")
            st.write(" ")
            st.metric(label = "F1_score⚖️", value="76.9%")
        image = Image.open("others/roc_curve.png")
        st.image(image, caption="ROC_Curve", use_column_width=True)

        col1, col2 = st.columns(2)

        with col1:
            image1 = Image.open('others/confusion_matrix_random_forest.png')
            st.image(image1, use_column_width=True)

        with col2:
            image3 = Image.open('others\confusion_matrix_xgboost.png')
            st.image(image3,  use_column_width=True)

        st.write(" ")
        st.write("#### Confusion Matrix of Models At Optimal Thresholds")

        col7, col8 = st.columns(2)

        with col7:
            image1 = Image.open('others\confusion_matrix_RF_TH_0.284).png')
            st.image(image1,  use_column_width=True)

        with col8:
            image3 = Image.open('others\confusion_matrix_xgboost_TH_0.024).png')
            st.image(image3, use_column_width=True)

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: emmanuel")
    st.write("password: 00000")