import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "alunos.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    alunos = Aluno.query.all()
    return render_template("lista.html", alunos=alunos)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if not nome or not email:
            return render_template(
                "formulario.html",
                titulo="Novo aluno",
                erro="Preencha nome e e-mail.",
                nome=nome,
                email=email,
            )

        aluno = Aluno(nome=nome, email=email)
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("formulario.html", titulo="Novo aluno")


@app.route("/editar/<int:aluno_id>", methods=["GET", "POST"])
def editar(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        if not nome or not email:
            return render_template(
                "formulario.html",
                titulo="Editar aluno",
                erro="Preencha nome e e-mail.",
                aluno_id=aluno.id,
                nome=nome,
                email=email,
            )

        aluno.nome = nome
        aluno.email = email
        db.session.commit()
        return redirect(url_for("index"))

    return render_template(
        "formulario.html",
        titulo="Editar aluno",
        aluno_id=aluno.id,
        nome=aluno.nome,
        email=aluno.email,
    )


@app.route("/excluir/<int:aluno_id>", methods=["POST"])
def excluir(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
