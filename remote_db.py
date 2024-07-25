from google.cloud import firestore

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