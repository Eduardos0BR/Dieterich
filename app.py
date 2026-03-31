"""
Dieterich — Loja de Produtos de Limpeza
Backend Flask
"""

from flask import Flask
from config import Config
from extensions import db
from routes import register_routes


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensões
    db.init_app(app)

    # Registra blueprints/rotas
    register_routes(app)

    # Cria tabelas se não existirem
    with app.app_context():
        db.create_all()
        from seed import seed_initial_data
        seed_initial_data()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
