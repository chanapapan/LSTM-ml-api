from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/") # what URL should trigger our function
def home():
    return "<p>Sentiment Analysis Inference API</p>" # returns the message in the user’s browser

@app.route('/get_json', methods=['GET', 'POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)