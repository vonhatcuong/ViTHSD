import tensorflow as tf
import numpy as np

from transformers import AutoTokenizer, TFXLMRobertaModel

# Model
class TargetedHSD:
    def __init__(self, model = None):
        print("Model: ", model)
        match model:
            case "xlmr2":
                self.__model = './model/bigrulstmcnn_xlmr2.h5'
                self.__tokenizer = 'xlm-roberta-base'  
            case 'visobert':
                self.__model = './model/bigrulstmcnn_visobert.h5'
                self.__tokenizer = 'uitnlp/visobert'
        self._tokenizer = AutoTokenizer.from_pretrained(self.__tokenizer)
        self._model = tf.keras.models.load_model(self.__model, custom_objects={'TFXLMRobertaModel': TFXLMRobertaModel})
        self.result = None
        self.orginal_label = None


    def predict(self, text):
        encoded_text = np.array(self._tokenizer([text], max_length=100, padding='max_length', truncation=True)['input_ids'])
        encoded_text = {
            "input_ids": np.asarray(self._tokenizer([text], max_length=50, padding='max_length', truncation=True)['input_ids']),
            "attention_mask": np.asarray(self._tokenizer([text], max_length=50, padding='max_length', truncation=True)['attention_mask'])
        }
        pred = self._model.predict(encoded_text)
        pred = np.argmax(pred.reshape(-1, 5, 4), axis=-1)
        self.orginal_label = pred[0]
    
    def return_label(self):
        true_labels = []
        TYPE = {
            1: "clean",
            2: "offensive",
            3: "hate"
        }
        LABEL = {
            0: "individual",
            1: "groups",
            2: "religion",
            3: "race",
            4: "politics"
        }

        for i in range(0, len(self.orginal_label)):
            if self.orginal_label[i] > 0:
                t = LABEL[i] + "#" + TYPE[int(self.orginal_label[i])]
                true_labels.append(t)

        self.result = true_labels
        return true_labels 
