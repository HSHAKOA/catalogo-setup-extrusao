import re
import random

print("=== SEN.AI Fase 1 ===")
print("Digite: oi, ajuda, python ou sair\n")

# Lista de padrões estilo ELIZA:
# Cada item tem: (regex, [lista de respostas possíveis])
padroes = [
    (r"eu estou (.*)", [
        "Por que você está {}?",
        "O que te faz estar {}?",
        "Há quanto tempo você está {}?",
    ]),
    (r"eu me sinto (.*)", [
        "Entendo. Por que você se sente {}?",
        "Quando você começou a se sentir {}?",
        "Você quer falar mais sobre se sentir {}?",
    ]),
    (r"eu quero (.*)", [
        "Por que você quer {}?",
        "O que mudaria se você conseguisse {}?",
        "O que te impede de conseguir {}?",
    ]),
    (r"por que (.*)", [
        "O que você acha sobre isso: {}?",
        "Essa pergunta é importante para você?",
        "Que respostas você já encontrou para: {}?",
    ]),
    (r"(.*)\?", [
        "Boa pergunta. O que você pensa sobre isso?",
        "Como você responderia essa pergunta?",
        "O que te levou a perguntar isso?",
    ]),
    (r"oi|olá|ola", [
        "Olá! Como você está hoje?",
        "Oi! Quer conversar sobre o que está sentindo?",
        "Que bom te ver por aqui. Como posso ajudar?",
    ]),
]

# Respostas de fallback (quando nenhum padrão combina)
fallback = [
    "Pode me contar mais sobre isso?",
    "Entendi. Fale um pouco mais.",
    "Isso parece importante para você.",
]

while True:
    mensagem = input("Você: ").lower().strip()

    if mensagem == "sair":
        print("SEN.AI: Até logo! Foi bom conversar com você.")
        break

    resposta_encontrada = False

    # Tenta casar a mensagem com cada padrão
    for padrao, respostas in padroes:
        resultado = re.match(padrao, mensagem)

        if resultado:
            resposta = random.choice(respostas)

            # Se o padrão capturou algo com (.*), usa format
            if resultado.groups():
                trecho_capturado = resultado.group(1).strip()
                print("SEN.AI:", resposta.format(trecho_capturado))
            else:
                print("SEN.AI:", resposta)

            resposta_encontrada = True
            break

    # Fallback inteligente se nenhum padrão for reconhecido
    if not resposta_encontrada:
        print("SEN.AI:", random.choice(fallback))
