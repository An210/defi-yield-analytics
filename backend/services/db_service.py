
import sqlite3
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "pools.db")

def register_email(email):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS alerts (email TEXT PRIMARY KEY)")
        cursor.execute("INSERT OR IGNORE INTO alerts VALUES (?)", (email,))
        conn.commit()

def check_apy_changes():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, apy FROM pools")
            current_pools = {row[0]: row[1] for row in cursor.fetchall()}
        response = requests.get("https://yields.llama.fi/pools", timeout=10)
        response.raise_for_status()
        new_pools = response.json()["data"]
        changes = []
        for pool in new_pools:
            pool_id = pool["pool"]
            new_apy = pool["apy"]
            old_apy = current_pools.get(pool_id)
            if old_apy is not None and abs(new_apy - old_apy) > 5:
                changes.append({"name": pool["project"], "apy_change": new_apy - old_apy})
        return changes
    except Exception as e:
        logging.error(f"Error checking APY changes: {e}")
        return []

def get_all_pools():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pools")
    data = cursor.fetchall()
    conn.close()
    return data

def get_top_pools():
    response = requests.get("https://yields.llama.fi/pools")
    data = response.json()["data"]
    filtered_pools = sorted(data, key=lambda x: x["tvlUsd"], reverse=True)[:20]
    return filtered_pools
