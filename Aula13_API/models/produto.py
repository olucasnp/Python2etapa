from . import db
from .base import ModeloBase


class Produto(ModeloBase):
    __tablename__ = "produtos"

    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0, nullable=False)

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.nome).all()

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "estoque": self.estoque,
            "data_criacao": str(self.data_criacao),
        }
