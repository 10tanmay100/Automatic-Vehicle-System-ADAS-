from scipy.stats import ks_2samp
import shutil
import zipfile
import os
import pandas as pd
from adas.exception import AdasException
import botocore
from pathlib import Path
import joblib
from adas.entity import *
from adas.constants import *
from adas.utils import read_yaml,read_data
from adas.logger import logging
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from adas.logger import logging

class DataTransformation:
    def __init__(self,ingest_config:DataIngestionConfig,transform_config:DataTransformationConfig):
        self.config=transform_config
        self.ingest_config = ingest_config
        self.scaler=StandardScaler()

    def __train_test_split_(self):
        lists_left=[]
        lists_right=[]
        lists_labels=[]
        for csv_folder in os.listdir(r"F:\Ineuron\Deep Learning\Road_Type_Classification(ADAS)\artifacts\data_ingestion\04-10-2024-14-52-35-52S"):
            path_=os.path.join(r"F:\Ineuron\Deep Learning\Road_Type_Classification(ADAS)\artifacts\data_ingestion\04-10-2024-14-52-35-52S",csv_folder)
            for sub_folder in os.listdir(path_):
                dataframe=pd.read_csv(os.path.join(path_,sub_folder))
                if csv_folder in ["pvs1","pvs3","pvs4","pvs5","pvs6","pvs9"]:
                    if sub_folder == "dataset_gps_mpu_left.csv":
                        columns_updated=[i+"_left" for i in dataframe.columns]
                        dataframe.columns=columns_updated
                        lists_left.append(dataframe)
                    elif sub_folder == "dataset_gps_mpu_right.csv":
                        columns_updated=[i+"_right" for i in dataframe.columns]
                        dataframe.columns=columns_updated
                        lists_right.append(dataframe)
                    elif sub_folder == "dataset_labels_1.csv":
                        lists_labels.append(dataframe)
        if len(lists_left)>0:
            concat_df_left=pd.concat(lists_left)
        #     concat_df_left.to_csv(f"_left.csv",index=False)
        if len(lists_right)>0:
            concat_df_right=pd.concat(lists_right)
        #     concat_df_right.to_csv(f"_right.csv",index=False)
        if len(lists_labels)>0:
            concat_df_lables=pd.concat(lists_labels)
        #     concat_df_lables.to_csv(f"_labels.csv",index=False)
        df=pd.merge(left=concat_df_left,right=concat_df_right,left_on="timestamp_left",right_on="timestamp_right")
        df=df.drop(["timestamp_left","timestamp_right"],axis=1)
        df=df.reset_index(drop=True)
        concat_df_lables=concat_df_lables.reset_index(drop=True)
        concatted_final=pd.concat([df,concat_df_lables],axis=1)
        X_train,y_train=concatted_final.drop(["Combined Labels"],axis=1),concatted_final["Combined Labels"]

        lists_left=[]
        lists_right=[]
        lists_labels=[]
        for csv_folder in os.listdir(r"F:\Ineuron\Deep Learning\Road_Type_Classification(ADAS)\artifacts\data_ingestion\04-10-2024-14-52-35-52S"):
            path_=os.path.join(r"F:\Ineuron\Deep Learning\Road_Type_Classification(ADAS)\artifacts\data_ingestion\04-10-2024-14-52-35-52S",csv_folder)
            for sub_folder in os.listdir(path_):
                dataframe=pd.read_csv(os.path.join(path_,sub_folder))
                if csv_folder in ["pvs2","pvs7","pvs8"]:
                    if sub_folder == "dataset_gps_mpu_left.csv":
                        columns_updated=[i+"_left" for i in dataframe.columns]
                        dataframe.columns=columns_updated
                        lists_left.append(dataframe)
                    elif sub_folder == "dataset_gps_mpu_right.csv":
                        columns_updated=[i+"_right" for i in dataframe.columns]
                        dataframe.columns=columns_updated
                        lists_right.append(dataframe)
                    elif sub_folder == "dataset_labels_1.csv":
                        lists_labels.append(dataframe)
        if len(lists_left)>0:
            concat_df_left=pd.concat(lists_left)
        #     concat_df_left.to_csv(f"_left.csv",index=False)
        if len(lists_right)>0:
            concat_df_right=pd.concat(lists_right)
        #     concat_df_right.to_csv(f"_right.csv",index=False)
        if len(lists_labels)>0:
            concat_df_lables=pd.concat(lists_labels)
        #     concat_df_lables.to_csv(f"_labels.csv",index=False)
        df=pd.merge(left=concat_df_left,right=concat_df_right,left_on="timestamp_left",right_on="timestamp_right")
        df=df.drop(["timestamp_left","timestamp_right"],axis=1)
        df=df.reset_index(drop=True)
        concat_df_lables=concat_df_lables.reset_index(drop=True)
        concatted_final=pd.concat([df,concat_df_lables],axis=1)
        X_test,y_test=concatted_final.drop(["Combined Labels"],axis=1),concatted_final["Combined Labels"]
        # concatted_final.to_csv(f"pvs_134569.csv",index=False)
        return X_train,X_test,y_train,y_test
                
    

    def __scale_data(self,X_train,X_test,y_train,y_test):
        X_train,X_test,y_train,y_test=self.__train_test_split_()
        logging.info("Splitting data into scaling function")
        y_train=y_train.reset_index(drop=True)
        logging.info("Resetting y train")
        y_test=y_test.reset_index(drop=True)
        logging.info("Resetting y test")
        scaled_train_path=os.path.join(self.config.transfromed_train_path,"train.csv")
        scaled_test_path=os.path.join(self.config.transfromed_test_path,"test.csv")

        X_train_scaled=pd.concat([pd.DataFrame(self.scaler.fit_transform(X_train),columns=X_train.columns),y_train],axis=1).to_csv(scaled_train_path,index=False)
        logging.info(f"Training scaled csv ready and stored in {scaled_train_path}")
        X_test_scaled=pd.concat([pd.DataFrame(self.scaler.transform(X_test),columns=X_test.columns),y_test],axis=1).to_csv(scaled_test_path,index=False)
        logging.info("Testing scaled csv ready and stored in {scaled_test_path}")
        joblib.dump(self.scaler,os.path.join(self.config.scaler_model_path,"scaler.joblib"))
        logging.info(f"Dumping the scaler object to,{os.path.join(self.config.scaler_model_path,'scaler.joblib')}")

    def apply_transformation(self):
        X_train,X_test,y_train,y_test=self.__train_test_split_()
        self.__scale_data(X_train,X_test,y_train,y_test)
