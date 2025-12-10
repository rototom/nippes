# Nextcloud Talk Bot - Externe Lösung (ohne Serverzugriff)

Diese Lösung funktioniert ohne Zugriff auf den Nextcloud-Server und ist ideal für Hetzner Storage Share oder andere gehostete Nextcloud-Instanzen.

## Funktionsweise

Der Bot läuft als externer Service und:
1. Verbindet sich über die Nextcloud Talk API
2. Überwacht Konversationen, in denen der Bot Mitglied ist
3. Reagiert auf bestimmte Trigger-Wörter (z.B. "nippes", "ist das nippes offen")
4. Sendet automatisch den aktuellen Status

## Voraussetzungen

1. **Bot-Benutzerkonto erstellen:**
   - In Nextcloud ein neues Benutzerkonto erstellen (z.B. "nippes-bot")
   - Optional: Bot-Benutzer zu einer Gruppe hinzufügen

2. **App-Passwort erstellen:**
   - Als Bot-Benutzer einloggen
   - Einstellungen > Sicherheit > App-Passwörter
   - Neues App-Passwort erstellen (z.B. "Talk Bot")
   - **WICHTIG:** Das App-Passwort kopieren und sicher aufbewahren!

3. **Bot zu Talk-Konversationen hinzufügen:**
   - In den gewünschten Talk-Konversationen den Bot-Benutzer hinzufügen
   - Der Bot muss Mitglied der Konversation sein, um Nachrichten zu sehen

4. **Nippes API muss erreichbar sein:**
   - Die Flask-App muss laufen
   - Die API muss vom Bot-Server aus erreichbar sein

## Installation

### 1. Abhängigkeiten installieren

```bash
pip install requests
```

### 2. Konfiguration

Kopiere die Beispiel-Konfiguration:
```bash
cp nextcloud_bot_config.env.example .env
```

Bearbeite `.env` und trage deine Werte ein:
```bash
NEXTCLOUD_URL=https://deine-nextcloud.de
BOT_USERNAME=nippes-bot
BOT_PASSWORD=dein-app-passwort
NIPPES_API_URL=http://localhost:5001/api/status
```

### 3. Umgebungsvariablen setzen

```bash
export $(cat .env | xargs)
```

Oder lade sie direkt im Skript:
```bash
source .env
python3 nextcloud_talk_bot.py
```

### 4. Bot starten

```bash
python3 nextcloud_talk_bot.py
```

Der Bot läuft jetzt und überwacht alle Konversationen, in denen er Mitglied ist.

## Verwendung

In einer Nextcloud Talk Konversation, in der der Bot Mitglied ist:

**Trigger-Wörter:**
- `nippes`
- `ist das nippes offen`
- `nippes status`
- `ist das nippes geöffnet`
- `nippes heute`

Der Bot antwortet automatisch mit dem aktuellen Status, z.B.:
```
🍺 Das Nippes ist heute geöffnet, viel Spaß damit!

Heute ist Mittwoch

Kommende geschlossene Gesellschaften: 15.12.2025, 20.12.2025
```

## Als Systemdienst ausführen

Für dauerhaften Betrieb kannst du den Bot als systemd-Service einrichten:

**`/etc/systemd/system/nippes-talk-bot.service`:**
```ini
[Unit]
Description=Nippes Nextcloud Talk Bot
After=network.target

[Service]
Type=simple
User=dein-benutzer
WorkingDirectory=/pfad/zum/nippes
EnvironmentFile=/pfad/zum/nippes/.env
ExecStart=/usr/bin/python3 /pfad/zum/nippes/nextcloud_talk_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Service aktivieren:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable nippes-talk-bot.service
sudo systemctl start nippes-talk-bot.service
```

## Anpassungen

### Trigger-Wörter ändern

Bearbeite die `TRIGGER_WORDS` Liste in `nextcloud_talk_bot.py`:
```python
TRIGGER_WORDS = ['nippes', 'dein-trigger', 'anderer-trigger']
```

### Check-Intervall anpassen

Ändere die Wartezeiten in der `run()` Methode:
```python
time.sleep(5)  # Sekunden zwischen Checks
```

### Nur bestimmte Konversationen überwachen

Füge eine Filterung in `run()` hinzu:
```python
for conv in conversations:
    token = conv.get('token')
    # Nur bestimmte Konversationen
    if token not in ['erlaubte-token-1', 'erlaubte-token-2']:
        continue
```

## Fehlerbehebung

### Bot antwortet nicht

1. **Prüfe Bot-Login:**
   ```bash
   curl -u "bot-username:bot-password" https://deine-nextcloud.de/ocs/v2.php/apps/spreed/api/v4/room
   ```

2. **Prüfe API-Erreichbarkeit:**
   ```bash
   curl http://localhost:5001/api/status
   ```

3. **Prüfe Bot-Mitgliedschaft:**
   - Stelle sicher, dass der Bot-Benutzer Mitglied der Konversation ist
   - Der Bot kann nur Nachrichten in Konversationen sehen, in denen er Mitglied ist

### "Unauthorized" Fehler

- Prüfe, ob das App-Passwort korrekt ist
- Stelle sicher, dass der Benutzername korrekt ist
- Prüfe, ob die Nextcloud-URL korrekt ist (ohne trailing slash)

### Bot sieht keine Nachrichten

- Der Bot muss Mitglied der Konversation sein
- Prüfe die Bot-Logs auf Fehler
- Stelle sicher, dass die Nextcloud Talk API aktiviert ist

## Sicherheit

- **App-Passwort sicher aufbewahren:** Nicht in Git committen!
- **.env Datei in .gitignore:** Füge `.env` zur `.gitignore` hinzu
- **Bot-Berechtigungen:** Der Bot-Benutzer sollte nur minimale Berechtigungen haben
- **HTTPS verwenden:** Stelle sicher, dass die Nextcloud-URL HTTPS verwendet

## Erweiterte Funktionen

### Mehrere Nextcloud-Instanzen

Du kannst mehrere Bot-Instanzen für verschiedene Nextcloud-Instanzen starten:
```bash
NEXTCLOUD_URL=https://nextcloud1.de BOT_USERNAME=bot1 python3 nextcloud_talk_bot.py &
NEXTCLOUD_URL=https://nextcloud2.de BOT_USERNAME=bot2 python3 nextcloud_talk_bot.py &
```

### Webhook-Alternative

Falls Nextcloud Webhooks unterstützt, könntest du auch einen Webhook-Endpoint in der Flask-App erstellen, der von Nextcloud aufgerufen wird.

## Support

Bei Problemen:
1. Prüfe die Logs: `journalctl -u nippes-talk-bot.service -f`
2. Teste die API: `curl http://localhost:5001/api/status`
3. Teste Nextcloud-Verbindung: Siehe Fehlerbehebung oben

