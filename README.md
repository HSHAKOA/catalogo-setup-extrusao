# Catálogo Técnico de Setup de Extrusão

Aplicação web leve em Flask para consulta rápida de setups no chão de fábrica.

## Arquitetura simples

- Backend único em `Flask`
- Dados do catálogo em JSON
- Frontend em HTML, CSS e JavaScript leve
- Banco SQLite para dados por usuário (transações)

## Estrutura de arquivos

- `app.py`: servidor Flask, endpoints do catálogo e API de usuários/transações
- `data/tool_catalog.json`: catálogo editável das ferramentas
- `data/app.db`: banco SQLite criado automaticamente na primeira execução
- `index.html`: tela única para o operador
- `style.css`: estilo mobile-first
- `app.js`: seleção rápida e exibição imediata

## Como rodar

```bash
pip install -r requirements.txt
flask --app app run --debug
```

Abra `http://127.0.0.1:5000`.

## API de persistência por usuário

A aplicação agora possui banco SQLite para armazenar dados de cada usuário separadamente.

### Criar usuário

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"maria"}'
```

### Listar usuários

```bash
curl http://127.0.0.1:5000/api/users
```

### Criar transação para um usuário

```bash
curl -X POST http://127.0.0.1:5000/api/users/1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "id":"tx-001",
    "description":"Salário",
    "amount":5000,
    "type":"income",
    "category":"Receita",
    "date":"2026-04-14"
  }'
```

### Listar transações de um usuário

```bash
curl http://127.0.0.1:5000/api/users/1/transactions
```

### Excluir transação de um usuário

```bash
curl -X DELETE http://127.0.0.1:5000/api/users/1/transactions/tx-001
```

## Como editar os dados do catálogo

Edite o arquivo `data/tool_catalog.json` (ou `tool_catalog.json`, para compatibilidade legada).

Cada item representa uma ferramenta com:

- `code`
- `name`
- `product`
- `cycle_time_seconds`
- `piece_weight_grams`
- `expected_scrap_percent`
- `time_per_piece_seconds`
- `machine_parameters`
- `operational_notes`
