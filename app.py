from disasterpets import create_app
from flask_cors import CORS
from flask import url_for, redirect, send_file
import os

app = create_app()
CORS(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')

@app.route('/<filename>',methods=['GET'])
def index(filename):
    imagePath = APP_STATIC + '\\images\\' + filename
    return send_file(imagePath, mimetype='image/jpg')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
