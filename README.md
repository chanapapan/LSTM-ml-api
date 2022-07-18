# LSTM-ml-api

## Unittest (?) on our own computer

$env:FLASK_APP = "hello" # exporting the FLASK_APP environment variable

flask run

Then on another terminal

test_api.py



## Docker
docker image build -t flask_docker .

docker run -p 5000:5000 -d flask_docker # prediction_app.py automatically starts

Then From local computer

curl.exe --data-binary "{'var1' : 'var1'}" http://localhost:5000/get_json

error : Content-Type not supported!
