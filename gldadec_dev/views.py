#!/usr/bin/env python3
"""
Created on 2024-04-16 (Tue) 23:14:54

@author: I.Azuma
"""
import os
from datetime import datetime
import pandas as pd

from flask import render_template, request, make_response
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

from gldadec_dev import app
from gldadec_dev.calc_circle import calculation_circle
from gldadec_dev.simple_run import run_simple_gldadec

UPLOAD_DIR = '/tmp'

@app.route('/')
def index():
	return render_template('layout.html',title='GLDADec-Home')

@app.route('/run', methods=['GET','POST'])
def run_simple():
	render_template('layout.html')
	title='GLDADec-Run'

	if request.method == 'GET':
		return render_template('files/simple_run.html',title=title)
	elif request.method == 'POST':
		deconv_res = run_simple_gldadec()
		return render_template('files/simple_run.html',title=title,table=(deconv_res.to_html(classes='table table-striped')))

@app.route('/calc', methods=['GET','POST'])
def calc():
	if request.method == 'GET':
		return render_template('files/calc.html')
	elif request.method == 'POST':
		diameter = request.form['diameter']
		result = calculation_circle(diameter)
		if len(result) == 2:
			return render_template('files/calc.html', area=result[0],circumference=result[1])
		else:
			return render_template('files/calc.html',error=result)

class UploadMixture(FlaskForm):
    file = FileField('Mixture & Reference', validators=[DataRequired()])
    submit1 = SubmitField('Upload1')

class UploadReference(FlaskForm):
    file = FileField('Reference', validators=[DataRequired()])
    submit2 = SubmitField('Upload2')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form1 = UploadMixture()

	if form1.validate_on_submit():
		file1 = form1.file.data
		print("Mixture Path:",form1.file)

		try:
			df1 = pd.read_csv(file1)
			print("Mixture File:")
			print(df1.head())
		except Exception as e:
			print(f"Error reading Mixture file: {e}")
		
		try:
			df2 = pd.read_csv(file2)
			print("Reference File:")
			print(df2.head())
		except Exception as e:
			print(f"Error reading Reference file: {e}")
	
	return render_template('files/upload.html', form1=form1)

@app.route('/upload_multi', methods=['GET', 'POST'])
def upload_multipart():
	"""
	upload_files = request.files.getlist('uploadFile_aa')
	for file in upload_files:
		fileName = file.filename
		print(fileName)
		saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") + str(fileName)
		save_path = os.path.join(UPLOAD_DIR, saveFileName)
		save_path = save_path.replace("\\", "/")
		print(save_path)
		file.save(save_path)
	"""
	for name in request.files:
		fs = request.files[name]
		fs.save('./tmp/'+fs.filename)

	return render_template('files/upload_multi.html')

if __name__ == '__main__':
    app.run()