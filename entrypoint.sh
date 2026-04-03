#!/bin/sh
set -e

echo "Waiting for database..."

python - <<'PY'
import os
import time
import pymysql

host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "3306"))
user = os.getenv("DB_USER", "root")
password = os.getenv("DB_PASSWORD", "123456")
database = os.getenv("DB_NAME", "support_demo")

for i in range(30):
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        conn.close()
        print("Database is ready.")
        break
    except Exception:
        print(f"Database not ready, retrying... ({i + 1}/30)")
        time.sleep(2)
else:
    raise SystemExit("Database did not become ready in time.")
PY

python init_db.py
python run.py