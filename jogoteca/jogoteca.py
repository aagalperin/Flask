from flask import Flask, flash, render_template, request, redirect, session, flash, url_for

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.senha = senha
        self.nome = nome
        self.nickname = nickname

usuario1 = Usuario('Anna Nabuco', 'Nina', '1234')
usuario2 = Usuario('Joao Ferreira', 'JN', 'abc')
usuario3 = Usuario('Carol Ferreira', 'Ferris', 'senha123')

usuarios = {usuario1.nickname: usuario1, usuario2.nickname : usuario2, usuario3.nickname: usuario3}

class Jogo:
    def __init__ (self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console
    
jogo1 = Jogo ('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Combat', 'Luta', 'PS2')
lista_jogos = [jogo1, jogo2, jogo3]

app = Flask(__name__)
# app.run(host='0.0.0.0', port=8080)
app.secret_key = 'alura'

#criando rota
@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)

# criando nova rota (ponte para direcionar nova pagina)
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista_jogos.append(jogo)
    return redirect(url_for('index'))
    
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima_pagina = proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario in usuarios:
        if senha == usuarios[usuario].senha:
            session['usuario_logado'] = usuarios[usuario].nickname
            flash(session['usuario_logado'] + ' logado com sucesso.')
            proxima = request.form['proxima']
            return redirect(proxima)
    else:
        flash('Usário não logado. Erro na autentificação')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

app.run(debug=True)