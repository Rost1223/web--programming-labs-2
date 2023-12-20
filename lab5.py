from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, Blueprint, render_template, request, session
import psycopg2

lab5 = Blueprint('lab5', __name__)

def dbConnect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='knowledge_base',
        user='rost_knowledge_base',
        password='1223')

    return conn

def dbClose(cursor, connection):
    cursor.close()
    connection.close()

@lab5.route('/lab5/')
def main():
    visibleUser = "Anon"
    if 'visibleUser' in session:
        visibleUser = session['visibleUser']
    return render_template("lab5.html", username=visibleUser)

    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users;")

    result = cur.fetchall()

    print(result)

    dbClose(cur, conn)

    return "go to console"

lab5.route('/lab5/users/')
def users():
    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users;")

    users = cur.fetchall()
    users = [user[0] for user in users]

    dbClose(cur, conn)

    return render_template("users.html", users=users)

@lab5.route('/lab5/register', methods=["GET", "POST"])
def registerPage():
    errors = []

    if request.method == "GET":
        return render_template("register.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username and password):
        errors.append("Пожалуйста, заполните все поля")
        print(errors)
        return render_template("register.html", errors=errors)


    hashPassword = generate_password_hash(password)

    conn = dbConnect()
    cur = conn.cursor()

    cur.execute(f"SELECT username FROM users WHERE username = %s", (username,))

    if cur.fetchone() is not None:
        errors.append("Пользователь с данным именем уже существует")
   
        dbClose(cur, conn)

        return render_template("register.html", errors=errors)

    cur.execute(f"INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id", (username, hashPassword))
    

    conn.commit()
    dbClose(cur, conn)

    return redirect("/lab5/login_lab5")



@lab5.route('/lab5/login_lab5', methods=["GET", "POST"])
def loginPage():
    errors = []


    if request.method == "GET":
        return render_template("login_lab5.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append("Пожалуйста, заполните все поля")
        print(errors)
        return render_template("login_lab5.html", errors=errors)

    conn = dbConnect()
    cur = conn.cursor()

    cur.execute(f"SELECT id, password FROM users WHERE username = %s", (username,))

    result = cur.fetchone()

    if result is None:
        errors.append("Неправильный логин или пароль")
        dbClose(cur, conn)
        return render_template("login_lab5.html", errors=errors)

    userID, hashPassword = result

    if check_password_hash(hashPassword, password):
        session['id'] = userID
        session['username'] = username
        session['visibleUser'] = username
        dbClose(cur, conn)
        return redirect("/lab5/")


    else:
        errors.append("Неправильный логин или пароль!")
        return render_template("login_lab5.html", errors=errors)



@lab5.route('/lab5/new_article', methods=["GET", "POST"])
def createArticle():
    errors = []


    userID = session.get("id")

    if userID is not None:
        if request.method == "GET":
            return render_template("new_article.html", errors=errors)

        if request.method == "POST":
            text_article = request.form.get("text_article")
            title = request.form.get("title_article")
            is_public = request.form.get("is_public") == "on"

            if len(text_article) == 0:
                errors.append("Заполните текст")
                return render_template("new_article.html", errors=errors)
            
            if len(title) == 0:
                errors.append("Введите название")
                return render_template("new_article.html", errors=errors)

            conn = dbConnect()
            cur = conn.cursor()

            cur.execute(f"INSERT INTO articles(user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s) RETURNING id",
                        (userID, title, text_article, is_public))

            new_article_id = cur.fetchone()[0]
            conn.commit()

            dbClose(cur, conn)

            return redirect(f"/lab5/articles/{new_article_id}")

    return redirect("/lab5/login_lab5")


@lab5.route('/lab5/articles/<int:article_id>')
def getArticle(article_id):
    userID = session.get('id')

    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()

        cur.execute(f"SELECT title, article_text, is_public, user_id FROM articles WHERE id = %s", (article_id,))

        articleBody = cur.fetchone()

        dbClose(cur, conn)

        if articleBody is None:
            return "Not found!"

        if not articleBody[2] and articleBody[3] != userID:
            return "Доступ запрещен!"

        text = articleBody[1].splitlines()

        return render_template("article.html", article_text=text, article_title=articleBody[0])


@lab5.route('/lab5/see_articles/<int:user_id>')
def get_user_articles(user_id):
    userID = session.get('id')
    if userID is not None:
        if userID != user_id:  
            return redirect("/lab5/login_lab5")

        conn = dbConnect()
        cur = conn.cursor()

        cur.execute("SELECT title FROM articles WHERE user_id = %s", (user_id,))

        articles = cur.fetchall()

        dbClose(cur, conn)
        return render_template("user_articles.html", articles=articles, user_id=user_id, username=session.get("username"))



@lab5.route('/lab5/logout')
def logout():
    session.clear()
    return redirect("/lab5/")