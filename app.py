import streamlit as st
from google.cloud import firestore
import os
import datetime
import time

# Set the environment variable for the service account key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"

# Initialize Firestore DB
db = firestore.Client()



def save_prediction(prediction, email, checkAnswer, dateOfCheck):
    # Convert date to datetime
    doc_ref = db.collection("predictions").add({
        "prediction": prediction,
        "email": email,
        "date": dateOfCheck,
        "checkAnswer": checkAnswer,
        "notified": False,
        "result": None
    })

def get_prediction_count():
    predictions_ref = db.collection("predictions")
    count = len(list(predictions_ref.stream()))
    return count

st.title("Ich sag's wie's ist:")


def create_date_input():
    global date_input
    global time_input  

# Calculate default values
    default_date = datetime.date.today() + datetime.timedelta(days=14)
    default_time = (datetime.datetime.now() + datetime.timedelta(hours=1)).time()

# Create columns for date and time input
    col1, col2 = st.columns(2)

    with col1:
        date_input = st.date_input("Bis zum ", value=default_date)

    with col2:
        time_input = st.time_input("um ", value=default_time)
    

create_date_input()


prediction = st.text_input("wird die Menschheit anerkennen, dass ...", placeholder="... der Mond aus grünem Käse besteht.")

checkAnswer = st.radio("Soll ich deine Vorhersage überprüfen?", ("Versuch's doch!", "Schaffst Du eh nicht."))

email = st.text_input("Wohin soll ich die Antwort schicken?", placeholder="irgend.jemand@irgend.wo")


if st.button("So isses nämlich!"):
    print(date_input)
    if prediction and email and date_input and time_input:
        save_prediction(prediction, email, checkAnswer, datetime.datetime.combine(date_input, time_input))
        notification_placeholder = st.empty()
        notification_placeholder.success("Ok, dann wollen wir mal sehen! Ich hab's mir gemerkt!")
        time.sleep(3)
        notification_placeholder.empty()
    else:
        notification_placeholder = st.empty()
        notification_placeholder.error("Bitte alle Felder ausfüllen.")
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
