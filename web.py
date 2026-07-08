import os
import hashlib

from loguru import logger
from functools import wraps
from main import connection, cursor, generate_password, sanitize_input
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SECURE=False, SESSION_COOKIE_SAMESITE="Lax")

def checklogin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'user_id' in session:
            return redirect(url_for('index'))

        try:
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_info = cursor.fetchone()
            if user_info:
                hash = hashlib.sha256(password.encode()).hexdigest()
                if user_info['password'] == hash:
                    session['user_id'] = user_info['user_id']
                    session['lvl'] = user_info['lvl']
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error="Неверный пароль")
            else:
                return render_template('login.html', error="Пользователь не найден")

        except Exception as e:
            logger.error(f"Ошибка при входе в систему: {e}")
            cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
            connection.commit()
            return 500

    return render_template('login.html')

@app.route('/')
@checklogin
def index():
    try:
        query = """
            SELECT 'logs_other' AS table_name, COUNT(*) AS rows_count FROM logs_other
            UNION ALL
            SELECT 'logs_server', COUNT(*) FROM logs_server
            UNION ALL
            SELECT 'logs_members', COUNT(*) FROM logs_members
            UNION ALL
            SELECT 'logs_messages', COUNT(*) FROM logs_messages;
        """
        results = cursor.execute(query).fetchall()
        counts = {row["table_name"]: row["rows_count"] for row in results}

        cursor.execute("SELECT COUNT(*) FROM errors")
        total_errors = cursor.fetchone()[0]
        users = cursor.execute("SELECT user_id, username, discriminator, avatar_url, lvl FROM users LIMIT 20;").fetchall()
        return render_template('index.html', total=sum(counts.values()), total_errors=total_errors, users=users)

    except Exception as e:
        logger.error(f"Ошибка главной страницы: {e}")
        cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
        connection.commit()
        return 500

@app.route('/delete_user', methods=['POST'])
@checklogin
def delete_user():
    try:
        cursor.execute("SELECT lvl FROM users WHERE user_id = ?", (session['user_id'],))
        user_lvl = cursor.fetchone()[0]
        if user_lvl == 2:
            user_id = request.form.get('user_id')
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            connection.commit()
            return "Успех! " + user_id
        else:
            return "Отказ в доступе"

    except Exception as e:
        logger.error(f"Ошибка при удалении пользователя: {e}")
        cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
        connection.commit()
        return 500

@app.route('/reset_pass', methods=['POST'])
@checklogin
def reset_pass():
    try:
        cursor.execute("SELECT lvl FROM users WHERE user_id = ?", (session['user_id'],))
        user_lvl = cursor.fetchone()[0]
        if user_lvl == 2:
            user_id = request.form.get('user_id')
            new = generate_password()
            hash = hashlib.sha256(new.encode()).hexdigest()
            cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (hash, int(user_id)))
            connection.commit()
            return "Успех! Новый пароль: " + new
        else:
            return "Отказ в доступе"

    except Exception as e:
        logger.error(f"Ошибка сброса паролья пользователя: {e}")
        cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
        connection.commit()
        return 500

@app.route('/logs')
@checklogin
def logs():
    return render_template('logs.html')

@app.route('/logs/messages')
@checklogin
def logs_messages():
    try:
        query = "SELECT * FROM logs_messages WHERE 1=1"
        params = []

        username = sanitize_input(request.args.get("username", ""), 100)
        user_id = sanitize_input(request.args.get("user_id", ""), 50)
        action_type = sanitize_input(request.args.get("action_type", ""), 20)
        content = sanitize_input(request.args.get("content", ""), 200)

        if username:
            query += " AND username LIKE ?"
            params.append(f"%{username}%")
        if user_id and user_id.isdigit():
            query += " AND user_id = ?"
            params.append(user_id)
        if action_type in ['DELETE', 'EDIT']:
            query += " AND action_type = ?"
            params.append(action_type)
        if content:
            query += " AND (old_content LIKE ? OR new_content LIKE ?)"
            params.extend([f"%{content}%", f"%{content}%"])

        query += " ORDER BY created_at DESC LIMIT 100"
        cursor.execute(query, params)
        logs = cursor.fetchall()
        return render_template("logs/messages.html", logs=logs)

    except Exception as e:
        logger.error(f"Ошибка вывода логов сообщений: {e}")
        cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
        connection.commit()
        return 500

@app.route('/logs/members')
@checklogin
def logs_members():
    try:
        query = "SELECT * FROM logs_members WHERE 1=1"
        params = []

        username = sanitize_input(request.args.get("username", ""), 100)
        user_id = sanitize_input(request.args.get("user_id", ""), 50)
        action_type = sanitize_input(request.args.get("action_type", ""), 20)

        if username:
            query += " AND username LIKE ?"
            params.append(f"%{username}%")
        if user_id and user_id.isdigit():
            query += " AND user_id = ?"
            params.append(user_id)
        if action_type in ['JOIN', 'LEAVE', 'BAN', 'UNBAN', 'EDITNICK']:
            query += " AND action_type = ?"
            params.append(action_type)

        query += " ORDER BY created_at DESC LIMIT 100"
        cursor.execute(query, params)
        logs = cursor.fetchall()
        return render_template("logs/members.html", logs=logs)

    except Exception as e:
        logger.error(f"Ошибка вывода логов участников: {e}")
        cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
        connection.commit()
        return 500

@app.route("/logs/server")
@checklogin
def logs_server():
    try:
        query = "SELECT * FROM logs_server WHERE 1=1"
        params = []

        username = sanitize_input(request.args.get("username", ""), 100)
        user_id = sanitize_input(request.args.get("user_id", ""), 50)
        action_type = sanitize_input(request.args.get("action_type", ""), 20)

        if username:
            query += " AND username LIKE ?"
            params.append(f"%{username}%")
        if user_id and user_id.isdigit():
            query += " AND user_id = ?"
            params.append(user_id)
        if action_type in ['EDITROLE', 'EDITCHANNEL', 'VOICECHANNEL', 'INVITES']:
            query += " AND action_type = ?"
            params.append(action_type)

        query += " ORDER BY created_at DESC LIMIT 100"
        cursor.execute(query, params)
        logs = cursor.fetchall()
        return render_template("logs/server.html", logs=logs)

    except Exception as e:
        logger.error(f"Ошибка вывода логов сервера: {e}")
        cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
        connection.commit()
        return 500

@app.route("/logs/other")
@checklogin
def logs_other():
    try:
        query = "SELECT * FROM logs_other WHERE 1=1"
        params = []

        username = sanitize_input(request.args.get("username", ""), 100)
        user_id = sanitize_input(request.args.get("user_id", ""), 50)
        action_type = sanitize_input(request.args.get("action_type", ""), 20)

        if username:
            query += " AND username LIKE ?"
            params.append(f"%{username}%")
        if user_id and user_id.isdigit():
            query += " AND user_id = ?"
            params.append(user_id)
        if action_type in ['USECOMMAND', 'EDITEMOJI', 'EDITSTICKER']:
            query += " AND action_type = ?"
            params.append(action_type)

        query += " ORDER BY created_at DESC LIMIT 100"
        cursor.execute(query, params)
        logs = cursor.fetchall()
        return render_template("logs/other.html", logs=logs)

    except Exception as e:
        logger.error(f"Ошибка вывода прочих логов: {e}")
        cursor.execute("INSERT INTO errors (error) VALUES (?)", (str(e),))
        connection.commit()
        return 500

@app.route("/settings")
@checklogin
def settings():
    cursor.execute("SELECT * FROM settings LIMIT 1")
    settings = cursor.fetchone()
    return render_template('settings.html', settings=settings)

@app.route('/logout')
@checklogin
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)

if __name__ == "__main__":
    run_flask()
