# luna/server/auth/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required

from luna.server import bcrypt
from luna.server.models import User, Email, Role
from luna.server.repositories import UserRepository, EmailRepository, UserHasRoleRepository
from luna.server.auth.forms import LoginForm, RegisterForm, NewPasswordForm

################
#### config ####
################

auth_blueprint = Blueprint('auth', __name__,)


################
#### routes ####
################

@auth_blueprint.route('/cadastro', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.email.data,
            password=form.password.data
        )

        user = UserRepository().create(user)
        
        UserHasRoleRepository().create(dict(
            user_id=user.id,
            role_id=Role.COMMON
        ))

        login_user(user)

        flash('Você foi cadastrado com sucesso!', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('auth/login.html', login_form=LoginForm(), register_form=form, new_password_form=NewPasswordForm())


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = UserRepository().findByUsername(form.email.data)
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Suas credenciais foram autenticadas com sucesso!', 'success')
            if user.has_role(Role.ADMIN):
                return redirect(url_for('admin.index'))
            if user.person is None:
                return redirect(url_for('profile.profile'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('Suas credenciais não foram reconhecidas.', 'error')
            return render_template('auth/login.html', login_form=form, register_form=RegisterForm(), new_password_form=NewPasswordForm())
    return render_template('auth/login.html', login_form=form, register_form=RegisterForm(), new_password_form=NewPasswordForm())


@auth_blueprint.route('/new_password', methods=['POST'])
def new_password():
    form = NewPasswordForm(request.form)
    return render_template('auth/login.html',
                           login_form=LoginForm(),
                           register_form=RegisterForm(),
                           new_password_form=form)


@auth_blueprint.route('/sair')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado. Até mais!', 'success')
    return redirect(url_for('auth.login'))
