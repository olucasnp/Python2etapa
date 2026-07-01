from datetime import datetime
from . import db


class Operacao(db.Model):
    """Model — dados e acesso ao banco (tabela operacoes)."""
    __tablename__ = "operacoes"

    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Float, nullable=False)
    num2 = db.Column(db.Float, nullable=False)
    operacao = db.Column(db.String(50), nullable=False)
    etapas = db.Column(db.String(200), nullable=False)
    resultado = db.Column(db.String(100), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def salvar(cls, num1, num2, operacao, etapas, resultado):
        registro = cls(
            num1=num1,
            num2=num2,
            operacao=operacao,
            etapas=etapas,
            resultado=str(resultado),
        )
        db.session.add(registro)  # corrigido: add(registro), não add(cls)
        db.session.commit()

    @classmethod
    def listar_recentes(cls, limite=10):
        return (
            cls.query.order_by(cls.criado_em.desc()).limit(limite).all()
        )

    def __repr__(self):
        return f"<Operacao {self.id}: {self.etapas}>"