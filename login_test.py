from flask import Flask, request, url_for, Response, redirect, abort, make_response

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/login', methods = ['GET'])
def show_loginform():
    return '''
        <form action = "/login" method = "post">
            Username: <input name = "username" type="text" />
            password: <input name = "password" type="password" />
            <input value ="Login" type = "submit" />
        </form>
    '''
    
def check_login(username, password):
    if username =='pi' and password == 'raspberry':
        return True
    else:
        return False

@app.route('/login', methods = ['POST'])
def do_login():
    username= request.form.get('username')
    password= request.form.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct</p>"
    else:
        return "<p>Login failed</p>"
'''
@app.route('/question',methods =['GET'])
def question():
    return request.args.get('answer')#args: 구분된 요청 URL 매개 변수들, ImutableMultiDict형

@app.route('/question',methods=['POST'])
def form_question():
    return request.form.get('answer')

'''

#curl -X POST http://localhost:8080/question --data "answer=1"
@app.route('/question',methods=['GET','POST'])
def question():
    return request.values.get('answer')

#curl -X POST http://localhost:8080/json -H "Content-Type: application/json" -d "{\"data\":\"answer\"}"
@app.route('/json', methods=['POST'])
def json():
    print(request.get_json())
    return str(request.get_json())

#http://127.0.0.1:8080/path?x=y
@app.route('/path',methods=['GET','POST'])
def get_path():
    return ("path: %s<br>"
            "script_root: %s<br>"
            "url: %s<br>"
            "base_url: %s<br>"
            "url_root: %s<br>") % (request.path, request.script_root,
                                   request.url, request.base_url, request.url_root)
            
#http://127.0.0.1:8080/response
@app.route('/response')
def custom_response():
    resp= make_response("이것은 응답 테스트입니다.")
    resp.headers.add('Text-Name','Response Test')
    return resp

@app.route('/hi')
def hi():
    return redirect("/hello")

#http://127.0.0.1:8080/notexisted
@app.errorhandler(404)
def error404(error):
    return "이 페이지는 존재하지 않습니다."

#http://127.0.0.1:8080/wrong
@app.route('/wrong')
def wrong():
    abort(401, "죄송합니다, 이 페이지는 존재하지 않습니다.")
    

#http://127.0.0.1:8080/cookie
@app.route('/cookie')
def hello_again():
    if request.cookies.get("visited"):
        return "Welcome back! Nice to seeu you agian"
    else:
        response= make_response("Hello there! Nice to meet you")
        response.set_cookie("visited", "yes")
        return response
    
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurerd (%d apples)',42)
app.logger.error('An error occured')


if __name__ == "__main__":  # 웹사이트를 호스팅하여 접속자에게 보여주기 위한 부분
   app.run(host="0.0.0.0", port = "8080")
   
   