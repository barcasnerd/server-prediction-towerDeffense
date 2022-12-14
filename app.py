import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from flask import Flask, render_template, request, jsonify
import os


app = Flask(__name__)



def prediccionesDelModelo(predictionInput):
    ## cargando el modelo creado
    model = load('model.joblib')        
    prediction = pd.DataFrame(np.array([predictionInput]), columns=['pos_xiTorre1','pos_xiTorre2','pos_xiTorre3','pos_xiTorre4','pos_xiTorre5','pos_xiTorre6','pos_xiTorre7','pos_yiTorre1','pos_yiTorre2','pos_yiTorre3','pos_yiTorre4','pos_yiTorre5','pos_yiTorre6','pos_yiTorre7','TipoTorre1','TipoTorre2','TipoTorre3','TipoTorre4','TipoTorre5','TipoTorre6','TipoTorre7'])    
    prediction = prediction.fillna(-1)
    return model.predict(prediction)



@app.route('/predecir/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /getmsg/?name=
    input = request.args.get("input", None)

    input = input.split(',')
    y = np.array(input)
    y = y.astype(np.float)

    a =prediccionesDelModelo(y)    
    a = a.tolist()[0]
    a = [int(eval(i)) for i in a]
    b = ",".join([str(i) for i in a])
    response = {}

    # Check if the user sent a name at all
    if not input:
        response["ERROR"] = "No input found. Please send an input."
    # Check if the user entered a number
    elif str(input).isdigit():        
        response["ERROR"] = "The name can't be numeric. Please send a string."   
    else:
        response["prediction"] = f"{b}"
        return jsonify({
            "prediction": b
        })        

    # Return the response in json format
    return jsonify(response)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))    
    app.run(host='0.0.0.0',port=port, debug=True)    