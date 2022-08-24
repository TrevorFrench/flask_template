from flask import Flask, render_template, request, Response
import pandas as pd
from convertors import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('upload.html')   
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
    df = pd.read_csv(request.files.get('file'))
    df = bittrex_order(df)
    return Response(
        df.to_csv(index = False),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=df.csv"})

if __name__ == '__main__':
   app.run(debug = True)