'''
@author: Yash Dhakade
Email: yinsights8@gmail.com
Date: 13-DEC-2023
'''



import os
import sys
import time
from Image_AutoTrainer.utils import config 
from Image_AutoTrainer.utils.config import  configureModel, configureData
from Image_AutoTrainer.utils import callbacks  as cb
from Image_AutoTrainer.utils import model
from Image_AutoTrainer.utils.info.exception import CustomException
from Image_AutoTrainer.utils.info.logger import logging 
from Image_AutoTrainer.utils import data_manager as dm

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)



conf_model = configureModel()
# conf_data = configureData()


# get the model from directory 
def get_unique_model_name(model_dir_name):
    model_file_name = time.strftime(f"{model_dir_name}_at%Y%m%d_%H%M%S.h5")
    model_file_path = os.path.join(config.TRAINED_MODEL_DIR, model_file_name)
    os.makedirs(config.TRAINED_MODEL_DIR, exist_ok=True)

    return model_file_path


def train():


    train_set, valid_set = dm.train_valid_datagen()
    # print(len(claass))

    # load the model and callbacks
    cbs = cb.callbacks()
    cmodel = model.custom_model()   

    # define steps per epoch
    steps_per_epoch = train_set.samples // train_set.batch_size
    validation_step = valid_set.samples // valid_set.batch_size

    logging.info("Training Started...")
    print("Training Started...")
    cmodel.fit(
        train_set,
        epochs = conf_model["EPOCHS"],
        validation_data = valid_set,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_step,
        callbacks=cbs
    )

    # save the trained Model to location
    model_file_path = get_unique_model_name(model_dir_name=conf_model["MODEL_NAME"])
    cmodel.save(model_file_path)
    print(f"model saved at following location :{model_file_path}")
    logging.info(f"Model successfully saved at following location :{model_file_path}")

    return cmodel