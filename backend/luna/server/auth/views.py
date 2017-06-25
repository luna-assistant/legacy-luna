# luna/server/auth/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required

from luna.server import bcrypt
from luna.server.models import User
from luna.server.repositories import UserRepository
from luna.server.auth.forms import LoginForm, RegisterForm

################
#### config ####
################

auth_blueprint = Blueprint('auth', __name__,)


################
#### routes ####
################

@auth_blueprint.route('/cadastro', methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data
        )

        user = UserRepository().create(user)
        login_user(user)

        flash('Você foi cadastrado com sucesso!', 'success')
        return redirect(url_for("main.dashboard"))
    return render_template('auth/login.html', login_form=LoginForm(), register_form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = next(UserRepository().findByField(
            'username', form.username.data), None)
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Suas credenciais foram autenticadas com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Suas credenciais não foram reconhecidas.', 'error')
            return render_template('auth/login.html', login_form=form, register_form=RegisterForm())
    return render_template('auth/login.html', login_form=form, register_form=RegisterForm())


@auth_blueprint.route('/sair')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado. Até mais!', 'success')
    return redirect(url_for('auth.login'))
