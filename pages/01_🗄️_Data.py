import streamlit as st
import pyodbc

st.set_page_config(
    page_title = "Data Page",
    page_icon="🗄️",
    layout="wide"
)

st.title("Telcos Database🗄️")

## Creating a connection to the database 
## Querying the database
@st.cache_resource(show_spinner="connecting to database ....")
def init_connection():
    return pyodbc.connect(
        "DRIVER = {SQL Server};SERVER= "
        + st.secrets["server"]
        +"; DATABASE="
        + st.secrets["database"]
        + "; UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )
connection = init_connection()

@st.cache_data(show_spinner="running_query...")
def running_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        st.write(cursor.description)
        df = pd.Dataframe.from_records(rows, columns=[column[0] for column in cursor.description])
    return df

def get_all_column():
    sql_query =  """ SELECT * FROM LP2_Telco_churn_first_3000 """
    df = running_query(sql_query)
    st.write(rows)
    return df

st.write(get_all_column())
st.selectbox("select..", options=["All columns", "Numerical columns", "Categorical columns"])