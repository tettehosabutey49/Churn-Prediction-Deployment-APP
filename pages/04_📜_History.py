import streamlit as st
import os
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title = "History Page",
    page_icon="⏰",
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
    def display_history_of_all_predictions():

        csv_path = "./data/history.csv"
        csv_exists = os.path.exists(csv_path)

        if csv_exists:
            history = pd.read_csv(csv_path)
            st.dataframe(history)
        else:
            st.write("No history of predictions yet.")


    if __name__ == "__main__":
        st.title("History Page")
        display_history_of_all_predictions()

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: emmanuel")
    st.write("password: 00000")