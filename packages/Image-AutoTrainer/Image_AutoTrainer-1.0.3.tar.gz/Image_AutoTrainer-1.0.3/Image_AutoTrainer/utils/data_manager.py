import tensorflow as tf
from Image_AutoTrainer.utils.config import configureData
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from Image_AutoTrainer.utils.info.logger import logging
from Image_AutoTrainer.utils.info.exception import CustomException
from keras.applications.resnet import preprocess_input
import numpy as np

import warnings
warnings.filterwarnings("ignore")



conf_data = configureData()

def train_valid_datagen():

    dataflow_kwargs = dict(
    class_mode  = "categorical",
    batch_size  = conf_data["BATCH_SIZE"],
    target_size = conf_data["IMAGE_SIZE"][:-1],
    interpolation = "nearest"
    )

    datagen_kwargs = dict(
        rescale = 1./255.0,
        validation_split=0.2
    )
    
    valid_datagen = ImageDataGenerator(**datagen_kwargs)

    valid_data = valid_datagen.flow_from_directory(
        directory = conf_data["VALID_DATA_DIR"],
        subset = "validation",
        shuffle = True,
        **dataflow_kwargs 
    )

    if conf_data["AGUMENTATION"]==True:
        train_datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=40, 
            width_shift_range=0.2, 
            height_shift_range=0.2, 
            shear_range=0.2, 
            zoom_range=0.2, 
            fill_mode="nearest", 
            horizontal_flip=True, 
            vertical_flip=True
        )
    else: 
        train_datagen = valid_datagen

    train_data = train_datagen.flow_from_directory(
        directory = conf_data["TRAIN_DATA_DIR"],
        subset = "training",
        shuffle = True,
        **dataflow_kwargs 
    )

    return train_data, valid_data

def get_classes():
    train_set, valid_set = train_valid_datagen()

    return train_set.class_indices 


def evaluate_model(model):
    logging.info("Evaluating Model...")
    print("\nEvaluating Model...\n")
    train_set, valid_set = train_valid_datagen()
    loss, accuracy = model.evaluate(valid_set)
    print(f"Loss: {loss}\nAccuracy : {accuracy}")


def manage_input_data(input_image):
    """ Converting to input array inot desired dimensions
    Args :
        input_image (nd array): image nd array

    returns :
        ndarray : resized and updated dimension image
    """

    image = input_image
    size = conf_data["IMAGE_SIZE"][:-1]
    resized_input_img = tf.image.resize(image,size)
    # img_array = tf.keras.preprocessing.image.img_to_array(image.numpy())
    img = np.expand_dims(resized_input_img,axis=0)
    
    return img