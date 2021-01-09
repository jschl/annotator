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

# TODO: refactor block
imgs = [f for f in os.listdir('static/') if f.endswith('jpg')]
nested_imgs = [[os.path.join(f, img) for img in os.listdir('static/' + f) if img.endswith('jpg')] \
     for f in os.listdir('static/') if os.path.isdir('static/' + f)]
nested_imgs = [el for el in nested_imgs if len(el)]
for el in nested_imgs:
    imgs.extend(el)
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

@app.route('/status', methods = ['POST'])
def set_status():
    status = ''
    status = request.get_data()
    if status != '':
        anno = Annotations(filename=imgs[cnt], annotation=status)
        try:
            print(imgs[cnt])
            db.session.add(anno)
            db.session.commit()
            return 'success'
        except Exception as e:
            print(e)
            return 'there was an error'
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)
