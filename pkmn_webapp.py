
from flask import Flask, url_for, render_template, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename

import cv2

import os
import pkmn
import time

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads/')
ALLOWED_EXTENSIONS = set(['png','gif','jpg','jpeg'])
URL_PATH = '/pkmn'

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
			path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
			print path
			f.save(path)
			string = pkmn_to_text(path)
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
    <p>
    <a href="/gallery">gallery of uploaded images</a>
	'''

@app.route('/img/<filename>')
def get_image(filename):
	i = open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
	if i:
		resp = make_response(i.read())
		resp.content_type = "image/" + filename[-3:]
		return resp
	else:
		return "404 not found"

def pkmn_to_txt(imgpath):
	pkimg = pkmn.pkmnimage(cv2.imread(imgpath, 1))
	string = '<b>BATTLE TEXT</b>:<br/>'+ "<br/>".join(pkimg.get_battletext())+ '<br/><b>MOVES</b>:<br/>'+ "<br/>".join(pkimg.get_movetext())
	print string
	return string

@app.route('/gallery')
def show_gallery():
	page = ['note: every image is reparsed every pageload so please don\'t refresh a buttload','<a href="/upload">upload a new image</a>']
	for fn in os.listdir(app.config['UPLOAD_FOLDER']):
		try:
			start = time.clock()
			text = pkmn_to_txt(os.path.join(app.config['UPLOAD_FOLDER'], fn))
			end = time.clock()
			page.append('<img src="{}/img/{}"/><br/>{}<br/>time: {}s'.format(URL_PATH, fn, text,(end-start)))
		except Exception as e:
			page.append('<img src="{}/img/{}"/><br/>couldn\'t parse ({})'.format(URL_PATH, fn, e))
			print e
	
	return "<hr/>".join(page)





if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=False)

