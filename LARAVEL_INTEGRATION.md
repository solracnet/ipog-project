# Integração Laravel + Agno Analytics

## Visão Geral

Laravel atua como **camada de produto**: auth, upload, gestão de tokens de IA, sessões e UI.
Python/Agno permanece como **motor de análise**, exposto via AgentOS (FastAPI `:7777`).

Cada usuário configura seu próprio token de LLM (Groq, OpenAI, Anthropic ou Google). Laravel armazena o token criptografado e o envia ao Python a cada requisição. Python usa o token em memória e nunca persiste.

---

## Diagrama de Fluxo

```
┌──────────────────────────────────────────────────────┐
│                    LARAVEL (:8000)                    │
│                                                      │
│  [Token UI]  → ApiTokenController                    │
│  [Upload UI] → FileUploadController                  │
│  [Chat UI]   → ChatSessionController                 │
│                    │                │                │
│            HTTP Client          SessionStore         │
│      (GuzzleHTTP/Http)   (users ↔ session_id)       │
│                    │                                 │
│           X-AI-Provider: groq                        │
│           X-AI-Token: <encrypted→decrypted>          │
└──────────────┬───────────────────────────────────────┘
               │  REST calls
               ▼
┌──────────────────────────────────────────────────────┐
│             PYTHON / AgentOS (:7777)                 │
│                                                      │
│  POST /upload        ← recebe arquivo               │
│  POST /chat          ← recebe prompt + session_id   │
│  GET  /files         ← lista arquivos disponíveis   │
│  GET  /sessions/{id} ← histórico de sessão          │
│                                                      │
│  Headers X-AI-Provider + X-AI-Token                 │
│    → model_factory(provider, api_key)               │
│    → instancia agents com modelo do usuário         │
│    → token usado em memória, nunca persistido       │
│                                                      │
│  AnalyticsWorkflow → 5 agents → 41 tools            │
│  data/ dir ← arquivos de usuário                    │
│  db/history.db ← sessões SQLite                     │
└──────────────────────────────────────────────────────┘
```

---

## Mudanças no Projeto Python

### 1. Endpoint de upload — `agno_os.py`

```python
from fastapi import UploadFile, File, HTTPException
import uuid, shutil
from pathlib import Path

DATA_DIR = Path("data")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed = {".csv", ".xlsx", ".xls"}
    suffix = Path(file.filename).suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, "Formato não suportado. Use CSV ou Excel.")

    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    dest = DATA_DIR / unique_name

    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"filename": unique_name, "original_name": file.filename}

@app.get("/files")
async def list_files():
    files = [f.name for f in DATA_DIR.iterdir() if f.suffix in {".csv", ".xlsx", ".xls"}]
    return {"files": files}
```

### 2. CORS — `agno_os.py`

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://seu-dominio-laravel.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. Filename dinâmico — `agents/agno_workflow.py`

`_prepare_input` injeta `SampleSuperstore.csv` como hardcode. Alterar para aceitar
`filename` via payload da sessão:

```python
# Atual (aprox. linha 40):
if not any(f in content for f in available_files):
    content = f"Arquivo: SampleSuperstore.csv\n\n{content}"

# Proposto: Laravel envia {"message": "...", "filename": "abc123_dados.csv"}
# Workflow injeta filename correto antes de passar aos agents
```

### 4. Refatorar `agents/model_factory.py` — suporte a token por request

Atualmente `get_model()` lê API key apenas de variáveis de ambiente. Precisa aceitar
`provider` e `api_key` como parâmetros para suportar tokens de usuário.

```python
# agents/model_factory.py — ATUAL (simplificado):
# Groq(id=...) → lê GROQ_API_KEY do env
# OpenAIChat(id=...) → lê OPENAI_API_KEY do env

# PROPOSTO:
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google import Gemini

PROVIDER_MODELS = {
    "groq":      ("groq",      "llama-3.3-70b-versatile"),
    "openai":    ("openai",    "gpt-4o-mini"),
    "anthropic": ("anthropic", "claude-sonnet-4-6"),
    "google":    ("google",    "gemini-2.0-flash"),
}

def get_model(provider: str = None, api_key: str = None):
    provider = provider or os.getenv("LLM_PROVIDER", "groq")
    
    if provider == "groq":
        return Groq(id="llama-3.3-70b-versatile", api_key=api_key or os.getenv("GROQ_API_KEY"))
    elif provider == "openai":
        return OpenAIChat(id="gpt-4o-mini", api_key=api_key or os.getenv("OPENAI_API_KEY"))
    elif provider == "anthropic":
        return Claude(id="claude-sonnet-4-6", api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    elif provider == "google":
        return Gemini(id="gemini-2.0-flash", api_key=api_key or os.getenv("GOOGLE_API_KEY"))
    raise ValueError(f"Provider não suportado: {provider}")
```

### 5. Receber token por request — `agno_os.py`

Extrair headers `X-AI-Provider` e `X-AI-Token` e repassar ao workflow:

```python
from fastapi import Header
from typing import Optional

@app.post("/v1/workflows/run")
async def run_workflow(
    request: WorkflowRequest,
    x_ai_provider: Optional[str] = Header(None),
    x_ai_token: Optional[str] = Header(None),
):
    # Instancia workflow com modelo do usuário
    workflow = AnalyticsWorkflow(
        ai_provider=x_ai_provider,
        ai_api_key=x_ai_token,
    )
    return await workflow.run(request)
```

`AnalyticsWorkflow.__init__` e `agno_teams.__init__` precisam aceitar e repassar
`ai_provider` + `ai_api_key` até `get_model(provider, api_key)`.

### 6. Dependência — verificar `requirements.txt`

```bash
grep python-multipart requirements.txt
# Se ausente, adicionar: python-multipart>=0.0.9

# Adicionar suporte aos novos providers se não existirem:
# anthropic>=0.40.0
# google-generativeai>=0.8.0
```

---

## Estrutura Laravel

### Migrations

```sql
-- Tabela de tokens de IA do usuário
CREATE TABLE user_ai_tokens (
    id         BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id    BIGINT NOT NULL REFERENCES users(id),
    provider   VARCHAR(50) NOT NULL,   -- 'groq' | 'openai' | 'anthropic' | 'google'
    api_token  TEXT NOT NULL,          -- armazenado criptografado (Laravel encrypted cast)
    label      VARCHAR(100),           -- nome amigável (ex: "Meu token OpenAI")
    is_active  BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE (user_id, provider)         -- um token ativo por provider por usuário
);

-- Sessões de chat (provider registrado para rastreabilidade)
CREATE TABLE chat_sessions (
    id                UUID PRIMARY KEY,
    user_id           BIGINT NOT NULL REFERENCES users(id),
    python_session_id VARCHAR(255),
    filename          VARCHAR(255),
    original_filename VARCHAR(255),
    ai_provider       VARCHAR(50),     -- provider usado nesta sessão
    created_at        TIMESTAMP,
    updated_at        TIMESTAMP
);
```

**Model `UserAiToken.php`** deve usar cast `encrypted` no campo `api_token`:

```php
protected $casts = [
    'api_token' => 'encrypted',
    'is_active' => 'boolean',
];
```

### Controllers

```
app/Http/Controllers/
├── ApiTokenController.php
│   ├── index()     → GET /settings/tokens    (lista tokens do user)
│   ├── store()     → POST /settings/tokens   (salva novo token)
│   ├── update()    → PUT /settings/tokens/{id}
│   └── destroy()   → DELETE /settings/tokens/{id}
│                     - token nunca exposto em resposta após salvo
│                     - apenas provider + label + is_active retornados
│
├── UploadController.php
│   └── store()     → POST /upload
│                     - valida arquivo (mimetypes, tamanho ≤10MB)
│                     - busca token ativo do user (qualquer provider)
│                     - envia para Python /upload via Http::post()
│                     - salva chat_session com filename + provider
│                     - retorna session_id para o frontend
│
└── ChatController.php
    ├── index()     → GET /chat/{session}
    ├── sessions()  → GET /sessions
    └── send()      → POST /chat/{session}
                      - busca session no banco (filename + provider)
                      - busca token do user para o provider da sessão
                      - monta payload {message, filename, session_id}
                      - envia headers X-AI-Provider + X-AI-Token ao Python
                      - retorna resposta ao frontend
```

### Service Layer

```
app/Services/
└── AgnoClient.php
    - wrap do Http do Laravel para comunicar com Python
    - métodos: uploadFile(), sendMessage(), getHistory(), listFiles()
    - centraliza URL base, timeout, error handling
    - injeta X-AI-Provider e X-AI-Token em TODOS os requests ao Python
    - nunca loga os headers de token
```

### Rotas

```php
// routes/web.php
Route::middleware('auth')->group(function () {
    // Gerenciamento de tokens de IA
    Route::get('/settings/tokens',          [ApiTokenController::class, 'index']);
    Route::post('/settings/tokens',         [ApiTokenController::class, 'store']);
    Route::put('/settings/tokens/{token}',  [ApiTokenController::class, 'update']);
    Route::delete('/settings/tokens/{token}', [ApiTokenController::class, 'destroy']);

    // Upload e chat
    Route::post('/upload',                  [UploadController::class, 'store']);
    Route::get('/sessions',                 [ChatController::class, 'sessions']);
    Route::get('/chat/{session}',           [ChatController::class, 'index']);
    Route::post('/chat/{session}',          [ChatController::class, 'send']);
});
```

### Frontend

```
resources/views/
├── settings/tokens.blade.php → formulário para cadastrar tokens por provider
├── upload.blade.php          → drag-and-drop, progresso de upload
└── chat.blade.php            → interface de chat

app/Livewire/
├── ApiTokenManager.php       → adicionar/remover tokens, selecionar provider ativo
├── FileUpload.php            → upload com seleção de provider
└── ChatInterface.php         → polling ou SSE para respostas longas
```

---

## Fluxo de Cadastro de Token

```
1. Usuário acessa /settings/tokens
2. Escolhe provider (Groq / OpenAI / Anthropic / Google)
3. Cola seu API key
4. Laravel valida formato básico (não chama API externa para validar)
5. Laravel salva criptografado: user_ai_tokens {user_id, provider, api_token (encrypted)}
6. Frontend exibe apenas: provider + label + "token cadastrado" (nunca o valor)
```

## Fluxo de Upload

```
1. Usuário arrasta CSV no Livewire FileUpload
2. Usuário seleciona provider (ou usa o ativo por padrão)
3. Laravel verifica: user tem token para o provider selecionado?
   → Não: redireciona para /settings/tokens com aviso
4. Laravel valida: mime, tamanho (max 10MB)
5. Laravel POST /upload → Python (multipart/form-data)
   headers: X-AI-Provider: groq | X-AI-Token: <decrypted_token>
6. Python salva em data/{uuid}_{nome}.csv
7. Python retorna: {"filename": "abc_dados.csv"}
8. Laravel cria chat_sessions: {user_id, filename, ai_provider, python_session_id: null}
9. Laravel redireciona para /chat/{session_id}
```

## Fluxo de Chat

```
1. Usuário digita pergunta
2. Laravel POST /chat/{session} {"message": "..."}
3. ChatController busca session → filename + ai_provider
4. ChatController busca user_ai_tokens para o provider da sessão → decripta token
5. AgnoClient POST http://python:7777/v1/workflows/run
   headers: X-AI-Provider: groq | X-AI-Token: <token>
   body: {"message": "...", "session_id": "...", "user_data": {"filename": "..."}}
6. Python extrai headers → get_model(provider, api_key) → instancia agents
7. Workflow roda → agentes → tools → resposta Markdown
8. Laravel retorna resposta ao frontend (token nunca aparece na resposta)
9. Livewire renderiza Markdown
```

---

## Pontos de Atenção

| Ponto | Detalhe |
|-------|---------|
| **Token nunca exposto** | `api_token` usa `encrypted` cast do Laravel. Nunca retornar valor em resposta de API. Nunca logar headers `X-AI-Token` |
| **Token inválido** | Python receberá erro 401 do provider LLM. Retornar erro legível ao usuário com instrução para revisar o token em `/settings/tokens` |
| **Provider por sessão** | Sessão está vinculada ao provider no momento do upload. Trocar provider requer nova sessão |
| **Isolamento de dados** | UUID no nome do arquivo evita colisão entre usuários |
| **Streaming** | AgentOS suporta SSE (`stream=True`). Laravel pode fazer proxy via `StreamedResponse` ou simplificar com polling |
| **Limpeza de arquivos** | Job `CleanupOldFiles` remove arquivos em `data/` e sessões inativas após X dias |
| **Auth entre serviços** | Header `X-Internal-Token` no AgnoClient + middleware Python para rejeitar chamadas externas diretas |
| **Deploy** | Laravel e Python como serviços separados. `supervisor`/`systemd` para Python. Nginx como reverse proxy |
| **Tamanho de arquivo** | Python carrega CSV inteiro em memória por chamada. Arquivos grandes (>50MB) podem falhar. Impor limite no Laravel |

---

## Providers Suportados

| Provider | Classe Agno | Modelo Padrão | Env Var Fallback |
|----------|------------|---------------|-----------------|
| `groq` | `agno.models.groq.Groq` | `llama-3.3-70b-versatile` | `GROQ_API_KEY` |
| `openai` | `agno.models.openai.OpenAIChat` | `gpt-4o-mini` | `OPENAI_API_KEY` |
| `anthropic` | `agno.models.anthropic.Claude` | `claude-sonnet-4-6` | `ANTHROPIC_API_KEY` |
| `google` | `agno.models.google.Gemini` | `gemini-2.0-flash` | `GOOGLE_API_KEY` |

Fallback: se usuário não tiver token cadastrado e env var existir no servidor, usa env var. Em produção, recomendar desabilitar fallback para forçar token do usuário.

---

## Dependências a Adicionar

| Projeto | Pacote | Motivo |
|---------|--------|--------|
| Python | `python-multipart>=0.0.9` | `UploadFile` do FastAPI exige |
| Python | `anthropic>=0.40.0` | Suporte ao provider Anthropic/Claude |
| Python | `google-generativeai>=0.8.0` | Suporte ao provider Google/Gemini |
| Laravel | `league/commonmark` | Renderizar Markdown do Python no Blade |
| Laravel | `guzzlehttp/guzzle` | Já incluso no Laravel — confirmar versão |

---

## Resumo das Mudanças por Arquivo

| Arquivo | Mudança |
|---------|---------|
| `agno_os.py` | +CORS middleware, +`POST /upload`, +`GET /files`, +extração de headers `X-AI-Provider`/`X-AI-Token` |
| `agents/model_factory.py` | `get_model(provider, api_key)` aceita parâmetros; suporte a 4 providers |
| `agents/agno_teams.py` | `__init__` aceita `ai_provider` + `ai_api_key`, repassa a `get_model()` |
| `agents/agno_workflow.py` | `__init__` aceita `ai_provider` + `ai_api_key`, repassa ao team; `_prepare_input` aceita filename dinâmico |
| `.env.example` | +`ALLOWED_ORIGINS`, +`ANTHROPIC_API_KEY`, +`GOOGLE_API_KEY` |
| **Novo** `app/Models/UserAiToken.php` | Model com `encrypted` cast no `api_token` |
| **Novo** `app/Services/AgnoClient.php` | HTTP client wrapper; injeta headers de token |
| **Novo** `app/Http/Controllers/ApiTokenController.php` | CRUD de tokens de IA por usuário |
| **Novo** `app/Http/Controllers/UploadController.php` | Recebe upload, busca token, delega ao AgnoClient |
| **Novo** `app/Http/Controllers/ChatController.php` | Gerencia sessões e mensagens com token |
| **Novo** `database/migrations/*_create_user_ai_tokens_table.php` | Schema de tokens |
| **Novo** `database/migrations/*_create_chat_sessions_table.php` | Schema de sessões (com `ai_provider`) |
| **Novo** `app/Livewire/ApiTokenManager.php` | UI de gerenciamento de tokens |
| **Novo** `app/Livewire/FileUpload.php` + `ChatInterface.php` | UI reativa |

---

## Ordem de Implementação Recomendada

1. Refatorar `model_factory.py` → `get_model(provider, api_key)` com 4 providers
2. Propagar `ai_provider`/`ai_api_key` por `agno_teams.py` → `agno_workflow.py`
3. Adicionar extração de headers + CORS + endpoints `/upload`/`/files` ao `agno_os.py`
4. Testar endpoints Python diretamente (curl/Postman) com headers de token
5. Criar migrations + models Laravel (`UserAiToken`, `ChatSession`)
6. Criar `AgnoClient.php` com injeção de headers
7. Criar `ApiTokenController` + UI de gerenciamento de tokens
8. Criar `UploadController` + `ChatController` + rotas
9. Criar componentes Livewire (tokens → upload → chat)
10. Ajustar `_prepare_input` no workflow para filename dinâmico
11. Testes end-to-end com cada provider
