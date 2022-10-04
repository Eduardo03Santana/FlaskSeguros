#from crypt import methods
from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import tblSegurado, tblSeguro, tblSeguradora, tblProduto
from . import db
from datetime import datetime
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    #if request.method == 'POST':
        #render_template("adesao.html",user=current_user,
        #produto=request.form.get('idProduto'))


    return render_template("home.html", user=current_user, seguradoras=tblSeguradora.query.all(), produtos=tblProduto.query.all())

@views.route('/adesao',methods=['POST','GET'])
@views.route('/adesao/<idProdutoR>',methods=['POST','GET'])
@login_required
def adesao(idProdutoR=''):
    if request.method == 'GET':
        flash("Escolha um dos produtos disponiveis", 'error')
        return redirect('/')
    if request.method == 'POST':
        checkSegurado = tblSegurado.query.filter_by(cpf=request.form.get('cpf')).first()
        if checkSegurado and tblSeguro.query.filter_by(idSegurado=checkSegurado.idSegurado, idProduto=idProdutoR).first():
            flash("Este segurado ja possui esse produto", 'error')
            return redirect('/')

        elif checkSegurado and not tblSeguro.query.filter_by(idSegurado=checkSegurado.idSegurado, idProduto=idProdutoR).first():
            seguro = tblSeguro(idProduto=idProdutoR, idSegurado=checkSegurado.idSegurado, qtdParcelas=12)
            db.session.add(seguro)
            db.session.commit()
            flash("Contrato do produto efetuado")
            return redirect('/perfil')

        elif not checkSegurado and request.form.get('cpf') != None:
            segurado = tblSegurado(nome=request.form.get('nome'), cpf=request.form.get('cpf'), ddd=request.form.get('ddd'), telefone=request.form.get('telefone'),dtCadastro=datetime.now(),idLogin=current_user.id)
            db.session.add(segurado)
            db.session.commit()
            segurado = tblSegurado.query.filter_by(cpf=request.form.get('cpf')).first()
            seguro = tblSeguro(idProduto=idProdutoR, idSegurado=segurado.idSegurado, qtdParcelas=12)
            db.session.add(seguro)
            db.session.commit()
            flash("Segurado aderido e contrato efetuado")
            return redirect('/perfil')
    return render_template('adesao.html', user=current_user, segurados=tblSegurado.query.filter_by(idLogin=current_user.id).all())


@views.route('/perfil', methods=['POST','GET'])
@login_required
def perfil():
    tempValue = f'''
    select d.nome as nmSeguradora,* from tblSegurado a
    inner join tblSeguro b
    on a.idSegurado = b.idSegurado
    inner join tblProduto c
    on b.idProduto = c.idProduto
    inner join tblSeguradora d
    on d.idSeguradora = c.idSeguradora
    where idLogin={str(current_user)[-2]}
    '''
    return render_template('perfil.html', data = db, user=current_user, seguradoras=tblSeguradora.query.all(), produtos=tblProduto.query.all(), seguros=db.session.execute(tempValue),segurados=tblSegurado.query.filter_by(idLogin=current_user.id).all())

@views.route('/excluirP')
def retornar():
  return redirect('/')
@views.route('/alterarP')
def retornar2():
  return redirect('/')
@views.route('/excluirP/<idProduto>', methods=['GET','POST'])
@login_required
def excluirProduto(idProduto=''):
    if current_user.tpUser == 0 and request.method == 'POST':
        execute = f'''delete from tblProduto where idProduto = {idProduto}'''
        db.session.execute(execute)
        db.session.commit()
        flash("Produto removido com sucesso")
    return redirect('/perfil')


@views.route('/alterarP/<idProdutoR>', methods=['GET','POST'])
@login_required
def alterarProduto(idProdutoR=''):
  if current_user.tpUser == 0:
    execute = []
    if request.form.get("nome") != tblProduto.query.filter_by(idProduto=idProdutoR).first().nmProduto: 
        execute.append(f"update tblProduto set nmProduto = '{request.form.get('nome')}' where idProduto = {idProdutoR};")
        flash("Nome do Produto atualizado")
    if request.form.get('dsProduto') != tblProduto.query.filter_by(idProduto=idProdutoR).first().dsProduto: 
        execute.append(f"update tblProduto set dsProduto = '{request.form.get('dsProduto')}' where idProduto = {idProdutoR};")
        flash("Descrição do Produto atualizada")
    if request.form.get("vlMensalidade").replace(",",".") != tblProduto.query.filter_by(idProduto=idProdutoR).first().vlMensalidade: 
        execute.append(f"update tblProduto set vlMensalidade = '{request.form.get('vlMensalidade').replace(',','.')}' where idProduto = {idProdutoR};")
        flash("Valor do Produto atualizado")
    for comando in execute:
        db.session.execute(comando)
    db.session.commit()

    return redirect('/perfil')
  else:
    flash("Acesso Negado", 'error')
    return redirect('/perfil')
  return render_template("home.html", user=current_user, seguradoras=tblSeguradora.query.all(), produtos=tblProduto.query.all())


@views.route('/excluirS', methods=['POST','GET'])
def retornar3():
  return redirect('/')

@views.route('/excluirS/<idSeguroR>', methods=['GET','POST'])
@login_required
def excluirSeguro(idSeguroR=''):
    if request.method == 'GET':
        return redirect('/')
    else:
        db.session.execute(f"delete from tblSeguro where idSeguro = {idSeguroR};")
        db.session.commit()
        flash("Contrato Cancelado")
    return redirect("/perfil")

@views.route('/excluirSegurado/<idSeguradoR>', methods=['GET','POST'])
@login_required
def excluirSegurado(idSeguradoR=''):
    if request.method == 'GET':
        return redirect('/')
    else:
        db.session.execute(f"delete from tblSegurado where idSegurado = {idSeguradoR};")
        db.session.execute(f"delete from tblSeguro where idSegurado = {idSeguradoR};")
        db.session.commit()
        flash("Segurado Deletado")
    return redirect("/perfil")


@views.route('/cadastrarP/<idSeguradoraR>', methods=['GET', 'POST'])
@login_required
def cadastrarProduto(idSeguradoraR = ''):
    if request.method == 'GET' or current_user.tpUser != 0: return redirect('/')
    else:
        produto = tblProduto(nmProduto = request.form.get('nmProduto'), dsProduto = request.form.get('dsProduto'), vlMensalidade = request.form.get('vlMensalidade').replace(",","."), idSeguradora = idSeguradoraR)
        db.session.add(produto)
        db.session.commit()
        flash('Produto inserido com sucesso')
        return redirect('/perfil')
    
@views.route('/alterarSeguradora/<idSeguradoraR>', methods=['POST','GET'])
@login_required
def alterarSeguradora(idSeguradoraR = ''):
    if request.method == 'GET' or current_user.tpUser == 1:
        redirect('/')
    else:
        seguradoraR = tblSeguradora.query.filter_by(idSeguradora=idSeguradoraR).first()
        if request.form.get('nmSeguradora') != seguradoraR.nome:
            execute = f'''update tblSeguradora 
                          set nome = '{request.form.get('nmSeguradora')}' 
                          where idSeguradora = {idSeguradoraR}'''
            db.session.execute(execute)
            db.session.commit()
            flash('Nome da Seguradora Alterado')
        return redirect('/perfil')

@views.route('/excluirSeguradora/<idSeguradoraR>', methods=['POST','GET'])
@login_required
def excluirSeguradora(idSeguradoraR = ''):
    if request.method == 'POST' and current_user.tpUser == 0:
        produtos = [ str(produto.idProduto) for produto in db.session.execute(f'''select * from tblProduto
                      where idSeguradora = {idSeguradoraR}''') ]
        db.session.execute(f'''delete from tblSeguro
                                where idProduto in ({",".join(produtos)})''')
        db.session.execute(f'''delete from tblProduto
                               where idProduto in ({",".join(produtos)})''')
        db.session.execute(f'''delete from tblSeguradora
                               where idSeguradora = {idSeguradoraR}''')
        db.session.commit()
        flash("A seguradora e todos seus produtos foram deletados permanentemente")
        return redirect('/perfil')
    return redirect('/')

@views.route('/cadastrarSeguradora', methods=['GET','POST'])
@login_required
def cadastrarSeguradora():
    if request.method == 'POST' and current_user.tpUser == 0:
        db.session.add(tblSeguradora(nome=request.form.get('nmSeguradora')))
        db.session.commit()
        return redirect('/perfil')
    return redirect('/')

@views.route('/alterarSegurado/<idSeguradoR>', methods=['GET','POST'])
def alterarSegurado(idSeguradoR):
    if request.method == 'POST':
        execucao = []
        segurado = tblSegurado.query.filter_by(idSegurado=idSeguradoR).first()
        if request.form.get('DDD') != segurado.ddd:
            execucao.append(f"update tblSegurado set ddd = '{request.form.get('ddd')}' where idSegurado = {idSeguradoR}")
            flash('DDD Atualizado')
        if request.form.get('telefone') != segurado.telefone:
            execucao.append(f"update tblSegurado set telefone = '{request.form.get('telefone')}' where idSegurado = {idSeguradoR}")
            flash('Telefone Atualizado')
        for exe in execucao:
            db.session.execute(exe)
        db.session.commit()
    return redirect('/perfil')
            
            
            

