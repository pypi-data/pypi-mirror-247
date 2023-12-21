from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from Image_AutoTrainer.decoder.utils import decodeImage
from Image_AutoTrainer.predict_engine import PredictClassifier
from threading import Timer
import webbrowser
import json
import os

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


class ClientApp():
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictClassifier(self.filename)



@app.route('/', methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route('/input',methods=['GET']) # route to display the home page
def form():
    return render_template('form.html')


@app.route('/Train', methods=['POST','GET']) # route to display the home page
def Model_Train():
    if request.method == "POST":
        try:
            # configure data
            TRAIN_DATA_DIR = request.form["TRAIN_DATA_DIR"]
            VALID_DATA_DIR = request.form["VALID_DATA_DIR"]

            IMG_HT = int(request.form["IMG_HT"])
            IMG_WT = int(request.form["IMG_WT"])
            CH = int(request.form["CH"])
            IMAGE_SIZE = IMG_HT, IMG_WT, CH

            BATCH_SIZE = int(request.form["BATCH_SIZE"])
            AGUMENTATION = bool(request.form["AGUMENTATION"].title())

            # Configure Model
            MODEL_NAME = request.form["MODEL_NAME"]
            EPOCHS = int((request.form["EPOCHS"]))
            CLASSES = int(request.form["CLASSES"])
            FREEZE_ALL = bool(request.form["FREEZE_ALL"].title())
        
            FREEZE_TILL = int(request.form["FREEZE_TILL"])
            OPTIMIZER = request.form["OPTIMIZER"]
            LOSS_FUNC = request.form["LOSS_FUNC"]


            config_file = {
                "TRAIN_DATA_DIR": TRAIN_DATA_DIR,
                "VALID_DATA_DIR": VALID_DATA_DIR,
                "IMAGE_SIZE": IMAGE_SIZE,
                "BATCH_SIZE": BATCH_SIZE,
                "AGUMENTATION": AGUMENTATION,
                "MODEL_NAME": MODEL_NAME,
                "EPOCHS": EPOCHS,
                "CLASSES": CLASSES,
                "FREEZE_ALL": FREEZE_ALL,
                "FREEZE_TILL": FREEZE_TILL,
                "OPTIMIZER": OPTIMIZER,
                "LOSS_FUNC": LOSS_FUNC,
            }

            with open('config.json', 'w') as f:
                json.dump(config_file, f)

            import train_engine
            from utils import data_manager as dm

            model = train_engine.train()
            result = dm.evaluate_model(model)
            print(result)
            

            return render_template('form.html', output=model)

        except Exception as e:
            print("Something went wrong:", str(e))
            return 'something went wrong'


        return render_template('form.html', output = model)

    else:
        return render_template('index.html')

@app.route('/test',methods=['GET','POST'])  # route to display the home page
@cross_origin()
def predcit():
    return render_template("predict.html")

@app.route('/predict',methods=['POST'])  # route to display the home page
@cross_origin()
def PredictRoute():
    clApp = ClientApp()
    image = request.json['image']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.predictor()
    return jsonify(result)



def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')


def start_app():
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=8080,debug=True)


if __name__ == "__main__":
    start_app()