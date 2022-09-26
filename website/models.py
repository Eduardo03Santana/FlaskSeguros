from tkinter.tix import MAX
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


class tblLogin(db.Model, UserMixin):
    __tablename__ = "tblLogin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    nome = db.Column(db.String(150))
    senha = db.Column(db.String(150))
    tpUser = db.Column(db.Integer) # 0 ADMIN | 1 usuario normal 


##class tblAdmin(db.Model):
##    __tablename__ = "tblAdmin"
##    idAdmin = db.Column(db.Integer, primary_key=True, autoincrement=True)
##    nome = db.Column(db.String(150))
##    sexo = db.Column(db.String(50))
##    cpf = db.Column(db.String(11), unique=True)
##    dtCadastro = db.Column(db.Date)
##    telefone = db.Column(db.String(150))
##    ddd = db.Column(db.String(10))
##    idLogin = db.Column(db.Integer, db.ForeignKey('tblLogin.id'))

class tblSegurado(db.Model):
    __tablename__ = "tblSegurado"
    idSegurado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    sexo = db.Column(db.String(50))
    cpf = db.Column(db.String(11), unique=True)
    dtCadastro = db.Column(db.Date)
    telefone = db.Column(db.String(150))
    ddd = db.Column(db.String(10))
    idLogin = db.Column(db.Integer, db.ForeignKey('tblLogin.id'))

class tblSeguradora(db.Model):
    __tablename__ = "tblSeguradora"
    idSeguradora = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    dtInicio = db.Column(db.Date)
    dtFim = db.Column(db.Date)


class tblSeguro(db.Model):
    __tablename__ = "tblSeguro"
    idSeguro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProduto = db.Column(db.Integer, db.ForeignKey('tblProduto.idProduto'))
    idSegurado = db.Column(db.Integer, db.ForeignKey('tblSegurado.idSegurado'))
    idSeguroTitular = db.Column(db.Integer, db.ForeignKey('tblSeguro.idSeguro'))
    dtInicio = db.Column(db.Date)
    dtFim = db.Column(db.Date)
    qtdParcelas = db.Column(db.Integer)
    

class tblSeguroParcela(db.Model):
    __tablename__ = "tblSeguroParcela"
    idSeguroParcela = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idSeguro = db.Column(db.Integer, db.ForeignKey('tblSeguro.idSeguro'))
    idSegurado = db.Column(db.Integer, db.ForeignKey('tblSegurado.idSegurado'))
    nrParcela = db.Column(db.String(50))
    vlParcela = db.Column(db.String(50))
    dtVencimento = db.Column(db.Date)
    dtPagamento = db.Column(db.Date)


class tblProduto(db.Model):
    __tablename__ = "tblProduto"
    idProduto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idSeguradora = db.Column(db.Integer, db.ForeignKey('tblSeguradora.idSeguradora'))
    nmProduto = db.Column(db.String(150))
    vlMensalidade = db.Column(db.String(50))
    dsProduto = db.Column(db.String(MAX))

