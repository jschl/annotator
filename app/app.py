import random
import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///annotations.db'
db = SQLAlchemy(app)

class Annotations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    annotation = db.Column(db.String(200), nullable=False)

imgs = [f for f in os.listdir('static/') if f.endswith('jpg')]
cnt = 0

@app.route('/index')
def annotate():
    return render_template('index.html')

@app.route("/getimage")
def get_img():
    global cnt
    cnt += 1
    if cnt >= len(imgs):
        return 'finished'
    return imgs[cnt-1]

@app.route('/status',methods = ['POST'])
def set_status():
    status = ''
    status = request.get_data()
    if status != '':
        anno = Annotations(filename=imgs[cnt], annotation=status)
        try:
            db.session.add(anno)
            db.session.commit()
            return 'success'
        except:
            return 'there was an error'
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)
