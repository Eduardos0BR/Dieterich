"""
Modelos do banco de dados — Dieterich
"""

from datetime import datetime
from extensions import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    emoji = db.Column(db.String(10), default="🧴")
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    produtos = db.relationship("Produto", back_populates="categoria", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "slug": self.slug,
            "emoji": self.emoji,
        }

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=True)          # None = "Sob consulta"
    preco_label = db.Column(db.String(60), nullable=True)  # ex: "A partir de R$ 12,90"
    emoji = db.Column(db.String(10), default="🧴")
    tag = db.Column(db.String(40), nullable=True)       # "Mais Vendido", "Novidade", etc.
    destaque = db.Column(db.Boolean, default=False)     # aparece em "mais vendidos"
    rank_destaque = db.Column(db.Integer, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=True)
    categoria = db.relationship("Categoria", back_populates="produtos")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "preco_label": self.preco_label or ("Sob consulta" if self.preco is None else f"R$ {self.preco:.2f}"),
            "emoji": self.emoji,
            "tag": self.tag,
            "destaque": self.destaque,
            "rank_destaque": self.rank_destaque,
            "categoria": self.categoria.nome if self.categoria else None,
        }

    def __repr__(self):
        return f"<Produto {self.nome}>"


class Depoimento(db.Model):
    __tablename__ = "depoimentos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao_cliente = db.Column(db.String(150), nullable=True)  # "Cliente há 3 anos"
    texto = db.Column(db.Text, nullable=False)
    estrelas = db.Column(db.Integer, default=5)
    iniciais = db.Column(db.String(3), nullable=True)   # geradas automaticamente
    aprovado = db.Column(db.Boolean, default=False)     # moderação
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.iniciais and self.nome:
            partes = self.nome.strip().split()
            self.iniciais = "".join(p[0].upper() for p in partes[:2])

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao_cliente": self.descricao_cliente,
            "texto": self.texto,
            "estrelas": self.estrelas,
            "iniciais": self.iniciais,
        }

    def __repr__(self):
        return f"<Depoimento de {self.nome}>"


class Contato(db.Model):
    __tablename__ = "contatos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(30), nullable=True)
    mensagem = db.Column(db.Text, nullable=False)
    lido = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "mensagem": self.mensagem,
            "lido": self.lido,
            "criado_em": self.criado_em.strftime("%d/%m/%Y %H:%M"),
        }

    def __repr__(self):
        return f"<Contato {self.nome} — {self.email}>"
