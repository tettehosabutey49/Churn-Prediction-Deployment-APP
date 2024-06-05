import streamlit as st

st.set_page_config(
    page_title = "Home Page",
    page_icon="🏠",
    layout="wide"
)

st.title("Telcos Churn Prediction APP")
st.image("others\Customer-Churn.png", caption="", use_column_width=True)


st.write("This prediction app gives stakeholders the opportunity to predict if customers will churn based on some features")