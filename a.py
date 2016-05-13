#coding:utf-8
from flask import Flask , request ,   render_template , flash , make_response , redirect , session
import time

app  = Flask(__name__)
## 用于加密的"种子"
app.secret_key = "wtf"
@app.route('/')
def function():
    a= request.headers
    b1 = request.url
    b2 = request.path
    b3 = request.script_root
    b4 = request.base_url
    b5 = request.url_root
    
    if 'counter' not in session:
        session['counter'] = 0
    else:
        session['counter']+=1
    return "OK" + "<br>" + str(a) + "<br><BR>this is you %s times views.."%session['counter']

@app.route('/session_view')
def session_view():
    '''
        每当一个请求进来是会自动根据cookie 的会话ID自动创建一个session类的实例对象
    '''
    return request.cookies['session']

@app.route('/login' , methods=["POST" , "GET"])
def login():
    if request.method == "POST":
        uid = request.form['uid']
        pwd = request.form['pwd']
        if uid == 'admin' and pwd == '123':
            ## 使用flash 消息闪现 要在开头设置 app.secret_key
            flash("Login suessecful")
            return render_template('login.html')
        else:
            return  render_template('login.html' , msg="username or password Error<br>%s"%uid)
    else:
        return render_template('login.html')

@app.route('/search' , methods=['POST' , 'GET'])
def search():
    ##
    ## 无论如何 , method 都会有 get方法..无论url是否带有参数!!??
    ## 此判断恒成立....
    ## if 'q' in request.args: ...这样判断可以哦
    ##
    if request.method == 'GET':
        q =''
        try:
            q = request.args['q']
        except Exception, e:
            pass
        return render_template('search.html' , msg='You input word is %s'%q)
    else:
        return render_template('search.html' , msg='xx')

## cookie \ response
@app.route('/page1')
def page1():
    #创建一个 response 对象
    rsp = make_response('go <a  href="%s">page2</a>'%'/page2')
    rsp.set_cookie('lasttime' , str(time.time()))
    return rsp
@app.route('/page2')
def page2():
    lasttime = request.cookies['lasttime']
    return 'lasttime ...... %s' %lasttime



## 重定向 redirect
## 使用cookies 判断是否是第一次 访问 然重定向到首页  ....
@app.route('/redirect_page')
def redirect_page():
#    try:
#        a = request.cookies['sfirst']
#        return redirect('/')
#    except Exception, e:
#        rspe = make_response(render_template('login.html'))
#        rspe.set_cookie('sfirst' ,'True')
#        return rspe
    if 'first' in request.cookies:
        return  redirect('/')
    else:
        rspe = make_response(render_template('login.html'))
        rspe.set_cookie('first' , 'Yes')
        return rspe
if __name__ == '__main__':
    app.run(host=  '0.0.0.0' , port=22333 , debug=True)