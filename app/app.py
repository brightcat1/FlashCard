#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request, url_for, redirect

import json

from models.database import MySQL

f = open("loginfo.json", 'r')
login_info = json.load(f)

db = MySQL(**login_info)

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

#「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/create_card.html")
def create_card():
    return render_template("create_card.html")

@app.route("/test.html")
def test():
    return render_template("test.html")

@app.route("/check.html")
def check():
    return render_template("check.html")

@app.route("/index",methods=["post"])
def post():
    name = request.form["name"]
    okyo = ["色不異空", "空不異色", "色即是空", "空即是色"]
    return render_template("index.html", name=name, okyo=okyo)


#おまじない
if __name__ == "__main__":
    app.run(debug=True)