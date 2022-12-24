# Group Project: Movie Recommendations

### Introduction 
In this project,
we use SVD, KNN and Collaborative filtering algorithms here.
we use the flask framework to do the recommendation server part. Each time the server calls the recommendation model's API, then return the user's movie ranking in 
* `http://128.2.205.109:8082/recommend/<userid>`

### Note: Please make sure you execute the following steps in Bash

### Start the recommendation service and model

* git clone https://github.com/cmu-seai/group-project-f22-mavericks
   
* Model:
   1. `cd recommendation_model`
   2. `python model_trials.py`  
Here we use pickle to store the model parameters

* service:
   1. `cd group-project-f22-mavericks`
   2. `python -m venv env`
   3. `source /env/bin/activate`
   4. `pip install -r requirements.txt`
   5. `cd recommendation-service`
   6. `python run.py (make sure the port 8082 is not occupied.)`

* containerization serivce:
   1. `cd group-project-f22-mavericks`
   2. `cd recommendation-service`
   3. `docker-compose up`
   4. `python3 load_balance.py`
   5. Run this on your browser `http://192.168.0.228:8082/<userid>`
