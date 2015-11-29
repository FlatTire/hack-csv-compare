#!/usr/bin/env python3.4
import os
from flask import Flask, request, redirect, render_template, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

DEFAULT_SKIP_ROWS = 1

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def upload_page():
    """Shows the upload form"""
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def compare_files():
    """Compare two uploaded files"""
    left = request.files['left']
    right = request.files['right']

    if not left:
        raise Exception('No left file submitted')
    elif not right:
        raise Exception('No right file submitted')



    return """<pre>Trying...</pre>"""

if __name__ == '__main__':
    app.run()
