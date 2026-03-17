#!/bin/bash
# JARVIS Setup Script für macOS
echo "╔═══════════════════════════════════╗"
echo "║   J.A.R.V.I.S. SETUP — macOS     ║"
echo "╚═══════════════════════════════════╝"

# Python venv
echo "→ Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# PortAudio für pyaudio (braucht Homebrew)
echo "→ Installing PortAudio via Homebrew..."
brew install portaudio 2>/dev/null || echo "  (already installed)"

# Python packages
echo "→ Installing Python packages..."
pip install --upgrade pip -q
pip install anthropic SpeechRecognition pyttsx3 pyaudio -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "╔═══════════════════════════════════╗"
echo "║  Nächste Schritte:                ║"
echo "║                                   ║"
echo "║  1. API Key setzen:               ║"
echo "║  export ANTHROPIC_API_KEY=sk-...  ║"
echo "║                                   ║"
echo "║  2. Text-Modus starten:           ║"
echo "║  python jarvis.py                 ║"
echo "║                                   ║"
echo "║  3. Sprach-Modus:                 ║"
echo "║  python jarvis.py --voice         ║"
echo "║                                   ║"
echo "║  4. HUD im Browser:               ║"
echo "║  open index.html                  ║"
echo "╚═══════════════════════════════════╝"
