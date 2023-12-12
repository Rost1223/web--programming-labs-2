from flask import Blueprint, redirect, url_for, render_template, request
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    return render_template('lab3.html')

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    if user == '':
        errors['user'] = 'Заполните поле!'

    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('order.html', order=order)


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('pay.html', price = price)

@lab3.route('/lab3/success')
def success():
    return render_template('success.html')


@lab3.route('/lab3/buy_ticket')
def buy():
    errors = {}
    name = request.args.get('name')
    type_ticket = request.args.get('type_ticket')
    shelf = request.args.get('shelf')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    exit_point = request.args.get('exit_point')
    arrival_point = request.args.get('arrival_point')
    date = request.args.get('date')

    if name == '':
        errors['name'] = 'Заполните поле!'


    if age is None or age == '':
        errors['age'] = 'Заполните поле!'
    else:
        age= int(age)
        if age < 18 or age > 120:
            errors['age'] = 'Возраст пассажира должен быть от 18 до 120 лет.'


    if exit_point == '':
        errors['exit_point'] = 'Заполните поле!'

    if arrival_point == '':
        errors['arrival_point'] = 'Заполните поле!'

    if date == '':
        errors['date'] = 'Заполните поле!'

    if request.args.get('baggage') == 'on':
        baggage = 'есть'
    else:
        baggage = 'нет'

    if request.args.get('type_ticket') == 'kid':
        type_ticket = 'детский'
    else:
        type_ticket = 'взрослый'

    if request.args.get('shelf') == 'lower':
        shelf = 'нижняя'
    elif request.args.get('shelf') == 'upper':
        shelf = 'верхняя'
    elif request.args.get('shelf') == 'upper side':
        shelf = 'верхняя боковая'
    else:
        shelf = 'нижняя боковая'

    return render_template('buy_ticket.html', name=name, type_ticket=type_ticket, shelf=shelf, baggage=baggage, age=age, exit_point=exit_point, arrival_point=arrival_point, date=date, errors=errors)