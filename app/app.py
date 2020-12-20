from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

imgs = [f for f in os.listdir('static/') if f.endswith('jpg')]
cnt = 0

@app.route('/index')
def annotate():
    return render_template('index.html')

@app.route("/getimage")
def get_img():
    global cnt
    cnt += 1
    return imgs[cnt]

@app.route('/test',methods = ['POST'])
def test1():
    new_freq = request.get_data()
    print(new_freq)
    return 'success'

if __name__ == '__main__':
    app.run(debug=True)
