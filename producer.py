import pytchat
import time
import sys 

from preprocessing import preprocess
from model import TargetedHSD
from kafkaHelper import initProducer, produceRecord

VID_ID = sys.argv[1]
MODEL_TYPE = sys.argv[2]

cls = TargetedHSD(model=MODEL_TYPE)

def predict (message):
    # Preprocess Data
    preprocessed_data = preprocess(message)

    #Predict
    cls.predict(preprocessed_data)

    return cls.return_label()

producer = initProducer()


# Streaming DataA
chat = pytchat.create(video_id=VID_ID)
if(chat.is_alive()):
    print("Livestream chat connected successfully")
    while chat.is_alive():
        for raw_data in chat.get().sync_items():
            start = time.time()
            predicted_data = predict(raw_data.message)
            end = time.time()
            predict_time = end-start
            data = {
                'timestamp': raw_data.timestamp,
                'datetime': raw_data.datetime,
                'userid': raw_data.id,
                'username': raw_data.author.name,
                'message': raw_data.message,
                'predict': predicted_data,
                'predict-time': predict_time,
            }
            produceRecord(data, producer, f"{MODEL_TYPE}_{VID_ID}")
