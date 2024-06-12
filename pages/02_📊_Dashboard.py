import streamlit as st
import matplotlib.pyplot as plt
import pyodbc
import pandas as pd
import seaborn as sns

st.set_page_config(
    page_title = "Dashboard Page",
    page_icon="📊",
    layout="wide"
)

st.title("Churn Prediction Dashboard📊")
st.write("Welcome to the Telcos Dataset Dashboard! 🚀 Explore insightful visualizations and uncover trends in customer churn and behavior. Use the filters to dive deeper into contract types, gender distribution, and more. Let's discover valuable insights together! 📊")

# Load your data
df = pd.read_csv('Data/clean_df.csv')
df.dropna(inplace=True)

# Streamlit app
#st.title("Churn Prediction Dashboard")

# Create sidebar filters
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

# Plot Contract Type by Churn
#st.write("#### Contract Type by Churn")
fig, ax = plt.subplots(figsize=(5, 3))
sns.countplot(data=filtered_df, x="Contract", hue="Churn", palette=palette_dict, ax=ax)
ax.set_title('Churn by Contract Type', fontsize=8)  # Adjust the font size as needed
ax.set_xlabel('Contract Type', fontsize=6)
st.pyplot(fig)
st.write(" ")
st.write(" ")

# Create two columns for visuals
col1, col2 = st.columns(2)

# Create a pie chart in the first column
with col1:
    #st.write("#### Churn Distribution")
    fig1, ax1 = plt.subplots()
    churn_counts = filtered_df['Churn'].value_counts()
    explode = tuple([0.05] * len(churn_counts))  # Explode each slice by 0.05
    ax1.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', explode=explode, colors=['brown', 'grey'])
    ax1.set_title('Churn Distribution')
    st.pyplot(fig1)

    st.write(" ")
    fig4, ax4 = plt.subplots()
    sns.countplot(data=df, x="SeniorCitizen", hue="Churn",palette={"No":"grey", "Yes":"Brown"})
    ax4.set_title('Churn by SeniorCitizen')
    plt.xticks(rotation=50)
    st.pyplot(fig4)


# Create a bar chart in the second column
with col2:
    #st.write("#### Churn Distribution by Gender")
    fig2, ax2 = plt.subplots()
    gender_churn_counts = filtered_df.groupby("gender")["Churn"].value_counts().unstack().fillna(0)
    gender_churn_counts.plot(kind='bar', stacked=True, ax=ax2, color=['brown','grey'])
    ax2.set_title('Churn Distribution by Gender')
    st.pyplot(fig2)

    #st.write("#### Payment Method Distribution by Churn")
    fig3, ax3 = plt.subplots()
    sns.countplot(data=df, x="PaymentMethod", hue="Churn", palette={"No": "grey", "Yes": "brown"})
    ax3.set_title('Churn by Payment Method Distribution')
    plt.xticks(rotation=50)
    st.pyplot(fig3)

    
