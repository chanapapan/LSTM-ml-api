# LSTM-ml-api

This repository contains the code for Sentiment Analysis on the WiseSight dataset using an LSTM model as well as for deploying this model on docker or AWS Elastic Beanstalk via FlaskAPI.

First, download the WiseSight dataset train.txt , train_label.txt, test.txt and test_label.txt from https://github.com/PyThaiNLP/wisesight-sentiment/tree/master/kaggle-competition into 01-train_model/data/

## 01-train_model

This folder contains the files for training the model and saving the best model which will be used for the API.

- 1-sentiment-analysis-LSTM.ipynb contains the code for the training, validation and testing the LSTM model. The vocabulary and the weights of the best model are saved.

- 2-inference.ipynb import the model class from model_and_utils.py for prediction.

- config.yml contains the parameters used for model traning and inference


## 02-local_api_test

This folder contains the files required to run the flask application on local computer and on docker.

inference_app.py define inference route that takes .json file as input and return a .json of the prediction 

To run the application on local

- python .\inference_app.py # start the local app

- python .\test_api.py # test the local app from local

To run the application on docker

- docker image build -t flask_docker .

- docker run -p 5000:5000  -d flask_docker

- curl.exe -H 'Content-Type: application/json' -d "@../input.json"  http://localhost:5000/inference # send json to application on docker to get the sentiment  prediction


## 03-to-eb

This folder contains the files required for deploying the model on AWS Elastic Beanstalk.

![aws1](https://user-images.githubusercontent.com/69254427/180447732-a27708d3-4cbd-472d-b5c0-d29479cb3701.jpg)










2.) Local Test

Run docker_api_test/inference_app.py

Run test_api.py

3.) Docker Test

docker image build -t flask_docker .

docker run -p 5000:5000 -d flask_docker

Then From local computer

curl.exe -H 'Content-Type: application/json' -d "@../input.json"  http://localhost:5000/inference

4.) AWS Elastic Beanstalk

Upload to-eb.zip

* succeeded with test code for POST and GET json
curl.exe -H 'Content-Type: application/json' -d "@ex_input.json"  http://sentimentanalysisapp-env.eba-gfiqdn9i.us-west-2.elasticbeanstalk.com/get_json

** but got error when pip installing requirements for the real sentiment analysis inference

2022/07/19 16:25:53.484392 [ERROR] An error occurred during execution of command [app-deploy] - [InstallDependency]. Stop running the command. Error: fail to install dependencies with requirements.txt file with error Command /bin/sh -c /var/app/venv/staging-LQM1lest/bin/pip install -r requirements.txt failed with error exit status 2. Stderr:ERROR: Exception:

LOG FILE
https://elasticbeanstalk-us-east-2-128408982530.s3.us-east-2.amazonaws.com/resources/environments/logs/tail/e-skpbh9thdf/i-015fa8c2e68eb99ae/TailLogs-1658248235920.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220719T163037Z&X-Amz-SignedHeaders=host&X-Amz-Expires=86400&X-Amz-Credential=AKIAIKOSE77CLMRUGX3Q%2F20220719%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=a2dd06921b7fbdd05f03612a03ebe7ea9afbd15c596cfd62aa5557afbc65e0e4
