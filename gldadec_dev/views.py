#!/usr/bin/env python3
"""
Created on 2024-04-16 (Tue) 23:14:54

@author: I.Azuma
"""
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
	result = run_simple_gldadec()
	return render_template('layout.html')

@app.route('/run')
def run_simple():
    return render_template('files/simple_run.html')

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

class UploadForm(FlaskForm):
    file = FileField('CSVファイルを選択', validators=[DataRequired()])
    submit = SubmitField('アップロード')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		file = form.file.data
		df = pd.read_csv(file)
		print(df.head())
	return render_template('files/upload.html', form=form)

if __name__ == '__main__':
    app.run()