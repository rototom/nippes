# Caddy Reverse Proxy Konfiguration

Wenn die Flask-App hinter einem Caddy Reverse Proxy läuft und `/api/status` einen 404-Fehler gibt, könnte es ein Problem mit der Proxy-Konfiguration sein.

## Mögliche Probleme

1. **Route wird nicht weitergeleitet:** Der Proxy leitet `/api/status` nicht an die Flask-App weiter
2. **Path-Rewriting:** Der Proxy ändert den Pfad, bevor er an die App weitergeleitet wird
3. **Route-Konflikte:** Eine andere Route überschreibt `/api/status`

## Lösung: Caddy-Konfiguration prüfen

### Beispiel-Caddy-Konfiguration (Caddyfile)

```caddy
nippes.okaris.de {
    reverse_proxy localhost:5001 {
        # Stelle sicher, dass alle Routen weitergeleitet werden
        header_up Host {host}
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

### Wichtig: Kein Path-Rewriting

Stelle sicher, dass der Proxy den Pfad **nicht** ändert:

```caddy
# FALSCH - würde /api/status zu /status ändern:
reverse_proxy localhost:5001 {
    rewrite /api/* /{path}
}

# RICHTIG - leitet alles weiter wie es ist:
reverse_proxy localhost:5001
```

## Testen

1. **Direkt testen (ohne Proxy):**
   ```bash
   curl http://localhost:5001/api/status
   ```

2. **Über Proxy testen:**
   ```bash
   curl https://nippes.okaris.de/api/status
   ```

3. **Prüfe Caddy-Logs:**
   ```bash
   journalctl -u caddy -f
   ```

## Alternative: Route direkt testen

Falls der Proxy Probleme macht, kannst du die API auch direkt lokal ansprechen (wie in der `.env` konfiguriert):
```
NIPPES_API_URL=http://localhost:5001/api/status
```

Das umgeht den Proxy komplett und sollte immer funktionieren, wenn Bot und App auf demselben Server laufen.

