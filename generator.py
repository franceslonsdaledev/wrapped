import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def load_data(filepath: str) -> dict:
    with open(filepath, "r") as f:
        return json.load(f)

def create_wrapped_card():
    # 1. Load data
    data = load_data("habits.json")
    
    # 2. Image dimensions (Instagram portrait: 1080 x 1350)
    width, height = 1080, 1350
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    
    # 3. Draw a custom vertical gradient (Deep dark charcoal to soft pastel peach/pink)
    color_top = (18, 18, 24)       # Sleek dark mode base
    color_bottom = (45, 27, 43)    # Warm aesthetic purple/pink tint
    
    for y in range(height):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / height))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / height))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # 4. Typography setup (Using default or system TTF fonts if available)
    try:
        # Tries to use standard system fonts; falls back gracefully if needed
        title_font = ImageFont.truetype("arial.ttf", 60)
        stat_font = ImageFont.truetype("arial.ttf", 90)
        label_font = ImageFont.truetype("arial.ttf", 32)
        small_font = ImageFont.truetype("arial.ttf", 26)
    except IOError:
        title_font = ImageFont.load_default()
        stat_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # 5. Render UI Elements
    # Header branding
    draw.text((80, 100), "@YOURCSBIGSISTER", fill=(255, 182, 193), font=small_font)
    draw.text((80, 140), "WEEKLY WRAPPED", fill=(255, 255, 255), font=title_font)
    draw.text((80, 210), data["week_label"], fill=(160, 160, 180), font=label_font)
    
    # Accent pill / divider line
    draw.rectangle([80, 270, 200, 278], fill=(255, 182, 193))

    # Stat Block 1: Coding Hours
    draw.text((80, 360), "TOTAL CODING TIME", fill=(160, 160, 180), font=label_font)
    draw.text((80, 410), f"{data['coding_hours']} HRS", fill=(255, 255, 255), font=stat_font)
    
    # Stat Block 2: Running
    draw.text((80, 580), "RUNNING DISTANCE", fill=(160, 160, 180), font=label_font)
    draw.text((80, 630), f"{data['running_km']} KM", fill=(255, 255, 255), font=stat_font)

    # Stat Block 3: Top Soundtrack / Vibe
    draw.text((80, 800), "HEAVY ROTATION AUDIO", fill=(160, 160, 180), font=label_font)
    draw.text((80, 850), data["top_artist"], fill=(255, 182, 193), font=title_font)

    # Footer quote card box
    draw.rounded_rectangle([80, 1030, 1000, 1220], radius=24, outline=(70, 60, 80), width=2, fill=(25, 22, 32))
    draw.text((120, 1080), f'"{data["favorite_quote"]}"', fill=(220, 220, 230), font=label_font)

    # 6. Save output image
    output_path = "weekly_wrapped_card.png"
    image.save(output_path, "PNG")
    print(f"Success! Generated your aesthetic card at: {Path(output_path).resolve()}")

if __name__ == "__main__":
    create_wrapped_card()