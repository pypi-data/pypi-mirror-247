import os
import tensorflow as tf
import numpy as np

from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.models import Model
from Image_AutoTrainer.utils.config import configureModel, configureData
from Image_AutoTrainer.utils import model_configure as mc
from Image_AutoTrainer.utils import data_manager as dm

import sys
from Image_AutoTrainer.utils.info.logger import logging
from Image_AutoTrainer.utils.info.exception import CustomException

import warnings
warnings.filterwarnings("ignore")

conf_model = configureModel()

conf_data = configureData()

def save_base_model(name, image_size):

    model = mc.get_model(name, image_size)
    model.save(f"original_{name}.h5")
    print(f"Base model {name} is saved !!\n\n")
    logging.info(f"Model {name} downloaded successfully")

def load_base_model(name, image_size):
    save_base_model(name, image_size)
    model_name = f"original_{name}.h5"
    model = tf.keras.models.load_model(model_name)
    print("Model loaded successfully !!!\n")
    model.summary()
    return model


def custom_model():

    my_model = load_base_model(conf_model["MODEL_NAME"], conf_data["IMAGE_SIZE"])

    # freeze all layers
    if conf_model["FREEZE_ALL"]:
        for layer in my_model.layers:
            layer.trainable = False
        print("\nFreezed all the layers...")
        
    
    # freeze all layers till the index
    elif (conf_model["FREEZE_TILL"] is not None) or (conf_model["FREEZE_TILL"] > 0):
        print(f"Freezing layers till {conf_model['FREEZE_TILL']}\n\n")
        for layer in my_model.layers[:conf_model["FREEZE_TILL"]]:
            layer.trainable = False     
        print(f"\nFreezed all the layers till {conf_model['FREEZE_TILL']}...")



    if conf_data["CLASSES"] > 2:
        print(f"\n\nnumber of classes is detected : {conf_data['CLASSES']}, applying softmax function")
        # define custom layers to the model
        flatten_in = Flatten()(my_model.output)
        prediction = Dense(units = conf_data["CLASSES"], activation='softmax')(flatten_in)
        full_model = Model(inputs = my_model.inputs, outputs = prediction)

    else: 
        # define custom layers to the model
        print(f"\n\nnumber of classes is detected : {conf_data['CLASSES']}, applying sigmoid function")
        flatten_in = Flatten()(my_model.output)
        prediction = Dense(units = conf_data["CLASSES"], activation='sigmoid')(flatten_in)
        full_model = Model(inputs = my_model.inputs, outputs = prediction)
    
    # print("Custom Model Summary:\n")
    # full_model.summary()

    full_model.compile(
        loss = conf_model["LOSS_FUNC"],
        optimizer = conf_model["OPTIMIZER"],
        metrics = ['accuracy']
    )

    return full_model




