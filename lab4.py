from flask import Blueprint, render_template, request
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4.html')

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'rost' and password == '1212':
        return render_template('success_login.html', username=username)
    elif username == '':
        error = 'Не введен логин'
    elif password == '':
        error = 'Не введен пароль'
    else:
        error = 'Неверные логин и/или пароль'
    return render_template('login.html', error=error, username=username, password=password)
    
