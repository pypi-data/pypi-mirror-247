import os
import json

with open('config.json','r') as f:
      params = json.load(f)

# configure data
TRAIN_DATA_DIR = params["TRAIN_DATA_DIR"]
VALID_DATA_DIR = params["VALID_DATA_DIR"]
# IMG_HT     = data["IMG_HT"]
# IMG_WT     = data["IMG_WT"]
# CH         = data["IMAGE_SIZE"]

# IMAGE_SIZE = IMG_HT, IMG_WT, CH
IMAGE_SIZE = params["IMAGE_SIZE"]

BATCH_SIZE     = params["BATCH_SIZE"]
AGUMENTATION   = params["AGUMENTATION"]

# Configure Model
MODEL_NAME     = params["MODEL_NAME"]
EPOCHS         = params["EPOCHS"]
CLASSES        = params["CLASSES"]
FREEZE_ALL     = params["FREEZE_ALL"]
FREEZE_TILL    = params["FREEZE_TILL"]
OPTIMIZER      = params["OPTIMIZER"]
LOSS_FUNC      = params["LOSS_FUNC"]




def configureData(
    TRAIN_DATA_DIR = TRAIN_DATA_DIR, VALID_DATA_DIR = VALID_DATA_DIR, AGUMENTATION = AGUMENTATION, 
    CLASSES = CLASSES, IMAGE_SIZE = IMAGE_SIZE, BATCH_SIZE = BATCH_SIZE
    ):
    CONFIG = {
        'TRAIN_DATA_DIR' : TRAIN_DATA_DIR,
        'VALID_DATA_DIR' : VALID_DATA_DIR,
        'AGUMENTATION': AGUMENTATION,
        'CLASSES' : CLASSES,
        'IMAGE_SIZE' : IMAGE_SIZE,
        'BATCH_SIZE' : BATCH_SIZE,
    }

    return CONFIG



def configureModel(
    MODEL_NAME=MODEL_NAME, EPOCHS = EPOCHS, OPTIMIZER=OPTIMIZER,LOSS_FUNC=LOSS_FUNC, 
    FREEZE_ALL=FREEZE_ALL,FREEZE_TILL=FREEZE_TILL
    ):
    CONFIG = {
        'MODEL_NAME' : MODEL_NAME,
        'EPOCHS' : EPOCHS,
        'FREEZE_ALL' : FREEZE_ALL,
        'FREEZE_TILL' : FREEZE_TILL,
        'OPTIMIZER': OPTIMIZER,
        'LOSS_FUNC' : LOSS_FUNC,

    }

    return CONFIG


TRAINED_MODEL_DIR = os.path.join(f"CheckPoints","models")


# calbacks dirs
# CHECKPOINT_DIR = os.path.join(f"{name}_model","checkpoint")
CHECKPOINT_DIR = os.path.join(f"CheckPoints","checkpoint")

BASE_LOG_DIR = "base_log_dir"
TENSORBOARD_ROOT_LOG_DIR = os.path.join(BASE_LOG_DIR,"tensorboard_log_dir")