# Import the necessary modules
from fraud_detection.pipeline.training_pipeline import TrainingPipeline

def main():
    # Start training pipeline
    print("🚀 Starting Training Pipeline...")
    training_pipeline = TrainingPipeline()
    training_pipeline.start_training_pipeline()

if __name__ == "__main__":
    main()
