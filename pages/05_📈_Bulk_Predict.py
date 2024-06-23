import streamlit as st
import joblib
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Set page configuration
st.set_page_config(
    page_title="Bulk Predict Page",
    page_icon="📈",
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

    st.title("Bulk Customer Churn Prediction📈")

    @st.cache_resource
    def load_forest_pipeline():
        pipeline = joblib.load("./models/Random_Forest.pkl")
        return pipeline

    @st.cache_resource
    def load_XGBoost_pipeline():
        pipeline = joblib.load("./models/XGBoost.pkl")
        return pipeline

    def select_model():
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            user_choice = st.selectbox("Select a model to use", options=["XGBoost🚀", "Random Forest🌲"], key="selected_model")
        with col2: 
            if user_choice == "XGBoost🚀":
                st.write("###### XGBoost Metrics🎯✨")
                st.metric(label= "Precision🎯✨", value="81%" )
            else: 
                st.write("##### Forest Metrics✨")
                st.write(" ")
                st.metric(label= "Precision🎯✨", value="82.4%" )

        with col3:
            if user_choice == "XGBoost🚀":
                st.write(" ")
                st.write(" ")
                st.metric(label = "F1_score⚖️" , value="77.5%")
            else: 
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.metric(label = "F1_score⚖️" , value="77%")

        with col4: 
            if user_choice == "XGBoost🚀":
                st.write(" ")
                st.write(" ")
                st.metric(label = "Optimal Threshold🎚️" , value="0.024")
            else :
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.metric(label="Optimal Threshold🎚️", value="0.284")
            
        if st.session_state["selected_model"] == "XGBoost🚀":
            pipeline = load_XGBoost_pipeline()
        else: 
            pipeline = load_forest_pipeline()
            
        st.success("Model loaded successfully")
        encoder = joblib.load("./models/label_encoder.pkl")
        return pipeline, encoder


    def make_bulk_prediction(pipeline, encoder, data):
        file_extension = data.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(data)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(data)
        elif file_extension == 'json':
            df = pd.read_json(data)
        else:
            st.error("Unsupported file format")
            return None
        

        # Make predictions
        preds = pipeline.predict(df)
        preds_decoded = encoder.inverse_transform(preds)
        probabilities = pipeline.predict_proba(df)[:, 1]

        # Add predictions and probabilities to the DataFrame
        df['Prediction'] = preds_decoded
        df['Probability'] = probabilities

        return df

    # Initialize session state for prediction
    if "prediction_df" not in st.session_state:
        st.session_state["prediction_df"] = None

    # Run the Streamlit app
    if __name__ == "__main__":
        pipeline, encoder = select_model()

        if st.checkbox("Do you want to make a prediction?"):
            uploaded_file = st.file_uploader("Upload your dataset", type=None)
            if uploaded_file is not None:
                if st.button("Predict"):
                    prediction_df = make_bulk_prediction(pipeline, encoder, uploaded_file)
                    if prediction_df is not None:
                        st.session_state["prediction_df"] = prediction_df
                        st.success("Predictions made successfully")

        if st.session_state["prediction_df"] is not None:
            st.divider()
            st.write("Predictions:")
            st.write(st.session_state["prediction_df"])

elif st.session_state["authentication_status"] is False:
    st.error("Wrong username/password")
elif st.session_state["authentication_status"] is None:
    st.info("Please login to access the website")
    st.write("username: emmanuel")
    st.write("password: 00000")