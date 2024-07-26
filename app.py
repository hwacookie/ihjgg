import streamlit as st
import datetime
import local_db as db
from google.cloud import firestore
import datetime
import time
import tools


# Initialize the session state for input fields
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = ''
if 'email' not in st.session_state:
    st.session_state['email'] = ''
if 'date' not in st.session_state:
    st.session_state['date'] = datetime.date.today() + datetime.timedelta(days=14)
if 'email_ok' not in st.session_state:
    st.session_state['email_ok'] = False


# Function to reset all input fields
def reset_inputs():
    st.session_state['prediction'] = None
    st.session_state['email'] = None
    st.session_state['date'] = datetime.date.today() + datetime.timedelta(days=14)
    st.session_state['email_ok'] = False
    st.rerun()  # Rerun the script to update the UI

# Function to set the input fields programmatically
def set_inputs(prediction, email, date, emailOk=False):
    st.session_state['prediction'] = prediction
    st.session_state['email'] = email
    st.session_state['date'] = date
    st.session_state['email_ok'] = emailOk
    st.rerun()  # Rerun the script to update the UI

st.title("Streamlit Forms Example")

# Create a form
#with st.form(key='prediction_form'):
prediction = st.text_input("Ich hab ja schon immer gesagt, dass ...", value=st.session_state['prediction'], key='form_prediction')
email = st.text_input("Wohin soll ich die Erinnerung schicken?", value=st.session_state['email'], key='form_email')
date = st.date_input("Und wann?", value=st.session_state['date'], key='form_date')
emailOk = st.checkbox("Ja, ich möchte per eMail an meine Vorhersage erinnert werden.", value=st.session_state['email_ok'], key='form_email_ok')

# Submit button for the form
submit_button = st.button(label='Submit')


# Handle form submission
if submit_button:
    if tools.checkEmailFormat(email):
        if prediction and email and date and emailOk:
            db.save_prediction(prediction, email, date)
            notification_placeholder = st.empty()
            notification_placeholder.success("Ok, dann wollen wir mal sehen! Ich hab's mir gemerkt!")
            time.sleep(3)
            notification_placeholder.empty()
            reset_inputs()
        else:
            notification_placeholder = st.empty()
            st.error("Bitte alle Felder ausfüllen.")
    else:
        st.error("Überprüfe deine eMail")



# Display the total number of predictions
prediction_count = db.get_prediction_count()
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