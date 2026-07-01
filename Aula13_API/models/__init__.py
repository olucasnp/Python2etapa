from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .produto import Produto

__all__ = ["db", "ModeloBase", "Produto"]
