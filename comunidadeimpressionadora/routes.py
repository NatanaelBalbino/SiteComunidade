from flask import render_template, redirect, url_for, request, flash
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required

lista_usuarios = ['Natanael', 'Samuel', 'Renato', 'Joel']


@app.route("/")  # Decorators
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
@login_required
def usuarios():
    return render_template("usuarios.html", lista_usuarios=lista_usuarios)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # fez login com sucesso
            flash('fLogin Feito com sucesso', 'alert-info')
            # analisando se existe o parametro next ma url
            param_next = request.args.get('next')
            if param_next:
                return redirect(param_next)
            else:
                # redirecionando para outra tela
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. Verifique Email e Senha', 'alert-danger')
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


@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template("perfil.html", foto_perfil=foto_perfil)


@app.route("/post/criar")
@login_required
def criar_post():
    return render_template("criarpost.html")
