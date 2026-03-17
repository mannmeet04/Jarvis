import os
import sys
import subprocess
import webbrowser
import datetime
import threading
import time
import json
import re
from typing import Optional


try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import anthropic
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


WAKE_WORD   = "jarvis"
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = """You are J.A.R.V.I.S., Tony Stark's AI assistant.
Respond concisely (1-2 sentences max), with dry wit and intelligence.
Address the user as "Boss" occasionally. Never break character.
For app/web commands you don't handle yourself, just confirm the action naturally."""


class Speaker:
    def __init__(self):
        self.engine = None
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                voices = self.engine.getProperty('voices')
                for v in voices:
                    if 'daniel' in v.name.lower() or 'alex' in v.name.lower():
                        self.engine.setProperty('voice', v.id)
                        break
                self.engine.setProperty('rate', 185)
                self.engine.setProperty('volume', 0.95)
            except Exception:
                self.engine = None

    def say(self, text):
        print(f"\n🤖 JARVIS: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                os.system(f'say -v Daniel "{text}"')
        else:
            os.system(f'say -v Daniel "{text}"')


class Launcher:
    APP_MAP = {
        "safari":       "Safari",
        "browser":      "Safari",
        "chrome":       "Google Chrome",
        "firefox":      "Firefox",
        "terminal":     "Terminal",
        "spotify":      "Spotify",
        "music":        "Music",
        "mail":         "Mail",
        "calendar":     "Calendar",
        "finder":       "Finder",
        "notes":        "Notes",
        "calculator":   "Calculator",
        "vscode":       "Visual Studio Code",
        "code":         "Visual Studio Code",
        "discord":      "Discord",
        "slack":        "Slack",
        "zoom":         "zoom.us",
        "maps":         "Maps",
        "photos":       "Photos",
        "messages":     "Messages",
        "facetime":     "FaceTime",
        "xcode":        "Xcode",
        "word":         "Microsoft Word",
        "excel":        "Microsoft Excel",
        "powerpoint":   "Microsoft PowerPoint",
    }

    WEBSITE_MAP = {
        "youtube":       "https://youtube.com",
        "google":        "https://google.com",
        "github":        "https://github.com",
        "netflix":       "https://netflix.com",
        "twitter":       "https://twitter.com",
        "instagram":     "https://instagram.com",
        "reddit":        "https://reddit.com",
        "stackoverflow": "https://stackoverflow.com",
        "linkedin":      "https://linkedin.com",
        "amazon":        "https://amazon.de",
        "wikipedia":     "https://wikipedia.org",
        "chatgpt":       "https://chat.openai.com",
        "weather":       "https://weather.com",
    }

    def open_app(self, name):
        app = self.APP_MAP.get(name.lower())
        if app:
            result = subprocess.run(
                ["open", "-a", app],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return f"Opening {app}, Boss."
            return f"I couldn't find {app} on this system."
        return None

    def open_website(self, name):
        url = self.WEBSITE_MAP.get(name.lower())
        if url:
            webbrowser.open(url)
            return f"Launching {name} in your browser."
        return None

    def search_web(self, query):
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching for '{query}'."

    def get_time(self):
        now = datetime.datetime.now()
        return f"It's {now.strftime('%H:%M')} on {now.strftime('%A, %B %d')}."

    def get_volume(self, level):
        level = max(0, min(100, level))
        os.system(f"osascript -e 'set volume output volume {level}'")
        return f"Volume set to {level} percent."

    def screenshot(self):
        path = os.path.expanduser(f"~/Desktop/jarvis_{int(time.time())}.png")
        os.system(f"screencapture {path}")
        return "Screenshot saved to your Desktop."

    def lock_screen(self):
        os.system('/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend')
        return "Locking the system. Stay safe, Boss."


class IntentParser:
    def __init__(self, launcher):
        self.launcher = launcher

    def parse(self, text):
        t = text.lower().strip()

        if any(w in t for w in ["what time", "what's the time", "uhrzeit", "time is it"]):
            return self.launcher.get_time()

        if "screenshot" in t:
            return self.launcher.screenshot()

        if any(w in t for w in ["lock screen", "lock the screen"]):
            return self.launcher.lock_screen()

        vol_match = re.search(r'volume\s+(?:to\s+)?(\d+)', t)
        if vol_match:
            return self.launcher.get_volume(int(vol_match.group(1)))

        for site in self.launcher.WEBSITE_MAP:
            if site in t and any(w in t for w in ["open", "launch", "go to", "show", "öffne"]):
                return self.launcher.open_website(site)

        for app in self.launcher.APP_MAP:
            if app in t and any(w in t for w in ["open", "launch", "start", "öffne", "starte"]):
                result = self.launcher.open_app(app)
                if result:
                    return result

        search_match = re.search(r'(?:search|google|suche nach?)\s+(?:for\s+)?(.+)', t)
        if search_match:
            return self.launcher.search_web(search_match.group(1))

        return None


class Brain:
    def __init__(self):
        self.client = None
        self.history = []
        if AI_AVAILABLE and ANTHROPIC_KEY:
            self.client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    def think(self, user_input):
        if not self.client:
            return "My AI core is offline. Set ANTHROPIC_API_KEY to enable it, Boss."

        self.history.append({"role": "user", "content": user_input})
        if len(self.history) > 20:
            self.history = self.history[-20:]

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                system=SYSTEM_PROMPT,
                messages=self.history,
            )
            reply = response.content[0].text
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"I encountered an error in my neural network: {str(e)[:60]}"


class Listener:
    def __init__(self):
        self.recognizer = None
        if SR_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.pause_threshold = 0.8
            self.recognizer.energy_threshold = 300

    def listen(self):
        if not SR_AVAILABLE or not self.recognizer:
            return None
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎤 Listening...", flush=True)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = self.recognizer.recognize_google(audio, language="de-DE,en-US")
            print(f"👤 You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"[Listener error] {e}")
            return None


class JARVIS:
    def __init__(self):
        self.speaker  = Speaker()
        self.launcher = Launcher()
        self.parser   = IntentParser(self.launcher)
        self.brain    = Brain()
        self.listener = Listener()

    def handle(self, text):
        response = self.parser.parse(text)
        if response is None:
            response = self.brain.think(text)
        self.speaker.say(response)

    def run_voice(self):
        self.speaker.say("J.A.R.V.I.S. online. All systems nominal. Awaiting your command, Boss.")
        print(f"\n🟢 Wake word: say '{WAKE_WORD}' to activate\n")
        while True:
            text = self.listener.listen()
            if text and WAKE_WORD in text:
                command = text.replace(WAKE_WORD, "").strip()
                if not command:
                    self.speaker.say("Yes, Boss?")
                    command = self.listener.listen()
                if command:
                    self.handle(command)

    def run_text(self):
        self.speaker.say("J.A.R.V.I.S. online. Text mode active.")
        print("\n" + "═"*50)
        print("  J.A.R.V.I.S. — Text Mode")
        print("  Type your command. 'quit' to exit.")
        print("═"*50 + "\n")
        while True:
            try:
                text = input("👤 You: ").strip()
                if not text:
                    continue
                if text.lower() in ("quit", "exit", "bye"):
                    self.speaker.say("Goodbye, Boss. Stay brilliant.")
                    break
                self.handle(text)
            except KeyboardInterrupt:
                self.speaker.say("Shutting down. Goodbye, Boss.")
                break


def main():
    jarvis = JARVIS()
    mode = "text"
    if len(sys.argv) > 1 and sys.argv[1] == "--voice":
        mode = "voice"
    if mode == "voice":
        if not SR_AVAILABLE:
            print("⚠  speech_recognition not installed. Falling back to text mode.")
            jarvis.run_text()
        else:
            jarvis.run_voice()
    else:
        jarvis.run_text()


if __name__ == "__main__":
    main()