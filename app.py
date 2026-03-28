from __future__ import annotations

import re
from dataclasses import dataclass

from flask import Flask, jsonify, render_template, request


app = Flask(__name__, template_folder=".", static_folder=".")


@dataclass(frozen=True)
class ReflectionRule:
    pattern: re.Pattern[str]
    templates: tuple[str, ...]


PRONOUN_SWAPS = {
    "eu": "você",
    "meu": "seu",
    "minha": "sua",
    "me": "te",
    "comigo": "com você",
    "sou": "é",
    "estou": "está",
    "você": "eu",
    "seu": "meu",
    "sua": "minha",
}

FILLERS = {
    "tipo",
    "mano",
    "cara",
    "né",
    "assim",
    "sabe",
    "real",
    "literalmente",
}

RULES = (
    ReflectionRule(
        pattern=re.compile(r"\b(ansios[oa]|ansiedade|preocupad[oa]|nervos[oa])\b", re.IGNORECASE),
        templates=(
            "Faz total sentido isso pesar. Quando a ansiedade bate, seu cérebro entra em modo de alerta. O que mais dispara esse gatilho em você?",
            "Parece que seu sistema de ameaça está no turbo agora. Em qual momento do dia isso fica mais intenso?",
        ),
    ),
    ReflectionRule(
        pattern=re.compile(r"\b(cansad[oa]|esgotad[oa]|sem energia|exaust[oa])\b", re.IGNORECASE),
        templates=(
            "Seu relato tem cara de sobrecarga mesmo. Quando corpo e mente pedem pausa, o foco cai. O que vem drenando mais sua energia?",
            "Entendi, parece um cansaço que não é só físico. Como está seu ritmo de descanso e sono nesses dias?",
        ),
    ),
    ReflectionRule(
        pattern=re.compile(r"\b(triste|desanimad[oa]|deprimid[oa]|vazi[oa])\b", re.IGNORECASE),
        templates=(
            "Sinto que isso está te pesando de verdade. Quando o humor cai, a motivação do cérebro despenca junto. O que você percebe que mudou primeiro?",
            "Obrigado por confiar isso. Se você topar, podemos explorar o que tem mantido esse desânimo ativo.",
        ),
    ),
    ReflectionRule(
        pattern=re.compile(r"\b(procrastin|trav[ae]i|bloquei[oa])\b", re.IGNORECASE),
        templates=(
            "Isso acontece muito quando o cérebro busca evitar desconforto imediato. Qual tarefa você está empurrando mais agora?",
            "Quando você fala em travar, eu escuto conflito entre vontade e pressão. O que torna esse começo tão difícil?",
        ),
    ),
)


def normalize_message(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text.strip().lower())
    words = [word for word in cleaned.split(" ") if word not in FILLERS]
    return " ".join(words)


def reflect_fragment(text: str) -> str:
    words = text.split()
    swapped = [PRONOUN_SWAPS.get(word, word) for word in words]
    return " ".join(swapped)


def choose_reply(message: str) -> str:
    normalized = normalize_message(message)

    for index, rule in enumerate(RULES):
        if rule.pattern.search(normalized):
            option = rule.templates[len(normalized) % len(rule.templates)]
            return option

    if "porque" in normalized or "por que" in normalized:
        return "Boa pergunta. Se a gente olhar com calma, o que você acha que seu cérebro está tentando proteger nesse cenário?"

    if normalized.endswith("?"):
        return "Curti sua pergunta. Antes de eu sugerir algo, como você mesmo interpreta isso no seu contexto?"

    if len(normalized.split()) <= 3:
        return "Tô com você. Me conta um pouco mais do contexto pra eu te devolver algo mais certeiro."

    reflected = reflect_fragment(normalized)
    return (
        f"Se entendi bem, você está dizendo: \"{reflected}\". "
        "Qual parte disso mais mexe com você agora?"
    )


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.post("/api/chat")
def chat() -> tuple[dict[str, str], int] | dict[str, str]:
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Envie uma mensagem para conversar."}), 400

    reply = choose_reply(message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
