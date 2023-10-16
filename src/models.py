from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            'is_active': self.is_active,
            'calificacion':  5
            # do not serialize the password, its a security breach
        }


class Estudio(db.Model):
    __tablename__ = 'estudio'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    logo = db.Column(db.String(250), nullable=False)
    slogan = db.Column(db.String(250), nullable=False)    
    videojuegos = db.relationship('Videojuego', backref='estudio', lazy=True)
    


    def __repr__(self):
        return '<Estudio %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            # do not serialize the password, its a security breach
        }

class Videojuego(db.Model):
    __tablename__ = 'videojuego'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    genero = db.Column(db.String(250), nullable=False)
    anio_lanzmaineto  = db.Column(db.String(250), nullable=False)      
    estudio_id = db.Column(db.Integer, db.ForeignKey('estudio.id'),
        nullable=False) 



    def __repr__(self):
        return '<Videojuego %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            # do not serialize the password, its a security breach
        }        