#!/usr/bin/env python3
"""
Created on 2024-04-16 (Tue) 23:16:39

@author: I.Azuma
"""
from flask import Flask

app = Flask(__name__)
app.config.from_object('gldadec_dev.config') # 追加

import gldadec_dev.views