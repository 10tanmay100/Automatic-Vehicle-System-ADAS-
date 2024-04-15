#importing the library
import os
from box.exceptions import BoxValueError
import yaml
from adas.logger import logging
import json
import sys
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
import pandas as pd
from typing import Any
from adas.exception import AdasException
# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import json
from importlib import import_module

#defining the read yaml function
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        logging.error("Error while reading yaml file")
        raise AdasException(e,sys) from e
    

@ensure_annotations
def create_directories(paths: list, verbose=True):
    try:
        base_paths = set()
        for path in paths:
            path = Path(path)
            base_path = path.parent
            if base_path not in base_paths:
                os.makedirs(base_path, exist_ok=True)
                base_paths.add(base_path)
            os.makedirs(path, exist_ok=True)
            if verbose:
                logging.info(f"Created directory at: {path}")
    except Exception as e:
        logging.error(f"Error while creating directory at:{paths}")
        raise AdasException(e,sys) from e

@ensure_annotations   
def read_data(file_path)->pd.DataFrame:
    try:
        df=pd.read_csv(file_path)
        logging.info(f"Reading file:{file_path}")
        return df
    except Exception as e:
        logging.error("Error while reading file")
        raise AdasException(e,sys) from e


@ensure_annotations
def write_yaml_file(file_path:str,content:object,replace:bool)->None:
    try:
        if replace:
            logging.info(f"Checking the existence of {file_path}")
            if os.path.exists(file_path):
                logging.info(f"Removing... {file_path}")
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        logging.info(f"Making the directory: {file_path}")
        with open(file_path,"w") as f:
            yaml.dump(content,f)
            logging.info("Dumping content yaml file",f)
    except Exception as e:
        logging.error(f"Error while writing content of yaml file, error is {e}")
        raise AdasException(e,sys) from e



@ensure_annotations
def load_config(file_path:Path):
    try:
        logging.info("Loading configuration code")
        with open(file_path) as file:
            return json.load(file)
    except Exception as e:
        logging.error("Error loading configuration",e)
        raise AdasException(e,sys) from e
