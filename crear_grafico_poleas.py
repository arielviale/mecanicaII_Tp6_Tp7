import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_pulley_graphic():
    fig, ax = plt.subplots(figsize=(9.2, 3.4), dpi=220)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Coordinate system: Pulleys centers at (20, 15) and (64, 15)
    cx1, cy1, R1 = 20.0, 15.0, 10.0
    cx2, cy2, R2 = 64.0, 15.0, 7.8
    
    # Tangents calculation
    L = cx2 - cx1
    deltaR = R1 - R2
    gamma = np.arcsin(deltaR / L)
    
    # Tangent points
    x1t = cx1 + R1 * np.sin(gamma)
    y1t = cy1 + R1 * np.cos(gamma)
    x2t = cx2 + R2 * np.sin(gamma)
    y2t = cy2 + R2 * np.cos(gamma)
    
    x1b = cx1 - R1 * np.sin(gamma)
    y1b = cy1 - R1 * np.cos(gamma)
    x2b = cx2 - R2 * np.sin(gamma)
    y2b = cy2 - R2 * np.cos(gamma)
    
    # Centerline
    ax.plot([cx1 - R1 - 3, cx2 + R2 + 3], [cy1, cy1], color='#94a3b8', lw=1.0, ls='-.', zorder=1)
    
    # Draw belt
    # Outer strand
    ax.plot([x1t, x2t], [y1t, y2t], color='#d97706', lw=4.5, zorder=2)
    ax.plot([x1t, x2t], [y1t, y2t], color='#fef3c7', lw=1.2, ls='--', zorder=3)
    ax.plot([x1b, x2b], [y1b, y2b], color='#d97706', lw=4.5, zorder=2)
    ax.plot([x1b, x2b], [y1b, y2b], color='#fef3c7', lw=1.2, ls='--', zorder=3)
    
    # Driver Pulley (Motor)
    c_p1 = plt.Circle((cx1, cy1), R1, color='#f0fdf4', ec='#15803d', lw=2.2, zorder=4)
    ax.add_patch(c_p1)
    c_p1_inner = plt.Circle((cx1, cy1), R1*0.82, color='#ffffff', ec='#15803d', ls=':', lw=1.2, zorder=5)
    ax.add_patch(c_p1_inner)
    c_hub1 = plt.Circle((cx1, cy1), 2.2, color='#15803d', zorder=6)
    ax.add_patch(c_hub1)
    
    # Spokes 1
    for angle in [0, 45, 90, 135]:
        rad = np.radians(angle)
        ax.plot([cx1 - R1*0.8*np.cos(rad), cx1 + R1*0.8*np.cos(rad)],
                [cy1 - R1*0.8*np.sin(rad), cy1 + R1*0.8*np.sin(rad)], color='#86efac', lw=1.5, zorder=5)
                
    # Driven Pulley (Pump)
    c_p2 = plt.Circle((cx2, cy2), R2, color='#f0f9ff', ec='#0369a1', lw=2.2, zorder=4)
    ax.add_patch(c_p2)
    c_p2_inner = plt.Circle((cx2, cy2), R2*0.82, color='#ffffff', ec='#0369a1', ls=':', lw=1.2, zorder=5)
    ax.add_patch(c_p2_inner)
    c_hub2 = plt.Circle((cx2, cy2), 1.8, color='#0369a1', zorder=6)
    ax.add_patch(c_hub2)
    
    # Spokes 2
    for angle in [0, 45, 90, 135]:
        rad = np.radians(angle)
        ax.plot([cx2 - R2*0.8*np.cos(rad), cx2 + R2*0.8*np.cos(rad)],
                [cy2 - R2*0.8*np.sin(rad), cy2 + R2*0.8*np.sin(rad)], color='#7dd3fc', lw=1.5, zorder=5)
    
    # Contact arc highlight on driven pulley
    theta = np.linspace(-np.pi/2 + gamma, np.pi/2 - gamma, 60)
    arc_x = cx2 + R2 * np.cos(theta)
    arc_y = cy2 + R2 * np.sin(theta)
    ax.plot(arc_x, arc_y, color='#0284c7', lw=4.5, zorder=7)
    
    # Pulley labels
    ax.text(cx1, cy1 + R1 + 2.8, "POLEA CONDUCTORA (MOTOR)", color='#166534', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(cx1, cy1 - R1 - 2.8, "D = 320 mm  |  1450 rpm", color='#1e293b', fontsize=8.5, fontweight='bold', ha='center')
    
    ax.text(cx2, cy2 + R2 + 2.8, "POLEA CONDUCIDA (BOMBA)", color='#0369a1', fontsize=9.5, fontweight='bold', ha='center')
    ax.text(cx2, cy2 - R2 - 2.8, "d = 250 mm  |  1856 rpm", color='#1e293b', fontsize=8.5, fontweight='bold', ha='center')
    
    # Center distance dimension line
    ax.annotate('', xy=(cx1, 2.2), xytext=(cx2, 2.2),
                arrowprops=dict(arrowstyle='<->', color='#b45309', lw=1.6))
    ax.text((cx1+cx2)/2, 3.2, "Distancia entre Centros Definitiva: CC = 641,4 mm (4 x SKF PHG SPB2180XP)",
            color='#92400e', fontsize=8.5, fontweight='bold', ha='center',
            bbox=dict(boxstyle='square,pad=0.2', facecolor='#fef3c7', edgecolor='#f59e0b', lw=1.0))
            
    # Center badge: Speed and Belts
    ax.text((cx1+cx2)/2, 17.5, "v = 24,30 m/s   |   Arco beta = 174\u00b0 (C3 = 0,99)",
            color='#0369a1', fontsize=9.0, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0f9ff', edgecolor='#0284c7', lw=1.2))
            
    ax.text((cx1+cx2)/2, 12.8, "DOTACION: 4 Correas Estrechas SKF SPB-XP",
            color='#15803d', fontsize=9.0, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.2))
            
    ax.set_xlim(5, 78)
    ax.set_ylim(-0.5, 29)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('transmision_correas_resuelto.png', facecolor='#ffffff', edgecolor='none', dpi=220)
    print("transmision_correas_resuelto.png created successfully on white background!")

if __name__ == '__main__':
    create_pulley_graphic()
