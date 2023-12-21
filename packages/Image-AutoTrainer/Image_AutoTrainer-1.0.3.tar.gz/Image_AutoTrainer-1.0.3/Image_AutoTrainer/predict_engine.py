import os
import tensorflow as tf
import Image_AutoTrainer.utils.config as config
import matplotlib.pyplot as plt
import numpy as np

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)



class PredictClassifier():
    def __init__(self, filename):

        self.filename = filename
        self.my_model = tf.keras.models.load_model(self.get_latest_model_path())

    
    # load the latest model form the directory
    def get_latest_model_path(self):
        availabel_models = os.listdir(config.TRAINED_MODEL_DIR)
        latest_model = sorted(availabel_models)[-1]
        self.latest_model_path = os.path.join(config.TRAINED_MODEL_DIR, latest_model)
        return self.latest_model_path


    def predictor(self):

        import Image_AutoTrainer.utils.config as config
        from Image_AutoTrainer.utils import data_manager as dm

        conf_data = config.configureData()
        conf_model = config.configureModel()

        img = tf.io.read_file(self.filename)
        img = tf.image.decode_jpeg(img)
        fit_img = dm.manage_input_data(img)
        result = self.my_model.predict(fit_img)

        objects_class = dm.get_classes()
        classes = {val : key for key, val in objects_class.items()}

        prediction = ""; confidence = ""

        if conf_data["CLASSES"] > 2:
            preds = np.argmax(result[0])
            prediction = classes[preds]
            confidence = round(100 * (np.max(result[0])),2)

        else:
            prediction = classes[int(result[0][0])]
            confidence = round(100 * (np.max(result[0])),2)


        return prediction, confidence
