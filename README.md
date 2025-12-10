# Nippes Öffnungsstatus

Eine einfache Webseite, die anzeigt, ob das Nippes in Münster heute geöffnet ist.

## Features

- Prüft automatisch die Öffnungszeiten (Mittwoch bis Samstag)
- Crawlt die offizielle Website, um geschlossene Gesellschaften zu erkennen
- Zeigt eine übersichtliche Statusanzeige
- Listet kommende geschlossene Gesellschaften auf

## Installation

1. Python 3.8+ installieren

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. PWA-Icons generieren:
```bash
python3 create_png_icons.py
```

## Verwendung

### Entwicklung

Die Anwendung starten:
```bash
python app.py
```

Die Webseite ist dann unter `http://localhost:5001` erreichbar.

### Production mit systemd

1. Service-File kopieren:
```bash
sudo cp nippes.service /etc/systemd/system/
```

2. Service aktivieren und starten:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nippes.service
sudo systemctl start nippes.service
```

3. Status prüfen:
```bash
sudo systemctl status nippes.service
```

4. Logs ansehen:
```bash
sudo journalctl -u nippes.service -f
```

## Technologie

- **Backend**: Flask (Python)
- **Web Scraping**: BeautifulSoup4, Requests
- **Frontend**: HTML/CSS mit modernem Design
- **Production Server**: Gunicorn
- **PWA**: Progressive Web App mit Service Worker und Manifest
- **Icons**: PNG-Icons mit Bier-Emoji 🍺

## PWA Installation

Die App kann als Progressive Web App (PWA) auf mobilen Geräten und Desktop-Browsern installiert werden:

- **Chrome/Edge**: Klicke auf das Install-Symbol in der Adressleiste
- **Safari (iOS)**: Tippe auf "Teilen" → "Zum Home-Bildschirm hinzufügen"
- **Firefox**: Klicke auf das Menü → "Seite installieren"

Nach der Installation erscheint die App wie eine native App mit eigenem Icon (🍺) und kann offline verwendet werden.

## Hinweise

- Die Anwendung crawlt die offizielle Website des Nippes, um aktuelle Termine zu erhalten
- Bei Netzwerkproblemen oder wenn die Website nicht erreichbar ist, werden geschlossene Gesellschaften möglicherweise nicht erkannt
- Die Öffnungszeiten sind fest auf Mittwoch bis Samstag eingestellt
- Die Daten werden täglich automatisch aktualisiert (Caching)
Nippes Öffnungszeiten Crawler
