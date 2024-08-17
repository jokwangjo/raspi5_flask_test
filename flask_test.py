from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Flask"
if __name__ == "__main__":  # 웹사이트를 호스팅하여 접속자에게 보여주기 위한 부분
   app.run(host="0.0.0.0", port = "8080")