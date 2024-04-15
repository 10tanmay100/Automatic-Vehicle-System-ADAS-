#importing library
from pathlib import Path


#defining the configuration yaml file path
CONFIG_FILE_PATH= Path("configs/config.yaml")
SCHEMA_SENSOR_PATH= Path("configs/schema_sensor.yaml")
SCHEMA_LABEL_PATH= Path("configs/schema_label.yaml")
PARAMS_FILE_PATH=Path ("configs/params.yaml")

TRACKING_URI="http://13.127.83.195:5000/"


BUCKET_NAME:str="adas-project-bucket-kaggle"
AWS_ACCESS_KEY_ID:str="AKIA2UC27SR2ZQDBQLM5"
AWS_SECRET_KEY_ID:str="XbHvl5b8Sdnao4fQ+5538UWwy0cFkJoYapTOwrar"