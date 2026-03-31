"""
Popula o banco com dados iniciais (roda apenas uma vez).
"""

from extensions import db
from models import Categoria, Produto, Depoimento


def seed_initial_data():
    # Só executa se o banco estiver vazio
    if Categoria.query.count() > 0:
        return

    # ── Categorias ─────────────────────────────────────────────────────────
    cats = [
        Categoria(nome="Limpeza Geral",       slug="limpeza-geral",    emoji="🧹"),
        Categoria(nome="Cozinha",             slug="cozinha",          emoji="🍳"),
        Categoria(nome="Banheiro",            slug="banheiro",         emoji="🚿"),
        Categoria(nome="Roupas & Lavanderia", slug="lavanderia",       emoji="👕"),
        Categoria(nome="Linha Profissional",  slug="profissional",     emoji="🏭"),
    ]
    db.session.add_all(cats)
    db.session.flush()  # gera IDs

    cat_map = {c.slug: c for c in cats}

    # ── Produtos ───────────────────────────────────────────────────────────
    produtos = [
        Produto(
            nome="Desengordurante Profissional",
            descricao="Potente, rápido e seguro. Remove gordura de cozinha, fogão e panelas com facilidade surpreendente.",
            preco=12.90,
            preco_label="A partir de R$ 12,90",
            emoji="🧴",
            tag="Mais Vendido",
            destaque=True,
            rank_destaque=1,
            categoria=cat_map["cozinha"],
        ),
        Produto(
            nome="Limpadores Multiuso",
            descricao="Uma solução, mil superfícies. Ideal para banheiro, cozinha, pisos e vidros. Cheiro fresco o dia todo.",
            preco=8.90,
            preco_label="A partir de R$ 8,90",
            emoji="🪣",
            categoria=cat_map["limpeza-geral"],
        ),
        Produto(
            nome="Kits de Vassoura & Rodo",
            descricao="Equipamentos duráveis, ergonômicos e com acabamento premium. Limpeza eficiente e sem esforço.",
            preco=29.90,
            preco_label="A partir de R$ 29,90",
            emoji="🧹",
            tag="Novidade",
            categoria=cat_map["limpeza-geral"],
        ),
        Produto(
            nome="Detergentes & Sabões",
            descricao="Para a louça que brilha, as mãos que agradecem. Variedade de aromas e fórmulas para todo bolso.",
            preco=3.50,
            preco_label="A partir de R$ 3,50",
            emoji="🫧",
            categoria=cat_map["cozinha"],
        ),
        Produto(
            nome="Produtos para Banheiro",
            descricao="Sanitizantes, removedores de calcário e desinfetantes potentes que eliminam germes e manchas.",
            preco=9.90,
            preco_label="A partir de R$ 9,90",
            emoji="🧼",
            tag="Promoção",
            categoria=cat_map["banheiro"],
        ),
        Produto(
            nome="Linha Profissional",
            descricao="Para empresas, condomínios, restaurantes e estabelecimentos que exigem limpeza de alta performance.",
            preco=None,
            preco_label="Sob consulta",
            emoji="🏭",
            categoria=cat_map["profissional"],
        ),
        # Mais vendidos (destaques no ranking)
        Produto(
            nome="Ypê Multiuso Lavanda 500ml",
            descricao="Cheiro inconfundível, eficiência total. O favorito das donas de casa.",
            preco=7.90,
            preco_label="R$ 7,90",
            emoji="🧴",
            destaque=True,
            rank_destaque=1,
            categoria=cat_map["limpeza-geral"],
        ),
        Produto(
            nome="Água Sanitária 2L",
            descricao="Desinfecção completa para toda a casa. Essencial no dia a dia.",
            preco=6.50,
            preco_label="R$ 6,50",
            emoji="🫙",
            destaque=True,
            rank_destaque=2,
            categoria=cat_map["limpeza-geral"],
        ),
        Produto(
            nome="Esponjas Scotch-Brite Pack 4un",
            descricao="Dura mais, limpa melhor. Sem arriscar arranhar suas panelas.",
            preco=12.00,
            preco_label="R$ 12,00",
            emoji="🧽",
            destaque=True,
            rank_destaque=3,
            categoria=cat_map["cozinha"],
        ),
        Produto(
            nome="Ariel Líquido Concentrado 3L",
            descricao="Roupas mais brancas, mais coloridas e com perfume duradouro.",
            preco=34.90,
            preco_label="R$ 34,90",
            emoji="🪴",
            destaque=True,
            rank_destaque=4,
            categoria=cat_map["lavanderia"],
        ),
    ]
    db.session.add_all(produtos)

    # ── Depoimentos ────────────────────────────────────────────────────────
    deps = [
        Depoimento(
            nome="Maria José Ramos",
            descricao_cliente="Cliente há 3 anos",
            texto="Nunca mais precisei ir ao supermercado buscar produto de limpeza. A Dieterich entrega em casa, o atendimento é ótimo e os preços são muito bons. Recomendo demais!",
            estrelas=5,
            aprovado=True,
        ),
        Depoimento(
            nome="Carlos Pereira",
            descricao_cliente="Empresário — Restaurante do Carlão",
            texto="Compro para o meu restaurante. Eles me ajudaram a escolher os produtos certos para a cozinha industrial e o custo-benefício é excelente. Parceria de confiança!",
            estrelas=5,
            aprovado=True,
        ),
        Depoimento(
            nome="Ana Souza",
            descricao_cliente="Cliente — Bairro Centro",
            texto="Simplesmente amei! Me indicaram um desengordurante que nunca havia usado e mudou minha vida. Minha cozinha nunca ficou tão limpa. Voltei na semana seguinte!",
            estrelas=5,
            aprovado=True,
        ),
    ]
    db.session.add_all(deps)
    db.session.commit()
    print("✅  Banco populado com dados iniciais.")
