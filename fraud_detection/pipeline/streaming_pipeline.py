import subprocess
import time

def start_producer():
    print("🚀 Starting Kafka Producer...")
    subprocess.run(['python', '-m', 'fraud_detection.data_generator.producer'])

def start_consumer():
    print("📥 Starting Kafka Consumer...")
    subprocess.run(['python', '-m', 'fraud_detection.streaming.consumer'])

def start_alerting():
    print("📧 Starting Alert Monitoring...")
    subprocess.run(['python', '-m', 'fraud_detection.utils.alerting'])

def run_pipeline():
    # Start processes
    processes = []
    p1 = subprocess.Popen(['python', '-m', 'fraud_detection.data_generator.producer'])
    processes.append(p1)
    
    time.sleep(5)  # Give producer time to start
    
    p2 = subprocess.Popen(['python', '-m', 'fraud_detection.streaming.consumer'])
    processes.append(p2)
    
    time.sleep(5)  # Give consumer time to start
    
    p3 = subprocess.Popen(['python', '-m', 'fraud_detection.utils.alerting'])
    processes.append(p3)
    
    # Wait for all processes to complete
    for p in processes:
        p.wait()

if __name__ == "__main__":
    run_pipeline()
