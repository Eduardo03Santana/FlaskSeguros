from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import tblLogin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = tblLogin.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.senha, password):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
        else:
            flash('Email ou senha incorreto(s).', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = tblLogin.query.filter_by(email=email).first()
        if user:
            flash('Email ja utilizado por um usuario.', category='error')
        elif len(email) < 4:
            flash('Email muito curto.', category='error')
        elif len(full_name) < 2:
            flash('Nome nao pode ser vazio.', category='error')
        elif password1 != password2:
            flash('Verifique as senhas inseridas.', category='error')
        elif len(password1) < 7:
            flash('Senha deve ter pelo menos 8 caracteres.', category='error')
        else:
            new_Login = tblLogin(email=email, nome=full_name, senha=generate_password_hash(
                password1, method='sha256'), tpUser=1)
            db.session.add(new_Login)
            db.session.commit()
            login_user(new_Login, remember=True)
            flash('Usuário Criado!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
