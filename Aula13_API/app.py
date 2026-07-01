import os

from flask import Flask, redirect, url_for

from controllers import api_produtos_bp, produtos_bp
from models import Produto, db

DADOS_INICIAIS = [
    ("Mouse USB", 49.90, 30),
    ("Teclado mecânico", 299.00, 12),
    ("Monitor 24\"", 899.00, 5),
    ("Webcam HD", 159.90, 20),
]


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "loja.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "aula13-api-rest-dev"

    db.init_app(app)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(api_produtos_bp)

    with app.app_context():
        db.create_all()
        if Produto.query.count() == 0:
            for nome, preco, estoque in DADOS_INICIAIS:
                db.session.add(Produto(nome=nome, preco=preco, estoque=estoque))
            db.session.commit()

    @app.route("/")
    def index():
        return redirect(url_for("produtos.lista"))

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
