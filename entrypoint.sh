#!/bin/sh
set -e

# Run schema creation + sample seed. Idempotent — safe to re-run.
i=0
until python seed.py; do
  i=$((i + 1))
  if [ "$i" -ge 10 ]; then
    echo ">>> seed.py kept failing after 10 attempts, aborting"
    exit 1
  fi
  echo ">>> seed.py failed, retrying in 2s ($i/10)..."
  sleep 2
done

echo ">>> Starting gunicorn on :5000"
exec gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
