import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_pulley_graphic():
    # Figure dimensions with aspect ratio ~ 2.25
    fig, ax = plt.subplots(figsize=(10.0, 4.6), dpi=220)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    # STRICT EQUAL ASPECT RATIO TO GUARANTEE CIRCLES (NEVER OVALS!)
    ax.set_aspect('equal', adjustable='box')
    
    # Coordinate system:
    # Motor pulley at cx1 = 6.0, Pump pulley at cx2 = 22.0
    # Diameter ratio: 320 mm vs 250 mm -> R1 = 3.20, R2 = 2.50
    cy = 7.0
    cx1, R1 = 6.0, 3.20
    cx2, R2 = 22.0, 2.50
    
    # Tangents calculation
    L = cx2 - cx1  # 16.0
    deltaR = R1 - R2  # 0.70
    gamma = np.arcsin(deltaR / L)
    
    # Tangent points on pulleys
    x1t = cx1 + R1 * np.sin(gamma)
    y1t = cy + R1 * np.cos(gamma)
    x2t = cx2 + R2 * np.sin(gamma)
    y2t = cy + R2 * np.cos(gamma)
    
    x1b = cx1 - R1 * np.sin(gamma)
    y1b = cy - R1 * np.cos(gamma)
    x2b = cx2 - R2 * np.sin(gamma)
    y2b = cy - R2 * np.cos(gamma)
    
    # Centerline
    ax.plot([cx1 - R1 - 1.5, cx2 + R2 + 1.5], [cy, cy], color='#94a3b8', lw=1.0, ls='-.', zorder=1)
    # Vertical centerlines
    ax.plot([cx1, cx1], [cy - R1 - 0.8, cy + R1 + 0.8], color='#cbd5e1', lw=0.8, ls=':', zorder=1)
    ax.plot([cx2, cx2], [cy - R2 - 0.8, cy + R2 + 0.8], color='#cbd5e1', lw=0.8, ls=':', zorder=1)
    
    # Belt strands
    # Top strand
    ax.plot([x1t, x2t], [y1t, y2t], color='#d97706', lw=5.0, zorder=2)
    ax.plot([x1t, x2t], [y1t, y2t], color='#ffffff', lw=1.2, ls='--', zorder=3)
    # Bottom strand
    ax.plot([x1b, x2b], [y1b, y2b], color='#d97706', lw=5.0, zorder=2)
    ax.plot([x1b, x2b], [y1b, y2b], color='#ffffff', lw=1.2, ls='--', zorder=3)
    
    # Belt wrap around pulleys (arcs)
    theta_driver = np.linspace(np.pi/2 + gamma, 3*np.pi/2 - gamma, 60)
    ax.plot(cx1 + R1 * np.cos(theta_driver), cy + R1 * np.sin(theta_driver), color='#d97706', lw=5.0, zorder=2)
    
    theta_driven = np.linspace(-np.pi/2 + gamma, np.pi/2 - gamma, 60)
    ax.plot(cx2 + R2 * np.cos(theta_driven), cy + R2 * np.sin(theta_driven), color='#d97706', lw=5.0, zorder=2)
    
    # Driver Pulley (Motor) - Perfect Circle
    c_p1 = plt.Circle((cx1, cy), R1, color='#f0fdf4', ec='#15803d', lw=2.5, zorder=4)
    ax.add_patch(c_p1)
    c_p1_rim = plt.Circle((cx1, cy), R1*0.82, color='#ffffff', ec='#16a34a', ls='--', lw=1.0, zorder=5)
    ax.add_patch(c_p1_rim)
    c_hub1 = plt.Circle((cx1, cy), 0.9, color='#15803d', zorder=6)
    ax.add_patch(c_hub1)
    
    # Spokes Driver
    for angle in [0, 45, 90, 135]:
        rad = np.radians(angle)
        ax.plot([cx1 - R1*0.78*np.cos(rad), cx1 + R1*0.78*np.cos(rad)],
                [cy - R1*0.78*np.sin(rad), cy + R1*0.78*np.sin(rad)], color='#86efac', lw=1.8, zorder=5)
                
    # Driven Pulley (Pump) - Perfect Circle
    c_p2 = plt.Circle((cx2, cy), R2, color='#f0f9ff', ec='#0369a1', lw=2.5, zorder=4)
    ax.add_patch(c_p2)
    c_p2_rim = plt.Circle((cx2, cy), R2*0.82, color='#ffffff', ec='#0284c7', ls='--', lw=1.0, zorder=5)
    ax.add_patch(c_p2_rim)
    c_hub2 = plt.Circle((cx2, cy), 0.75, color='#0369a1', zorder=6)
    ax.add_patch(c_hub2)
    
    # Spokes Driven
    for angle in [0, 45, 90, 135]:
        rad = np.radians(angle)
        ax.plot([cx2 - R2*0.78*np.cos(rad), cx2 + R2*0.78*np.cos(rad)],
                [cy - R2*0.78*np.sin(rad), cy + R2*0.78*np.sin(rad)], color='#7dd3fc', lw=1.8, zorder=5)
    
    # Contact arc highlight on driven pulley
    ax.plot(cx2 + R2 * np.cos(theta_driven), cy + R2 * np.sin(theta_driven), color='#0284c7', lw=5.5, zorder=7)
    
    # ------------------ TOP LABELS (ABOVE PULLEYS, NO OVERLAP) ------------------
    ax.text(cx1, cy + R1 + 1.2, "POLEA CONDUCTORA (MOTOR)", color='#166534', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(cx1, cy + R1 + 0.4, "D = 320 mm   |   1450 rpm", color='#0f172a', fontsize=9.5, fontweight='bold', ha='center')
    
    ax.text(cx2, cy + R2 + 1.2, "POLEA CONDUCIDA (BOMBA)", color='#0369a1', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(cx2, cy + R2 + 0.4, "d = 250 mm   |   1856 rpm", color='#0f172a', fontsize=9.5, fontweight='bold', ha='center')
    
    # ------------------ CENTER BADGES (BETWEEN STRANDS, SPACED PROPERLY) ------------------
    cx_mid = (cx1 + cx2) / 2.0  # 14.0
    
    ax.text(cx_mid, cy + 0.75, "v = 24,30 m/s   |   Arco \u03b2 = 174\u00b0 (C3 = 0,99)",
            color='#0369a1', fontsize=9.5, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f0f9ff', edgecolor='#0284c7', lw=1.3))
            
    ax.text(cx_mid, cy - 0.75, "DOTACION: 4 Correas SKF PHG SPB2240XP",
            color='#15803d', fontsize=9.5, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.3))
            
    # ------------------ BOTTOM DIMENSION LINE (CC, CLEARLY SEPARATED) ------------------
    y_dim = 1.9
    ax.annotate('', xy=(cx1, y_dim), xytext=(cx2, y_dim),
                arrowprops=dict(arrowstyle='<->', color='#b45309', lw=2.0))
    # Extension lines
    ax.plot([cx1, cx1], [cy - R1 - 0.3, y_dim - 0.4], color='#cbd5e1', lw=1.0, ls=':')
    ax.plot([cx2, cx2], [cy - R2 - 0.3, y_dim - 0.4], color='#cbd5e1', lw=1.0, ls=':')
    
    ax.text(cx_mid, y_dim - 0.85, "Distancia entre Centros Definitiva: CC = 671,4 mm (SKF cuadratica)",
            color='#92400e', fontsize=9.5, fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='square,pad=0.3', facecolor='#fef3c7', edgecolor='#f59e0b', lw=1.2))
            
    # Bounds with generous margins
    ax.set_xlim(1.0, 27.0)
    ax.set_ylim(0.2, 12.5)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('transmision_correas_resuelto.png', facecolor='#ffffff', edgecolor='none', dpi=220)
    print("transmision_correas_resuelto.png created successfully with STRICT ASPECT RATIO and NO OVERLAPS!")

if __name__ == '__main__':
    create_pulley_graphic()
