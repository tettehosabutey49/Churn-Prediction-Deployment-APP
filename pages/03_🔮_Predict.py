import streamlit as st
import joblib
import pandas as pd
import xgboost

# Set page configuration
st.set_page_config(
    page_title="Predict Page",
    page_icon="🔮",
    layout="wide"
)
st.title("Customer Churn Prediction")

@st.cache_resource
def load_forest_pipeline():
    pipeline = joblib.load("./models/Random_Forest.pkl")
    return pipeline

@st.cache_resource
def load_XGBoost_pipeline():
    pipeline = joblib.load("./models/XGBoost.pkl")
    return pipeline

def select_model():
    col1, col2, col3,col4 = st.columns(4)

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

def make_prediction(pipeline, encoder):
    gender = st.session_state["gender"]
    senior_citizen = st.session_state["senior_citizen"]
    partner = st.session_state["partner"]
    dependents = st.session_state["dependents"]
    tenure = st.session_state["tenure"]
    phone_service = st.session_state["phone_service"]
    multiple_lines = st.session_state["multiple_lines"]
    internet_service = st.session_state["internet_service"]
    online_security = st.session_state["online_security"]
    online_backup = st.session_state["online_backup"]
    device_protection = st.session_state["device_protection"]
    tech_support = st.session_state["tech_support"]
    streaming_tv = st.session_state["streaming_tv"]
    streaming_movies = st.session_state["streaming_movies"]
    contract = st.session_state["contract"]
    paperless_billing = st.session_state["paperless_billing"]
    payment_method = st.session_state["payment_method"]
    monthly_charges = st.session_state["monthly_charges"]
    total_charges = st.session_state["total_charges"]

    data = [[gender, senior_citizen, partner, dependents, tenure, phone_service, multiple_lines, 
             internet_service, online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies, 
             contract, paperless_billing, payment_method, monthly_charges, total_charges]]
    
    columns = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
        "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
        "PaymentMethod", "MonthlyCharges", "TotalCharges"
    ]

    df = pd.DataFrame(data, columns=columns)

    pred = pipeline.predict(df)
    pred_int = int(pred[0])
    prediction = encoder.inverse_transform([pred_int])
    probability = pipeline.predict_proba(df)

    st.session_state["prediction"] = prediction
    st.session_state["probability"] = probability

def display_form():
    pipeline, encoder = select_model()

    with st.form("input-features"):
        col1, col2 = st.columns(2)
    
        with col1:
            gender = st.selectbox("What is your Gender?", options=["Male", "Female"], key="gender")
            senior_citizen = st.selectbox("What is your senior citizen level?", options=[0, 1, 2, 3], key="senior_citizen")
            partner = st.selectbox("Do you have a Partner?", options=["Yes", "No"], key="partner")
            dependents = st.selectbox("Have you got any dependents?", options=["Yes", "No"], key="dependents")
            tenure = st.select_slider("How many years have you spent at the company?", options=range(0, 75, 1), key="tenure")
            phone_service = st.selectbox("Do you have any phone service?", options=["Yes", "No"], key="phone_service")
            multiple_lines = st.selectbox("Have you got multiple lines?", options=["Yes", "No"], key="multiple_lines")
            internet_service = st.selectbox("Do you have internet service?", options=["DSL", "Fiber Optic", "No"], key="internet_service")
            online_security = st.selectbox("Do you have Online Security?", options=["Yes", "No"], key="online_security")
        
        with col2:
            online_backup = st.selectbox("Do you have online backup?", options=["Yes", "No"], key="online_backup")
            device_protection = st.selectbox("Is your device protected?", options=["Yes", "No"], key="device_protection")
            tech_support = st.selectbox("Do you have Tech support?", options=["Yes", "No"], key="tech_support")
            streaming_tv = st.selectbox("Are you subcribed to streaming tv?", options=["Yes", "No"], key="streaming_tv")
            streaming_movies = st.selectbox("Are you subscribed to movie streaming?", options=["Yes", "No"], key="streaming_movies")
            contract = st.selectbox("What is your contract duration?", options=['Month-to-month', 'One year', 'Two year'], key="contract")
            paperless_billing = st.selectbox("Do you use paperless billing?", options=["Yes", "No"], key="paperless_billing")
            payment_method = st.selectbox("What payment method do you use?", options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)',
            'Credit card (automatic)'], key="payment_method")
            monthly_charges = st.slider("What is your monthly charge?", min_value=18, max_value=119, key="monthly_charges")
            total_charges = st.slider("What is your total charge?", min_value=18, max_value=8672, key="total_charges")

        st.form_submit_button("Submit", on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))

# Initialize session state for prediction and probability
if "prediction" not in st.session_state:
    st.session_state["prediction"] = None
if "probability" not in st.session_state:
    st.session_state["probability"] = None

# Run the Streamlit app
if __name__ == "__main__":
    display_form()

    #muting the session state
    #st.write(st.session_state)
    
    final_prediction = st.session_state["prediction"]

    if final_prediction is not None:
        st.divider()
        if final_prediction == "Yes": 
            st.write(f"Prediction: {final_prediction[0]}")
            st.write(f' This customer is lively to Churn')
        st.write(f"Probability: {st.session_state['probability'][0]}")
