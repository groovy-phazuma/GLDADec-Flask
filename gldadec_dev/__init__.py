from flask import Flask

app = Flask(__name__, static_folder='C:/github/GLDADec-Flask/gldadec_dev/images')
app.config.from_object('gldadec_dev.config') # 追加

#app.config['SECRET_KEY'] = SECRET_KEY
#app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

import gldadec_dev.views
