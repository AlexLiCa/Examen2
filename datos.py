from flask import Flask, jsonify,abort,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

from sqlalchemy import false


app = Flask(__name__)

#configuracion de la base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///examen.db' #conexion con la base de datos
db = SQLAlchemy(app) #aqui le decimos que la puede modificar
ma = Marshmallow(app)

class Task(db.Model): #representacion de una tarea en base de datos y una tarea
    id = db.Column(db.Integer, primary_key=True) #Creamos un id que crezca automaticamente 
    name = db.Column(db.String(255)) #El parentesis es para indicar el tamaño del string, puedo agregar un unique para que no se repita 
    check = db.Column(db.Boolean)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, name, check, date):
        self.name = name
        self.check = False
        self.date = datetime.datetime.now()

    
    def __repr__(self):
        datos = "{"+"id: " + str(self.id) +","+ "name:" + str(self.name) +","+ " check:" + str(self.check)+"}"
        return datos

db.create_all()
class TaskSchema(ma.Schema):
    class meta:
        fields = ('id','name','check')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

all_tasks = Task.query.all()


@app.route('/')
def hello_world():
    return '<h1>Hola bienvenido a mi Api</h1> '


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    tasks = []
    for task in all_tasks:
        task = {
        'id': task.id,
        'name': task.name,
        'check': task.check,
        'date': task.date
    }
        tasks.append(task)
    return  jsonify({'task': tasks}), 201
  
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    t = Task.query.get_or_404(id)
    task = {
        'id': t.id,
        'name': t.name,
        'check': t.check,
        'date': t.date
    }
    return jsonify({'task': task})


@app.route('/api/tasks', methods=['POST'])
def create_task():
    new_task = Task(name=request.json['name'], check = False, date = datetime.datetime.now)
    db.session.add(new_task)
    db.session.commit()
    all_tasks = Task.query.all()
    tasks = []
    for task in all_tasks:
        task = {
        'id': task.id,
        'name': task.name,
        'check': task.check,
        'date': task.date
    }
        tasks.append(task)
    return jsonify({'task': tasks}), 201

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    t = Task.query.get_or_404(id)
    print(type(t))
    t.name = request.json.get('name', t.name)  
    t.check = request.json.get('check', t.check)   
    t.date = datetime.datetime.now()
    db.session.commit()
    all_tasks = Task.query.all()
    tasks = []
    for task in all_tasks:
        task = {
        'id': task.id,
        'name': task.name,
        'check': task.check,
        'date': t.date
    }
        tasks.append(task)
    return jsonify({'task': tasks}), 201

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    t = Task.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    all_tasks = Task.query.all()
    tasks = []
    for task in all_tasks:
        task = {
        'id': task.id,
        'name': task.name,
        'check': task.check,
        'date': t.date
    }
        tasks.append(task)
    return jsonify({'task': tasks}), 201

  

if __name__ == '__main__':
    app.run(debug=True)




    

