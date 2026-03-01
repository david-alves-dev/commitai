# CommitAI

CommitAI e um bot do Telegram que ajuda devs a padronizar titulo e descricao de commits seguindo o padrao **Conventional Commits**. A ideia nasceu dentro da empresa onde trabalho, pois nao existia um formato consistente. Com o CommitAI, qualquer pessoa descreve o que fez e recebe um commit pronto, tecnico e padronizado.

## O que ele faz

- Gera titulo e descricao de commit no formato Conventional Commits
- Mantem o formato rigoroso com dois blocos Markdown
- Suporta texto e audio (transcricao via OpenAI)
- Responde direto no Telegram para agilizar o fluxo de trabalho

## Como funciona

1. O usuario clica em **Gerar commit** no bot do Telegram
2. Envia um texto (ou audio) descrevendo a alteracao
3. O bot usa um prompt especializado (`prompts/commitai.md`) para gerar:
   - **Titulo do commit** (1a linha)
   - **Descricao do commit** (bullets quando necessario)

## Requisitos

- Python 3.10+
- Chave do bot do Telegram
- Chave de API da OpenAI

## Instalacao

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuracao

No arquivo `main.py` sao usadas duas chaves:

- `TELEGRAM_BOT_API_KEY`
- `OPENAI_API`

Recomendado: usar variaveis de ambiente e **nao** deixar chaves hardcoded.

Crie um arquivo `.env` na raiz do projeto com as chaves:

```
TELEGRAM_BOT_API_KEY=sua_chave
OPENAI_API=sua_chave
```

Exemplo:

```python
TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY", "")
OPENAI_API = os.getenv("OPENAI_API", "")
```

## Executando

```bash
python main.py
```

O bot roda em **polling** e ja fica ouvindo mensagens no Telegram.

## Estrutura do projeto

- `main.py`: bot do Telegram e integracao com OpenAI
- `prompts/commitai.md`: prompt com regras de formatacao do commit
- `requirements.txt`: dependencias

## Exemplo de uso

Entrada do usuario:

> "Corrigi o retorno da funcao e diminui o tempo de sleep nos testes"

Resposta do bot:

🏷️ **Título do commit:**
```
refactor: reduz tempo de espera para testes
```

📝 **Descrição do commit:**
```
- Ajusta retornos das funcoes para garantir consistencia
- Diminui o tempo de sleep para agilizar testes
```

## Observacoes importantes

- O formato retornado segue estritamente o padrao definido em `prompts/commitai.md`
- O bot nao inventa informacoes que o usuario nao forneceu
- Evite textos vagos: quanto mais claro o resumo, melhor o commit

## Sobre o Autor

- **Nome:** David Alves
- **Site:** `https://davidalves.dev/`
- **LinkedIn:** `https://www.linkedin.com/in/davidalves-dev/`
