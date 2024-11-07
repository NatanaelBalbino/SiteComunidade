from flask import render_template, redirect, url_for, request, flash
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import secrets
import os


@app.route("/")  # Decorators
def home():
    return render_template("home.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
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
            flash(f'Login Feito com sucesso', 'alert-info')
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
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("perfil.html", foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    # Adicionar nome aleatório na imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_imagem = nome + codigo + extensao
    caminho_imagem = os.path.join(app.root_path, 'static/fotos_perfil', nome_imagem)

    # Reduzir o Tamanho da Imagem
    tamanho_imagem = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho_imagem)

    # Salvar a Imagem
    imagem.save(caminho_imagem)
    return nome_imagem


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route("/perfil/editar", methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Perfil Atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route("/post/criar", methods=['GET', 'POST'])
@login_required
def criar_post():
    return render_template("criarpost.html")

