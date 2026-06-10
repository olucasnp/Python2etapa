from flask import Flask, render_template
app = Flask(__name__)

Dado_usuario = {"nome": "Ana", "email": "ana@email.com"}
Alunos = {'Lucas', 'Davi', 'Caio', 'Bernardo'}
Notas = {}

@app.route('/')
def index():
    return render_template('layout.html', nome ='Lucas', idade = '17', Dado_usuario = Dado_usuario, Alunos = Alunos, Nota=5)

if __name__ == '__main__':
    app.run(debug=True)
