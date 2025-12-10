#!/usr/bin/env python3
"""
Nextcloud Talk Bot - Externe Lösung ohne Serverzugriff
Verwendet die Nextcloud Talk API über ein Bot-Benutzerkonto

Voraussetzungen:
1. Bot-Benutzerkonto in Nextcloud erstellen (z.B. "nippes-bot")
2. App-Passwort für den Bot erstellen (Einstellungen > Sicherheit > App-Passwörter)
3. Bot zu den gewünschten Talk-Konversationen hinzufügen
"""

import requests
import time
import json
import os
from datetime import datetime

# Lade .env Datei falls vorhanden
def load_env_file():
    """Lädt Umgebungsvariablen aus .env Datei."""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Überspringe Kommentare und leere Zeilen
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    # Setze nur wenn nicht bereits als Umgebungsvariable gesetzt
                    if key not in os.environ:
                        os.environ[key] = value

# Lade .env Datei
load_env_file()

# Konfiguration - Bitte anpassen!
NEXTCLOUD_URL = os.environ.get('NEXTCLOUD_URL', 'https://deine-nextcloud.de')
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'nippes-bot')
BOT_PASSWORD = os.environ.get('BOT_PASSWORD', '')  # App-Passwort hier eintragen
NIPPES_API_URL = os.environ.get('NIPPES_API_URL', 'http://localhost:5001/api/status')

# Trigger-Wörter, auf die der Bot reagiert
TRIGGER_WORDS = ['nippes', 'ist das nippes offen', 'nippes status', 'ist das nippes geöffnet', 'nippes heute']

class NextcloudTalkBot:
    def __init__(self):
        self.base_url = NEXTCLOUD_URL.rstrip('/')
        self.username = BOT_USERNAME
        self.password = BOT_PASSWORD
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json'
        })
    
    def get_conversations(self):
        """Holt alle Konversationen des Bots."""
        url = f"{self.base_url}/ocs/v2.php/apps/spreed/api/v4/room"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            if 'ocs' in data and 'data' in data['ocs']:
                return data['ocs']['data']
            return []
        except Exception as e:
            print(f"Fehler beim Abrufen der Konversationen: {e}")
            return []
    
    def get_messages(self, token, limit=50):
        """Holt die letzten Nachrichten einer Konversation."""
        url = f"{self.base_url}/ocs/v2.php/apps/spreed/api/v1/chat/{token}"
        params = {'limit': limit}
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if 'ocs' in data and 'data' in data['ocs']:
                return data['ocs']['data']
            return []
        except Exception as e:
            print(f"Fehler beim Abrufen der Nachrichten: {e}")
            return []
    
    def send_message(self, token, message):
        """Sendet eine Nachricht in eine Konversation."""
        url = f"{self.base_url}/ocs/v2.php/apps/spreed/api/v1/chat/{token}"
        data = {'message': message}
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Fehler beim Senden der Nachricht: {e}")
            return False
    
    def get_nippes_status(self):
        """Holt den Nippes-Status von der API."""
        try:
            response = requests.get(NIPPES_API_URL, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                'is_open': False,
                'message': f'Fehler beim Abrufen des Status: {str(e)}'
            }
    
    def format_status_message(self, status_data):
        """Formatiert die Status-Nachricht für Talk."""
        message = status_data.get('message', 'Status unbekannt')
        
        # Füge zusätzliche Infos hinzu
        day = status_data.get('day', '')
        if day:
            message += f"\n\nHeute ist {day}"
        
        # Kommende geschlossene Termine
        upcoming = status_data.get('upcoming_closed', [])
        if upcoming:
            dates_str = ', '.join(upcoming)
            message += f"\n\nKommende geschlossene Gesellschaften: {dates_str}"
        
        return message
    
    def check_and_respond(self, token):
        """Prüft neue Nachrichten und antwortet bei Bedarf."""
        messages = self.get_messages(token)
        
        # Prüfe die letzten Nachrichten
        for msg in reversed(messages):  # Von alt nach neu
            message_text = msg.get('message', '').lower()
            actor_id = msg.get('actorId', '')
            
            # Ignoriere eigene Nachrichten
            if actor_id == self.username:
                continue
            
            # Prüfe auf Trigger-Wörter
            if any(trigger in message_text for trigger in TRIGGER_WORDS):
                # Hole Status und antworte
                status = self.get_nippes_status()
                response_message = self.format_status_message(status)
                self.send_message(token, response_message)
                print(f"Antwort gesendet in Konversation {token}")
                return True
        
        return False
    
    def run(self):
        """Hauptschleife des Bots."""
        print(f"Bot gestartet für Benutzer: {self.username}")
        print(f"Nextcloud URL: {self.base_url}")
        print(f"Nippes API: {NIPPES_API_URL}")
        print("Bot läuft... Drücke Ctrl+C zum Beenden")
        
        last_check = {}
        
        try:
            while True:
                conversations = self.get_conversations()
                
                for conv in conversations:
                    token = conv.get('token')
                    if not token:
                        continue
                    
                    # Prüfe nur alle 10 Sekunden pro Konversation
                    if token in last_check:
                        if time.time() - last_check[token] < 10:
                            continue
                    
                    self.check_and_respond(token)
                    last_check[token] = time.time()
                
                # Warte 5 Sekunden vor dem nächsten Check
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\nBot wird beendet...")
        except Exception as e:
            print(f"Fehler in der Hauptschleife: {e}")

def main():
    """Hauptfunktion."""
    # Prüfe Konfiguration
    if not BOT_PASSWORD:
        print("FEHLER: BOT_PASSWORD nicht gesetzt!")
        print("Setze die Umgebungsvariable oder ändere das Skript.")
        print("\nBeispiel:")
        print("export BOT_PASSWORD='dein-app-passwort'")
        print("export NEXTCLOUD_URL='https://deine-nextcloud.de'")
        print("export NIPPES_API_URL='http://localhost:5001/api/status'")
        return 1
    
    bot = NextcloudTalkBot()
    bot.run()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

