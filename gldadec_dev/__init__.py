from flask import Flask

app = Flask(__name__)
app.config.from_object('gldadec_dev.config') # 追加

import gldadec_dev.views
