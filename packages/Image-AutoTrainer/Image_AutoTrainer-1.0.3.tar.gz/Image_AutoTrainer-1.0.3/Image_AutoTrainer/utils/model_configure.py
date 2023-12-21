import tensorflow as tf
import os
import sys
import json
from Image_AutoTrainer.utils.config import configureData, configureModel
from Image_AutoTrainer.utils.info.exception import CustomException
from Image_AutoTrainer.utils.info.logger import logging
from tensorflow.keras.applications import Xception, VGG16, VGG19, ResNet50, ResNet101, ResNet152, ResNet50V2, ResNet101V2
from tensorflow.keras.applications import ResNet152V2, InceptionV3, MobileNet, MobileNetV2, DenseNet121, DenseNet169
from tensorflow.keras.applications import DenseNet201, NASNetMobile, EfficientNetB0, EfficientNetB1, EfficientNetB2

conf_model = configureModel()

conf_data = configureData()


def get_model(model_name=conf_model["MODEL_NAME"], input_shape=conf_data["IMAGE_SIZE"]):
    
    name = model_name.lower()

    try : 
        if name == "Xception".lower():
            logging.info(f"Loading {name}..")

            model = Xception(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model pretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")
            
        elif name == "VGG16".lower():

            logging.info(f"Loading {name}..")

            model = VGG16(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")


        elif name == "VGG19".lower():

            logging.info(f"Loading {name}..")

            model = VGG19(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")


        elif name == "ResNet50".lower():
            
            logging.info(f"Loading {name}..")

            model = ResNet50(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")


        elif name == "ResNet101".lower():
            
            logging.info(f"Loading {name}..")

            model = ResNet101(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")



        elif name == "ResNet50V2".lower().lower():
            
            logging.info(f"Loading {name}..")

            model = ResNet50V2(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "ResNet101V2".lower():
            
            logging.info(f"Loading {name}..")

            model = ResNet101V2(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "ResNet152V2".lower():

            logging.info(f"Loading {name}..")

            model = ResNet152V2(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "InceptionV3".lower():

            logging.info(f"Loading {name}..")

            model = InceptionV3(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "MobileNet".lower():
            
            logging.info(f"Loading {name}..")

            model = MobileNet(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "MobileNetV2".lower():

            logging.info(f"Loading {name}..")

            model = MobileNetV2(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "DenseNet121":

            logging.info(f"Loading {name}..")

            model = DenseNet121(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "DenseNet169".lower():

            logging.info(f"Loading {name}..")

            model = DenseNet169(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "DenseNet201".lower():

            logging.info(f"Loading {name}..")

            model = DenseNet201(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "NASNetMobile".lower():

            logging.info(f"Loading {name}..")

            model = NASNetMobile(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "EfficientNetB0".lower():

            logging.info(f"Loading {name}..")

            model = EfficientNetB0(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")
        
        elif name == "EfficientNetB1".lower():

            logging.info(f"Loading {name}..")

            model = EfficientNetB1(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

        elif name == "EfficientNetB2".lower():

            logging.info(f"Loading {name}..")

            model = EfficientNetB2(include_top=False,  weights="imagenet", input_shape=input_shape)
            print(f"\npretrainde_model {name} loading Done...")
            logging.info(f"pretrainde_model {name} loading Done...")

    except Exception as e:
        logging.info(f"Model {name} not available")
        raise CustomException(e,sys)
    

    return model
