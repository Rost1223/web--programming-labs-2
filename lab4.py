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

@lab4.route('/lab4/grain_order', methods = ['GET', 'POST'])
def grain_order():
    error = None
    grain = None
    weight = None
    skidka = ''
    price = 0
    if request.method == 'POST':
        grain = request.form.get('grain')
        weight = request.form.get('weight')

        if weight is None or weight == '':
            error = 'Не введен вес'
        else:
            weight = float(weight)

            if weight <= 0:
                error = 'Неверное значение веса'
            elif weight > 500:
                error = 'Такого объема сейчас нет в наличии'
            else: 
                if grain == 'yachmen':
                    price = 12000*weight
                elif grain == 'oves':
                    price = 8500*weight
                elif grain == 'pshenitsa':
                    price = 8700*weight
                else:
                    price = 14000*weight
                
                if weight > 50 and weight <= 500:
                        price = price*0.9
                        skidka  = 'Применена скидка за большой объём'


    return render_template('grain_order.html', error=error, grain=grain, weight=weight, price=price, skidka=skidka)