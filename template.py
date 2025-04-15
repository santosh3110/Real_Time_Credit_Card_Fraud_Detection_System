import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "fraud_detection"

list_of_files = [
    f"{project_name}/__init__.py",
    
    # 🔹 COMPONENTS (Pipeline stages)
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/stage_00_data_ingestion.py",
    f"{project_name}/components/stage_01_data_validation.py",
    f"{project_name}/components/stage_02_feature_engineering.py",
    f"{project_name}/components/stage_03_model_training.py",
    f"{project_name}/components/stage_04_evaluation.py",

    # 🔹 CONFIGURATION
    f"{project_name}/config/__init__.py",
    f"{project_name}/config/configuration.py",

    # 🔹 CONSTANTS
    f"{project_name}/constant/__init__.py",
    f"{project_name}/constant/project_constants.py",

    # 🔹 ENTITY CLASSES
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",

    # 🔹 EXCEPTION HANDLING
    f"{project_name}/exception/__init__.py",
    f"{project_name}/exception/exception_handler.py",

    # 🔹 LOGGING
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/log.py",

    # 🔹 PIPELINE ORCHESTRATION
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/streaming_pipeline.py",

    # 🔹 UTILITIES
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/util.py",
    f"{project_name}/utils/alerting.py",

    # 🔹 DATA GENERATION (faker-based streaming)
    f"{project_name}/data_generator/__init__.py",
    f"{project_name}/data_generator/producer.py",
    f"{project_name}/data_generator/schema.py",

    # 🔹 KAFKA CONSUMER FOR REAL-TIME
    f"{project_name}/streaming/__init__.py",
    f"{project_name}/streaming/consumer.py",
    
    # 🔹 CONFIGURATION FILES
    "config/config.yaml",
    "config/kafka_config.yaml",

    # 🔹 DOCKER + ENTRY POINT
    ".dockerignore",
    "Dockerfile",
    "app.py",                # main script for starting system
    "setup.py",              # for pip install -e .

    # 🔹 FOR LOGGING, MODELS, DATA STORAGE
    "logs/.gitkeep",
    "saved_models/.gitkeep",
    "artifacts/.gitkeep",
    "data/.gitkeep",
    "research/.gitkeep",
    "README.md"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filename}")
    else:
        logging.info(f"{filename} is already created")
