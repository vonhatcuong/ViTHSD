import time
import subprocess
import sys 
import threading

VID_ID = sys.argv[1]
MODEL_TYPE = sys.argv[2]
DB_URI = sys.argv[3]

def start_zookeeper ():
    # Start ZooKeeper server
    zookeeper_cmd = "~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties &"
    subprocess.Popen(zookeeper_cmd, shell=True)
    time.sleep(10)
    subprocess.run("clear", shell=True)
    print("Running Zookeeper Server")

def start_kafka ():
# Start Kafka server
    kafka_cmd = "~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties &"
    subprocess.Popen(kafka_cmd, shell=True)
    time.sleep(10)
    subprocess.run("clear", shell=True)
    print("Running Kafka Server")

def youtube_consumer ():
    youtube_consumer_cmd = f"python3 consumer.py {MODEL_TYPE}_{VID_ID} {DB_URI} &"
    subprocess.Popen(youtube_consumer_cmd, shell=True)
    print("Running Consumer")

def youtube_producer ():
    youtube_producer_cmd = f"python3 producer.py {VID_ID} {MODEL_TYPE} &"
    subprocess.Popen(youtube_producer_cmd, shell=True)
    print("Running Producer")

def stream():
    consumer_thread = threading.Thread(target=youtube_consumer)
    producer_thread = threading.Thread(target=youtube_producer)
    
    consumer_thread.start()
    # time.sleep(5)
    producer_thread.start()

if __name__ == '__main__':
    start_zookeeper()
    time.sleep(10)
    start_kafka()
    time.sleep(10)
    stream()
