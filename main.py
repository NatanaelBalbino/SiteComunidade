from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, FormCriarConta

app = Flask(__name__)

lista_usuarios = ['Natanael', 'Samuel', 'Renato', 'Joel']

app.config['SECRET_KEY'] = 'b9d98df936fa1890ebfc8ded3f97e684'


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
        # criou conta com sucesso
        flash(f'Conta Criada com sucesso no email: {form_criarconta.email.data}', 'alert-success')
        # redirecionando para outra tela
        return redirect(url_for('home'))
    return render_template("login.html", form_login=form_login, form_criarconta=form_criarconta)


if __name__ == '__main__':
    app.run(debug=True)
