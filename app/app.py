#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request, url_for, redirect
import mysql.connector as voca_db
import json
import random


f = open("serinfo.json", 'r')
login_info = json.load(f)

connect = voca_db.connect(
    host=login_info["host"],
    port=login_info["port"],
    user=login_info["user"],
    password=login_info["password"],
    database=login_info["database"]
)

connect.ping(reconnect=True)
cur = connect.cursor()

#Flaskオブジェクトの生成
app = Flask(__name__)

#単語のテストの順番を決める用（インデックス）の集合
voca_index = []

vaca_info = []

i = 0


#「/」へアクセスがあった場合に、index.htmlへ飛ばす
@app.route("/")
def main():
    return redirect(url_for('index'))


#「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/index.html")
def index():
    return render_template("index.html")

#「/create_card.html」へアクセスがあった場合に、「create_card.html」を返す
@app.route("/create_card.html")
def create_card():
    return render_template("create_card.html")

@app.route("/add_card",methods=["post"])
def post():
    word = request.form["word"]
    mean = request.form["mean"]
    cur.execute("INSERT INTO vocabook (word, mean) VALUES ('{word}', '{mean}');".format(word=word, mean=mean))
    connect.commit()
    return redirect(url_for('create_card'))

#「/test.html」へアクセスがあった場合に、「test.html」を返す
@app.route("/test.html")
def test():
    return render_template("test.html")

#「/test_main.html」へアクセスがあった場合に、「test.html」を返す
@app.route("/test",methods=["post"])
def voca_test():
    voca_index = []
    shuffle = request.form["shuffle"]
    cur.execute('SELECT * FROM vocabook')
    voca_info = cur.fetchall()
    for i in range(voca_info.size()):
        voca_index.append(i)
    if shuffle == 1:
        random.shuffle(voca_index)
    return render_template('test_main.html', voca_info = voca_info, voca_index = voca_index[i])

#「/test_main.html」へアクセスがあった場合に、「test.html」を返す
@app.route("/answer",methods=["post"])
def voca_answer():
    return render_template('test_main.html', ans = voca_info[voca_index[i]][2])

#「/check.html」へアクセスがあった場合に、「check.html」を返す
@app.route("/check.html")
def check():
    return render_template("check.html")

    

if __name__ == "__main__":
    app.run(debug=True)
