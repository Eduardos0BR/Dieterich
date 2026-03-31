"""
Registro de rotas — Dieterich
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from extensions import db
from models import Produto, Depoimento, Categoria, Contato


# ── Blueprint principal (páginas HTML) ─────────────────────────────────────
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing page principal — renderiza base.html com dados do banco."""
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.id).all()
    destaques = (
        Produto.query
        .filter_by(ativo=True, destaque=True)
        .order_by(Produto.rank_destaque)
        .all()
    )
    depoimentos = (
        Depoimento.query
        .filter_by(aprovado=True)
        .order_by(Depoimento.criado_em.desc())
        .limit(3)
        .all()
    )
    categorias = Categoria.query.filter_by(ativo=True).all()

    config = current_app.config
    return render_template(
        "index.html",
        produtos=produtos,
        destaques=destaques,
        depoimentos=depoimentos,
        categorias=categorias,
        whatsapp=config["WHATSAPP_NUMBER"],
        store_address=config["STORE_ADDRESS"],
        store_phone=config["STORE_PHONE"],
        store_email=config["STORE_EMAIL"],
        store_hours=config["STORE_HOURS"],
        maps_url=config["GOOGLE_MAPS_URL"],
    )


@main_bp.route("/contato", methods=["POST"])
def contato_post():
    """Recebe o formulário de contato e salva no banco."""
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    telefone = request.form.get("telefone", "").strip()
    mensagem = request.form.get("mensagem", "").strip()

    erros = []
    if not nome:
        erros.append("Nome é obrigatório.")
    if not email or "@" not in email:
        erros.append("E-mail inválido.")
    if not mensagem:
        erros.append("Mensagem é obrigatória.")

    if erros:
        flash("; ".join(erros), "erro")
        return redirect(url_for("main.index") + "#contato")

    novo = Contato(nome=nome, email=email, telefone=telefone, mensagem=mensagem)
    db.session.add(novo)
    db.session.commit()

    flash("Mensagem enviada com sucesso! Entraremos em contato em breve. 🧡", "sucesso")
    return redirect(url_for("main.index") + "#contato")


# ── Blueprint da API REST (JSON) ───────────────────────────────────────────
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/produtos", methods=["GET"])
def api_produtos():
    """Lista todos os produtos ativos.
    Query params: ?categoria=<slug>&destaque=true
    """
    query = Produto.query.filter_by(ativo=True)

    categoria_slug = request.args.get("categoria")
    if categoria_slug:
        cat = Categoria.query.filter_by(slug=categoria_slug, ativo=True).first()
        if cat:
            query = query.filter_by(categoria_id=cat.id)

    if request.args.get("destaque") == "true":
        query = query.filter_by(destaque=True).order_by(Produto.rank_destaque)

    produtos = query.order_by(Produto.id).all()
    return jsonify([p.to_dict() for p in produtos])


@api_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def api_produto_detalhe(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return jsonify(produto.to_dict())


@api_bp.route("/depoimentos", methods=["GET"])
def api_depoimentos():
    """Lista depoimentos aprovados."""
    deps = (
        Depoimento.query
        .filter_by(aprovado=True)
        .order_by(Depoimento.criado_em.desc())
        .all()
    )
    return jsonify([d.to_dict() for d in deps])


@api_bp.route("/depoimentos", methods=["POST"])
def api_depoimento_criar():
    """Recebe novo depoimento (aguarda aprovação)."""
    data = request.get_json(silent=True) or {}
    nome = data.get("nome", "").strip()
    texto = data.get("texto", "").strip()
    estrelas = int(data.get("estrelas", 5))
    descricao_cliente = data.get("descricao_cliente", "").strip()

    if not nome or not texto:
        return jsonify({"erro": "nome e texto são obrigatórios"}), 400
    if not (1 <= estrelas <= 5):
        return jsonify({"erro": "estrelas deve ser entre 1 e 5"}), 400

    dep = Depoimento(
        nome=nome,
        texto=texto,
        estrelas=estrelas,
        descricao_cliente=descricao_cliente,
        aprovado=False,  # aguarda moderação
    )
    db.session.add(dep)
    db.session.commit()
    return jsonify({"mensagem": "Depoimento enviado! Aguarda aprovação.", "id": dep.id}), 201


@api_bp.route("/categorias", methods=["GET"])
def api_categorias():
    cats = Categoria.query.filter_by(ativo=True).all()
    return jsonify([c.to_dict() for c in cats])


@api_bp.route("/contato", methods=["POST"])
def api_contato():
    """Endpoint JSON para contato via fetch/AJAX."""
    data = request.get_json(silent=True) or {}
    nome = data.get("nome", "").strip()
    email = data.get("email", "").strip()
    telefone = data.get("telefone", "").strip()
    mensagem = data.get("mensagem", "").strip()

    if not nome or not email or not mensagem:
        return jsonify({"erro": "nome, email e mensagem são obrigatórios"}), 400

    novo = Contato(nome=nome, email=email, telefone=telefone, mensagem=mensagem)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Contato recebido com sucesso!"}), 201


# ── Blueprint de administração simples ─────────────────────────────────────
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
def admin_index():
    total_produtos = Produto.query.filter_by(ativo=True).count()
    total_contatos = Contato.query.count()
    nao_lidos = Contato.query.filter_by(lido=False).count()
    pendentes = Depoimento.query.filter_by(aprovado=False).count()
    return render_template(
        "admin/index.html",
        total_produtos=total_produtos,
        total_contatos=total_contatos,
        nao_lidos=nao_lidos,
        pendentes=pendentes,
    )


@admin_bp.route("/contatos")
def admin_contatos():
    contatos = Contato.query.order_by(Contato.criado_em.desc()).all()
    return render_template("admin/contatos.html", contatos=contatos)


@admin_bp.route("/contatos/<int:cid>/lido", methods=["POST"])
def admin_marcar_lido(cid):
    c = Contato.query.get_or_404(cid)
    c.lido = True
    db.session.commit()
    return redirect(url_for("admin.admin_contatos"))


@admin_bp.route("/depoimentos")
def admin_depoimentos():
    deps = Depoimento.query.order_by(Depoimento.criado_em.desc()).all()
    return render_template("admin/depoimentos.html", depoimentos=deps)


@admin_bp.route("/depoimentos/<int:did>/aprovar", methods=["POST"])
def admin_aprovar(did):
    d = Depoimento.query.get_or_404(did)
    d.aprovado = True
    db.session.commit()
    return redirect(url_for("admin.admin_depoimentos"))


@admin_bp.route("/depoimentos/<int:did>/rejeitar", methods=["POST"])
def admin_rejeitar(did):
    d = Depoimento.query.get_or_404(did)
    db.session.delete(d)
    db.session.commit()
    return redirect(url_for("admin.admin_depoimentos"))


# ── Registro de todos os blueprints ────────────────────────────────────────
def register_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500
