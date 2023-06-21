from flask import Flask, render_template, request 
from jinja2 import Environment
from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
app = Flask(__name__) # название объекта и директива

app.config['SECRET_KEY']='KFC'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///students.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    patronymic = db.Column(db.String(80))
    group = db.Column(db.Integer)
    #date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self): # метод __repr__
        return '<name %r>' % self.id


@app.route('/') #маршрут или декоратор для отслеживания html-страницы
def index(): # функция
    sl=Users.query.all()
    return render_template('index.html', sl=sl)
    
@app.route('/file', methods=['POST', 'GET']) 
def file():
    username=request.form.get('USERNAME')
    surname=request.form.get('SURNAME')
    patronymic=request.form.get('PATRONYMIC')
    group=request.form.get('GROUP')
    
    user=Users(name=username, surname=surname, patronymic=patronymic, group=group)
    try:
        db.session.add(user)
        db.session.commit()
        sl=Users.query.all()
        message= 'The student has been added'
        return render_template('index.html', sl=sl, message=message)  
    except:
        return 'Error'

@app.route('/base') 
def base():
    return render_template('base.html')

@app.route('/studentlist') #маршрут
def studentlist():
   sl=Users.query.all()
   return render_template('studentlist.html', sl=sl )


@app.route('/name/<student_id>') #маршрут
def name(student_id):
    student=Users.query.filter_by(id=student_id).first()
    #return str(name)
    return render_template('name.html', student=student)

if __name__=="__main__": # указывает что этот файл главный
    app.run(debug=True)