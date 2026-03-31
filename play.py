python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edite o .env com seus dados
python app.py          # http://localhost:5000