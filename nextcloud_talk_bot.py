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
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        # Track bereits verarbeitete Nachrichten, um Doppelantworten zu vermeiden
        self.processed_messages = set()  # Set von (token, message_id) Tupeln
    
    def get_conversations(self):
        """Holt alle Konversationen des Bots."""
        url = f"{self.base_url}/ocs/v2.php/apps/spreed/api/v4/room"
        try:
            response = self.session.get(url)
            
            # Prüfe ob Antwort JSON ist
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                print(f"⚠ WARNUNG: Antwort ist kein JSON! Content-Type: {content_type}")
                print(f"Erste 500 Zeichen der Antwort: {response.text[:500]}")
            
            response.raise_for_status()
            
            # Versuche JSON zu parsen
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"⚠ JSON Parse Fehler: {e}")
                print(f"Response Text: {response.text[:1000]}")
                return []
            
            if 'ocs' in data and 'data' in data['ocs']:
                return data['ocs']['data']
            else:
                print(f"⚠ Unerwartete Antwort-Struktur: {data}")
                return []
        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP Fehler beim Abrufen der Konversationen: {e}")
            print(f"Response: {response.text[:500] if 'response' in locals() else 'Keine Antwort'}")
            return []
        except Exception as e:
            print(f"✗ Fehler beim Abrufen der Konversationen: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_messages(self, token, limit=50):
        """Holt die letzten Nachrichten einer Konversation."""
        # Versuche verschiedene API-Endpunkte
        # Hinweis: Für direkte Chats (Typ 1) könnte ein anderer Endpoint benötigt werden
        endpoints = [
            (f"{self.base_url}/ocs/v2.php/apps/spreed/api/v1/chat/{token}", "v1"),
            (f"{self.base_url}/ocs/v2.php/apps/spreed/api/v3/chat/{token}", "v3"),
            (f"{self.base_url}/ocs/v2.php/apps/spreed/api/v4/chat/{token}", "v4"),
        ]
        
        for url, version in endpoints:
            # Versuche verschiedene Parameter-Kombinationen
            param_sets = [
                {'limit': limit},
                {'limit': limit, 'lookIntoFuture': '0'},
                {'limit': limit, 'includeLastRead': '0'},
                {},  # Keine Parameter
            ]
            
            for params in param_sets:
                try:
                    response = self.session.get(url, params=params)
                    
                    # Prüfe Status Code
                    if response.status_code == 500:
                        # Versuche nächste Parameter-Kombination
                        continue
                    
                    if response.status_code == 404:
                        # Versuche nächste Parameter-Kombination
                        continue
                    
                    if response.status_code == 403:
                        # Versuche nächste Parameter-Kombination
                        continue
                    
                    response.raise_for_status()
                    
                    # Prüfe Content-Type
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/json' not in content_type:
                        # Versuche nächste Parameter-Kombination
                        continue
                    
                    data = response.json()
                    if 'ocs' in data and 'data' in data['ocs']:
                        messages = data['ocs']['data']
                        print(f"    → API {version} mit Parametern {params}: {len(messages)} Nachrichten gefunden")
                        return messages
                    elif isinstance(data, list):
                        # Manche APIs geben direkt eine Liste zurück
                        print(f"    → API {version} mit Parametern {params}: {len(data)} Nachrichten gefunden (direkte Liste)")
                        return data
                    else:
                        # Versuche nächste Parameter-Kombination
                        continue
                        
                except requests.exceptions.HTTPError as e:
                    if response.status_code in [404, 500, 403]:
                        # Versuche nächste Parameter-Kombination
                        continue
                    # Versuche nächste Parameter-Kombination
                    continue
                except Exception as e:
                    # Versuche nächste Parameter-Kombination
                    continue
        
        # Alle Endpoints fehlgeschlagen
        print(f"    → Alle API-Endpunkte fehlgeschlagen für {token}")
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
            response = requests.get(NIPPES_API_URL, timeout=5, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.SSLError as e:
            print(f"⚠ SSL-Fehler bei API-Aufruf: {e}")
            # Versuche ohne SSL-Verifizierung
            try:
                response = requests.get(NIPPES_API_URL, timeout=5, verify=False)
                response.raise_for_status()
                return response.json()
            except Exception as e2:
                return {
                    'is_open': False,
                    'message': f'Fehler beim Abrufen des Status: {str(e2)}'
                }
        except Exception as e:
            print(f"⚠ Fehler beim API-Aufruf: {e}")
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
    
    def check_and_respond(self, token, conversation_name=None):
        """Prüft neue Nachrichten und antwortet bei Bedarf."""
        messages = self.get_messages(token)
        
        # Wenn keine Nachrichten verfügbar (z.B. wegen Berechtigungsproblemen)
        if not messages:
            return False
        
        # Prüfe die letzten Nachrichten
        for msg in reversed(messages):  # Von alt nach neu
            message_text = msg.get('message', '').lower()
            actor_id = msg.get('actorId', '')
            actor_display_name = msg.get('actorDisplayName', actor_id)
            message_id = msg.get('id', 'unknown')
            
            # Ignoriere eigene Nachrichten
            if actor_id == self.username:
                continue
            
            # Prüfe auf Trigger-Wörter
            matched_trigger = None
            for trigger in TRIGGER_WORDS:
                if trigger in message_text:
                    matched_trigger = trigger
                    break
            
            if matched_trigger:
                # WICHTIG: Markiere Nachricht SOFORT als verarbeitet, um Doppelantworten zu vermeiden
                message_key = (token, message_id)
                if message_key in self.processed_messages:
                    # Nachricht bereits verarbeitet, überspringe
                    continue
                
                # Markiere Nachricht als verarbeitet BEVOR wir irgendetwas tun
                self.processed_messages.add(message_key)
                
                # Begrenze die Größe des Sets (älteste Einträge entfernen)
                if len(self.processed_messages) > 1000:
                    # Entferne die ältesten 500 Einträge
                    self.processed_messages = set(list(self.processed_messages)[500:])
                
                # Prüfe ob API erreichbar ist
                try:
                    test_response = requests.get(NIPPES_API_URL, timeout=2, verify=False)
                    if test_response.status_code != 200:
                        print(f"⚠ API nicht erreichbar (Status {test_response.status_code}), überspringe Antwort")
                        print(f"   URL: {NIPPES_API_URL}")
                        continue
                except requests.exceptions.SSLError as e:
                    print(f"⚠ SSL-Fehler bei API-Aufruf: {e}, überspringe Antwort")
                    continue
                except Exception as e:
                    print(f"⚠ API nicht erreichbar ({e}), überspringe Antwort")
                    continue
                
                # Begrenze die Größe des Sets (älteste Einträge entfernen)
                if len(self.processed_messages) > 1000:
                    # Entferne die ältesten 500 Einträge
                    self.processed_messages = set(list(self.processed_messages)[500:])
                
                # Hole Status und antworte
                status = self.get_nippes_status()
                response_message = self.format_status_message(status)
                if self.send_message(token, response_message):
                    conv_info = f" ({conversation_name})" if conversation_name else ""
                    print(f"✓ Antwort gesendet in Konversation {token}{conv_info} (auf Nachricht von {actor_display_name})")
                    return True
                else:
                    print(f"✗ Fehler beim Senden der Antwort in Konversation {token}")
        
        return False
    
    def run(self):
        """Hauptschleife des Bots."""
        print(f"Bot gestartet für Benutzer: {self.username}")
        print(f"Nextcloud URL: {self.base_url}")
        print(f"Nippes API: {NIPPES_API_URL}")
        print("Bot läuft... Drücke Ctrl+C zum Beenden")
        print()
        
        last_check = {}
        error_count = {}
        
        try:
            while True:
                conversations = self.get_conversations()
                
                if not conversations:
                    print("⚠ Keine Konversationen gefunden. Stelle sicher, dass der Bot Mitglied in Talk-Konversationen ist.")
                    time.sleep(30)  # Warte länger wenn keine Konversationen
                    continue
                
                # Zeige Status nur alle 60 Sekunden, um Logs ruhiger zu halten
                current_time = time.time()
                if not hasattr(self, '_last_status_time') or current_time - self._last_status_time > 60:
                    print(f"✓ Überwache {len(conversations)} Konversation(en)...")
                    self._last_status_time = current_time
                
                for conv in conversations:
                    token = conv.get('token')
                    name = conv.get('displayName', conv.get('name', 'Unbekannt'))
                    conv_type = conv.get('type', 'unknown')
                    
                    if not token:
                        continue
                    
                    # Prüfe nur alle 10 Sekunden pro Konversation
                    if token in last_check:
                        if time.time() - last_check[token] < 10:
                            continue
                    
                    # Überspringe Konversationen mit zu vielen Fehlern
                    if error_count.get(token, 0) > 10:
                        if error_count[token] == 11:  # Nur einmal warnen
                            print(f"⚠ Überspringe Konversation {token} ({name}) wegen wiederholter Fehler")
                        continue
                    
                    # Debug: Zeige welche Konversation geprüft wird
                    print(f"\nPrüfe Konversation: {name} (Typ: {conv_type}, Token: {token})")
                    
                    try:
                        if self.check_and_respond(token, name):
                            error_count[token] = 0  # Reset Fehlerzähler bei Erfolg
                        else:
                            # Wenn keine Nachrichten verfügbar waren, reduziere Fehlerzähler langsam
                            if error_count.get(token, 0) > 0:
                                error_count[token] = max(0, error_count[token] - 1)
                    except Exception as e:
                        error_count[token] = error_count.get(token, 0) + 1
                        if error_count[token] <= 3:  # Nur erste Fehler ausgeben
                            print(f"✗ Fehler in Konversation {token} ({name}): {e}")
                        import traceback
                        traceback.print_exc()
                    
                    last_check[token] = time.time()
                
                # Warte 5 Sekunden vor dem nächsten Check
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\nBot wird beendet...")
        except Exception as e:
            print(f"Fehler in der Hauptschleife: {e}")
            import traceback
            traceback.print_exc()

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
    
    # Zeige Konfiguration (ohne Passwort)
    print("=== Bot Konfiguration ===")
    print(f"Nextcloud URL: {NEXTCLOUD_URL}")
    print(f"Bot Username: {BOT_USERNAME}")
    print(f"Bot Password: {'*' * len(BOT_PASSWORD) if BOT_PASSWORD else 'NICHT GESETZT'}")
    print(f"Nippes API URL: {NIPPES_API_URL}")
    print("=" * 30)
    print()
    
    # Teste Verbindung
    print("Teste Nextcloud-Verbindung...")
    bot = NextcloudTalkBot()
    test_url = f"{bot.base_url}/ocs/v2.php/apps/spreed/api/v4/room"
    try:
        test_response = bot.session.get(test_url)
        print(f"Test Request Status: {test_response.status_code}")
        if test_response.status_code == 200:
            print("✓ Verbindung erfolgreich!")
        else:
            print(f"⚠ Status Code: {test_response.status_code}")
            print(f"Response: {test_response.text[:200]}")
    except Exception as e:
        print(f"✗ Verbindungstest fehlgeschlagen: {e}")
        return 1
    
    print()
    bot.run()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

