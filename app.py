import streamlit as st
from google.cloud import firestore
import datetime

# Initialize Firestore DB
db = firestore.Client()

def save_prediction(prediction, email, date):
    doc_ref = db.collection("predictions").add({
        "prediction": prediction,
        "email": email,
        "date": date,
        "notified": False,
        "result": None
    })

st.title("Future Prediction App")

prediction = st.text_input("Enter your prediction")
email = st.text_input("Enter your email")
date = st.date_input("When should we check this prediction?")

if st.button("Submit Prediction"):
    if prediction and email and date:
        save_prediction(prediction, email, date)
        st.success("Prediction saved!")
    else:
        st.error("Please fill all fields.")
