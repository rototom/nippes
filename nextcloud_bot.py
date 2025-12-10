#!/usr/bin/env python3
"""
Nextcloud Talk Bot für Nippes Status
Erweiterte Python-Version mit besserer JSON-Verarbeitung

Registrierung in Nextcloud:
sudo -u www-data php /var/www/nextcloud/occ talk:command:add nippes "Nippes Status" "/pfad/zum/nextcloud_bot.py {ARGUMENTE} {USER}" 2 3
"""

import sys
import json
import requests
import os

# URL zur API (kann über Umgebungsvariable gesetzt werden)
API_URL = os.environ.get('API_URL', 'http://localhost:5001/api/status')

def get_status():
    """Holt den Status von der API."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            'is_open': False,
            'message': f'Fehler beim Abrufen des Status: {str(e)}'
        }

def format_message(data):
    """Formatiert die Nachricht für Nextcloud Talk."""
    message = data.get('message', 'Status unbekannt')
    
    # Füge Tag hinzu
    day = data.get('day', '')
    if day:
        message += f"\n\nHeute ist {day}"
    
    # Füge kommende geschlossene Termine hinzu
    upcoming = data.get('upcoming_closed', [])
    if upcoming:
        dates_str = ', '.join(upcoming)
        message += f"\n\nKommende geschlossene Gesellschaften: {dates_str}"
    
    # Füge letzte Aktualisierung hinzu
    last_update = data.get('last_update')
    if last_update:
        message += f"\n\nLetzte Aktualisierung: {last_update}"
    
    return message

def main():
    """Hauptfunktion."""
    # Hole Status
    status_data = get_status()
    
    # Formatiere und gebe aus
    output = format_message(status_data)
    print(output)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

