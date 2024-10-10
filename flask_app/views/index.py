from flask import render_template
from flask import Blueprint

index_module = Blueprint("index", __name__)

@index_module.route("/",methods=['GET'])
def index_get():
    return render_template('index.html')

