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
    cur.execute('DROP TABLE IF EXISTS vocaindex')
    cur.execute('CREATE TABLE vocaindex (id INTEGER PRIMARY KEY AUTO_INCREMENT, vindex INTEGER NOT NULL);')
    connect.commit()
    return render_template("test.html")

#「/test_main.html」へアクセスがあった場合に、「test.html」を返す
@app.route("/test",methods=["post"])
def voca_test():
    voca_index = []
    shuffle = request.form["shuffle"]
    cur.execute('SELECT * FROM vocabook')
    voca_info = cur.fetchall()
    for i in range(len(voca_info)):
        voca_index.append(i)
    if shuffle == "1":
        random.shuffle(voca_index)
    for i in range(len(voca_index)):
        cur.execute("INSERT INTO vocaindex (vindex) VALUES ('{vindex}');".format(vindex=voca_index[i]))
    connect.commit()
    flag = 1
    return render_template('test_main.html', voca_info = voca_info, voca_index = voca_index[0], shuffle = shuffle, flag = flag)

#「/test_main.html」へアクセスがあった場合に、「test.html」を返す
@app.route("/next",methods=["post"])
def next_test():
    voca_index = []
    shuffle = request.form["shuffle"]
    cur.execute('SELECT * FROM vocabook')
    voca_info = cur.fetchall()
    for i in range(len(voca_info)):
        voca_index.append(i)
    if shuffle == "1":
        random.shuffle(voca_index)
    for i in range(len(voca_index)):
        cur.execute("INSERT INTO vocaindex (vindex) VALUES ('{vindex}');".format(vindex=voca_index[i]))
    connect.commit()
    flag = 1
    return render_template('test_main.html', voca_info = voca_info, voca_index = voca_index[0], shuffle = shuffle, flag = flag)

#「/test_main.html」へアクセスがあった場合に、「test.html」を返す
@app.route("/answer",methods=["post"])
def voca_answer():
    cur.execute('SELECT * FROM vocaindex')
    index_info = cur.fetchall()
    index_num = int(index_info[0][1])
    cur.execute('SELECT mean FROM vocabook where id = {a}'.format(a = str(index_num + 1)))
    ans_info = cur.fetchall()
    flag = 0
    cur.execute("DELETE FROM vocaindex  WHERE id = {a};".format(a = str(index_num + 1)))
    connect.commit()
    return render_template('test_main.html', ans = ans_info, flag = flag)

#「/check.html」へアクセスがあった場合に、「check.html」を返す
@app.route("/check.html")
def check():
    return render_template("check.html")

    

if __name__ == "__main__":
    app.run(debug=True)
