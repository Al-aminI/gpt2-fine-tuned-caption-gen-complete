from flask import Flask, render_template, session, url_for, Response, request, flash, redirect, jsonify
from transformers import pipeline
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
app.app_context().push()

UPLOAD_FOLDER = 'static/assets/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")


@app.route('/')
def cht():

    return render_template("web.html", note = "")

@app.route('/gen', methods = ["GET", "POST"])
def gen():
    if request.method == "POST":
        img = request.files["im"]
        filename = secure_filename(img.filename)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print(filename)
        out = genCap(filename)

        return render_template("web.html", note = out)

def genCap(input):
    
    #print('static/assets/images/' + input)
    out = image_to_text('static/assets/images/' + input)
    return str(str(out).split(':')[1]).replace('}', "").replace(']', "").replace("'", "")

if __name__ == '__main__':
   
    app.run(debug=True)