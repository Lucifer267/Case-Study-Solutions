Setup

python -m venv venv
source venv/bin/activate  (Windows: venv\Scripts\activate)
pip install -r requirements.txt

-- Seed Database
python seed.py

-- Run Server
python app.py

-- Test Endpoint
GET http://127.0.0.1:5000/api/companies/1/alerts/low-stock
