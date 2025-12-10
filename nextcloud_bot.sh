#!/bin/bash
# Nextcloud Talk Bot Script für Nippes Status
# Registrierung: sudo -u www-data php /var/www/nextcloud/occ talk:command:add nippes "Nippes Status" "/pfad/zum/nextcloud_bot.sh {ARGUMENTE} {USER}" 2 3

# URL zur API (anpassen falls nötig)
API_URL="${API_URL:-http://localhost:5001/api/status}"

# Hole Status von der API
RESPONSE=$(curl -s "$API_URL")

# Parse JSON Antwort (einfache Methode)
MESSAGE=$(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
IS_OPEN=$(echo "$RESPONSE" | grep -o '"is_open":[^,}]*' | cut -d':' -f2)

# Formatiere Ausgabe für Nextcloud Talk
if [ "$IS_OPEN" = "true" ]; then
    echo "$MESSAGE"
else
    echo "$MESSAGE"
fi

# Optional: Füge zusätzliche Infos hinzu
DAY=$(echo "$RESPONSE" | grep -o '"day":"[^"]*"' | cut -d'"' -f4)
if [ -n "$DAY" ]; then
    echo ""
    echo "Heute ist $DAY"
fi

# Zeige kommende geschlossene Termine
UPCOMING=$(echo "$RESPONSE" | grep -o '"upcoming_closed":\[[^]]*\]' | grep -o '"[^"]*"' | tr -d '"' | tr '\n' ' ')
if [ -n "$UPCOMING" ]; then
    echo ""
    echo "Kommende geschlossene Gesellschaften: $UPCOMING"
fi

exit 0

