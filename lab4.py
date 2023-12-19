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
    

@lab4.route('/lab4/fridge', methods = ['GET', 'POST'])
def fridge():
    error = None
    temp = None
    snowflakes = None
    if request.method == 'POST':
        temp = request.form.get('temp')

        if temp is None or temp == '':
            error = 'Ошибка: не задана температура'
        else:
            temp = int(temp)

            if temp < -12:
                error = 'Не удалось установить температуру — слишком низкое значение'
            elif temp > -1:
                error = 'Не удалось установить температуру — слишком высокое значение'
            elif temp >= -12 and temp < -9:
                snowflakes = '***'
            elif temp >= -8 and temp < -5:
                snowflakes = '**'
            else:
                snowflakes = '*'
    return render_template('fridge.html', error=error, temp=temp, snowflakes=snowflakes)
