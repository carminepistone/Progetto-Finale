# 🌍 Travel Agent API

Un assistente virtuale per la pianificazione di viaggi. Dato un messaggio in linguaggio naturale, l'agente cerca voli, hotel e crea un itinerario personalizzato giorno per giorno.

---

## Cosa fa questo progetto

Scrivi qualcosa come _"Vorrei organizzare un viaggio a Roma dal 10 al 15 giugno, siamo in due"_ e l'agente:

- cerca i voli disponibili
- trova gli hotel
- genera un piano di viaggio dettagliato (mattina, pomeriggio, sera)
- risponde a domande storiche sulla destinazione

---

## Struttura del progetto

```
travel-agent-api/
├── travel_agent_api/
│   ├── __init__.py
│   ├── main.py                          # Punto di avvio dell'API
│   ├── routes/
│   │   └── chat_router.py               # Endpoint /chat/travel-agent
│   ├── services/
│   │   └── agent_service.py             # Cervello dell'agente
│   └── tools/
│       ├── flights_finder.py            # Ricerca voli (SerpApi)
│       ├── hotels_finder.py             # Ricerca hotel (SerpApi)
│       ├── chain_travel_plan.py         # Generazione itinerario (OpenAI)
│       └── chain_historical_expert.py   # Info storiche (OpenAI)
├── tests/
│   └── __init__.py
├── .env                                 # Le tue chiavi API (NON caricare su Git)
├── .env.example                         # Template delle variabili d'ambiente
├── pyproject.toml                       # Dipendenze del progetto
└── poetry.lock                          # Versioni esatte delle librerie
```

---

## Requisiti

- Python tra 3.10 e 3.x (< 4.0)
- [Poetry](https://python-poetry.org/) per gestire le dipendenze
- Una chiave API di [OpenAI](https://platform.openai.com)
- Una chiave API di [SerpApi](https://serpapi.com)

---

## Installazione

### 1. Clona il progetto

```bash
git clone <url-del-tuo-repository>
cd travel-agent-api
```

### 2. Installa le dipendenze

```bash
poetry install
```

### 3. Crea il file delle variabili d'ambiente

```bash
cp .env.example .env
```

Apri il file `.env` e inserisci le tue chiavi:

```
OPENAI_API_KEY="la-tua-chiave-openai"
SERPAPI_API_KEY="la-tua-chiave-serpapi"
```

**Come ottenere le chiavi:**

- **OpenAI**: registrati su [platform.openai.com](https://platform.openai.com) → vai su Settings → API Keys → "Create new secret key"
- **SerpApi**: registrati su [serpapi.com](https://serpapi.com) → vai su Dashboard → copia la chiave già creata automaticamente

> ⚠️ Non caricare mai il file `.env` su Git. Contiene le tue credenziali personali. Aggiungi `.env` al tuo `.gitignore`.

---

## Avvio del server

```bash
poetry run uvicorn travel_agent_api.main:app --reload --port 8080
```

Il server parte su `http://127.0.0.1:8080`

---

## Come testare l'API

Apri il browser e vai su:

```
http://127.0.0.1:8080/docs
```

Si aprirà l'interfaccia **Swagger UI**, generata automaticamente da FastAPI. Da qui puoi fare richieste di prova direttamente dal browser senza scrivere codice.

### Endpoint disponibile

```
POST /chat/travel-agent
```

### Esempio di richiesta

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Vorrei organizzare un viaggio a Roma dal 10 al 15 giugno 2025, siamo 2 adulti"
    }
  ]
}
```

---

## Esempi di prompt da provare

### Informazioni storiche
- "Raccontami la storia dell'antica Roma"
- "Chi erano i Medici e che ruolo hanno avuto nel Rinascimento fiorentino?"

### Pianificazione viaggio
- "Vorrei organizzare un viaggio a Venezia dal 15 al 20 giugno. Siamo una coppia, budget 2000€, ci interessa arte e cucina locale."
- "Vacanza in famiglia a Roma dal 1 al 7 agosto, 2 adulti e 2 bambini, budget 3000€, un bambino è celiaco."

### Ricerca voli
- "Cerco voli da FCO (Roma) a CDG (Parigi) per 2 adulti, partenza 5 luglio 2025 e ritorno 12 luglio."
- "Voli da MXP (Milano) a BCN (Barcellona) per una persona, andata 20 agosto ritorno 25 agosto."

### Ricerca hotel
- "Cerco un hotel 4 stelle nel centro di Roma per 2 adulti dal 15 al 20 maggio."
- "Hotel a Firenze per una famiglia (2 adulti, 2 bambini) dal 1 al 7 agosto, preferibilmente 3 stelle."

---

## Frontend (opzionale)

Se vuoi usare l'interfaccia grafica in Laravel, scarica il codice del frontend ed esegui:

```bash
cd web_TravelAgent
composer install
npm install
npm run dev
php artisan serve
```

Poi apri `http://localhost:8000` nel browser.

> ⚠️ Il frontend comunica con l'API sulla porta **8080**. Tieni il server API avviato in un terminale separato:
> ```bash
> poetry run uvicorn travel_agent_api.main:app --reload --port 8080
> ```

---

## Dipendenze principali

| Libreria | A cosa serve |
|---|---|
| `fastapi` | Crea l'API web |
| `uvicorn` | Fa girare il server |
| `openai` | Connessione a GPT-4o-mini |
| `langchain-openai` | Usa OpenAI dentro LangChain |
| `langgraph` | Gestisce il flusso dell'agente |
| `pydantic` | Valida i dati in entrata |
| `python-dotenv` | Legge le variabili dal file `.env` |
| `google-search-results` | Client per SerpApi (voli e hotel) |

---

## Problemi comuni

**Il server non parte** → assicurati di essere nella cartella del progetto e di usare `poetry run` prima del comando uvicorn.

**`ModuleNotFoundError: No module named 'langchain_openai'`** → esegui `poetry install` per installare tutte le dipendenze nell'ambiente virtuale.

**`ImportError: cannot import name 'GoogleSearch' from 'serpapi'`** → il pacchetto corretto è `google-search-results`, non `serpapi`. Esegui `poetry add google-search-results` e rimuovi `serpapi` se presente.

**Errore di chiave API** → controlla che il file `.env` esista nella cartella del progetto e che le chiavi siano corrette (senza spazi extra).

**Nessun risultato per i voli o gli hotel** → SerpApi ha un piano gratuito con un numero limitato di ricerche mensili. Verifica il tuo saldo su [serpapi.com/dashboard](https://serpapi.com/dashboard).

**Python non compatibile** → questo progetto richiede Python 3.10 o superiore (ma inferiore a 4.0). Verifica con `python --version`.