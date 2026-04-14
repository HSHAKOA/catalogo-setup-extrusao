from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, abort, g, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "tool_catalog.json"
LEGACY_DATA_FILE = BASE_DIR / "tool_catalog.json"
DATABASE_FILE = DATA_DIR / "app.db"


app = Flask(__name__, template_folder=".", static_folder=".")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(DATABASE_FILE)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


@app.teardown_appcontext
def close_db(exception: Exception | None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )
    db.commit()


def load_catalog() -> list[dict[str, Any]]:
    source = DATA_FILE if DATA_FILE.exists() else LEGACY_DATA_FILE
    with source.open(encoding="utf-8") as file:
        tools = json.load(file)
    return sorted(tools, key=lambda item: item["code"])


def get_tool_by_code(code: str) -> dict[str, Any]:
    normalized = code.strip().upper()
    for tool in load_catalog():
        if tool["code"].upper() == normalized:
            return tool
    abort(404)


def get_user_or_404(user_id: int) -> sqlite3.Row:
    user = get_db().execute("SELECT id, username, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        abort(404, description="Usuário não encontrado.")
    return user


@app.before_request
def ensure_database() -> None:
    init_db()


@app.get("/")
def index():
    tools = load_catalog()
    return render_template("index.html", tools=tools, initial_tool=tools[0] if tools else None)


@app.get("/api/tools")
def list_tools():
    return jsonify(load_catalog())


@app.get("/api/tools/<string:code>")
def tool_details(code: str):
    return jsonify(get_tool_by_code(code))


@app.post("/api/users")
def create_user():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    if not username:
        return jsonify({"error": "O campo 'username' é obrigatório."}), 400

    db = get_db()
    try:
        cursor = db.execute("INSERT INTO users (username) VALUES (?)", (username,))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Este nome de usuário já existe."}), 409

    user = db.execute("SELECT id, username, created_at FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(dict(user)), 201


@app.get("/api/users")
def list_users():
    rows = get_db().execute(
        "SELECT id, username, created_at FROM users ORDER BY created_at DESC"
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.get("/api/users/<int:user_id>/transactions")
def list_user_transactions(user_id: int):
    get_user_or_404(user_id)
    rows = get_db().execute(
        """
        SELECT id, description, amount, type, category, date, created_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC, created_at DESC
        """,
        (user_id,),
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.post("/api/users/<int:user_id>/transactions")
def create_user_transaction(user_id: int):
    get_user_or_404(user_id)
    payload = request.get_json(silent=True) or {}

    required_fields = ["id", "description", "amount", "type", "category", "date"]
    missing = [field for field in required_fields if payload.get(field) in (None, "")]
    if missing:
        return jsonify({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}."}), 400

    tx_type = payload["type"]
    if tx_type not in {"income", "expense"}:
        return jsonify({"error": "O campo 'type' deve ser 'income' ou 'expense'."}), 400

    try:
        amount = float(payload["amount"])
    except (TypeError, ValueError):
        return jsonify({"error": "O campo 'amount' deve ser numérico."}), 400

    db = get_db()
    try:
        db.execute(
            """
            INSERT INTO transactions (id, user_id, description, amount, type, category, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(payload["id"]),
                user_id,
                str(payload["description"]).strip(),
                amount,
                tx_type,
                str(payload["category"]).strip(),
                str(payload["date"]),
            ),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Já existe uma transação com esse id para outro registro."}), 409

    created = db.execute(
        """
        SELECT id, description, amount, type, category, date, created_at
        FROM transactions
        WHERE id = ?
        """,
        (str(payload["id"]),),
    ).fetchone()
    return jsonify(dict(created)), 201


@app.delete("/api/users/<int:user_id>/transactions/<string:transaction_id>")
def delete_user_transaction(user_id: int, transaction_id: str):
    get_user_or_404(user_id)
    db = get_db()
    cursor = db.execute(
        "DELETE FROM transactions WHERE user_id = ? AND id = ?",
        (user_id, transaction_id),
    )
    db.commit()

    if cursor.rowcount == 0:
        abort(404, description="Transação não encontrada para este usuário.")

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
