# Esse aqui é o controller "de humano" — quem abre no navegador e vê página bonita.
# A lógica de buscar dados é a MESMA do produtos_api.py (mesmo Model, mesmo banco).
# A diferença tá só no final: render_template em vez de jsonify.

from flask import Blueprint, render_template

from models import Produto, db

# Prefixo /produtos — rotas HTML. A API paralela mora em /api/produtos (outro Blueprint).
produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")


@produtos_bp.route("/")
def lista():
    # Olha: Produto.listar() — idêntico ao GET /api/produtos. Copia e cola a consulta.
    produtos = Produto.listar()

    # Aqui entra a View! Flask monta o HTML com Jinja (tabela, links, CSS...).
    # Na API seria: return jsonify([p.para_dict() for p in produtos])
    # Resumindo: mesmos produtos, saída diferente — página vs JSON.
    return render_template("produtos/lista.html", produtos=produtos)


@produtos_bp.route("/<int:produto_id>")
def detalhe(produto_id):
    produto = db.session.get(Produto, produto_id)

    if not produto:
        # 404 com template — o usuário vê uma página amigável "não encontrado".
        # Na API: return jsonify({"erro": "Produto não encontrado"}), 404  (sem HTML).
        return render_template("produtos/nao_encontrado.html", produto_id=produto_id), 404

    # Passa o objeto pro template; Jinja usa {{ produto.nome }}, {{ produto.preco }}, etc.
    # Equivalente na API: return jsonify(produto.para_dict())
    return render_template("produtos/detalhe.html", produto=produto)
