from xmlrpc.client import APPLICATION_ERROR
import os
from flask import Flask, request, jsonify
import pickle, json
import yaml
import torch
import os, sys
from model_and_utils import MySentimentModel, INT_TO_LABEL

with open("./config.yml", "r") as ymlfile:
    config = yaml.full_load(ymlfile)
with open(config['vocab_path'], 'rb') as f:
    vocab = pickle.load(f)

model = MySentimentModel(config, vocab, INT_TO_LABEL)
model.load_state_dict(torch.load(config['model_path'], map_location=torch.device('cpu')))
model.eval()

application = Flask(__name__)

@application.route("/") # what URL should trigger our function
def home():
    return "<p>Sentiment Analysis Inference API Homepage</p>" # returns the message in the user’s browser

@application.route('/inference', methods=['GET', 'POST'])
def inference():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        string_json = request.get_json(force=True).encode()
        dict_json = json.loads(string_json)
        text = dict_json['text']
        prediction = model.predict(text)
        return jsonify(
                Sentiment=prediction,
                )
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(debug=True, host='0.0.0.0', port=port)

if __name__ == "__main__":
    application.debug = True
    application.run()