#!/bin/bash
# Script zum Neustarten der Flask-App

echo "Stoppe Flask-App..."
systemctl stop nippes.service

echo "Warte 2 Sekunden..."
sleep 2

echo "Starte Flask-App neu..."
systemctl start nippes.service

echo "Warte 3 Sekunden..."
sleep 3

echo "Prüfe Status..."
systemctl status nippes.service --no-pager

echo ""
echo "Teste API-Endpoint..."
curl -s http://localhost:5001/api/status | head -20

