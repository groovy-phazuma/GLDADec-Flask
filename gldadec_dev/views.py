#!/usr/bin/env python3
"""
Created on 2024-04-16 (Tue) 23:14:54

@author: I.Azuma
"""
from flask import render_template, request
from gldadec_dev import app
from gldadec_dev.calc_circle import calculation_circle

@app.route('/')
def index():
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
        'test_titles':['title1','title2','title3']
    }
    return render_template('files/index.html', my_dict=my_dict)

@app.route('/calc')
def other():
    return render_template('files/calc.html')

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
		
if __name__ == '__main__':
    app.run()