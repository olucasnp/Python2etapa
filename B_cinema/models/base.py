# Cenário: B - Cinema
# Aluno: Lucas Nepomuceno

from datetime import datetime

from . import db


class ModeloBase(db.Model):
    """Classe base abstrata: todas as tabelas herdam id e data de criação."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
