import tensorflow as tf
from Image_AutoTrainer.utils import config
import time 
import os

conf_model = config.configureModel()


def callbacks(name=conf_model["MODEL_NAME"], base_dir="."):

    
    # Saving tensorboard logs into directory
    base_log_dir = config.TENSORBOARD_ROOT_LOG_DIR
    unique_logs = time.strftime("log_at_%Y%m%d_%H%M%S")
    tensorboard_cb_dir = os.path.join(base_log_dir, unique_logs)
    os.makedirs(tensorboard_cb_dir, exist_ok=True)

    tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir=tensorboard_cb_dir)

    # checkpoint callbacks
    checkpoint_file = os.path.join(config.CHECKPOINT_DIR, f"{name}_checkpoint.h5")
    os.makedirs(config.CHECKPOINT_DIR, exist_ok=True)

    checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_file,
        save_best_only=True
    )

    callback_list = [tensorboard_cb, checkpoint_cb]
    return callback_list