import os
from PIL import Image, ImageDraw, ImageFont

def create_annotated_diagram2():
    if not os.path.exists('diagrama2_skf.png'):
        print("diagrama2_skf.png not found")
        return
    
    img = Image.open('diagrama2_skf.png').convert('RGBA')
    W, H = img.size  # 860, 535
    
    overlay = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Exact calibrated coordinates:
    # X axis: P = 1 kW at x=62, P = 10 kW at x=285, P = 100 kW at x=507, P = 1000 kW at x=730
    # Y axis: n = 100 rpm at y=403, n = 1000 rpm at y=278, n = 10000 rpm at y=154
    # Pd = 72.71 kW: log10(72.71) = 1.8616 -> x = 62 + (730-62)*(1.8616/3) = 476.5
    # n2 = 1856 rpm: log10(1856) = 3.2686 -> y = 403 - 249 * ((3.2686-2)/2) = 245.1
    
    x_pt = 477
    y_pt = 245
    
    # Horizontal guideline from left axis (x=62) to target point
    draw.line([(62, y_pt), (x_pt, y_pt)], fill=(220, 38, 38, 255), width=2)
    # Vertical guideline from bottom axis (y=403) to target point
    draw.line([(x_pt, y_pt), (x_pt, 403)], fill=(220, 38, 38, 255), width=2)
    
    # Axis markers
    # At left axis (n = 1856 rpm):
    draw.polygon([(52, y_pt - 4), (62, y_pt), (52, y_pt + 4)], fill=(220, 38, 38, 255))
    # At bottom axis (Pd = 72.71 kW):
    draw.polygon([(x_pt - 4, 413), (x_pt, 403), (x_pt + 4, 413)], fill=(220, 38, 38, 255))
    
    # Target bullseye
    draw.ellipse([(x_pt - 14, y_pt - 14), (x_pt + 14, y_pt + 14)], fill=(239, 68, 68, 80), outline=(220, 38, 38, 240), width=2)
    draw.ellipse([(x_pt - 7, y_pt - 7), (x_pt + 7, y_pt + 7)], fill=(220, 38, 38, 255), outline=(255, 255, 255, 255), width=2)
    draw.ellipse([(x_pt - 2, y_pt - 2), (x_pt + 2, y_pt + 2)], fill=(254, 240, 138, 255))
    
    # Callout Box above target point
    # We place it slightly to the left so it doesn't cross the right border
    box_w, box_h = 320, 52
    box_x0 = x_pt - 220
    box_y0 = y_pt - 75
    box_x1 = box_x0 + box_w
    box_y1 = box_y0 + box_h
    
    draw.rectangle([(box_x0, box_y0), (box_x1, box_y1)], fill=(15, 23, 42, 245), outline=(220, 38, 38, 255), width=2)
    # Pointer line from box to target point
    draw.line([(box_x0 + 190, box_y1), (x_pt, y_pt - 14)], fill=(220, 38, 38, 255), width=2)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 13)
        font_sub = ImageFont.truetype("arialbd.ttf", 12)
        font_badge = ImageFont.truetype("arialbd.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        
    draw.text((box_x0 + 10, box_y0 + 7), "PUNTO DE TRABAJO RESUELTO:", fill=(254, 240, 138, 255), font=font_title)
    draw.text((box_x0 + 10, box_y0 + 28), "Pd = 72,71 kW @ 1856 rpm  ->  Perfil SPB-XP", fill=(255, 255, 255, 255), font=font_sub)
    
    # Axis callouts:
    # Bottom callout: Pd = 72.71 kW
    draw.rectangle([(x_pt - 55, 415), (x_pt + 55, 435)], fill=(15, 23, 42, 240), outline=(220, 38, 38, 255), width=1)
    draw.text((x_pt - 48, 418), "Pd = 72,71 kW", fill=(255, 255, 255, 255), font=font_sub)
    
    # Bottom Resolution Banner: full width centered from x=62 to x=730
    draw.rectangle([(62, 452), (730, 484)], fill=(2, 132, 199, 240), outline=(14, 165, 233, 255), width=2)
    draw.text((80, 460), "RESOLUCION: Se adopta Perfil Estrecho de Alta Potencia SKF SPB-XP (Extra Power)", fill=(255, 255, 255, 255), font=font_badge)
    
    annotated = Image.alpha_composite(img, overlay).convert('RGB')
    annotated.save("diagrama2_skf_resuelto.png", quality=95)
    print("diagrama2_skf_resuelto.png calibrated and created successfully!")

if __name__ == '__main__':
    create_annotated_diagram2()
