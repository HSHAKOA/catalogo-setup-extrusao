from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import Flask, abort, jsonify, render_template


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "tool_catalog.json"


app = Flask(__name__)


def load_catalog() -> list[dict[str, Any]]:
    with DATA_FILE.open(encoding="utf-8") as file:
        tools = json.load(file)
    return sorted(tools, key=lambda item: item["code"])


def get_tool_by_code(code: str) -> dict[str, Any]:
    normalized = code.strip().upper()
    for tool in load_catalog():
        if tool["code"].upper() == normalized:
            return tool
    abort(404)


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


if __name__ == "__main__":
    app.run(debug=True)
