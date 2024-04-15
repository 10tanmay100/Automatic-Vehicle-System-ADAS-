#imporing libraries
from dataclasses import dataclass
from pathlib import Path

#defining the dataingestion configuration data types
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir:Path
    S3_bucket_name:str
    local_data_folder:Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir:Path
    transfromed_train_path:Path
    transfromed_test_path:Path
    scaler_model_path:Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir:Path