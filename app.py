from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Banco de dados (Render usa DATABASE_URL no ambiente)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('postgresql://lista_tst_user:Q6l0XHfKeqCKdNz5kEnPv88zrYqfSYLN@dpg-d0edlsuuk2gs73fcp5a0-a/lista_tst', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Funcionário
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    observacao = db.Column(db.String(200))
    nota = db.Column(db.Float, nullable=False)
    evento = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    lista = db.Column(db.String(20), nullable=False) 
    
    
class Atualizacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    observacao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    funcionario = db.relationship('Funcionario', backref=db.backref('atualizacoes', lazy=True))


# Página principal com menu
@app.route('/')
def index():
    return render_template('index.html')

# Formulário de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Inserir funcionário no banco
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    funcionario = Funcionario(
        nome=request.form['nome'],
        observacao=request.form['observacao'],
        nota=float(request.form['nota']),
        evento=request.form['evento'],
        data=datetime.strptime(request.form['data'], '%Y-%m-%d').date(),
        lista=request.form['lista']
    )
    db.session.add(funcionario)
    db.session.commit()
    return redirect(url_for('listar'))

# Listagem
@app.route('/listar')
def listar():
    novos = Funcionario.query.filter_by(lista='novos').all()
    favoritos = Funcionario.query.filter_by(lista='favoritos').all()
    excluidos = Funcionario.query.filter_by(lista='excluidos').all()
    return render_template('listar.html', favoritos=favoritos, excluidos=excluidos, novos=novos)

# Edição
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    funcionario = Funcionario.query.get_or_404(id)

    if request.method == 'POST':
        funcionario.nome = request.form['nome']
        funcionario.observacao = request.form['observacao']
        funcionario.nota = float(request.form['nota'])
        funcionario.evento = request.form['evento']
        funcionario.data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        funcionario.lista = request.form['lista']

        db.session.commit()
        return redirect(url_for('listar'))

    return render_template('editar.html', funcionario=funcionario)

# Exclusão
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect(url_for('listar'))


@app.route('/atualizar/<int:funcionario_id>', methods=['GET', 'POST'])
def atualizar(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)

    if request.method == 'POST':
        observacao = request.form['observacao']
        data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        tipo = request.form['tipo']  

        nova_atualizacao = Atualizacao(
            funcionario_id=funcionario.id,
            observacao=observacao,
            data=data,
            tipo=tipo 
        )
        db.session.add(nova_atualizacao)
        db.session.commit()
        return redirect(url_for('listar'))

    return render_template('atualizar.html', funcionario=funcionario)


@app.route('/ver_atualizacoes/<int:funcionario_id>')
def ver_atualizacoes(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    atualizacoes = Atualizacao.query.filter_by(funcionario_id=funcionario_id).order_by(Atualizacao.data.desc()).all()

    positivas = sum(1 for a in atualizacoes if a.tipo == 'positiva')
    negativas = sum(1 for a in atualizacoes if a.tipo == 'negativa')

    return render_template('ver_atualizacoes.html', funcionario=funcionario,
                           atualizacoes=atualizacoes, positivas=positivas, negativas=negativas)


# Execução local
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

