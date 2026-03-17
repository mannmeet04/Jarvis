# J.A.R.V.I.S.
### Just A Rather Very Intelligent System

Ein KI-Sprachassistent im Tony-Stark-Stil für macOS — mit Spracherkennung, App-Steuerung und Claude AI als Gehirn.

---

## Features

- **Sprache erkennen** — Mikrofon-Eingabe via `SpeechRecognition`
- **Apps öffnen** — "open spotify", "open terminal", "open vscode" ...
- **Websites öffnen** — "open youtube", "open github" ...
- **Web suchen** — "search for Python tutorials"
- **KI-Antworten** — Claude AI für alles andere
- **Text-to-Speech** — JARVIS antwortet mit Stimme
- **HUD Interface** — Iron Man-style Browseroberfläche

---

## Schnellstart

```bash
cd jarvis
bash setup.sh

# API Key setzen (optional, aber für KI nötig)
export ANTHROPIC_API_KEY=sk-ant-...

# Text-Modus
source .venv/bin/activate
python jarvis.py

# Sprach-Modus
python jarvis.py --voice

# HUD im Browser
open index.html
```

---

## Sprachbefehle

| Befehl | Was passiert |
|---|---|
| `open spotify` | Öffnet Spotify |
| `open terminal` | Öffnet Terminal |
| `open youtube` | Browser → YouTube |
| `open github` | Browser → GitHub |
| `search for X` | Google-Suche nach X |
| `what time is it` | Aktuelle Uhrzeit |
| `take a screenshot` | Screenshot auf Desktop |
| `set volume to 50` | Lautstärke auf 50% |
| `lock the screen` | Bildschirm sperren |
| Alles andere | Claude AI antwortet |

---

## Struktur

```
jarvis/
├── jarvis.py       # Python-Backend (Sprache + Logik)
├── index.html      # HUD-Oberfläche (Browser)
├── requirements.txt
├── setup.sh
└── README.md
```
