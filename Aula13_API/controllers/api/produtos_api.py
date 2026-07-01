# Olha só: esse arquivo é a "versão API" do produtos_controller.
# Mesma ideia, mesma lógica, MESMO Model (Produto.listar, db.session.get...).
# O que muda? Na outra ponta, em vez de render_template("lista.html"),
# a gente devolve jsonify(...) — ou seja, dados crus pro cliente consumir.

from flask import Blueprint, jsonify, request

from models import Produto, db

# Blueprint separado com prefixo /api — fica claro: tudo daqui é JSON, não HTML.
api_produtos_bp = Blueprint("api_produtos", __name__, url_prefix="/api")


@api_produtos_bp.route("/produtos", methods=["GET"])
def listar():
    # Isso aqui é IGUALZINHO ao controller HTML: busca no banco do mesmo jeito.
    produtos = Produto.listar()

    # Lá no produtos_controller.py seria:
    #   return render_template("produtos/lista.html", produtos=produtos)
    # Aqui a gente troca a View HTML por JSON. Sem Jinja, sem tabela bonitinha —
    # só a lista de dicts que o Postman, o React ou qualquer app consegue ler.
    return jsonify([p.para_dict() for p in produtos])


@api_produtos_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def detalhe(produto_id):
    produto = db.session.get(Produto, produto_id)

    if not produto:
        # No HTML a gente renderizava nao_encontrado.html com status 404.
        # Na API não tem página de erro — manda um JSON explicando e pronto.
        return jsonify({"erro": "Produto não encontrado"}), 404

    # De novo: render_template("detalhe.html", produto=produto)  →  jsonify(...)
    return jsonify(produto.para_dict())


@api_produtos_bp.route("/produtos", methods=["POST"])
def criar():
    # Formulário HTML? request.form["nome"]
    # API REST? request.get_json() — o body vem em JSON, não em <input name="...">
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Envie JSON no body (Content-Type: application/json)"}), 400

    try:
        produto = Produto(
            nome=str(dados["nome"]).strip(),
            preco=float(dados["preco"]),
            estoque=int(dados.get("estoque", 0)),
        )
    except (KeyError, ValueError, TypeError):
        return jsonify({"erro": "Campos obrigatórios: nome, preco"}), 400

    if not produto.nome:
        return jsonify({"erro": "Nome não pode ser vazio"}), 400

    # Model continua igual — add, commit, mesma coisa de sempre.
    db.session.add(produto)
    db.session.commit()

    # 201 = "criei um recurso novo" (REST fala assim).
    # Em HTML você redirecionaria pro detalhe; aqui devolve o objeto criado em JSON.
    return jsonify(produto.para_dict()), 201


@api_produtos_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar(produto_id):
    produto = db.session.get(Produto, produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400

    # Atualiza só o que veio no JSON — o resto fica como estava.
    if "nome" in dados:
        produto.nome = str(dados["nome"]).strip()
    if "preco" in dados:
        produto.preco = float(dados["preco"])
    if "estoque" in dados:
        produto.estoque = int(dados["estoque"])

    db.session.commit()

    # Sem redirect, sem flash message — só o produto atualizado em JSON.
    return jsonify(produto.para_dict())


@api_produtos_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def excluir(produto_id):
    produto = db.session.get(Produto, produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    db.session.delete(produto)
    db.session.commit()

    # 204 = deu certo, mas não tem corpo na resposta (nada de HTML "foi excluído!").
    return "", 204
