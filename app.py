import streamlit as st
from google.cloud import firestore
import os
import datetime
import time

# Set the environment variable for the service account key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"

# Initialize Firestore DB
db = firestore.Client()

def save_prediction(prediction, email, date, checkAnswer):
    # Convert date to datetime
    date = datetime.datetime.combine(date, datetime.datetime.min.time())
    doc_ref = db.collection("predictions").add({
        "prediction": prediction,
        "email": email,
        "date": date,
        "checkAnswer": checkAnswer,
        "notified": False,
        "result": None
    })

def get_prediction_count():
    predictions_ref = db.collection("predictions")
    count = len(list(predictions_ref.stream()))
    return count

st.title("Future Prediction App")

prediction = st.text_input("Enter your prediction")
# Add a radio button with options "Yes" and "No"
checkAnswer = st.radio("Do you want me to try to check the answer?", ("Yes", "No"))

email = st.text_input("Enter your email")
date = st.date_input("When should we check this prediction?")

if st.button("Submit Prediction"):
    if prediction and email and date:
        save_prediction(prediction, email, date, checkAnswer)
        notification_placeholder = st.empty()
        notification_placeholder.success("Prediction saved!")
        time.sleep(3)
        notification_placeholder.empty()
    else:
        notification_placeholder = st.empty()
        notification_placeholder.error("Please fill all fields.")
        time.sleep(3)
        notification_placeholder.empty()

# Display the total number of predictions
prediction_count = get_prediction_count()
st.sidebar.markdown(f"### Total Predictions: {prediction_count}")

# Styling to place the prediction count at the bottom-left corner
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True
)
