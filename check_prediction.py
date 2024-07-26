import base64
import json
import datetime
import smtplib
import os
import openai
from keys import Keys
from chatgpt import verify_prediction_with_chatgpt
from google.cloud import firestore
from email.mime.text import MIMEText




# Initialize Firestore DB
db = firestore.Client()


# OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    api_key = Keys.OPENAI_KEY
        

openai.api_key = api_key

chatgpt_available = True
if not verify_prediction_with_chatgpt("Does the earth revolve around the sun?"):
    print("Error: Failed to verify prediction with ChatGPT")
    chatgpt_available = False


def check_predictions(request):
    # Query predictions that are due for checking
    predictions_ref = db.collection("predictions").where("date", "<=", datetime.date.today()).where("notified", "==", False)
    predictions = predictions_ref.stream()

    for prediction in predictions:
        prediction_data = prediction.to_dict()
        # Verify prediction result with ChatGPT
        result = verify_prediction_with_chatgpt(prediction_data["prediction"])
        
        # Send email
        send_email(prediction_data["email"], prediction_data["prediction"], result)
        
        # Update Firestore document
        prediction.reference.update({
            "notified": True,
            "result": result
        })

    return "Predictions checked", 200

def verify_prediction_with_chatgpt(prediction):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Has the following prediction come true? {prediction}",
        max_tokens=50
    )
    answer = response.choices[0].text.strip()
    return "true" if "yes" in answer.lower() else "false"

def send_email(to_email, prediction, result):
    msg = MIMEText(f"The prediction '{prediction}' is {result}.")
    msg["Subject"] = "Prediction Result"
    msg["From"] = "your-email@example.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.login("your-email@example.com", "your-password")
        server.sendmail("your-email@example.com", [to_email], msg.as_string())