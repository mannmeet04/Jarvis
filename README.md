# J.A.R.V.I.S.

Ein KI-Sprachassistent im Tony-Stark-Stil mit Spracherkennung, App-Steuerung und Gemini als Gehirn.

---

## Features

- **Sprache erkennen** — Mikrofon-Eingabe 
- **Apps öffnen** — "open spotify", "open terminal", "open vscode" ...
- **Websites öffnen** — "open youtube", "open github" ...
- **Web suchen** — "search for Python tutorials"
- **KI-Antworten** — Gemini für alles andere
- **Text-to-Speech** — JARVIS antwortet mit Stimme
- **HUD Interface** — Filmische Browseroberfläche

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

# im Browser
open index.html
```

---
