import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(2 * cm, 28.5 * cm, "UNIVERSIDAD TECNOLÓGICA NACIONAL — FRC | MECÁNICA II")
            self.drawRightString(19 * cm, 28.5 * cm, "Entrega Oficial: TP N° 6 (Rodamientos) & TP N° 7 (Correas)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(2 * cm, 28.3 * cm, 19 * cm, 28.3 * cm)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(2 * cm, 1.6 * cm, 19 * cm, 1.6 * cm)

        self.drawString(2 * cm, 1.2 * cm, "Autor: Hugo Ariel Martinez — Ingeniería Mecatrónica (Plan 2026)")
        self.drawRightString(19 * cm, 1.2 * cm, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

def generar_pdf():
    pdf_path = "Entrega_Oficial_TP6_TP7_Hugo_Martinez.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    formula_style = ParagraphStyle(
        'Formula_Box',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#ffffff"),
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0369a1"),
        alignment=1
    )

    story = []

    # ==================== PORTADA / ENCABEZADO FORMAL ====================
    # Academic Header Table
    header_data = [
        [
            Paragraph("<b>UNIVERSIDAD TECNOLÓGICA NACIONAL</b><br/>Facultad Regional Córdoba", ParagraphStyle('Utn', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor("#0f172a"))),
            Paragraph("<b>CÁTEDRA DE MECÁNICA II</b><br/>Ingeniería Mecatrónica — Ciclo 2026", ParagraphStyle('Cat', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=2, textColor=colors.HexColor("#0f172a")))
        ]
    ]
    t_header = Table(header_data, colWidths=[8.5 * cm, 8.5 * cm])
    t_header.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 1.5, colors.HexColor("#0284c7")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 15))

    # Title Box
    story.append(Paragraph("INFORME TÉCNICO FORMAL DE ENTREGA", title_style))
    story.append(Paragraph("<b>TRABAJO PRÁCTICO N° 6:</b> Rodamientos SKF (Eje Intermediario de Ventilación)<br/><b>TRABAJO PRÁCTICO N° 7:</b> Transmisión por Correas Trapezoidales SKF (Bomba Centrífuga)", subtitle_style))

    # Metadata Box
    meta_data = [
        [Paragraph("<b>Autor / Estudiante:</b>", body_style), Paragraph("<b>Hugo Ariel Martinez</b> (Ingeniería Mecatrónica)", body_style)],
        [Paragraph("<b>Docente a Cargo:</b>", body_style), Paragraph("<b>Prof. Ing. Andrés Lanfranco</b>", body_style)],
        [Paragraph("<b>Asignatura:</b>", body_style), Paragraph("Mecánica II — Universidad Tecnológica Nacional (UTN-FRC)", body_style)],
        [Paragraph("<b>Normativa Aplicada:</b>", body_style), Paragraph("Norma ISO 281:2007, ISO 76:2006, ISO 4184, DIN 2211, DIN 7753 y Catálogo General SKF", body_style)],
        [Paragraph("<b>Repositorio Oficial:</b>", body_style), Paragraph("https://github.com/arielviale/mecanicaII_Tp6_Tp7 (Deploy: mecanicaii-tp6-tp7.vercel.app)", body_style)],
        [Paragraph("<b>Fecha de Emisión:</b>", body_style), Paragraph("Noviembre 2026", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[4.2 * cm, 12.8 * cm])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 15))

    # ==================== PARTE 1: TP 6 RODAMIENTOS ====================
    story.append(Paragraph("PARTE 1: TRABAJO PRÁCTICO N° 6 — DIMENSIONAMIENTO DE RODAMIENTOS SKF", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=10))

    story.append(Paragraph("<b>1.1 Enunciado y Datos de Partida Oficiales</b>", h2_style))
    story.append(Paragraph(
        "Se proyecta un eje intermediario de transmisión cilíndrico accionado por una polea en su extremo izquierdo y que comanda un engranaje cilíndrico recto central. "
        "El eje gira a una velocidad angular constante de <b>n = 2400 rpm</b>. "
        "Las dimensiones geométricas axiales normalizadas son:",
        body_style
    ))
    story.append(Paragraph("• Voladizo de la polea al Apoyo 1 (Rodamiento A): <b>L₁ = 100 mm (10 cm)</b><br/>"
                           "• Distancia entre Apoyo 1 y engranaje central: <b>L₂ = 200 mm (20 cm)</b><br/>"
                           "• Distancia entre engranaje y Apoyo 2 (Rodamiento B): <b>L₃ = 250 mm (25 cm)</b><br/>"
                           "• Vano total entre apoyos: <b>L₂ + L₃ = 450 mm (45 cm)</b><br/>"
                           "• Asientos de rodamientos normalizados: <b>d₁ = 40 mm</b> (Apoyo 1) y <b>d₂ = 30 mm</b> (Apoyo 2)", body_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Reacciones ortogonales en los apoyos obtenidas del DCL de la cátedra:</b>", body_style))
    story.append(Paragraph("• <b>Plano vertical x-y:</b> RAy = 390 kgf &nbsp;|&nbsp; RBy = 39 kgf<br/>"
                           "• <b>Plano horizontal x-z:</b> RAz = 521 kgf &nbsp;|&nbsp; RBz = 55 kgf", formula_style))

    # Image of shaft if available
    if os.path.exists("eje_ensamblaje_cad.jpg"):
        story.append(Spacer(1, 4))
        img = Image("eje_ensamblaje_cad.jpg", width=14.5 * cm, height=4.2 * cm)
        story.append(img)
        story.append(Paragraph("<i>Figura 1: Esquema de ensamble CAD del árbol con cotas oficiales y ubicación de componentes.</i>", ParagraphStyle('Fig', fontName='Helvetica-Oblique', fontSize=8, alignment=1, textColor=colors.HexColor("#64748b"))))
        story.append(Spacer(1, 8))

    story.append(Paragraph("<b>1.2 Fuerza Radial Resultante (Fr) y Carga Dinámica Equivalente (P) — Norma ISO 281</b>", h2_style))
    story.append(Paragraph(
        "Dado que el engranaje recto y la polea no generan empuje axial (Fa = 0), el factor radial de la norma ISO 281 es X = 1 y el factor axial Y = 0. "
        "Por ende, la carga dinámica equivalente P coincide exactamente con la fuerza radial resultante Fr:",
        body_style
    ))

    calc_p_data = [
        [
            Paragraph("<b>APOYO 1 (d₁ = 40 mm)</b><br/>"
                      "Fr₁ = √(RAy² + RAz²) = √(390² + 521²) = <b>650,80 kgf</b><br/>"
                      "P₁ = Fr₁ × 0,00980665 kN/kgf = <b>6,384 kN</b>", formula_style),
            Paragraph("<b>APOYO 2 (d₂ = 30 mm)</b><br/>"
                      "Fr₂ = √(RBy² + RBz²) = √(39² + 55²) = <b>67,42 kgf</b><br/>"
                      "P₂ = Fr₂ × 0,00980665 kN/kgf = <b>0,661 kN</b>", formula_style)
        ]
    ]
    t_calc_p = Table(calc_p_data, colWidths=[8.5 * cm, 8.5 * cm])
    story.append(t_calc_p)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1.3 Selección en Catálogo SKF (Tabla 1.1) y Verificación de Vida Útil</b>", h2_style))
    story.append(Paragraph(
        "Para rodamientos rígidos de bolas, el exponente de duración es p = 3. Las ecuaciones de vida nominal básica según ISO 281 son:",
        body_style
    ))
    story.append(Paragraph("L₁₀ = (C / P)³ &nbsp;[millones de revoluciones] &nbsp;&nbsp;|&nbsp;&nbsp; L₁₀h = (10⁶ / [60 · n]) · L₁₀ = 6,9444 · L₁₀ &nbsp;[horas]", formula_style))

    # Table of comparison
    comp_header = [
        Paragraph("Apoyo", table_header_style),
        Paragraph("Rodamiento", table_header_style),
        Paragraph("d [mm]", table_header_style),
        Paragraph("D [mm]", table_header_style),
        Paragraph("B [mm]", table_header_style),
        Paragraph("C [kN]", table_header_style),
        Paragraph("C₀ [kN]", table_header_style),
        Paragraph("L₁₀ [10⁶ rev]", table_header_style),
        Paragraph("L₁₀h [h]", table_header_style),
        Paragraph("Estado ISO", table_header_style),
    ]

    comp_rows = [
        comp_header,
        [Paragraph("1", table_cell_style), Paragraph("61808", table_cell_style), Paragraph("40", table_cell_style), Paragraph("52", table_cell_style), Paragraph("7", table_cell_style), Paragraph("4,49", table_cell_style), Paragraph("3,75", table_cell_style), Paragraph("0,35", table_cell_style), Paragraph("2,4 h", table_cell_style), Paragraph("Rechazado", table_cell_style)],
        [Paragraph("1", table_cell_style), Paragraph("61908", table_cell_style), Paragraph("40", table_cell_style), Paragraph("62", table_cell_style), Paragraph("12", table_cell_style), Paragraph("13,8", table_cell_style), Paragraph("10,0", table_cell_style), Paragraph("10,1", table_cell_style), Paragraph("70,1 h", table_cell_style), Paragraph("Rechazado", table_cell_style)],
        [Paragraph("1", table_cell_style), Paragraph("* 6208", table_cell_style), Paragraph("40", table_cell_style), Paragraph("80", table_cell_style), Paragraph("18", table_cell_style), Paragraph("32,5", table_cell_style), Paragraph("19,0", table_cell_style), Paragraph("131,9", table_cell_style), Paragraph("916 h", table_cell_style), Paragraph("Insuficiente", table_cell_style)],
        [Paragraph("<b>1</b>", table_cell_bold), Paragraph("<b>* 6308</b>", table_cell_bold), Paragraph("<b>40</b>", table_cell_bold), Paragraph("<b>90</b>", table_cell_bold), Paragraph("<b>23</b>", table_cell_bold), Paragraph("<b>42,3</b>", table_cell_bold), Paragraph("<b>24,0</b>", table_cell_bold), Paragraph("<b>290,9</b>", table_cell_bold), Paragraph("<b>2020 h</b>", table_cell_bold), Paragraph("<b>ADOPTADO ✓</b>", table_cell_bold)],
        [Paragraph("2", table_cell_style), Paragraph("61806", table_cell_style), Paragraph("30", table_cell_style), Paragraph("42", table_cell_style), Paragraph("7", table_cell_style), Paragraph("4,49", table_cell_style), Paragraph("2,90", table_cell_style), Paragraph("312,9", table_cell_style), Paragraph("2173 h", table_cell_style), Paragraph("Cumple", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_bold), Paragraph("<b>61906 (Clase)</b>", table_cell_bold), Paragraph("<b>30</b>", table_cell_bold), Paragraph("<b>47</b>", table_cell_bold), Paragraph("<b>9</b>", table_cell_bold), Paragraph("<b>7,28</b>", table_cell_bold), Paragraph("<b>4,55</b>", table_cell_bold), Paragraph("<b>1333,5</b>", table_cell_bold), Paragraph("<b>9261 h</b>", table_cell_bold), Paragraph("<b>ADOPTADO ✓</b>", table_cell_bold)],
        [Paragraph("2", table_cell_style), Paragraph("* 6206", table_cell_style), Paragraph("30", table_cell_style), Paragraph("62", table_cell_style), Paragraph("16", table_cell_style), Paragraph("20,3", table_cell_style), Paragraph("11,2", table_cell_style), Paragraph("28914", table_cell_style), Paragraph("200758 h", table_cell_style), Paragraph("Sobredim.", table_cell_style)],
    ]

    t_comp = Table(comp_rows, colWidths=[1.2*cm, 2.5*cm, 1.4*cm, 1.4*cm, 1.4*cm, 1.6*cm, 1.6*cm, 2.2*cm, 2.0*cm, 2.0*cm])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor("#e0f2fe")),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor("#dcfce7")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Conclusión de Selección para TP 6:</b><br/>"
        "• <b>Apoyo 1 (d = 40 mm):</b> Se selecciona el rodamiento rígido de bolas <b>SKF Explorer * 6308</b> (D = 90 mm, B = 23 mm, C = 42,3 kN). Garantiza L₁₀h = 2020 h (&ge; 2000 h requeridas). Factor de seguridad estática s₀ = C₀ / P = 24,0 / 6,384 = <b>3,76 &ge; 1,5</b>.<br/>"
        "• <b>Apoyo 2 (d = 30 mm):</b> Se selecciona el rodamiento <b>SKF 61906</b> elegido en clase (D = 47 mm, B = 9 mm, C = 7,28 kN). Ofrece una vida útil L₁₀h = 9260,7 h y un elevadísimo factor de seguridad estática s₀ = 4,55 / 0,661 = <b>6,88</b>, siendo óptimo para minimizar peso y rozamiento.",
        body_style
    ))

    # ==================== PARTE 2: TP 7 CORREAS ====================
    story.append(PageBreak())
    story.append(Paragraph("PARTE 2: TRABAJO PRÁCTICO N° 7 — TRANSMISIÓN POR CORREAS TRAPEZOIDALES SKF", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0284c7"), spaceAfter=10))

    story.append(Paragraph("<b>2.1 Enunciado y Datos de Funcionamiento Oficiales</b>", h2_style))
    story.append(Paragraph(
        "Se diseña la transmisión por correas trapezoidales para accionar una <b>bomba centrífuga</b> a partir de un <b>motor eléctrico trifásico de inducción</b> con las siguientes especificaciones:",
        body_style
    ))

    tp7_specs = [
        [Paragraph("<b>Potencia Nominal del Motor (Pr):</b>", body_style), Paragraph("<b>75 HP (55,93 kW)</b>", body_style)],
        [Paragraph("<b>Velocidad del Motor (n₁):</b>", body_style), Paragraph("<b>1450 rpm</b> (Eje Conductor)", body_style)],
        [Paragraph("<b>Tipo de Arranque del Motor:</b>", body_style), Paragraph("<b>Arranque Directo</b> (Heavy starts en Tabla 3 SKF)", body_style)],
        [Paragraph("<b>Máquina Conducida:</b>", body_style), Paragraph("<b>Bomba centrífuga</b> — Clase 1 (Light duty)", body_style)],
        [Paragraph("<b>Velocidad de la Bomba (n₂):</b>", body_style), Paragraph("<b>1856 rpm</b> (Eje Conducido)", body_style)],
        [Paragraph("<b>Régimen de Operación Diario:</b>", body_style), Paragraph("<b>20 horas al día</b> (Columna > 16 h/día en Tabla 3 SKF)", body_style)],
        [Paragraph("<b>Diámetros Primitivos de Poleas:</b>", body_style), Paragraph("Conductora <b>D = 320 mm</b> &nbsp;|&nbsp; Conducida <b>d = 250 mm</b>", body_style)],
        [Paragraph("<b>Relación de Transmisión (Ir):</b>", body_style), Paragraph("<b>Ir = 1856 / 1450 = 320 / 250 = 1,28</b> (Multiplicador de velocidad)", body_style)],
        [Paragraph("<b>Distancia entre Centros Preliminar (CCp):</b>", body_style), Paragraph("<b>650 mm</b>", body_style)],
    ]
    t_tp7_specs = Table(tp7_specs, colWidths=[6.5 * cm, 10.5 * cm])
    t_tp7_specs.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_tp7_specs)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>2.2 Secuencia Oficial de Cálculo SKF (6 Pasos Normativos)</b>", h2_style))

    story.append(Paragraph(
        "<b>PASO 1: Factor de Servicio (C₂) y Potencia de Diseño (Pd)</b><br/>"
        "• Tabla 3 SKF (Pág. 16): Bomba centrífuga (Clase 1) + Arranque directo (Heavy starts) + Servicio continuo (> 16 h/día) &rarr; <b>C₂ = 1,30</b>.<br/>"
        "• Potencia motor métrica: Pr = 75 HP × 0,7457 = <b>55,93 kW</b>.<br/>"
        "• Potencia de diseño: <b>Pd = Pr × C₂ = 55,93 kW × 1,30 = 72,71 kW</b>.",
        body_style
    ))

    story.append(Paragraph(
        "<b>PASO 2: Selección del Perfil de Correa (Diagrama 2 y Tabla 5a SKF)</b><br/>"
        "• Ingreso al Diagrama 2 Log-Log con <b>Pd = 72,71 kW</b> y <b>n₂ = 1856 rpm</b> (polea más rápida): el punto cae plenamente en el campo <b>SPB-XP (Extra Power)</b>.<br/>"
        "• Geometría SPB: Ancho superior bo = 16,3 mm, altura h = 13 mm. Diámetro mínimo recomendado dmín = 140 mm.<br/>"
        "• Verificación de diámetro mínimo: <b>d = 250 mm &ge; 140 mm (Cumple holgadamente ✓)</b>.",
        body_style
    ))

    # Diagram 2 image if available
    if os.path.exists("diagrama2_skf.png"):
        story.append(Spacer(1, 3))
        img_diag = Image("diagrama2_skf.png", width=12.0 * cm, height=4.8 * cm)
        story.append(img_diag)
        story.append(Paragraph("<i>Figura 2: Diagrama 2 SKF — Selección del perfil de correas trapezoidales (Wedge Belts).</i>", ParagraphStyle('Fig2', fontName='Helvetica-Oblique', fontSize=8, alignment=1, textColor=colors.HexColor("#64748b"))))
        story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>PASO 3: Longitud Primitiva Preliminar, Longitud Normalizada y Distancia entre Centros Definitiva (CC)</b><br/>"
        "• Rango admisible para CCp: 0,7·(D+d) = 399 mm &le; <b>650 mm</b> &le; 2,0·(D+d) = 1140 mm (Cumple ✓).<br/>"
        "• Longitud primitiva preliminar:<br/>"
        "&nbsp;&nbsp;Ld,prelim = 2·CCp + 1,57·(D + d) + (D - d)² / (4·CCp) = 2(650) + 1,57(570) + 70² / 2600 = <b>2196,8 mm</b>.<br/>"
        "• Selección en Catálogo Comercial SKF (Tabla 8): Longitud normalizada <b>Ld = 2180 mm &rarr; SKF PHG SPB2180XP</b> (Factor <b>C₁ = 0,92</b>).<br/>"
        "• Distancia entre centros definitiva resolviendo la ecuación cuadrática exacta de SKF:<br/>"
        "&nbsp;&nbsp;A = Ld/4 - (π/8)·(D+d) = 545 - 223,84 = 321,16 mm &nbsp;|&nbsp; B = (D-d)² / 8 = 4900 / 8 = 612,5 mm²<br/>"
        "&nbsp;&nbsp;<b>CC = A + √(A² - B) = 321,16 + √(321,16² - 612,5) = 321,16 + 320,21 = 641,4 mm</b>.",
        body_style
    ))

    story.append(Paragraph(
        "<b>PASO 4: Cinemática, Velocidad Tangencial y Factor de Arco (C₃)</b><br/>"
        "• Velocidad lineal: v = (π · d · n₂) / 60 000 = (π · 250 · 1856) / 60 000 = <b>24,30 m/s</b> (&le; 30 m/s admisible ✓).<br/>"
        "• Relación geométrica: (D - d) / CC = (320 - 250) / 641,4 = 0,109 &rarr; De Tabla 7 SKF: <b>β = 174° &rarr; Factor C₃ = 0,99</b>.",
        body_style
    ))

    story.append(Paragraph(
        "<b>PASO 5: Capacidad y Potencia Admisible por Correa (Padm)</b><br/>"
        "• De la Tabla 9h (pág. 47) para perfil SPB a 1856 rpm:<br/>"
        "&nbsp;&nbsp;Potencia básica nominal interpolada: <b>Pb = 20,89 kW</b>.<br/>"
        "&nbsp;&nbsp;Potencia adicional por relación de multiplicación (Ir = 1,28): <b>ΔPb = 0,87 kW</b>.<br/>"
        "&nbsp;&nbsp;Potencia básica total por correa: <b>Pb,total = 20,89 + 0,87 = 21,75 kW</b>.<br/>"
        "• Potencia admisible corregida: <b>Padm = Pb,total × C₁ × C₃ = 21,75 kW × 0,92 × 0,99 = 19,81 kW / correa</b>.",
        body_style
    ))

    story.append(Paragraph(
        "<b>PASO 6: Número Definitivo de Correas (N)</b><br/>"
        "• Cantidad teórica: <b>N_teor = Pd / Padm = 72,71 kW / 19,81 kW = 3,67 correas</b>.<br/>"
        "• Redondeo al entero superior inmediato: <b>N = 4 correas SKF PHG SPB2180XP</b>.",
        body_style
    ))

    # Summary Table TP7
    story.append(Spacer(1, 6))
    summary_tp7 = [
        [Paragraph("<b>Componente</b>", table_header_style), Paragraph("<b>Especificación Técnica Comercial Definitiva</b>", table_header_style)],
        [Paragraph("Correas Trapezoidales", table_cell_bold), Paragraph("<b>4 Correas Estrechas de Alta Potencia SKF PHG SPB2180XP</b>", table_cell_style)],
        [Paragraph("Perfil de Correa", table_cell_bold), Paragraph("<b>SPB-XP</b> (bo = 16,3 mm | bd = 14,0 mm | h = 13,0 mm)", table_cell_style)],
        [Paragraph("Polea Conductora (Motor)", table_cell_bold), Paragraph("Polea de 4 ranuras SPB, diámetro primitivo <b>D = 320 mm</b>, eje 1450 rpm", table_cell_style)],
        [Paragraph("Polea Conducida (Bomba)", table_cell_bold), Paragraph("Polea de 4 ranuras SPB, diámetro primitivo <b>d = 250 mm</b>, eje 1856 rpm", table_cell_style)],
        [Paragraph("Distancia entre Ejes", table_cell_bold), Paragraph("<b>CC = 641,4 mm</b> (ajuste de tensado: -19 mm montaje, +27 mm tensado)", table_cell_style)],
        [Paragraph("Vida Útil Estimada", table_cell_bold), Paragraph("Apta para servicio continuo industrial <b>20 h/día</b> con arranque directo", table_cell_style)],
    ]
    t_sum7 = Table(summary_tp7, colWidths=[5.5 * cm, 11.5 * cm])
    t_sum7.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_sum7)

    # Formal Signature / Approval Box
    story.append(Spacer(1, 16))
    sign_data = [
        [
            Paragraph("<b>FIRMA DEL ESTUDIANTE:</b><br/><br/><br/>_____________________________________<br/><b>Hugo Ariel Martinez</b><br/>Ingeniería Mecatrónica — UTN-FRC", ParagraphStyle('Sign1', fontName='Helvetica', fontSize=8.5, alignment=1)),
            Paragraph("<b>VISADO DE CÁTEDRA:</b><br/><br/><br/>_____________________________________<br/><b>Prof. Ing. Andrés Lanfranco</b><br/>Titular de Cátedra Mecánica II", ParagraphStyle('Sign2', fontName='Helvetica', fontSize=8.5, alignment=1))
        ]
    ]
    t_sign = Table(sign_data, colWidths=[8.5 * cm, 8.5 * cm])
    t_sign.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF SUCCESSFULLY GENERATED AT: {pdf_path}")

if __name__ == '__main__':
    generar_pdf()
