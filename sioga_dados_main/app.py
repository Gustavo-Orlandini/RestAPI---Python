from flask import Flask
import pandas as pd
from reliability.Fitters import Fit_Weibull_2P
from reliability.Distributions import Weibull_Distribution
import logging
from flask import Flask, request, jsonify
from reliability_functions_sioga import *

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()  
    data = pd.DataFrame.from_dict(data)
    weibul_reliability = calculate_weibull_params(data)
    return weibul_reliability