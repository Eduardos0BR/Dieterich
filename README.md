# Dieterich — Backend Flask

Backend completo para a landing page da Dieterich Produtos de Limpeza.

## Estrutura do Projeto

```
dieterich/
├── app.py              # Entry point — cria e inicia a aplicação
├── config.py           # Configurações (dev, prod, test)
├── extensions.py       # Instâncias das extensões Flask (SQLAlchemy)
├── models.py           # Modelos do banco de dados (ORM)
├── routes.py           # Todas as rotas: site, API REST e admin
├── seed.py             # Dados iniciais do banco
├── requirements.txt    # Dependências Python
├── .env.example        # Variáveis de ambiente (copie para .env)
│
├── templates/
│   ├── base.html       # Layout base com nav e footer dinâmicos
│   ├── index.html      # Landing page completa (usa dados do banco)
│   ├── 404.html        # Página de erro 404
│   ├── 500.html        # Página de erro 500
│   └── admin/
│       ├── index.html       # Painel administrativo
│       ├── contatos.html    # Lista e gerência de contatos
│       └── depoimentos.html # Moderação de depoimentos
│
└── static/
    ├── css/
    │   └── styles.css   # Estilos da landing page
    ├── js/              # Scripts extras (opcional)
    └── img/             # Imagens e favicon
```

## Instalação e Execução

### 1. Clone ou copie os arquivos

```bash
cd dieterich
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com seus dados reais
```

### 5. Execute o servidor

```bash
python app.py
```

Acesse: **http://localhost:5000**

---

## Rotas Disponíveis

### Site
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Landing page principal |
| POST | `/contato` | Recebe formulário de contato (form HTML) |

### API REST (JSON)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/produtos` | Lista produtos (`?categoria=slug&destaque=true`) |
| GET | `/api/produtos/<id>` | Detalhe de um produto |
| GET | `/api/categorias` | Lista categorias |
| GET | `/api/depoimentos` | Lista depoimentos aprovados |
| POST | `/api/depoimentos` | Envia novo depoimento (aguarda moderação) |
| POST | `/api/contato` | Envia contato via JSON (AJAX) |

### Admin
| Rota | Descrição |
|------|-----------|
| `/admin/` | Painel com resumo |
| `/admin/contatos` | Lista contatos recebidos |
| `/admin/depoimentos` | Modera depoimentos (aprovar / rejeitar) |

---

## Banco de Dados

O projeto usa **SQLite** por padrão (arquivo `instance/dieterich.db`).  
Para produção, defina `DATABASE_URL` no `.env` apontando para PostgreSQL.

O banco é criado e populado automaticamente na primeira execução.

### Modelos

- **Categoria** — categorias de produtos
- **Produto** — catálogo com preço, emoji, tag e flag de destaque
- **Depoimento** — avaliações com moderação (aprovado/pendente)
- **Contato** — mensagens recebidas pelo formulário

---

## Deploy em Produção

### Com Gunicorn

```bash
pip install gunicorn
gunicorn "app:create_app()" -w 4 -b 0.0.0.0:8000
```

### Variáveis obrigatórias em produção

```
SECRET_KEY=chave-longa-e-aleatoria
DATABASE_URL=postgresql://...
```
