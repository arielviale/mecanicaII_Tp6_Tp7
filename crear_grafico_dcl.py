import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_shaft_resolution_graphic():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.2, 4.2), dpi=220)
    fig.patch.set_facecolor('#ffffff')
    
    # ------------------ TOP: PLANO VERTICAL X-Y ------------------
    ax1.set_facecolor('#f8fafc')
    ax1.set_title("PLANO VERTICAL x-y  (Flexion vertical y equilibrio de momentos)", color='#0369a1', fontsize=9, fontweight='bold', loc='left', pad=4)
    
    # Beam
    beam1 = patches.Rectangle((10, 18), 70, 3, facecolor='#e2e8f0', edgecolor='#0284c7', lw=1.5)
    ax1.add_patch(beam1)
    
    # Loads and reactions
    # Ftp = 227 kgf down at x=10
    ax1.annotate('', xy=(10, 21), xytext=(10, 31), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2))
    ax1.text(10, 33, "Ftp = 227 kgf", color='#b91c1c', fontsize=8, fontweight='bold', ha='center')
    
    # RAy = 390 kgf up at x=23
    ax1.annotate('', xy=(23, 18), xytext=(23, 7), arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.2))
    ax1.text(23, 3, "RAy = 390 kgf", color='#15803d', fontsize=8, fontweight='bold', ha='center')
    
    # Fte = 202 kgf down at x=49
    ax1.annotate('', xy=(49, 21), xytext=(49, 31), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2))
    ax1.text(49, 33, "Fte = 202 kgf", color='#b91c1c', fontsize=8, fontweight='bold', ha='center')
    
    # RBy = 39 kgf up at x=80
    ax1.annotate('', xy=(80, 18), xytext=(80, 7), arrowprops=dict(arrowstyle='->', color='#0284c7', lw=2.2))
    ax1.text(80, 3, "RBy = 39 kgf", color='#0369a1', fontsize=8, fontweight='bold', ha='center')
    
    # Cotas
    ax1.annotate('', xy=(10, 14), xytext=(23, 14), arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1))
    ax1.text(16.5, 14.8, "10 cm", color='#475569', fontsize=7.5, fontweight='bold', ha='center')
    
    ax1.annotate('', xy=(23, 14), xytext=(49, 14), arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1))
    ax1.text(36, 14.8, "20 cm", color='#475569', fontsize=7.5, fontweight='bold', ha='center')
    
    ax1.annotate('', xy=(49, 14), xytext=(80, 14), arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1))
    ax1.text(64.5, 14.8, "25 cm", color='#475569', fontsize=7.5, fontweight='bold', ha='center')
    
    ax1.set_xlim(2, 88)
    ax1.set_ylim(-1, 38)
    ax1.axis('off')
    
    # ------------------ BOTTOM: PLANO HORIZONTAL X-Z ------------------
    ax2.set_facecolor('#f8fafc')
    ax2.set_title("PLANO HORIZONTAL x-z  (Flexion horizontal y equilibrio de momentos)", color='#7c3aed', fontsize=9, fontweight='bold', loc='left', pad=4)
    
    # Beam
    beam2 = patches.Rectangle((10, 18), 70, 3, facecolor='#e2e8f0', edgecolor='#7c3aed', lw=1.5)
    ax2.add_patch(beam2)
    
    # Frp = 393 kgf up at x=10
    ax2.annotate('', xy=(10, 18), xytext=(10, 8), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2))
    ax2.text(10, 4, "Frp = 393 kgf", color='#b91c1c', fontsize=8, fontweight='bold', ha='center')
    
    # RAz = 521 kgf down at x=23
    ax2.annotate('', xy=(23, 21), xytext=(23, 31), arrowprops=dict(arrowstyle='->', color='#15803d', lw=2.2))
    ax2.text(23, 33, "RAz = 521 kgf", color='#15803d', fontsize=8, fontweight='bold', ha='center')
    
    # Fre = 73 kgf down at x=49
    ax2.annotate('', xy=(49, 21), xytext=(49, 31), arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2.2))
    ax2.text(49, 33, "Fre = 73 kgf", color='#b91c1c', fontsize=8, fontweight='bold', ha='center')
    
    # RBz = 55 kgf up at x=80
    ax2.annotate('', xy=(80, 18), xytext=(80, 8), arrowprops=dict(arrowstyle='->', color='#7c3aed', lw=2.2))
    ax2.text(80, 4, "RBz = 55 kgf", color='#6d28d9', fontsize=8, fontweight='bold', ha='center')
    
    # Cotas
    ax2.annotate('', xy=(10, 14), xytext=(23, 14), arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1))
    ax2.text(16.5, 14.8, "10 cm", color='#475569', fontsize=7.5, fontweight='bold', ha='center')
    
    ax2.annotate('', xy=(23, 14), xytext=(49, 14), arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1))
    ax2.text(36, 14.8, "20 cm", color='#475569', fontsize=7.5, fontweight='bold', ha='center')
    
    ax2.annotate('', xy=(49, 14), xytext=(80, 14), arrowprops=dict(arrowstyle='<->', color='#64748b', lw=1))
    ax2.text(64.5, 14.8, "25 cm", color='#475569', fontsize=7.5, fontweight='bold', ha='center')
    
    ax2.set_xlim(2, 88)
    ax2.set_ylim(-1, 38)
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig('eje_resolucion_cargas.png', facecolor='#ffffff', edgecolor='none', dpi=220)
    print("eje_resolucion_cargas.png created successfully on white background!")

if __name__ == '__main__':
    create_shaft_resolution_graphic()
