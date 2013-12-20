#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, request, send_from_directory
from werkzeug import secure_filename
from imagemanipulationfunctions import binarizeImage, entropyImage, heatmapImage


#this is bullshit to get the right path for Windows
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')

#this is generic flask shit
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = ['jpg']

#the app routes are basically what happens when you hit certain URLs such as / or uploads

#this route just shows a static html file
@app.route("/")
def index():
    return render_template("index.html")

#this route is the form action from index.html, it takes the image that was uploaded and does stuff
# then it redirects users to the page that displays everything
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            defect_count = binarizeImage(UPLOAD_FOLDER, filename,100)
            entropyImage(UPLOAD_FOLDER, filename)
            heatmapImage(UPLOAD_FOLDER, filename)


            return redirect(url_for('uploaded_file', filename=filename, defect=defect_count))


#this is our display page, where the results are shown
@app.route('/show/<filename>/<defect>')
def uploaded_file(filename,defect):
    original = 'http://127.0.0.1:5000/uploads/' + filename
    bin = 'http://127.0.0.1:5000/uploads/bin_' + filename
    heat = 'http://127.0.0.1:5000/uploads/heat_' + filename
    entropy = 'http://127.0.0.1:5000/uploads/ent_' + filename
    return render_template('display_image.html', original=original, bin=bin, heat=heat, entropy=entropy, defect=defect)

#this is some shit to let the server display images from the /uploads folder
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


#this is a function to restrict our uploads to JPGs or whatever
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#more standard flask stuff
if __name__ == "__main__":
    app.run(debug=True)