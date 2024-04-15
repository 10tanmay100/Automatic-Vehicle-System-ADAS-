from adas.entity import DataIngestionConfig
import boto3
import sys
from datetime import datetime
import os
import zipfile
import pandas as pd
from adas.exception import AdasException
import botocore
from adas.constants import *
from adas.utils import read_yaml,read_data
from adas.logger import logging

class DataValidation():
    def __init__(self,ingest_config:DataIngestionConfig):
        self.ingest_config = ingest_config
        self.__schema_sensor_config = read_yaml(SCHEMA_SENSOR_PATH)
        self.__schema_label_config = read_yaml(SCHEMA_LABEL_PATH)

    def validate_sensor__number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            logging.info("Number of columns validation started!!!")
            # for csvs in dataframes_folder:
            #      print(csvs)
            number_of_columns=len(self.__schema_sensor_config["columns"])
            if len(dataframe.columns)==number_of_columns:
                    logging.info(f"data frame columns and number of columns checking passed...->> {len(dataframe.columns)==number_of_columns}")
                    logging.info("Number of columns validation ended!!!")
                    return True
            else:
                    logging.info(f"data frame columns and number of columns checking failed...->> {len(dataframe.columns)==number_of_columns}")
                    logging.info("Number of columns validation ended!!!")
                    return False
        except Exception as e:
            logging.error("validate number of columns check has some issue..")
            raise AdasException(e,sys) from e
        
    def validate_label__number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            logging.info("Number of columns validation started!!!")
            # for csvs in dataframes_folder:
            #      print(csvs)
            number_of_columns=len(self.__schema_label_config["columns"])
            print(len(dataframe.columns))
            print(number_of_columns)
            if len(dataframe.columns)==number_of_columns:
                    logging.info(f"data frame columns and number of columns checking passed...->> {len(dataframe.columns)==number_of_columns}")
                    logging.info("Number of columns validation ended!!!")
                    return True
            else:
                    logging.info(f"data frame columns and number of columns checking failed...->> {len(dataframe.columns)==number_of_columns}")
                    logging.info("Number of columns validation ended!!!")
                    return False
        except Exception as e:
            logging.error("validate number of columns check has some issue..")
            raise AdasException(e,sys) from e
        
    def apply_validation(self):
        bool_list=[]
        for csv_folder in os.listdir(self.ingest_config.local_data_folder):
            path_=os.path.join(self.ingest_config.local_data_folder,csv_folder)
            for sub_folder in os.listdir(path_):
                if "dataset_labels.csv"==sub_folder:
                    dataframe=read_data(os.path.join(path_,sub_folder))
                    if self.validate_label__number_of_columns(dataframe):
                         bool_list.append(True)
                else:
                    print(os.path.join(path_,sub_folder))
                    dataframe=read_data(Path(os.path.join(path_,sub_folder)))
                    if self.validate_sensor__number_of_columns(dataframe):
                         bool_list.append(True)
                print (bool_list)
        if bool_list.count(True)==27:
             print(bool_list)
             return True
        return False



                