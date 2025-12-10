# Nextcloud Talk Bot Integration

Dieses Dokument erklärt, wie du den Nippes Status Bot in Nextcloud Talk integrierst.

## Option 1: Shell-Skript Bot (Einfach)

### Voraussetzungen

1. Die Flask-App muss laufen und unter `http://localhost:5001` (oder einer anderen URL) erreichbar sein
2. `curl` muss auf dem Server installiert sein
3. Nextcloud OCC-Zugriff

### Installation

1. Kopiere das Skript auf den Server:
```bash
cp nextcloud_bot.sh /usr/local/bin/nippes-bot.sh
chmod +x /usr/local/bin/nippes-bot.sh
```

2. Teste das Skript manuell:
```bash
/usr/local/bin/nippes-bot.sh
```

3. Registriere den Bot in Nextcloud:
```bash
sudo -u www-data php /var/www/nextcloud/occ talk:command:add nippes "Nippes Status" "/usr/local/bin/nippes-bot.sh {ARGUMENTE} {USER}" 2 3
```

**Parameter:**
- `nippes` - Name des Befehls (wird als `/nippes` verwendet)
- `"Nippes Status"` - Beschreibung
- `/usr/local/bin/nippes-bot.sh` - Pfad zum Skript
- `2` - Antwort-Typ (2 = normale Nachricht)
- `3` - Anzahl der Argumente (0 = keine)

4. Falls die API unter einer anderen URL läuft, setze die Umgebungsvariable:
```bash
export API_URL="http://deine-server-url:5001/api/status"
```

### Verwendung

In einer Nextcloud Talk Konversation:
```
/nippes
```

Der Bot antwortet mit dem aktuellen Status.

## Option 2: Python Bot (Erweitert)

### Voraussetzungen

1. Python 3 installiert
2. `requests` Bibliothek: `pip install requests`
3. Die Flask-App muss laufen

### Installation

1. Installiere Abhängigkeiten:
```bash
pip install requests
```

2. Kopiere das Skript:
```bash
cp nextcloud_bot.py /usr/local/bin/nippes-bot.py
chmod +x /usr/local/bin/nippes-bot.py
```

3. Teste das Skript:
```bash
/usr/local/bin/nippes-bot.py
```

4. Registriere den Bot:
```bash
sudo -u www-data php /var/www/nextcloud/occ talk:command:add nippes "Nippes Status" "/usr/local/bin/nippes-bot.py {ARGUMENTE} {USER}" 2 3
```

### Konfiguration

Setze die API-URL über Umgebungsvariable:
```bash
export API_URL="http://deine-server-url:5001/api/status"
```

Oder ändere die URL direkt im Skript.

## Option 3: Direkter API-Zugriff

Du kannst auch direkt die API-Endpoint verwenden:

```bash
curl http://localhost:5001/api/status
```

Die Antwort ist im JSON-Format:
```json
{
  "is_open": true,
  "message": "🍺 Das Nippes ist heute geöffnet, viel Spaß damit!",
  "day": "Mittwoch",
  "last_update": "10.12.2025 19:00",
  "upcoming_closed": ["15.12.2025", "20.12.2025"]
}
```

## Bot entfernen

Um den Bot zu entfernen:
```bash
sudo -u www-data php /var/www/nextcloud/occ talk:command:delete nippes
```

## Verfügbare Befehle

- `/nippes` - Zeigt den aktuellen Status an

## Fehlerbehebung

1. **Bot antwortet nicht:**
   - Prüfe, ob die Flask-App läuft: `curl http://localhost:5001/api/status`
   - Prüfe die Logs: `journalctl -u nippes.service -f`
   - Teste das Skript manuell

2. **Permission Denied:**
   - Stelle sicher, dass das Skript ausführbar ist: `chmod +x nextcloud_bot.sh`
   - Prüfe die Dateiberechtigungen

3. **API nicht erreichbar:**
   - Prüfe die Firewall-Einstellungen
   - Stelle sicher, dass die App auf `0.0.0.0` läuft (nicht nur `localhost`)
   - Prüfe die API_URL Umgebungsvariable

## Erweiterte Nutzung

Du kannst den Bot auch mit Argumenten erweitern, z.B.:
- `/nippes morgen` - Status für morgen
- `/nippes woche` - Status für die ganze Woche

Dafür müsstest du die Skripte entsprechend anpassen.

