# Catalogo Tecnico de Setup de Extrusao

Aplicacao web leve em Flask para consulta rapida de setups no chao de fabrica.

## Arquitetura simples

- Backend unico em `Flask`
- Dados fixos em arquivo JSON
- Frontend em HTML, CSS e JavaScript leve
- Sem banco, sem login, sem historico

## Estrutura de arquivos

- `app.py`: servidor Flask e endpoints
- `data/tool_catalog.json`: catalogo editavel das ferramentas
- `templates/index.html`: tela unica para o operador
- `static/style.css`: estilo mobile-first
- `static/app.js`: selecao rapida e exibicao imediata

## Como rodar

```bash
pip install -r requirements.txt
flask --app app run --debug
```

Abra `http://127.0.0.1:5000`.

## Como editar os dados

Edite o arquivo `data/tool_catalog.json`.

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

Depois de salvar o JSON, recarregue a pagina.

## Publicar em nuvem

Recomendacao simples: usar `Render` com deploy por GitHub.

### Fluxo sugerido

1. Suba este projeto para um repositorio no GitHub.
2. Edite os dados em `data/tool_catalog.json`.
3. Faça `git add`, `git commit` e `git push`.
4. O Render publica automaticamente a nova versao.

### Arquivos de deploy

- `requirements.txt`: dependencias do projeto
- `render.yaml`: configuracao do servico web

### No Render

1. Crie uma conta.
2. Conecte o GitHub.
3. Crie um novo `Blueprint` ou `Web Service` usando este repositorio.
4. O Render vai usar:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

### Resultado

Voce passa a ter uma URL publica, por exemplo:

`https://seu-catalogo.onrender.com`

Toda alteracao feita no codigo ou no JSON e enviada com `git push` vira nova publicacao.
