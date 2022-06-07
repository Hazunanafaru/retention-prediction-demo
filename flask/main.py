import os
import numpy as np
from crypt import methods
from dotenv import load_dotenv
from flask import Flask, request
from util import transform, load_model

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello Bambang {}!".format(name)

@app.route("/predict", methods = ["POST"])
def predict():
    # transofrm data
    predict_data = transform(request.get_json())

    # load model and standard_scaler
    model, sc = load_model()

    # do the prediction
    result = model.predict(sc.transform(np.array([predict_data])))
    model_pred = {"left": bool(result > 0.5)}
    
    return model_pred

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))