from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionArtifact:
    file_path_leftsensor:Path 
    file_path_rightsensor:Path 
    file_path_label:Path 

@dataclass
class DataValidationArtifact:
    validation_status:bool
