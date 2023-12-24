from flask import Blueprint, request, render_template, redirect
from Db import db
from Db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import and_

lab6 = Blueprint('lab6', __name__)

@lab6.route("/lab6/check")
def main():
    my_users = users.query.all()
    print(my_users)
    return "result in console!"

@lab6.route("/lab6/checkarticles")
def checkarticles():
    my_articles = articles.query.all()
    print(my_articles)
    return "result in console!"

@lab6.route("/lab6/register", methods=["GET", "POST"])
def register():
    errors = []

    if request.method == "GET":
        return render_template("register_lab6.html", errors=errors)
    
    username_form = request.form.get('username_form')
    password_form = request.form.get('password_form')

    if not (username_form):
        errors.append("Пожалуйста, введите имя пользователя/пароль")
        print(errors)
    
    if len(password_form) < 5:
        errors.append("Пароль должен содержать не менее 5 символов")
        print(errors)

    isUserExist = users.query.filter_by(username=username_form).first()

    if isUserExist is not None:
        errors.append("Пользователь с данным именем уже существует")
        print(errors)
    
    if errors:
        return render_template("register_lab6.html", errors=errors)
    
    hashedPswd = generate_password_hash(password_form, method='pbkdf2')

    newUser = users(username=username_form, password=hashedPswd)

    db.session.add(newUser)
    db.session.commit()

    return redirect('/lab6/login')

@lab6.route("/lab6/login", methods=["GET", "POST"])
def login():
    errors = []
    if request.method == "GET":
        return render_template('login_lab6.html')

    username_form = request.form.get('username')
    password_form = request.form.get('password')

    if not username_form:
        errors.append("Пожалуйста, введите имя пользователя")
        print(errors)
    elif not password_form:
        errors.append("Пожалуйста, введите пароль")
        print(errors)
    else:
        my_user = users.query.filter_by(username=username_form).first()

        if my_user is not None:
            if check_password_hash(my_user.password, password_form):
                login_user(my_user, remember=False)
                return redirect('/lab6/articles')
            else:
                errors.append("Неправильный пароль")
                print(errors)
        else:
            errors.append("Пользователя не существует")
            print(errors)

    if errors:
        return render_template("login_lab6.html", errors=errors)
        
    return render_template('login_lab6.html')


@lab6.route("/lab6/articles")
@login_required
def articles_list():
    my_articles = articles.query.filter_by(user_id=current_user.id).all()
    username = current_user.username
    all_articles = articles.query.join(users).filter(and_(articles.is_public==True, users.id != current_user.id)).all()
    return render_template('list_articles.html', articles=my_articles, username=username, all_articles=all_articles)

@lab6.route('/lab6/logout')
@login_required
def logout():
    logout_user()
    return redirect("/lab6/")


@lab6.route('/lab6/new_article', methods=["GET", "POST"])
@login_required
def createArticle():
    errors = []

    if request.method == "GET":
        return render_template("new_article_lab6.html", errors=errors)

    if request.method == "POST":
        text_article = request.form.get("text_article")
        title = request.form.get("title_article")
        is_public = request.form.get("is_public") == "on"

        if len(text_article) == 0:
            errors.append("Заполните текст")
        
        if len(title) == 0:
            errors.append("Введите название")

        if errors:
            return render_template("new_article_lab6.html", errors=errors)
        
        new_article = articles(title=title, article_text=text_article, is_public=is_public, user_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
    
        return redirect(f"/lab6/articles/{new_article.id}")

    return redirect("/lab6/login")


@lab6.route('/lab6/')
def home():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Аноним"

    return render_template('lab6.html', username=username)


@lab6.route('/lab6/articles/<int:article_id>')
@login_required
def viewArticle(article_id):
    article = articles.query.get(article_id)

    if article is None:
        return "Заметка не найдена"

    if article.user_id != current_user.id and not article.is_public:
       return "Заметка недоступна для просмотра"

    paragraphs = article.article_text.split('\n')

    return render_template("article_lab6.html", article=article, paragraphs=paragraphs)