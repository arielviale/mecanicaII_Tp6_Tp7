import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Ensure graphics exist
import crear_diagrama2_resuelto
import crear_grafico_poleas
import crear_grafico_dcl

crear_diagrama2_resuelto.create_annotated_diagram2()
crear_grafico_poleas.create_pulley_graphic()
crear_grafico_dcl.create_shaft_resolution_graphic()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running header (pages 2 to end)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(1.2 * cm, 28.5 * cm, 19.8 * cm, 28.5 * cm)
            self.drawString(1.2 * cm, 28.7 * cm, "UNIVERSIDAD TECNOLOGICA NACIONAL - FRC | CATEDRA DE MECANICA II")
            self.drawRightString(19.8 * cm, 28.7 * cm, "Entrega Oficial: TP N 6 (Rodamientos) y TP N 7 (Correas)")

        # Running footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(1.2 * cm, 1.3 * cm, 19.8 * cm, 1.3 * cm)

        self.drawString(1.2 * cm, 0.9 * cm, "Autor: Hugo Ariel Martinez - Tecnicatura Universitaria en Mecatronica (UTN-FRC)")
        page_text = f"Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(19.8 * cm, 0.9 * cm, page_text)
        self.restoreState()

def generar_pdf(pdf_path="Entrega_Oficial_TP6_TP7_Hugo_Martinez.pdf"):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=1.2 * cm,
        rightMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()

    # Base typography (Pure ASCII + standard Latin-1 safe characters)
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#0369a1"),
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=3
    )

    formula_style = ParagraphStyle(
        'Formula_Box',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.6,
        leading=9.8,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=4,
        spaceBefore=2,
        spaceAfter=3
    )

    fig_caption_style = ParagraphStyle(
        'FigCaption',
        fontName='Helvetica-Oblique',
        fontSize=7.2,
        leading=9.2,
        alignment=1,
        textColor=colors.HexColor("#475569"),
        spaceBefore=2,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=8.8,
        textColor=colors.HexColor("#ffffff"),
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.2,
        leading=8.8,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=8.8,
        textColor=colors.HexColor("#0369a1"),
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGINA 1: PORTADA, ENUNCIADO TP6 Y GRAFICOS RESUELTOS DE CARGAS
    # =========================================================================
    header_data = [
        [
            Paragraph("<b>UNIVERSIDAD TECNOLOGICA NACIONAL</b><br/>Facultad Regional Cordoba", ParagraphStyle('Utn', fontName='Helvetica-Bold', fontSize=9, leading=11.5, textColor=colors.HexColor("#0f172a"))),
            Paragraph("<b>CATEDRA DE MECANICA II</b><br/>Tecnicatura Universitaria en Mecatronica - Ciclo 2026", ParagraphStyle('Cat', fontName='Helvetica-Bold', fontSize=9, leading=11.5, alignment=2, textColor=colors.HexColor("#0f172a")))
        ]
    ]
    t_header = Table(header_data, colWidths=[9.3 * cm, 9.3 * cm])
    t_header.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 1.2, colors.HexColor("#0284c7")),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))

    story.append(Paragraph("INFORME TECNICO FORMAL DE ENTREGA", title_style))
    story.append(Paragraph("<b>TRABAJO PRACTICO N 6:</b> Rodamientos SKF (Eje Intermediario) &nbsp;|&nbsp; <b>TRABAJO PRACTICO N 7:</b> Correas Trapezoidales SKF (Bomba Centrifuga)", subtitle_style))

    meta_data = [
        [Paragraph("<b>Autor / Estudiante:</b>", body_style), Paragraph("<b>Hugo Ariel Martinez</b> (Tecnicatura Universitaria en Mecatronica)", body_style)],
        [Paragraph("<b>Docente Titular:</b>", body_style), Paragraph("<b>Prof. Ing. Andres Lanfranco</b>", body_style)],
        [Paragraph("<b>Catedra e Institucion:</b>", body_style), Paragraph("Mecanica II - Universidad Tecnologica Nacional (UTN-FRC)", body_style)],
        [Paragraph("<b>Normativa Oficial:</b>", body_style), Paragraph("Normas ISO 281:2007, ISO 76:2006, ISO 4184, DIN 2211, DIN 7753 y Catalogo General SKF", body_style)],
        [Paragraph("<b>Plataforma SCADA:</b>", body_style), Paragraph("https://mecanicaii-tp6-tp7.vercel.app (GitHub: arielviale/mecanicaII_Tp6_Tp7)", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[3.8 * cm, 14.8 * cm])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 1.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.8),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    story.append(Paragraph("PARTE 1: TRABAJO PRACTICO N 6 - DIMENSIONAMIENTO DE RODAMIENTOS SKF", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#0284c7"), spaceAfter=3))

    story.append(Paragraph("<b>1.1 Enunciado y Parametros de Diseno del Eje</b>", h2_style))
    story.append(Paragraph(
        "Se dimensionan los apoyos de un eje intermediario que gira a <b>n = 2400 rpm</b> constante. "
        "Solicitado por una polea en voladizo (extremo izquierdo) y un engranaje recto central. Cotas: "
        "Voladizo a Apoyo 1: <b>L<sub>1</sub> = 100 mm (10 cm)</b> | Apoyo 1 a engranaje: <b>L<sub>2</sub> = 200 mm (20 cm)</b> | "
        "Engranaje a Apoyo 2: <b>L<sub>3</sub> = 250 mm (25 cm)</b> | Vano entre apoyos: <b>L<sub>2</sub> + L<sub>3</sub> = 450 mm (45 cm)</b>. "
        "Diametros de asiento: <b>d<sub>1</sub> = 40 mm</b> (Apoyo 1) y <b>d<sub>2</sub> = 30 mm</b> (Apoyo 2).",
        body_style
    ))

    story.append(Paragraph("<b>1.2 Reacciones en los Apoyos y Cargas Dinamicas Equivalentes P (ISO 281)</b>", h2_style))
    story.append(Paragraph(
        "Al no existir empuje axial (Fa = 0), el factor radial ISO 281 es X = 1, resultando la carga equivalente igual a la resultante radial (P = Fr):",
        body_style
    ))

    calc_p_data = [
        [
            Paragraph("<b>APOYO 1 (d<sub>1</sub> = 40 mm)</b><br/>"
                      "RAy = 390 kgf  |  RAz = 521 kgf<br/>"
                      "Fr<sub>1</sub> = raiz(390<sup>2</sup> + 521<sup>2</sup>) = <b>650,80 kgf</b><br/>"
                      "P<sub>1</sub> = Fr<sub>1</sub> * 0,009807 = <b>6,384 kN</b>", formula_style),
            Paragraph("<b>APOYO 2 (d<sub>2</sub> = 30 mm)</b><br/>"
                      "RBy = 39 kgf  |  RBz = 55 kgf<br/>"
                      "Fr<sub>2</sub> = raiz(39<sup>2</sup> + 55<sup>2</sup>) = <b>67,42 kgf</b><br/>"
                      "P<sub>2</sub> = Fr<sub>2</sub> * 0,009807 = <b>0,661 kN</b>", formula_style)
        ]
    ]
    t_calc_p = Table(calc_p_data, colWidths=[9.3 * cm, 9.3 * cm])
    story.append(t_calc_p)
    story.append(Spacer(1, 4))

    # DOS GRAFICOS DE TP6: Figura 1 (Ensamble CAD) y Figura 2 (DCL Ortogonal con Cargas)
    # Ratios: CAD = 1007/527 = 1.911 (w=8.8 cm, h=4.6 cm) | DCL = 2023/924 = 2.189 (w=8.8 cm, h=4.02 cm)
    p1_img1 = Image("eje_ensamblaje_cad.jpg", width=8.8 * cm, height=4.6 * cm) if os.path.exists("eje_ensamblaje_cad.jpg") else Paragraph("Img 1", body_style)
    p1_img2 = Image("eje_resolucion_cargas.png", width=8.8 * cm, height=4.02 * cm) if os.path.exists("eje_resolucion_cargas.png") else Paragraph("Img 2", body_style)

    cap1 = Paragraph("<i>Figura 1: Ensamble CAD y cotas longitudinales (10-20-25 cm).</i>", fig_caption_style)
    cap2 = Paragraph("<i>Figura 2: Resolucion DCL ortogonal (cargas y reacciones calculadas).</i>", fig_caption_style)

    graphics_tp6_table = Table([
        [p1_img1, p1_img2],
        [cap1, cap2]
    ], colWidths=[9.3 * cm, 9.3 * cm])
    graphics_tp6_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(graphics_tp6_table)

    # =========================================================================
    # PAGINA 2: TABLA SKF TP6, VERIFICACIONES NORMATIVAS Y DICTAMEN
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>1.3 Seleccion en Catalogo General SKF (Tabla 1.1) y Verificacion de Vida Util (ISO 281)</b>", h2_style))
    story.append(Paragraph(
        "Para rodamientos rigidos de una hilera de bolas, el exponente de fatiga es p = 3. Las formulas normativas ISO 281 son:<br/>"
        "<b>L<sub>10</sub> = (C / P)<sup>3</sup></b> [millones de revoluciones] &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>L<sub>10h</sub> = (10<sup>6</sup> / [60 * n]) * L<sub>10</sub> = 6,9444 * L<sub>10</sub></b> [horas de servicio]",
        body_style
    ))

    comp_header = [
        Paragraph("Apoyo", table_header_style),
        Paragraph("Rodamiento", table_header_style),
        Paragraph("d [mm]", table_header_style),
        Paragraph("D [mm]", table_header_style),
        Paragraph("B [mm]", table_header_style),
        Paragraph("C [kN]", table_header_style),
        Paragraph("C<sub>0</sub> [kN]", table_header_style),
        Paragraph("L<sub>10</sub> [10<sup>6</sup> rev]", table_header_style),
        Paragraph("L<sub>10h</sub> [horas]", table_header_style),
        Paragraph("Estado ISO 281", table_header_style),
    ]

    comp_rows = [
        comp_header,
        [Paragraph("1", table_cell_style), Paragraph("61808", table_cell_style), Paragraph("40", table_cell_style), Paragraph("52", table_cell_style), Paragraph("7", table_cell_style), Paragraph("4,49", table_cell_style), Paragraph("3,75", table_cell_style), Paragraph("0,35", table_cell_style), Paragraph("2,4 h", table_cell_style), Paragraph("Rechazado (&lt; 2000 h)", table_cell_style)],
        [Paragraph("1", table_cell_style), Paragraph("61908", table_cell_style), Paragraph("40", table_cell_style), Paragraph("62", table_cell_style), Paragraph("12", table_cell_style), Paragraph("13,8", table_cell_style), Paragraph("10,0", table_cell_style), Paragraph("10,1", table_cell_style), Paragraph("70,1 h", table_cell_style), Paragraph("Rechazado (&lt; 2000 h)", table_cell_style)],
        [Paragraph("1", table_cell_style), Paragraph("* 6208", table_cell_style), Paragraph("40", table_cell_style), Paragraph("80", table_cell_style), Paragraph("18", table_cell_style), Paragraph("32,5", table_cell_style), Paragraph("19,0", table_cell_style), Paragraph("131,9", table_cell_style), Paragraph("916,0 h", table_cell_style), Paragraph("Insuficiente (&lt; 2000 h)", table_cell_style)],
        [Paragraph("<b>1</b>", table_cell_bold), Paragraph("<b>* 6308 (Explorer)</b>", table_cell_bold), Paragraph("<b>40</b>", table_cell_bold), Paragraph("<b>90</b>", table_cell_bold), Paragraph("<b>23</b>", table_cell_bold), Paragraph("<b>42,3</b>", table_cell_bold), Paragraph("<b>24,0</b>", table_cell_bold), Paragraph("<b>290,9</b>", table_cell_bold), Paragraph("<b>2020,1 h</b>", table_cell_bold), Paragraph("<b>ADOPTADO [OK]</b>", table_cell_bold)],
        [Paragraph("2", table_cell_style), Paragraph("61806", table_cell_style), Paragraph("30", table_cell_style), Paragraph("42", table_cell_style), Paragraph("7", table_cell_style), Paragraph("4,49", table_cell_style), Paragraph("2,90", table_cell_style), Paragraph("312,9", table_cell_style), Paragraph("2173,0 h", table_cell_style), Paragraph("Cumple (&gt; 2000 h)", table_cell_style)],
        [Paragraph("<b>2</b>", table_cell_bold), Paragraph("<b>61906 (Clase)</b>", table_cell_bold), Paragraph("<b>30</b>", table_cell_bold), Paragraph("<b>47</b>", table_cell_bold), Paragraph("<b>9</b>", table_cell_bold), Paragraph("<b>7,28</b>", table_cell_bold), Paragraph("<b>4,55</b>", table_cell_bold), Paragraph("<b>1333,5</b>", table_cell_bold), Paragraph("<b>9260,7 h</b>", table_cell_bold), Paragraph("<b>ADOPTADO [OK]</b>", table_cell_bold)],
        [Paragraph("2", table_cell_style), Paragraph("* 6206", table_cell_style), Paragraph("30", table_cell_style), Paragraph("62", table_cell_style), Paragraph("16", table_cell_style), Paragraph("20,3", table_cell_style), Paragraph("11,2", table_cell_style), Paragraph("28914", table_cell_style), Paragraph("200758 h", table_cell_style), Paragraph("Sobredimensionado", table_cell_style)],
    ]

    t_comp = Table(comp_rows, colWidths=[1.1*cm, 2.9*cm, 1.3*cm, 1.3*cm, 1.3*cm, 1.5*cm, 1.5*cm, 2.4*cm, 2.3*cm, 3.0*cm])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor("#e0f2fe")),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor("#dcfce7")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>1.4 Verificaciones Oficiales de Catalogo General SKF (7 Pasos Metodologicos)</b>", h2_style))
    story.append(Paragraph(
        "- <b>Paso 4 (Vida Requerida segun Tabla 9 SKF):</b> Para maquinas de funcionamiento intermitente con servicio continuo requerido (ventiladores/sopladores industriales), la vida minima especificada es L<sub>10h,req</sub> = 2000 horas. El Apoyo 1 entrega 2020,1 h (&gt;= 2000 h [OK]) y el Apoyo 2 entrega 9260,7 h (&gt;= 2000 h [OK]).<br/>"
        "- <b>Paso 5 (Vida Util Modificada SKF Explorer L<sub>10m</sub>):</b> Con factor aSKF para lubricacion grado de viscosidad ISO VG 68 y limpieza industrial (eta_c = 0,6), aSKF = 1,45. La vida real estimada resulta: L<sub>10mh</sub> = aSKF * L<sub>10h</sub> = 1,45 * 2020 h = <b>2929 horas de servicio</b>.<br/>"
        "- <b>Paso 6 (Verificacion de Carga Estatica s<sub>0</sub> - ISO 76, Tabla 11):</b><br/>"
        "&nbsp;&nbsp;Apoyo 1 (6308): s<sub>0</sub> = C<sub>0</sub> / P<sub>0</sub> = 24,0 kN / 6,384 kN = <b>3,76 &gt;= 1,5 (Cumple con amplio margen [OK])</b>.<br/>"
        "&nbsp;&nbsp;Apoyo 2 (61906): s<sub>0</sub> = C<sub>0</sub> / P<sub>0</sub> = 4,55 kN / 0,661 kN = <b>6,88 &gt;= 1,5 (Cumple de forma optima [OK])</b>.<br/>"
        "- <b>Paso 7 (Verificacion de Carga Minima Requerida Frm y Velocidad Limite):</b><br/>"
        "&nbsp;&nbsp;Frm = kr * (v * n / 1000)<sup>0,5</sup> * (dm / 100)<sup>2</sup>: Frm<sub>1</sub> = 0,08 kN &lt;&lt; 6,38 kN [OK]. Frm<sub>2</sub> = 0,02 kN &lt;&lt; 0,66 kN [OK].<br/>"
        "&nbsp;&nbsp;Velocidad limite termica SKF: 6308 permite 9500 rpm (&gt;&gt; 2400 rpm [OK]). 61906 permite 18000 rpm (&gt;&gt; 2400 rpm [OK]).",
        body_style
    ))

    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>Dictamen Tecnico de Seleccion TP 6:</b><br/>"
        "1. <b>Apoyo 1 (d = 40 mm):</b> Se adopta <b>SKF Explorer * 6308</b> (D = 90 mm, B = 23 mm, C = 42,3 kN, C<sub>0</sub> = 24,0 kN). Es el unico de su clase que supera el umbral critico de 2000 horas para soportar las severas cargas combinadas del vano.<br/>"
        "2. <b>Apoyo 2 (d = 30 mm):</b> Se adopta <b>SKF 61906</b> (D = 47 mm, B = 9 mm, C = 7,28 kN, C<sub>0</sub> = 4,55 kN, eleccion oficial de catedra en clases). Otorga L<sub>10h</sub> = 9260,7 h con minimo rozamiento, reduccion del 72% en masa y minimo volumen axial.",
        body_style
    ))

    # =========================================================================
    # PAGINA 3: TP 7 CORREAS - ENUNCIADO, PASO 1, PASO 2 Y AMBOS GRAFICOS RESUELTOS
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("PARTE 2: TRABAJO PRACTICO N 7 - TRANSMISION POR CORREAS TRAPEZOIDALES SKF", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#0284c7"), spaceAfter=3))

    story.append(Paragraph("<b>2.1 Enunciado y Especificaciones Oficiales de la Transmision</b>", h2_style))
    story.append(Paragraph(
        "Se proyecta el accionamiento de una <b>bomba centrifuga</b> accionada por un <b>motor electrico trifasico de induccion</b> bajo las condiciones de servicio indicadas:",
        body_style
    ))

    tp7_specs = [
        [Paragraph("<b>Potencia Nominal del Motor (Pr):</b>", body_style), Paragraph("<b>75 HP (55,93 kW)</b>", body_style)],
        [Paragraph("<b>Velocidad del Motor (n<sub>1</sub>):</b>", body_style), Paragraph("<b>1450 rpm</b> (Eje Conductor)", body_style)],
        [Paragraph("<b>Tipo de Arranque del Motor:</b>", body_style), Paragraph("<b>Arranque Directo</b> (Heavy starts en Tabla 3 SKF)", body_style)],
        [Paragraph("<b>Maquina Conducida:</b>", body_style), Paragraph("<b>Bomba centrifuga</b> - Clase 1 (Light duty)", body_style)],
        [Paragraph("<b>Velocidad de la Bomba (n<sub>2</sub>):</b>", body_style), Paragraph("<b>1856 rpm</b> (Eje Conducido)", body_style)],
        [Paragraph("<b>Regimen Diario:</b>", body_style), Paragraph("<b>20 horas/dia</b> (Columna &gt; 16 h/dia en Tabla 3 SKF)", body_style)],
        [Paragraph("<b>Diametros Primitivos de Poleas:</b>", body_style), Paragraph("Conductora <b>D = 320 mm</b>  |  Conducida <b>d = 250 mm</b>", body_style)],
        [Paragraph("<b>Relacion de Transmision (Ir):</b>", body_style), Paragraph("<b>Ir = 1856 / 1450 = 320 / 250 = 1,28</b> (Multiplicador de velocidad)", body_style)],
        [Paragraph("<b>Distancia entre Centros Preliminar (CCp):</b>", body_style), Paragraph("<b>650 mm</b>", body_style)],
    ]
    t_tp7_specs = Table(tp7_specs, colWidths=[6.5 * cm, 12.1 * cm])
    t_tp7_specs.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_tp7_specs)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>2.2 Resolucion Paso a Paso Oficial SKF (Pasos 1 y 2 con Graficos Resueltos)</b>", h2_style))
    story.append(Paragraph(
        "<b>PASO 1: Factor de Servicio (C<sub>2</sub>) y Potencia de Diseno (Pd):</b><br/>"
        "- Tabla 3 SKF (Pag. 16): Bomba centrifuga (Clase 1) + Arranque directo + &gt; 16 h/dia -&gt; <b>C<sub>2</sub> = 1,30</b>.<br/>"
        "- Potencia motor en kW: Pr = 75 HP * 0,7457 = <b>55,93 kW</b>. Potencia de diseno: <b>Pd = Pr * C<sub>2</sub> = 55,93 kW * 1,30 = 72,71 kW</b>.<br/>"
        "<b>PASO 2: Seleccion del Perfil de Correa (Diagrama 2 y Tabla 5a SKF):</b><br/>"
        "- Ingreso al Diagrama 2 Log-Log con <b>Pd = 72,71 kW</b> y <b>n<sub>2</sub> = 1856 rpm</b>: el punto cae en la zona <b>SPB-XP (Extra Power)</b>.<br/>"
        "- Verificacion diametro minimo: <b>d = 250 mm &gt;= d<sub>min</sub> = 140 mm (Cumple holgadamente [OK])</b>.",
        body_style
    ))

    # AMBOS GRAFICOS DE TP7: Figura 3 (Diagrama 2 Resuelto) y Figura 4 (Transmision Cinematica)
    # Proporciones reales estrictas (sin distorsion ni achatamiento):
    # Diag 2 SKF: 860x535 (ratio 1.607) -> 11.0 cm x 6.84 cm
    # Transmision Poleas: 2200x1011 (ratio 2.176) -> 13.0 cm x 5.97 cm
    if os.path.exists("diagrama2_skf_resuelto.png"):
        img3 = Image("diagrama2_skf_resuelto.png", width=11.2 * cm, height=6.97 * cm)
        img3.hAlign = 'CENTER'
        story.append(img3)
        story.append(Paragraph("<i>Figura 3: Resolucion en Diagrama 2 SKF - Punto exacto de trabajo (Pd = 72,71 kW @ 1856 rpm) en el campo SPB-XP.</i>", fig_caption_style))

    if os.path.exists("transmision_correas_resuelto.png"):
        img4 = Image("transmision_correas_resuelto.png", width=13.0 * cm, height=5.97 * cm)
        img4.hAlign = 'CENTER'
        story.append(img4)
        story.append(Paragraph("<i>Figura 4: Resolucion geometrica y cinematica de la transmision con poleas circulares, CC = 671,4 mm y 4 correas SKF PHG SPB2240XP.</i>", fig_caption_style))

    # =========================================================================
    # PAGINA 4: PASOS 3 A 6 TP7, ESPECIFICACIONES RESUMEN Y FIRMAS
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>2.3 Resolucion Paso a Paso (Pasos 3 a 6, Resumen Comercial y Cierre)</b>", h2_style))
    story.append(Paragraph(
        "<b>PASO 3: Longitud Primitiva Preliminar, Longitud Normalizada y Distancia entre Centros Definitiva (CC):</b><br/>"
        "- Rango admisible para CCp: 0,7 * (D + d) = 399 mm &lt;= <b>650 mm</b> &lt;= 2,0 * (D + d) = 1140 mm (Cumple [OK]).<br/>"
        "- Longitud primitiva preliminar:<br/>"
        "&nbsp;&nbsp;Ld,prelim = 2 * CCp + 1,57 * (D + d) + (D - d)<sup>2</sup> / (4 * CCp) = 2(650) + 1,57(570) + 70<sup>2</sup> / 2600 = <b>2196,8 mm</b>.<br/>"
        "- <b>Seleccion Normalizada Oficial de Catedra (Serie ISO 4184 / Tabla 8 SKF):</b><br/>"
        "&nbsp;&nbsp;Se adopta la longitud normalizada inmediata superior: <b>Ld = 2240 mm -&gt; SKF PHG SPB2240XP</b> (Factor de longitud <b>C<sub>1</sub> = 0,92</b>).<br/>"
        "&nbsp;&nbsp;<i>(Nota de catalogo: SKF comercializa ademas la medida intermedia no preferida Ld = 2180 mm con CC = 641,4 mm; ambas entregan identico factor C1 = 0,92).</i><br/>"
        "- Distancia entre centros definitiva por ecuacion cuadratica exacta SKF con Ld = 2240 mm:<br/>"
        "&nbsp;&nbsp;A = Ld/4 - (pi/8) * (D + d) = 560 - 223,84 = 336,16 mm &nbsp;|&nbsp; B = (D - d)<sup>2</sup> / 8 = 4900 / 8 = 612,5 mm<sup>2</sup><br/>"
        "&nbsp;&nbsp;<b>CC = A + raiz(A<sup>2</sup> - B) = 336,16 + raiz(336,16<sup>2</sup> - 612,5) = 336,16 + 335,25 = 671,4 mm</b>.<br/>"
        "&nbsp;&nbsp;Verificacion de rango: 399 mm &lt;= <b>671,4 mm</b> &lt;= 1140 mm (Cumple holgadamente [OK]).<br/>"
        "&nbsp;&nbsp;Ajuste de recorrido segun Tabla SKF: -19 mm (montaje facil) y +27 mm (compensacion por elongacion).<br/>"
        "<b>PASO 4: Cinematica, Velocidad Tangencial y Factor de Arco (C<sub>3</sub>):</b><br/>"
        "- Velocidad lineal: <b>v = (pi * d * n<sub>2</sub>) / 60 000 = (pi * 250 * 1856) / 60 000 = 24,30 m/s</b> (&lt;= 30 m/s admisible [OK]).<br/>"
        "- Geometria de contacto: (D - d) / CC = (320 - 250) / 671,4 = 0,104 -&gt; De Tabla 7 SKF: <b>beta = 174 grados -&gt; Factor C<sub>3</sub> = 0,99</b>.<br/>"
        "<b>PASO 5: Capacidad y Potencia Admisible por Correa (Padm):</b><br/>"
        "- De la Tabla 9h (Pag. 47) para perfil SPB a 1856 rpm con d = 250 mm:<br/>"
        "&nbsp;&nbsp;Potencia basica nominal interpolada: <b>Pb = 20,89 kW</b>.<br/>"
        "&nbsp;&nbsp;Potencia adicional por relacion de multiplicacion (Ir = 1,28): <b>Delta_Pb = 0,87 kW</b>.<br/>"
        "&nbsp;&nbsp;Potencia basica total por correa: <b>Pb,total = 20,89 + 0,87 = 21,75 kW</b>.<br/>"
        "- Potencia admisible corregida: <b>Padm = Pb,total * C<sub>1</sub> * C<sub>3</sub> = 21,75 kW * 0,92 * 0,99 = 19,81 kW / correa</b>.<br/>"
        "<b>PASO 6: Numero Definitivo de Correas (N):</b><br/>"
        "- Cantidad teorica: <b>N_teor = Pd / Padm = 72,71 kW / 19,81 kW = 3,67 correas</b>.<br/>"
        "- Redondeo al entero superior inmediato: <b>N = 4 correas SKF PHG SPB2240XP</b> (Eleccion Catedra).",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Summary Table TP7
    summary_tp7 = [
        [Paragraph("<b>Componente</b>", table_header_style), Paragraph("<b>Especificacion Tecnica Comercial Definitiva</b>", table_header_style)],
        [Paragraph("Correas Trapezoidales", table_cell_bold), Paragraph("<b>4 Correas Estrechas de Alta Potencia SKF PHG SPB2240XP (Eleccion Catedra)</b>", table_cell_style)],
        [Paragraph("Perfil y Seccion", table_cell_bold), Paragraph("<b>SPB-XP</b> (bo = 16,3 mm | bd = 14,0 mm | h = 13,0 mm)", table_cell_style)],
        [Paragraph("Polea Conductora (Motor)", table_cell_bold), Paragraph("Polea comercial 4 ranuras SPB, diametro primitivo <b>D = 320 mm</b>, eje 1450 rpm", table_cell_style)],
        [Paragraph("Polea Conducida (Bomba)", table_cell_bold), Paragraph("Polea comercial 4 ranuras SPB, diametro primitivo <b>d = 250 mm</b>, eje 1856 rpm", table_cell_style)],
        [Paragraph("Distancia entre Ejes", table_cell_bold), Paragraph("<b>CC = 671,4 mm</b> (carrera de tensado: -19 mm instalacion, +27 mm retensado)", table_cell_style)],
        [Paragraph("Rendimiento Operativo", table_cell_bold), Paragraph("Apto para regimen continuo industrial <b>20 h/dia</b> con arranque directo (Seguridad 109%)", table_cell_style)],
    ]
    t_sum7 = Table(summary_tp7, colWidths=[5.4 * cm, 13.2 * cm])
    t_sum7.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_sum7)
    story.append(Spacer(1, 10))

    # Formal Signature / Approval Box
    sign_data = [
        [
            Paragraph("<b>FIRMA DEL ESTUDIANTE / AUTOR:</b><br/><br/><br/>_____________________________________<br/><b>Hugo Ariel Martinez</b><br/>Tecnicatura Universitaria en Mecatronica - UTN-FRC", ParagraphStyle('Sign1', fontName='Helvetica', fontSize=8, alignment=1)),
            Paragraph("<b>VISADO Y APROBACION DE CATEDRA:</b><br/><br/><br/>_____________________________________<br/><b>Prof. Ing. Andres Lanfranco</b><br/>Titular de Catedra Mecanica II", ParagraphStyle('Sign2', fontName='Helvetica', fontSize=8, alignment=1))
        ]
    ]
    t_sign = Table(sign_data, colWidths=[9.3 * cm, 9.3 * cm])
    t_sign.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF SUCCESSFULLY GENERATED AT: {pdf_path}")

if __name__ == '__main__':
    generar_pdf()
