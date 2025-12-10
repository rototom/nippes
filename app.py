from flask import Flask, render_template
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
import json
import os
from threading import Lock

app = Flask(__name__)

# Cache-Datei für geschlossene Daten
CACHE_FILE = '/root/nippes/closed_dates_cache.json'
CACHE_LOCK = Lock()
CACHE_DURATION_HOURS = 24  # Cache für 24 Stunden

def crawl_closed_dates():
    """Crawlt die Nippes-Website und extrahiert alle Daten mit geschlossenen Gesellschaften."""
    try:
        url = "https://www.nippes-muenster.de/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        closed_dates = set()
        
        # Suche nach Datumsangaben im Format DD.MM.YY gefolgt von "geschlossene Gesellschaft"
        # Die geschlossenen Gesellschaften stehen in der Liste der Veranstaltungen
        text = soup.get_text()
        
        # Pattern für Datum gefolgt von "geschlossene Gesellschaft"
        # Format: DD.MM.YY geschlossene Gesellschaft
        pattern = r'(\d{2})\.(\d{2})\.(\d{2})\s+geschlossene\s+gesellschaft'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        # Konvertiere gefundene Daten zu datetime-Objekten
        for match in matches:
            day, month, year = match.groups()
            # Jahr interpretieren (YY -> 20YY)
            full_year = 2000 + int(year)
            try:
                date_obj = datetime(full_year, int(month), int(day))
                closed_dates.add(date_obj.date())
            except ValueError:
                # Ungültiges Datum überspringen
                continue
        
        # Auch nach einzelnen "geschlossen" Einträgen suchen (z.B. "31.12.25 geschlossen - Silvester")
        pattern_closed = r'(\d{2})\.(\d{2})\.(\d{2})\s+geschlossen'
        matches_closed = re.finditer(pattern_closed, text, re.IGNORECASE)
        
        for match in matches_closed:
            day, month, year = match.groups()
            full_year = 2000 + int(year)
            try:
                date_obj = datetime(full_year, int(month), int(day))
                closed_dates.add(date_obj.date())
            except ValueError:
                continue
        
        return closed_dates
    except Exception as e:
        print(f"Fehler beim Crawlen der Website: {e}")
        return set()

def load_cached_dates():
    """Lädt gecachte geschlossene Daten aus der Datei."""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                # Prüfe, ob Cache noch gültig ist (weniger als 24 Stunden alt)
                if datetime.now() - cache_time < timedelta(hours=CACHE_DURATION_HOURS):
                    # Konvertiere String-Daten zurück zu date-Objekten
                    dates = [datetime.fromisoformat(d).date() for d in cache_data['dates']]
                    return set(dates), cache_time
    except Exception as e:
        print(f"Fehler beim Laden des Caches: {e}")
    return None, None

def save_cached_dates(closed_dates):
    """Speichert geschlossene Daten in der Cache-Datei."""
    try:
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'dates': [d.isoformat() for d in closed_dates]
        }
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f)
    except Exception as e:
        print(f"Fehler beim Speichern des Caches: {e}")

def get_closed_dates():
    """Holt geschlossene Daten aus dem Cache oder crawlt neu, falls nötig."""
    with CACHE_LOCK:
        # Versuche Cache zu laden
        cached_dates, cache_time = load_cached_dates()
        
        if cached_dates is not None:
            print(f"Verwende gecachte Daten vom {cache_time.strftime('%Y-%m-%d %H:%M:%S')}")
            return cached_dates, cache_time
        
        # Cache ist abgelaufen oder nicht vorhanden, crawle neu
        print("Cache abgelaufen oder nicht vorhanden, crawle Website neu...")
        closed_dates = crawl_closed_dates()
        save_cached_dates(closed_dates)
        now = datetime.now()
        print(f"Neue Daten gecrawlt: {len(closed_dates)} geschlossene Termine gefunden")
        return closed_dates, now

def is_open_today(closed_dates):
    """Prüft, ob das Nippes heute geöffnet ist."""
    today = datetime.now().date()
    weekday = today.weekday()  # 0 = Montag, 6 = Sonntag
    
    # Öffnungszeiten: Mittwoch (2) bis Samstag (5)
    if weekday < 2 or weekday > 5:
        return False, "Heute ist nicht Mittwoch bis Samstag"
    
    # Prüfe auf geschlossene Gesellschaften
    if today in closed_dates:
        return False, "Heute ist geschlossene Gesellschaft"
    
    return True, "Das Nippes ist heute geöffnet, viel Spaß damit!"

@app.route('/')
def index():
    """Hauptseite, die den Öffnungsstatus anzeigt."""
    # Hole geschlossene Daten und Zeitstempel
    closed_dates, last_update = get_closed_dates()
    
    # Prüfe Öffnungsstatus
    is_open, message = is_open_today(closed_dates)
    
    # Hole auch die nächsten geschlossenen Termine für Info
    today = datetime.now().date()
    upcoming_closed = sorted([d for d in closed_dates if d >= today])[:5]
    
    return render_template('index.html', 
                         is_open=is_open, 
                         message=message,
                         upcoming_closed=upcoming_closed,
                         last_update=last_update)

@app.route('/refresh')
def refresh_cache():
    """Manueller Endpoint zum Neuladen des Caches."""
    try:
        # Lösche Cache-Datei, damit beim nächsten Aufruf neu gecrawlt wird
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        
        # Crawle sofort neu
        closed_dates = crawl_closed_dates()
        save_cached_dates(closed_dates)
        
        return {
            'status': 'success',
            'message': f'Cache aktualisiert. {len(closed_dates)} geschlossene Termine gefunden.',
            'timestamp': datetime.now().isoformat()
        }, 200
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Fehler beim Aktualisieren: {str(e)}'
        }, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

