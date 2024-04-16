#!/usr/bin/env python3
"""
Created on 2024-04-16 (Tue) 23:14:54

@author: I.Azuma
"""
from tutorial import app

@app.route('/test')
def index():
    return 'Hellow World! Test'