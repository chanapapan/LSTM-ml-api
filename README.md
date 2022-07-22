# LSTM-ml-api

This repository contains the code for Sentiment Analysis on the WiseSight dataset using an LSTM model as well as for deploying this model on docker or AWS Elastic Beanstalk using FlaskAPI.

First, download the WiseSight dataset <code>train.txt</code> , <code>train_label.txt</code>, <code>test.txt</code> and <code>test_label.txt</code> from https://github.com/PyThaiNLP/wisesight-sentiment/tree/master/kaggle-competition into <code>01-train_model/data/</code>

## 01-train_model

This folder contains the files for training the model and saving the best model which will be used for the API.

- <code>1-sentiment-analysis-LSTM.ipynb</code> contains the code for the training, validation and testing the LSTM model. The vocabulary and the weights of the best model are saved.

- <code>2-inference.ipynb</code> import the model class from <code>model_and_utils.py</code> for prediction.

- <code>config.yml</code> contains the parameters used for model traning and inference


## 02-local_api_test

This folder contains the files required to run the flask application on local computer and on docker.

<code>inference_app.py</code> define inference route that takes .json file as input and return a .json of the prediction 

To run the application on local

- <code>python .\inference_app.py</code> # start the local app

- <code>python .\test_api.py</code> # test the local app from local

<img src="https://user-images.githubusercontent.com/69254427/180448051-a2a9266c-bafa-4b41-82cf-15c57eae4055.jpg" width="90%"></img> 

To run the application on docker

- <code>docker image build -t flask_docker .</code>

- <code>docker run -p 5000:5000  -d flask_docker</code>

- <code>curl.exe -H 'Content-Type: application/json' -d "@../input.json"  http://localhost:5000/inference</code> # send json to application on docker to get the sentiment  prediction

<img src="https://user-images.githubusercontent.com/69254427/180448028-29fa3643-c342-400c-8803-aa7322d5393d.jpg" width="90%"></img> 

## 03-to-eb

This folder contains the files required for deploying the model on AWS Elastic Beanstalk.

Steps

- Go to Elastic Beanstalk > "Creat new application" > set "Application Name"

![aws1](https://user-images.githubusercontent.com/69254427/180447732-a27708d3-4cbd-472d-b5c0-d29479cb3701.jpg)

- Select "Platform" as "Python" > "Application Code" > "Upload Your Code"

<img src="https://user-images.githubusercontent.com/69254427/180447984-ab3e4b33-aa47-46f4-9871-b1fcac004209.jpg" width="90%"></img> 

- Set "Scource Code" as "Local" > "Choose file" > Upload <code>to-elasticbean.zip</code> which must contain <code>application.py</code>, <code>requirements.txt</code>, <code>.ebextensions/python.config</code> and other files needed for prediction zipped into one .ZIP file

<img src="https://user-images.githubusercontent.com/69254427/180447995-44d3c401-2028-4797-b476-ac3a821c9abf.jpg" width="90%"></img> 

- Go to "Configure more options" > "Modify instances" > set "Root colume type" to "General Purpose (SSD)" > size to 10 GB

<img src="https://user-images.githubusercontent.com/69254427/180448003-800abc25-1d30-4bc4-a8ac-9fd3e12d39a0.jpg" width="90%"></img> 

- "EC2 instance types" > "t2.small"

<img src="https://user-images.githubusercontent.com/69254427/180448011-cb635bf1-e8ba-45bf-b64c-e6a424b0cf05.jpg" width="90%"></img> 

- Create Application & wait until done

<img src="https://user-images.githubusercontent.com/69254427/180448018-2094df2e-5c53-4787-ac29-63ff51ec0844.jpg" width="90%"></img> 

-  <code>curl.exe -H 'Content-Type: application/json' -d "@./input.json"  http://chanapasentimentanalysisapp-env-1.eba-ddggkdwc.us-west-2.elasticbeanstalk.com/inference</code>

<img src="https://user-images.githubusercontent.com/69254427/180448024-47a81a0c-9343-4b3e-87fd-532e39e1454c.jpg" width="90%"></img> 


 <code>OP_datasets</code> folder
