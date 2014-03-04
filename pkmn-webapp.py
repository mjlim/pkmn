
from flask import Flask, url_for, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import cv2

import os
import pkmn

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png','gif','jpg','jpeg'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def root():
	return "HELLO!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		print f.filename
		if f and allowed_file(f.filename):
			path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
			print path
			f.save(path)
			pkimg = pkmn.pkmnimage(cv2.imread(path, 1))
			string = '<b>BATTLE TEXT</b>:<br/>'+ "<br/>".join(pkimg.get_battletext())+ '<br/><b>MOVES</b>:<br/>'+ "<br/>".join(pkimg.get_movetext())
			print string
			return string

	return '''
    <!doctype html>
    <title>upload pokemon battle screenshot</title>
    <h1>upload a pokemon battle screenshot</h1>
    <p>only supports generic battle text screens (i.e. MAGIKARP used SPLASH!) and the move select screen for now</p>
    <p>will read the text and display it (hopefully)</p>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
	'''


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=False)

