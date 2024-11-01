from flask import render_template, redirect, url_for, request, flash
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import Usuario

lista_usuarios = ['Natanael', 'Samuel', 'Renato', 'Joel']


@app.route("/")  # Decorators
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # fez login com sucesso
        flash('Login Feito com sucesso', 'alert-info')
        # redirecionando para outra tela
        return redirect(url_for('home'))
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # criptografando a senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        # criar usuario
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        # criando sessão para o usuário
        database.session.add(usuario)
        # commit dos dados do usuário
        database.session.commit()
        # criou conta com sucesso
        flash(f'Conta Criada com sucesso no email: {form_criarconta.email.data}', 'alert-success')
        # redirecionando para outra tela
        return redirect(url_for('home'))
    return render_template("login.html", form_login=form_login, form_criarconta=form_criarconta)
