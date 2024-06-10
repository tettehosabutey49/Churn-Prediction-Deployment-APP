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

st.title("Dashboard")
st.write("This Dashboard gives users the opportunity to understand and derive insights from the Telcos Dataset by answering some analytical questions")


st.title("Telcos Database🗄️")

# Creating a DataFrame for data information
data_info = {
    "Column": ["CustomerID", "Gender", "SeniorCitizen", "Partner", "Dependents", "Tenure", 
               "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
               "Online Backup", "Device Protection", "Tech SUpport", "StreamingTV", "Streaming Movies", "Contract", "Paperless Billing", "Payment Method", "Montly Charges", "Total Charges", "Churn"],
    "Description": ["Unique Customer ID", "Male or Female", "0, 1, 2, 3", "Yes or No", "Yes or No", "Yes or No", "Number of Years at company", "Yes or No", 
                    "Yes or No", "Yes or No", "DSL, Fiber Optic", "Yes or No", "Yes or No", "Yes or No", "Yes or No","One Year, Month to Moth, Two years", "Yes or No", "Mailed Check, Credit card, Electronic check, Bank transfer", 
                    "Charges per month", "total charges throughout contract", "Yes or No"    
                    ]
}

df_info = pd.DataFrame(data_info)

# Displaying the DataFrame as a table
st.text("Data Information")
st.table(df_info)

## Creating a connection to the database 
## Querying the database
@st.cache_resource(show_spinner="Connecting to database...")
def init_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

connection = init_connection()

@st.cache_data(show_spinner="Running query...")
def running_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
    return df

def get_all_column():
    sql_query = """SELECT * FROM LP2_Telco_churn_first_3000"""
    df = running_query(sql_query)
    return df


# Main script to display the data
df = get_all_column()

st.markdown("<h2 style='font-size:24px;'>Churn Distribution</h2>", unsafe_allow_html=True)
# Main script to display the data
df = get_all_column()

# Create a pie chart
fig1, ax1 = plt.subplots()
churn_counts = df['Churn'].value_counts()
ax1.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%',explode=(0.05,0.005), colors=['brown', 'grey'])
ax1.set_title('Churn Distribution')

# Create a second pie chart
fig2, ax2 = plt.subplots()
gender_churn_counts = df.groupby("gender")["Churn"].value_counts().unstack().fillna(0)
gender_churn_counts.plot(kind='bar', stacked=True, ax=ax2, color=['brown', 'grey'])
ax2.set_title('Churn Distribution by Gender')


# Display the plots side by side
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)

with col2:
    st.pyplot(fig2)



   