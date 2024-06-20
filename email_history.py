from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# MySQL database connection
db = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12714674",
    password="15cCYtDhUC",
    database="sql12714674"
)
cursor = db.cursor()

# Load the data for spam call numbers
spam_call_numbers = pd.read_csv('spam_call.csv')['Phone Number'].tolist()

@app.route('/email/predict_spam', methods=['POST'])
def predict_spam_email():
    text = request.form['text']
    processed_text = preprocess_text(text)
    prediction = best_model.predict([processed_text])[0]
    result = 'Spam' if prediction == 1 else 'Ham (Not Spam)'
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO email_spam_predictions (text, result, created_at) VALUES (%s, %s, %s)"
    values = (text, result, current_time)
    cursor.execute(query, values)
    db.commit()
    
    return result

@app.route('/email/history', methods=['GET'])
def get_email_spam_history():
    query = "SELECT text, result, created_at FROM email_spam_predictions ORDER BY created_at DESC"
    cursor.execute(query)
    predictions = cursor.fetchall()
    predictions_list = []
    for prediction in predictions:
        prediction_data = {
            'text': prediction[0],
            'result': prediction[1],
            'created_at': prediction[2].strftime("%Y-%m-%d %H:%M:%S")
        }
        predictions_list.append(prediction_data)
    return jsonify(predictions_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001, debug=False)
