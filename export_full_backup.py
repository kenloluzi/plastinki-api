import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def export_table(conn, table_name, filename):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    # Получаем имена колонок
    colnames = [desc[0] for desc in cur.description]
    data = []
    for row in rows:
        record = dict(zip(colnames, row))
        # Преобразуем datetime в строку для JSON
        for k, v in record.items():
            if hasattr(v, 'isoformat'):
                record[k] = v.isoformat()
        data.append(record)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    print(f"✅ {table_name}: {len(data)} записей сохранено в {filename}")

if __name__ == '__main__':
    print("📦 Начинаю экспорт всех данных...")
    conn = psycopg2.connect(DATABASE_URL)
    export_table(conn, 'users', 'users_backup.json')
    export_table(conn, 'records', 'records_backup.json')
    export_table(conn, 'orders', 'orders_backup.json')
    export_table(conn, 'order_items', 'order_items_backup.json')
    conn.close()
    print("🎉 Полный бэкап завершён!")