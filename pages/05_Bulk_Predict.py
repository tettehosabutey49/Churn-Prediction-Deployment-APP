import streamlit as st
import joblib
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Predict Page",
    page_icon="🔮",
    layout="wide"
)
st.title("Bulk Customer Churn Prediction")

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


def make_prediction(pipeline, encoder, data):
    file_extension = data.name.split('.')[-1].lower()
    
    if file_extension == 'csv':
        df = pd.read_csv(data)
    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(data)
    elif file_extension == 'json':
        df = pd.read_json(data)
    else:
        st.error("Unsupported file format")
        return None, None

    pred = pipeline.predict(df)
    pred_int = int(pred[0])
    prediction = encoder.inverse_transform([pred_int])
    probability = pipeline.predict_proba(df)
    return prediction, probability

# Initialize session state for prediction and probability
if "prediction" not in st.session_state:
    st.session_state["prediction"] = None
if "probability" not in st.session_state:
    st.session_state["probability"] = None

# Run the Streamlit app
if __name__ == "__main__":
    pipeline, encoder = select_model()

    if st.checkbox("Do you want to make a prediction?"):
        uploaded_file = st.file_uploader("Upload your dataset", type=None)
        if uploaded_file is not None:
            if st.button("Predict"):
                prediction, probability = make_prediction(pipeline, encoder, uploaded_file)
                if prediction.size > 0 and probability.size > 0:
                    st.session_state["prediction"] = prediction
                    st.session_state["probability"] = probability
                    st.success("Prediction made successfully")

    final_prediction = st.session_state["prediction"]

    if final_prediction is not None:
        st.divider()
        if final_prediction == "Yes": 
            st.write(f"Prediction: {final_prediction[0]}")
            st.write(f' This customer is likely to Churn')
            st.write(f"Probability of this customer churning is: {round(st.session_state['probability'][0][1]*100, 2)}%")
        else:
            st.write(f"Prediction: {final_prediction[0]}")
            st.write(f' This customer is not likely to Churn')
            st.write(f"Probability of this customer not churning is : {round(st.session_state['probability'][0][0]*100, 2)}%")
