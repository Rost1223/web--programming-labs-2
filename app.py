from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return '''


<!doctype html>
<html>
    <head>
        <title>«НГТУ, ФБ, Лабораторные работы»</title>     
    </head>
     <body>
        <header>
        НГТУ, ФБ, WEB-программирование, часть 2. Спиок лабораторных
        </header>
         
            <ol>
             <a href="/lab1" target="_blank" >Первая лабораторная</a>
            </ol>
        
        <footer>
            &copy; Разуванов Ростислав, ФБИ-14, 3 курс, 2023
        </footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
   return'''
<!doctype html>
<html>
    <head>
        <title>Разуванов Ростислав Сергеевич, лабораторная 1</title>
        
    </head>
     <body>
        <header>
        НГТУ, ФБ, Лабораторная работа 1
        </header>
          <h1>Разуванов Ростислав Сергеевич</h1>
        
        <p>Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.  
        </p>
        
        <footer>
            &copy; Разуванов Ростислав, ФБИ-14, 3 курс, 2023
        </footer>
    </body>
</html>
'''

