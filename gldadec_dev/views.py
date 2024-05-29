#!/usr/bin/env python3
"""
Created on 2024-04-16 (Tue) 23:14:54

@author: I.Azuma
"""
from flask import render_template
from gldadec_dev import app

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