from inspect import signature
import neptune.new as neptune

run = neptune.init_run(
    project="mavericks/recommendation",
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI0ZjZiYzJlZC03MDllLTQzY2QtYmNiNS1lZjI3ZjBkYTVkODUifQ=="
) 

params = {"learning_rate": 0.001, "optimizer": "Adam"}
run["parameters"] = params

# for epoch in range(10):
#     run["train/loss"].log(0.9 ** epoch)
#     run["train/acc"].log(1.01**epoch)
#     run["eval/loss"].log(0.98**epoch)
#     run["eval/acc"].log(1.02**epoch)

#run["eval/f1_score"] = 0.66
run["data_versions/train"].track_files("../recommendation_model/newrate_movie.csv")
run["data_sample"].upload('../recommendation_model/newrate_movie.csv')

#run["f1_score"] = 0.95


#Model Registry to store ML models and manage their lifecycle

#Registering a model
# model = neptune.init_model(
#     name="Prediction model",
#     key="MODTEST9", 
#     project="mavericks/recommendation",
#     api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI0ZjZiYzJlZC03MDllLTQzY2QtYmNiNS1lZjI3ZjBkYTVkODUifQ=="
# )

# Creating a model version trained on a set of hyperparameters
model_version_1 = neptune.init_model_version(
    model = "REC-MODTEST9",
    project= "mavericks/recommendation",
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI0ZjZiYzJlZC03MDllLTQzY2QtYmNiNS1lZjI3ZjBkYTVkODUifQ=="
)

# Upload the model binary
model_version_1["model/binary"].upload("../recommendation_model/finalized_modelA.pkl")

#Log model metadata
model_version_1["model/rmse"] = 1.173671
model_version_1["model/fit_time"] = 8.612353
model_version_1["model/test_time"] = 0.564454
#model_version_1["model/parameters"] = model_params
#model_version_1["model/environment"].upload("environment.yml")
model_version_1["model/data"].track_files('../recommendation_model/newrate_movie.csv')

#Log model signature
#model_version_1[model/signature].upload("model_signature.json")

#Set model stage
model_version_1.change_stage("staging") #possible values: none, staging, production and archive
#Associate model with current run
model_version_1["model/run"] = run["sys/id"].fetch()

model_version_1.stop()


model_version_2 = neptune.init_model_version(
    model = "REC-MODTEST9",
    project= "mavericks/recommendation",
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI0ZjZiYzJlZC03MDllLTQzY2QtYmNiNS1lZjI3ZjBkYTVkODUifQ=="
)

# Upload the model binary
model_version_2["model/binary"].upload("../recommendation_model/finalized_modelB.pkl")

#Log model metadata
model_version_2["model/rmse"] = 1.156432
model_version_2["model/fit_time"] = 8.1456782
model_version_2["model/test_time"] = 0.543453
model_version_2["model/data"].track_files('../recommendation_model/newrate_movie.csv')


#Set model stage
model_version_2.change_stage("staging") #possible values: none, staging, production and archive
#Associate model with current run
model_version_2["model/run"] = run["sys/id"].fetch()

model_version_2.stop()

run.stop()
