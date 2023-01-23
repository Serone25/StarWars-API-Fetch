from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    #Representacion en string del objeto en el que estamos con uno de los atributos, en este caso el username
    #Representación del objeto con un solo valor
    def __repr__(self):
        return '<User %r>' % self.username

    #Cuando iteramos un objeto, lo que le vamos a pedir a la base de datos que muestre u obtenga
    # Representación total del objeto, por eso no se pide el password, para que no se vea 
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return  self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.email,
            "description": self.description
        }