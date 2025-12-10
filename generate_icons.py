#!/usr/bin/env python3
"""
Generiert PWA-Icons aus einem Bier-Emoji.
Benötigt: Pillow (pip install pillow)
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow nicht installiert. Installiere mit: pip install pillow")
    exit(1)

def create_icon(size):
    """Erstellt ein Icon mit Bier-Emoji."""
    # Erstelle ein Bild mit transparentem Hintergrund
    img = Image.new('RGBA', (size, size), (102, 126, 234, 255))  # #667eea Farbe
    draw = ImageDraw.Draw(img)
    
    # Versuche, eine Schriftart zu verwenden, die Emojis unterstützt
    try:
        # Verwende eine große Schriftgröße für das Emoji
        font_size = int(size * 0.6)
        # Versuche System-Schriftarten
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", font_size)
            except:
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Zeichne das Bier-Emoji
    text = "🍺"
    # Berechne Position für zentriertes Emoji
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) // 2, (size - text_height) // 2)
    
    draw.text(position, text, font=font, fill=(255, 255, 255, 255))
    
    return img

def main():
    """Hauptfunktion zum Generieren der Icons."""
    sizes = [192, 512]
    static_dir = 'static'
    
    # Erstelle static-Verzeichnis falls nicht vorhanden
    os.makedirs(static_dir, exist_ok=True)
    
    for size in sizes:
        icon = create_icon(size)
        filename = f'{static_dir}/icon-{size}.png'
        icon.save(filename, 'PNG')
        print(f'Icon erstellt: {filename} ({size}x{size})')

if __name__ == '__main__':
    main()

