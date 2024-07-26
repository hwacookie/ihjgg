from google.cloud import firestore
import sqlite3
import datetime



def initDB():


    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('predictions.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table named "predictions"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prediction TEXT NOT NULL,
        email TEXT NOT NULL,
        date DATE NOT NULL,
        creationDate DATE NOT NULL,
        notified BOOLEAN NOT NULL DEFAULT 0,
        result TEXT,
        checkAnswer BOOLEAN NOT NULL DEFAULT 0
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Database and table created successfully.")



# Function to save a prediction into the database
def save_prediction(prediction, email, date, publicOk):
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO predictions (prediction, email, date, creationDate, notified, result, checkAnswer, public)
    VALUES (?, ?, ?, ?, 0, NULL, ?, ?)
    ''', (prediction, email, date.isoformat(), datetime.datetime.now(), False, publicOk))
    conn.commit()
    conn.close()

def get_public_bets():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT prediction FROM predictions WHERE public=1 ORDER BY creationDate DESC LIMIT 15')
    bets = cursor.fetchall()
    bets = [''.join(map(str, tup)) for tup in bets]
    conn.close()
    return bets


# Function to get the total count of predictions
def get_prediction_count():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM predictions')
    count = cursor.fetchone()[0]
    conn.close()
    return count