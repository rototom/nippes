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

## Hinweise

- Die Anwendung crawlt die offizielle Website des Nippes, um aktuelle Termine zu erhalten
- Bei Netzwerkproblemen oder wenn die Website nicht erreichbar ist, werden geschlossene Gesellschaften möglicherweise nicht erkannt
- Die Öffnungszeiten sind fest auf Mittwoch bis Samstag eingestellt
Nippes Öffnungszeiten Crawler
