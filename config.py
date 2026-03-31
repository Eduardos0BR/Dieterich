import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ── Segurança ──────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-troque-em-producao")

    # ── Banco de dados (SQLite por padrão) ─────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'dieterich.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── E-mail (configurar em produção) ───────────────────
    MAIL_FROM = os.environ.get("MAIL_FROM", "contato@dieterich.com.br")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@dieterich.com.br")

    # ── WhatsApp ──────────────────────────────────────────
    WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "5547999999999")

    # ── Loja ──────────────────────────────────────────────
    STORE_NAME = "Dieterich Produtos de Limpeza"
    STORE_ADDRESS = "Rua Exemplo, 123 — Centro, Rio do Sul – SC"
    STORE_PHONE = "(47) 9 9999-9999"
    STORE_EMAIL = "contato@dieterich.com.br"
    STORE_HOURS = "Seg a Sex: 8h–18h | Sábado: 8h–12h"
    GOOGLE_MAPS_URL = "https://maps.google.com"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
