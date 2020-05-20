#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request, url_for, redirect
import mysql.connector as voca_db
import json

from models.database import MySQL

f = open("loginfo.json", 'r')
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
    return render_template("index.html")


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
    return render_template("create_card.html")

#「/test.html」へアクセスがあった場合に、「test.html」を返す
@app.route("/test.html")
def test():
    return render_template("test.html")

#「/check.html」へアクセスがあった場合に、「check.html」を返す
@app.route("/check.html")
def check():
    return render_template("check.html")

    

if __name__ == "__main__":
    app.run(debug=True)