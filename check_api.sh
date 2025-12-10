#!/bin/bash
# Script zum Testen der API-Erreichbarkeit

echo "Teste API-Endpunkte..."
echo ""

# Test 1: Root
echo "1. Teste Root-Endpoint:"
curl -s http://localhost:5001/ | head -20
echo ""
echo ""

# Test 2: API Status
echo "2. Teste API Status-Endpoint:"
curl -s http://localhost:5001/api/status
echo ""
echo ""

# Test 3: Prüfe ob Prozess läuft
echo "3. Prüfe ob Flask/Gunicorn läuft:"
ps aux | grep -E "(flask|gunicorn|python.*app.py)" | grep -v grep
echo ""

# Test 4: Prüfe Port
echo "4. Prüfe ob Port 5001 offen ist:"
netstat -tlnp 2>/dev/null | grep 5001 || ss -tlnp 2>/dev/null | grep 5001
echo ""

