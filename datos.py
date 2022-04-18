from flask import Flask, jsonify,abort,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime
from sqlalchemy import false


app = Flask(__name__)

#configuracion de la base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///examen.db' 
db = SQLAlchemy(app) 
ma = Marshmallow(app)

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True) #Este seria el RFID 
    un = db.Column(db.String(15)) #Username 
    name = db.Column(db.String(20)) #Nombre del usuario 
    ap = db.Column(db.String(20)) #apellido paterno
    am = db.Column(db.String(20)) #apellido materno 
    check = db.Column(db.Boolean) # este  check esta por que en la imagen en la parte de "ext" parece ser una opcion seleccionable 
    email = db.Column(db.String(30))#correo electronico del usuario 
    dep = db.Column(db.String(15))#departamento en el que trabaj el usuario 
    date = db.Column(db.DateTime, default=datetime.datetime.now) #ultima fecha de modificacion del usuario 

    def __init__(self, ap, am, name, un, email, dep, check, date):
        self.name = name
        self.ap = ap
        self.am = am
        self.un = un
        self.email = email
        self.dep = dep
        self.check = False
        self.date = datetime.datetime.now()


    
    def __repr__(self):
        datos = "{"+"id: " + str(self.id) +","+ "name:" + str(self.name) +","+ " check:" + str(self.check)+"}"
        return datos

#db.create_all()

class UserSchema(ma.Schema):
    class meta:
        fields = ('id','name','check', 'un', 'email','dep')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

all_users = User.query.all()


@app.route('/')
def hello_world():
    return '<h1>Buenas tardes</h1> '

#---------------------------------------------------------------------------------
# nombre de la funcion: get_users()
# entradas: ninguna
# salidas: un json con cada una lista de diccionarios de todos los usuarios 
# objetivo de la funcion: recuperar todos los usuarios que se encuentran en la base de datos "examen.db"
#---------------------------------------------------------------------------------
@app.route('/api/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    users = []
    for user in all_users:
        user = {
        'id': user.id,
        'name': user.name,
        'ap': user.ap,
        'am': user.am,
        'un': user.un,
        'email': user.email,
        'dep': user.dep,
        'check': user.check,
        'date': user.date
    }
        users.append(user)
    return  jsonify({'user': users}), 201
#---------------------------------------------------------------------------------
# nombre de la funcion: get_user()
# entradas: integer que sea de un usuario 
# salidas: un json con un diccionario del usuario que se recupero 
# objetivo de la funcion: buscar un solo usuario dentro de la base de datos "examen.db"
#---------------------------------------------------------------------------------
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    t = User.query.get_or_404(id)
    user = {
        'id': t.id,
        'name': t.name,
        'un': t.un,
        'ap': t.ap,
        'am': t.am,
        'email': t.email,
        'check': t.check,
        'dep': t.dep,
        'date': t.date
    }
    return jsonify({'user': user})

#---------------------------------------------------------------------------------
# nombre de la funcion: create_user()
# entradas: ninguna 
# salidas: una lista de diccionarios con todos los usuarios registrados hasta el momento 
# objetivo de la funcion: agregar un usuario a la base de datos "examen.db"
#---------------------------------------------------------------------------------
@app.route('/api/users', methods=['POST'])
def create_user():
    try: #primero intentamos crear el usuario con el apellido materno 
        new_user = User(
            name=request.json['name'], 
            ap = request.json['ap'], 
            am = request.json['am'], 
            check = False, 
            date = datetime.datetime.now,
            un=request.json['un'],
            email = request.json['email'],
            dep = request.json['dep']
        )
    except: #En caso de que el apellido materno no se envie se crea con espacio en blanco 
          new_user = User(
            name=request.json['name'], 
            ap = request.json['ap'], 
            am = "",
            check = False, 
            date = datetime.datetime.now,
            un=request.json['un'],
            email = request.json['email'],
            dep = request.json['dep']
          )
#Se considero que el unico espacio que una empresa podria omitir seria que no el usuario solo tenga un apellido , los demas campos son obligatorios 
    db.session.add(new_user)
    db.session.commit()
    all_users = User.query.all()
    users = []
    for user in all_users:
        user = {
        'id': user.id,
        'name': user.name,
        'ap': user.ap,
        'am': user.am,
        'un': user.un,
        'email': user.email,
        'dep': user.dep,
        'check': user.check,
        'date': user.date
    }
        users.append(user)
    return jsonify({'user': users}), 201
#---------------------------------------------------------------------------------
# nombre de la funcion: update_user(id)
# entradas: un integer 
# salidas: una lista de diccionarios de todos los usuarios en la base de datos 
# objetivo de la funcion: actualizar algun campo del usuario, el id y la fecha no las puede modificar el 
#---------------------------------------------------------------------------------
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    t = User.query.get_or_404(id)
#---------------------------------------------------------------------------
# En esta seccion se verifican los datos que se envian , en caso de que falte uno conserva su valor actual 
#---------------------------------------------------------------------------
    t.name = request.json.get('name', t.name) 
    t.ap = request.json.get('ap', t.ap)  
    t.am = request.json.get('am', t.am)  
    t.un = request.json.get('un', t.un)  
    t.email = request.json.get('email', t.email)   
    t.dep = request.json.get('dep', t.dep)
    t.check = request.json.get('check', t.check)   
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
    t.date = datetime.datetime.now()
    db.session.commit()
    all_users = User.query.all()
    users = []
    for user in all_users:
        user = {
        'id': user.id,
        'name': user.name,
        'ap': user.ap,
        'am': user.am,
        'un': user.un,
        'email': user.email,
        'dep': user.dep,
        'check': user.check,
        'date': user.date
    }
        users.append(user)
    return jsonify({'user': users}), 201

#---------------------------------------------------------------------------------
# nombre de la funcion: delete_user()
# entradas: un integer 
# salidas: una lista de diccionarios de todos los usuarios en la base de datos 
# objetivo de la funcion: eliminar un usuario de la base de datos 
#---------------------------------------------------------------------------------

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    t = User.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    all_users = User.query.all()
    users = []
    for user in all_users:
        user = {
        'id': user.id,
        'name': user.name,
        'ap': user.ap,
        'am': user.am,
        'un': user.un,
        'email': user.email,
        'dep': user.dep,
        'check': user.check,
        'date': user.date
    }
        users.append(user)
    return jsonify({'user': users}), 201

  

if __name__ == '__main__':
    app.run(debug=True)




    

