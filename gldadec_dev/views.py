#!/usr/bin/env python3
"""
Created on 2024-04-16 (Tue) 23:14:54

@author: I.Azuma
"""
import os
import pandas as pd

from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

from gldadec_dev import app
from gldadec_dev.calc_circle import calculation_circle
from gldadec_dev.simple_run import run_simple_gldadec

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

@app.route("/calc", methods=['GET','POST'])
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
    file = FileField('Mixture', validators=[DataRequired()])
    submit = SubmitField('Upload_1')

class UploadReference(FlaskForm):
    file = FileField('Reference', validators=[DataRequired()])
    submit = SubmitField('Upload_2')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form1 = UploadMixture()
	form2 = UploadReference()

	if form1.validate_on_submit() and form2.validate_on_submit():

		file1 = form1.file.data
		df1 = pd.read_csv(file1)
		print(df1.head())
	
		file2 = form2.file.data
		df2 = pd.read_csv(file2)
		print(df2.head())
	
	return render_template('files/upload.html', form1=form1, form2=form1)

if __name__ == '__main__':
    app.run()