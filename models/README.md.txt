# Dexcom Cron (Render)

## What it does
- Pull Dexcom glucose readings
- Store in SQLite (data/dexcom.sqlite)
- Optional: run model inference (placeholder)

## Local run
1) Create .env from .env.example
2) Install:
   pip install -r requirements.txt
3) Run:
   python -u app/main.py
