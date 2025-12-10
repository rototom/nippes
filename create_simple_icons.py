#!/usr/bin/env python3
"""
Erstellt einfache PNG-Icons mit Bier-Emoji.
Funktioniert auch ohne Pillow - erstellt SVG-Dateien, die als PNG verwendet werden können.
"""

import os
import base64

def create_svg_icon(size):
    """Erstellt ein SVG-Icon mit Bier-Emoji."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <rect width="{size}" height="{size}" fill="#667eea"/>
  <text x="50%" y="50%" font-size="{int(size * 0.6)}" text-anchor="middle" dominant-baseline="central" font-family="Arial, sans-serif">🍺</text>
</svg>'''
    return svg

def main():
    """Hauptfunktion zum Generieren der Icons."""
    sizes = [192, 512]
    static_dir = 'static'
    
    # Erstelle static-Verzeichnis falls nicht vorhanden
    os.makedirs(static_dir, exist_ok=True)
    
    for size in sizes:
        svg_content = create_svg_icon(size)
        filename = f'{static_dir}/icon-{size}.svg'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f'SVG-Icon erstellt: {filename} ({size}x{size})')
        print('Hinweis: Für PWA werden PNG-Dateien benötigt. Konvertiere die SVGs mit einem Tool wie Inkscape oder ImageMagick.')

if __name__ == '__main__':
    main()

