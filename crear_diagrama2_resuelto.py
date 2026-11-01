import os
from PIL import Image, ImageDraw, ImageFont

def create_annotated_diagram2():
    # Load original Diagram 2
    if not os.path.exists('diagrama2_skf.png'):
        print("diagrama2_skf.png not found")
        return
    
    img = Image.open('diagrama2_skf.png').convert('RGBA')
    W, H = img.size
    
    # Create overlay for crisp drawing
    overlay = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # In Diagram 2 SKF:
    # X axis: Pd from 1 kW to 1000 kW (logarithmic, 3 decades)
    # The grid area in the scanned image:
    # Left border of grid approx x = 180, right border approx x = 780
    # Top border (n=5000) approx y = 145, bottom border (n=100) approx y = 445
    # Let's calibrate carefully:
    # 1 kW -> x=188, 10 kW -> x=396, 100 kW -> x=605, 1000 kW -> x=812
    # For Pd = 72.71 kW: log10(72.71) = 1.8616 -> x = 188 + (605-188)*(1.8616-0)/(2-0) = 575
    # For n = 1856 rpm: log10(1856) = 3.2686 -> between n=1000 (y=265) and n=2000 (y=210)
    # y = 265 - (265-210)*(log10(1856)-log10(1000))/(log10(2000)-log10(1000)) = 265 - 55*(0.2686/0.3010) = 216
    
    x_pt = 560
    y_pt = 222
    
    # Draw horizontal dashed crosshair line
    draw.line([(180, y_pt), (x_pt, y_pt)], fill=(220, 38, 38, 240), width=2)
    # Draw vertical dashed crosshair line
    draw.line([(x_pt, y_pt), (x_pt, 455)], fill=(220, 38, 38, 240), width=2)
    
    # Target circle glow
    draw.ellipse([(x_pt - 14, y_pt - 14), (x_pt + 14, y_pt + 14)], fill=(239, 68, 68, 70), outline=(220, 38, 38, 200), width=2)
    draw.ellipse([(x_pt - 6, y_pt - 6), (x_pt + 6, y_pt + 6)], fill=(220, 38, 38, 255), outline=(255, 255, 255, 255), width=2)
    
    # Text Banner Box
    box_x0 = x_pt - 150
    box_y0 = y_pt - 65
    box_x1 = x_pt + 210
    box_y1 = y_pt - 12
    
    draw.rectangle([(box_x0, box_y0), (box_x1, box_y1)], fill=(15, 23, 42, 235), outline=(220, 38, 38, 255), width=2)
    
    # Pointer line from box to point
    draw.line([(x_pt, box_y1), (x_pt, y_pt - 8)], fill=(220, 38, 38, 255), width=2)
    
    # Text inside box
    try:
        font_b = ImageFont.truetype("arialbd.ttf", 15)
        font_s = ImageFont.truetype("arial.ttf", 13)
    except:
        font_b = ImageFont.load_default()
        font_s = ImageFont.load_default()
        
    draw.text((box_x0 + 10, box_y0 + 6), "PUNTO DE TRABAJO RESUELTO:", fill=(254, 240, 138, 255), font=font_b)
    draw.text((box_x0 + 10, box_y0 + 28), "Pd = 72,71 kW @ 1856 rpm  ->  Perfil SPB-XP", fill=(255, 255, 255, 255), font=font_s)
    
    # Bottom Callout Badge
    draw.rectangle([(180, 465), (780, 498)], fill=(2, 132, 199, 230), outline=(14, 165, 233, 255), width=1)
    draw.text((195, 473), "RESOLUCION: Se adopta Perfil Estrecho de Alta Potencia SKF SPB-XP (Extra Power)", fill=(255, 255, 255, 255), font=font_b)
    
    # Merge overlay with original
    annotated = Image.alpha_composite(img, overlay).convert('RGB')
    annotated.save("diagrama2_skf_resuelto.png", quality=95)
    print("diagrama2_skf_resuelto.png created successfully!")

if __name__ == '__main__':
    create_annotated_diagram2()

