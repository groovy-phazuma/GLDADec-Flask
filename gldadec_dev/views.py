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
from gldadec_dev.simple_run import run_simple_gldadec


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data_storage/uploads')
MIXTURE_FOLDER = os.path.join(BASE_DIR, 'data_storage/uploads/mixture_files')
GS_FOLDER = os.path.join(BASE_DIR, 'data_storage/uploads/ground_truth_files')
GS_FOLDER = os.path.join(BASE_DIR, 'data_storage/uploads/marker_dicts')
RESULT_FOLDER = os.path.join(BASE_DIR, 'data_storage/results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template('layout.html',title='GLDADec-Home')

@app.route('/run_home', methods=['GET','POST'])
def run_simple():
	render_template('layout.html')

	# Get the list of files in the uploaded mixture files
	mixture_data = []
    # Loop through the files in the uploads folder
	for filename in os.listdir(MIXTURE_FOLDER):
		file_path = os.path.join(MIXTURE_FOLDER, filename)

		if filename.endswith('.csv'):
            # Load the CSV file into a DataFrame and get its shape
			df = pd.read_csv(file_path)
			shape = df.shape  # (rows, columns)
		else:
			shape = "N/A"  # For non-CSV files, we can set shape as Not Applicable

		mixture_data.append({'name': filename, 'shape': shape})
	
	gs_data = []
    # Loop through the files in the uploads folder
	for filename in os.listdir(GS_FOLDER):
		file_path = os.path.join(GS_FOLDER, filename)

		if filename.endswith('.csv'):
            # Load the CSV file into a DataFrame and get its shape
			df = pd.read_csv(file_path)
			shape = df.shape  # (rows, columns)
		else:
			shape = "N/A"  # For non-CSV files, we can set shape as Not Applicable

		gs_data.append({'name': filename, 'shape': shape})
	
	marker_data = []
    # Loop through the files in the uploads folder
	for filename in os.listdir(GS_FOLDER):
		file_path = os.path.join(GS_FOLDER, filename)

		if filename.endswith('.pkl'):
			tmp_dic = pd.read_pickle(file_path)
			shape = len(tmp_dic)
		else:
			shape = "N/A"  # For non-CSV files, we can set shape as Not Applicable

		marker_data.append({'name': filename, 'shape': shape})
		
	if request.method == 'GET':
		return render_template('files/simple_run.html', mixture_data=mixture_data, marker_data=marker_data)
	
	elif request.method == 'POST':
		# collect the selected files
		selected_mixture_file = request.form['selected_mixture_file']
		selected_marker_file = request.form['selected_marker_file']

		file_name = selected_mixture_file.split('_')[0]

		mixture_file_path = os.path.join(MIXTURE_FOLDER, selected_mixture_file).replace('\\', '/')
		marker_file_path = os.path.join(GS_FOLDER, selected_marker_file).replace('\\', '/')
	
		deconv_res = run_simple_gldadec(mixture_file=mixture_file_path, marker_file=marker_file_path)
		deconv_res.to_csv(os.path.join(RESULT_FOLDER, f'{file_name}_deconv_res.csv'), index=False)

		return render_template('files/simple_run.html', mixture_data=mixture_data, marker_data=marker_data, 
						 	   table=(deconv_res.to_html(classes='table table-striped')))

class UploadMixture(FlaskForm):
    file = FileField('Mixture & Reference', validators=[DataRequired()])
    submit1 = SubmitField('Upload1')

class UploadReference(FlaskForm):
    file = FileField('Reference', validators=[DataRequired()])
    submit2 = SubmitField('Upload2')


@app.route('/upload_multi', methods=['GET', 'POST'])
def upload_multipart():
	for name in request.files:
		fs = request.files[name]
		#fs.save('./tmp/'+fs.filename)
		filepath = save_file(fs)
		print(filepath)
	
	return render_template('files/upload_multi.html')

def save_file(file):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return filepath


if __name__ == '__main__':
    app.run()