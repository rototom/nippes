# Troubleshooting - Nextcloud Talk Bot

## Problem: Statuscode 996 - Keine Berechtigung

Wenn du den Fehler `statuscode 996` siehst, bedeutet das, dass der Bot keine Berechtigung hat, Nachrichten zu lesen.

### Lösung 1: Bot als Moderator setzen

1. Gehe zu den Einstellungen der Talk-Konversation
2. Wähle den Bot-Benutzer aus der Teilnehmerliste
3. Setze die Rolle auf **"Moderator"** oder **"Admin"**
4. Speichere die Änderungen

Der Bot sollte jetzt Nachrichten lesen können.

### Lösung 2: Öffentliche Gruppe verwenden

Teste den Bot in einer **öffentlichen Gruppe** statt in einem direkten Chat:
- Öffentliche Gruppen haben oft weniger strenge Berechtigungen
- Der Bot kann dort möglicherweise Nachrichten lesen, auch ohne Moderator-Rechte

### Lösung 3: Webhook-Alternative (falls verfügbar)

Falls Nextcloud Talk Webhooks unterstützt, könntest du einen Webhook-Endpoint in der Flask-App erstellen, der von Nextcloud aufgerufen wird, wenn eine Nachricht gesendet wird.

## Problem: Bot reagiert nicht auf Nachrichten

### Prüfe:

1. **Bot läuft:** Ist der Bot-Prozess aktiv?
   ```bash
   ps aux | grep nextcloud_talk_bot
   ```

2. **Bot ist Mitglied:** Ist der Bot-Benutzer Mitglied der Konversation?

3. **Berechtigungen:** Hat der Bot-Benutzer Moderator- oder Admin-Rechte?

4. **Trigger-Wörter:** Werden die richtigen Trigger-Wörter verwendet?
   - `nippes`
   - `ist das nippes offen`
   - `nippes status`
   - `ist das nippes geöffnet`
   - `nippes heute`

5. **API erreichbar:** Kann der Bot die Nippes-API erreichen?
   ```bash
   curl http://localhost:5001/api/status
   ```

## Problem: 500 Internal Server Error

Ein 500-Fehler kann verschiedene Ursachen haben:

1. **Nextcloud-Konfiguration:** Prüfe die Nextcloud-Logs
2. **PHP-Konfiguration:** Prüfe PHP-Fehlerlogs
3. **Talk-App:** Stelle sicher, dass die Talk-App aktualisiert ist
4. **Berechtigungen:** Prüfe Dateiberechtigungen auf dem Server

## Debug-Modus aktivieren

Um mehr Informationen zu erhalten, aktiviere die Debug-Ausgaben im Bot-Skript. Die Debug-Ausgaben zeigen:
- Welche Konversationen geprüft werden
- Welche API-Endpunkte verwendet werden
- Welche Fehler auftreten
- Ob Nachrichten gefunden werden

## Häufige Probleme

### Bot sieht Konversationen, aber keine Nachrichten

**Ursache:** Bot hat keine Berechtigung, Nachrichten zu lesen.

**Lösung:** Setze den Bot-Benutzer als Moderator oder Admin in den Konversationen.

### Bot stürzt ab

**Ursache:** Unbehandelte Exceptions.

**Lösung:** Prüfe die Logs und stelle sicher, dass alle Abhängigkeiten installiert sind.

### Bot antwortet nicht

**Ursache:** Trigger-Wörter werden nicht erkannt oder API ist nicht erreichbar.

**Lösung:** 
- Prüfe die Trigger-Wörter (Groß-/Kleinschreibung wird ignoriert)
- Prüfe, ob die Nippes-API erreichbar ist
- Prüfe die Bot-Logs auf Fehler

## Support

Bei weiteren Problemen:
1. Prüfe die Bot-Logs: `journalctl -u nippes-talk-bot.service -f`
2. Prüfe die Nextcloud-Logs
3. Teste die API: `curl http://localhost:5001/api/status`
4. Prüfe die Konfiguration in `.env`

