from adas.utils import *
from adas.entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig
import boto3
from sklearn.ensemble import RandomForestClassifier
import sys
import joblib
from datetime import datetime
import os
import shutil
from sklearn.model_selection import train_test_split,GridSearchCV
import zipfile
import numpy as np
import pandas as pd
from adas.exception import AdasException
from adas.constants import *
from adas.logger import logging
from sklearn.metrics import precision_score,recall_score,f1_score
from mlflow.models.signature import ModelSignature, infer_signature
from sklearn.svm import SVC
import mlflow
import warnings
warnings.filterwarnings("ignore")


class ModelTrainer:
    def __init__(self,ingest_config:DataIngestionConfig,transform_config:DataTransformationConfig,config:ModelTrainerConfig):
        self.config = config
        self.ingest_config = ingest_config
        self.transform_config = transform_config
        self.__params = read_yaml(Path(PARAMS_FILE_PATH))



    def train(self):
        try:
            mlflow.set_tracking_uri(uri=TRACKING_URI)
            now = datetime.now()
            # #generating the folder based on the current datetime
            # date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            # print("The set tracking uri is ", mlflow.get_tracking_uri())
            # exp_id = mlflow.create_experiment(
            #     name="create_exp_artifact"+date_time,
            #     tags={"version": "v1", "priority": "p1"}
            # )
            # get_exp = mlflow.get_experiment(exp_id)

            train_path=Path(os.path.join(self.transform_config.transfromed_train_path,"train.csv"))
            X_tr=read_data(train_path)

            test_path=Path(os.path.join(self.transform_config.transfromed_test_path,"test.csv"))
            X_ts=read_data(test_path)

            X_train=X_tr.drop(["Combined Labels"],axis=1)

            X_test=X_ts.drop(["Combined Labels"],axis=1)

            y_train=X_tr["Combined Labels"]
            m={i:int(idx) for idx,i in enumerate(X_tr["Combined Labels"].unique())}
  
            y_train=y_train.map(m)

            y_test=X_ts["Combined Labels"]
            print("before test",y_test)
            s
            y_test=y_test.map(m)


            exp_id="891896892431559114"
            with mlflow.start_run(experiment_id=exp_id):
                        mlflow.log_artifacts(train_path)
                        mlflow.log_artifacts(test_path)

                        clf = RandomForestClassifier(max_depth=self.__params['max_depth'],class_weight='balanced')
                        clf.fit(X_train, y_train)
                        logging.info("Fitting on the data")

                        predictions = clf.predict(X_test)
                        logging.info("Predicting..")
                        precision=precision_score(y_test,predictions,average="weighted")
                        recall=recall_score(y_test,predictions,average="weighted")
                        f1=f1_score(y_test,predictions,average="weighted")
                        print(precision,recall,f1)

                        mlflow.log_metric("Precision Score",precision)
                        mlflow.log_metric("Recall Score",recall)
                        mlflow.log_metric("F1 Score",f1)

                        mlflow.sklearn.log_model(clf, "model_.h5")

            model_path=os.path.join(self.config.root_dir,"model_"+".h5")

            logging.info(f"Dumping model {model_path}")
            joblib.dump(clf, model_path)
        except Exception as e:
            logging.error("Error while training",e)
            raise AdasException(e,sys) from e


        