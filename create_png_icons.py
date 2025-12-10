#!/usr/bin/env python3
"""
Erstellt PNG-Icons für PWA.
Versucht Pillow zu verwenden, falls nicht verfügbar werden einfache farbige Quadrate erstellt.
"""

import os

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("Pillow nicht verfügbar. Installiere mit: pip install pillow")
    print("Erstelle einfache farbige Icons als Fallback...")

def create_icon_pillow(size):
    """Erstellt Icon mit Pillow."""
    img = Image.new('RGBA', (size, size), (102, 126, 234, 255))  # #667eea
    draw = ImageDraw.Draw(img)
    
    # Versuche Emoji-Schriftart zu finden
    font_size = int(size * 0.6)
    try:
        # macOS
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Apple Color Emoji.ttc", font_size)
    except:
        try:
            # Linux
            font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", font_size)
        except:
            # Fallback
            font = ImageFont.load_default()
    
    text = "🍺"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2)
    
    draw.text(position, text, font=font, fill=(255, 255, 255, 255))
    return img

def create_icon_simple(size):
    """Erstellt einfaches Icon ohne Pillow."""
    # Erstelle ein einfaches farbiges Quadrat mit Text
    # Da wir kein Pillow haben, erstellen wir eine SVG und konvertieren sie später
    # Oder wir erstellen ein sehr einfaches PNG mit base64
    # Für jetzt: Erstelle SVG, das als PNG verwendet werden kann
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">
  <rect width="{size}" height="{size}" fill="#667eea"/>
  <text x="50%" y="50%" font-size="{int(size * 0.6)}" text-anchor="middle" dominant-baseline="central" fill="white">🍺</text>
</svg>'''
    return svg_content

def main():
    """Hauptfunktion."""
    sizes = [192, 512]
    static_dir = 'static'
    os.makedirs(static_dir, exist_ok=True)
    
    if HAS_PILLOW:
        for size in sizes:
            icon = create_icon_pillow(size)
            filename = f'{static_dir}/icon-{size}.png'
            icon.save(filename, 'PNG')
            print(f'PNG-Icon erstellt: {filename} ({size}x{size})')
    else:
        print("\nPillow nicht verfügbar. Erstelle SVG-Dateien...")
        print("Für PWA benötigst du PNG-Dateien.")
        print("Optionen:")
        print("1. Installiere Pillow: pip install pillow")
        print("2. Konvertiere SVG zu PNG mit einem Online-Tool oder ImageMagick")
        print("3. Verwende die SVG-Dateien direkt (nicht alle Browser unterstützen SVG in PWAs)")
        
        for size in sizes:
            svg_content = create_icon_simple(size)
            filename = f'{static_dir}/icon-{size}.svg'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            print(f'SVG-Icon erstellt: {filename}')

if __name__ == '__main__':
    main()

