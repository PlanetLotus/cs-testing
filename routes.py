from bottle import route

@route('/testing/')
def hello():
    return "Hello World!"
