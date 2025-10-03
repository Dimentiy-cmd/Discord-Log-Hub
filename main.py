import os
import sys
import string
import random
import sqlite3
import importlib
import subprocess

from loguru import logger

if not os.path.exists("data"):
    os.mkdir("data")

if os.path.exists("config.py"):
    config = importlib.import_module("config")
    TOKEN = config.TOKEN
    if TOKEN == "":
        logger.error("ОШИБКА | Не указан токен бота!")
        sys.exit(1)
else:
    logger.error("ОШИБКА | Файл конфига не найден!")
    sys.exit(1)

if sys.platform == "win32":
    db_path = "data/data.db"
elif sys.platform == "linux":
    db_path = "/data/data.db"
elif sys.platform == "darwin":
    db_path = "data/data.db"

connection = sqlite3.connect(db_path, check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

def use_embed(guild_id):
    cursor.execute("SELECT use_embed FROM settings WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()
    if result is None:
        return True
    return bool(result["use_embed"])

def get_system_color(guild_id):
    cursor.execute("SELECT system_color FROM settings WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()
    return int(result[0].lstrip('#'), 16)

def generate_password():
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(8))
    return password

def sanitize_input(input_string, max_length=255):
    if not input_string:
        return ""
    return str(input_string).strip()[:max_length]

if __name__ == "__main__":
    try:
        flask_proc = subprocess.Popen(["python", "web.py"])
        bot_proc = subprocess.Popen(["python", "bot.py"])

        flask_proc.wait()
        bot_proc.wait()
    except KeyboardInterrupt:
        pass
