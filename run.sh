python freeze.py
cp build/index.html .
export FLASK_ENV=development
export FLASK_APP=main.py
flask run