#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import joblib
warnings.filterwarnings('ignore')
from Input_Script import FeatureExtraction


gbc = joblib.load(r"C:\Users\RAMYASRI\Downloads\Phishing-URL-Detection-master\Phishing-URL-Detection-master\Model\Xgboost.joblib")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Handle the POST request
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('result.html', xx =round(y_pro_non_phishing,2),url=url )
    # Handle the GET request
    return render_template("result.html", xx =-1)


if __name__ == "__main__":
    app.run(debug=True)