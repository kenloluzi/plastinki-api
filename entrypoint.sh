#!/bin/sh
set -e

# Функция проверки, есть ли данные в таблице records
check_db_populated() {
    python -c "
from app import create_app
from app.models import Record
app = create_app()
with app.app_context():
    # Создадим таблицы, если их нет (безопасно)
    from app.extensions import db
    db.create_all()
    count = Record.query.count()
    exit(0 if count > 0 else 1)
" 2>/dev/null
}

echo ">>> Checking if database is already populated..."
if check_db_populated; then
    echo ">>> Database already contains records. Skipping seed."
else
    echo ">>> Database is empty. Running seed.py..."
    python seed.py
fi

echo ">>> Starting gunicorn on :5000"
exec gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'