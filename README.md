# Mecánica II — Plataforma SCADA Industrial y Motor de Cálculo SKF
### Entrega de Trabajos Prácticos N° 6 (Rodamientos) y N° 7 (Correas Trapezoidales)

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployed-black?style=for-the-badge&logo=vercel)](https://mecanicaii-tp6-tp7.vercel.app/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/es/docs/Web/HTML)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite3](https://img.shields.io/badge/SQLite3-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Python 3.10+](https://img.shields.io/badge/Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ISO 281 & 76](https://img.shields.io/badge/Norma-ISO_281_%2F_ISO_76-10b981?style=for-the-badge)](https://www.iso.org/)

---

## 🏛️ Datos Académicos y Autoría
* **Institución:** Universidad Tecnológica Nacional — Facultad Regional Córdoba (UTN-FRC)
* **Carrera:** Ingeniería Mecatrónica (Plan 2026)
* **Cátedra:** Mecánica II
* **Profesor a cargo:** Ing. Andrés Lanfranco
* **Autor / Estudiante:** **Hugo Ariel Martinez**
* **Fecha de Entrega:** Octubre / Noviembre 2026
* **Tema Central:** Dimensionamiento, Simulación Paramétrica, Modelado CAD Fotorrealista y Verificación de Vida Útil de Transmisiones Mecánicas bajo Normativa Oficial SKF (ISO 281 e ISO 76).

---

## 🌐 Enlaces Oficiales de Entrega
* 🚀 **Plataforma Web SCADA en Vivo:** [**https://mecanicaii-tp6-tp7.vercel.app/**](https://mecanicaii-tp6-tp7.vercel.app/)
* 📦 **Repositorio Oficial en GitHub:** [**https://github.com/arielviale/mecanicaII_Tp6_Tp7**](https://github.com/arielviale/mecanicaII_Tp6_Tp7)

---

## 📖 Descripción General del Proyecto

Este proyecto constituye la entrega formal, interactiva y computacional de los **Trabajos Prácticos N° 6 y N° 7** de la cátedra **Mecánica II**. Trasciende el formato de cálculo estático tradicional mediante una **plataforma interactiva tipo SCADA industrial** desarrollada en arquitectura web moderna, respaldada por una **base de datos relacional SQLite (`skf_catalog.db`)** y un motor matemático en Python.

La aplicación permite tanto la **verificación instantánea de los enunciados oficiales** como la **resolución de cualquier variante paramétrica**, recalculando cinemática, esfuerzos vectoriales, selección de componentes y vida útil en tiempo real con sinópticos vectoriales animados en SVG y renderizado isométrico 3D.

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │                    INTERFAZ SCADA WEB (index.html)                     │
   │  - Multi-Vista de Eje: Ensamblaje CAD, Isométrico 3D, DCL Ortogonal    │
   │  - Plano de Corte Normalizado SKF 1.1 con Giro de Bolas a 2400 rpm     │
   │  - Descomposición Vectorial de Cargas Radiales (Ry, Rz, Fr, theta)     │
   │  - Transmisión por Poleas Animada con Escalado Dinámico Tangencial     │
   │  - Diagrama 2 SKF Log-Log Interactivo con Cursor de Potencia           │
   │  - Guía Paso a Paso Interactiva (7 Pasos) y Memoria Técnica Imprimible │
   │  - Explorador Relacional de Base de Datos SQLite (52 Rodamientos)      │
   └──────────▲──────────────────────────────────▲──────────────────────────┘
              │                                  │
   ┌──────────┴──────────────┐        ┌──────────┴──────────┐
   │ BASE DE DATOS SQLITE    │        │ MOTOR MATEMÁTICO    │
   │ - rodamientos_bolas (52)│        │ - ingenieria_skf.py │
   │ - correas_potencia (T9) │        │ - cli_ingenieria.py │
   │ - factores C1, C2, C3, i│        │ - Solver Cuadrático │
   └─────────────────────────┘        └─────────────────────┘
```

---

## ⚙️ Módulo 1: Trabajo Práctico N° 6 — Rodamientos Rígidos de Bolas SKF

### Enunciado Oficial
* **Velocidad de rotación constante:** $n = 2400\text{ rpm}$
* **Apoyo 1 (Rodamiento A, $d_1 = 40\text{ mm}$):** $R_{Ay} = 390\text{ kgf}$, $R_{Az} = 521\text{ kgf}$
* **Apoyo 2 (Rodamiento B, $d_2 = 30\text{ mm}$):** $R_{By} = 39\text{ kgf}$, $R_{Bz} = 55\text{ kgf}$

### 1. Composición Vectorial y Carga Dinámica Equivalente P (Norma ISO 281)
Al no existir componentes axiales ($F_a = 0$), el factor radial es $X = 1$, cumpliéndose que la carga dinámica equivalente radial es idéntica a la fuerza radial resultante actuante ($P = F_r$):
* **Apoyo 1 ($d_1 = 40\text{ mm}$):**
  $$F_{r1} = \sqrt{R_{Ay}^2 + R_{Az}^2} = \sqrt{390^2 + 521^2} = \mathbf{650,80\text{ kgf}} \implies P_1 = 650,80 \times 0,009807 = \mathbf{6,384\text{ kN}}$$
* **Apoyo 2 ($d_2 = 30\text{ mm}$):**
  $$F_{r2} = \sqrt{R_{By}^2 + R_{Bz}^2} = \sqrt{39^2 + 55^2} = \mathbf{67,42\text{ kgf}} \implies P_2 = 67,42 \times 0,009807 = \mathbf{0,6614\text{ kN}}$$

### 2. Selección de Rodamientos y Resultados Oficiales de Cátedra
* **Apoyo 1 ($d_1 = 40\text{ mm}$):**
  * **Rodamiento Seleccionado:** **SKF `* 6308` (SKF Explorer)**
  * Dimensiones: $d = 40\text{ mm}$, $D = 90\text{ mm}$, $B = 23\text{ mm}$
  * Capacidades: $C = 42,3\text{ kN}$, $C_0 = 24,0\text{ kN}$, $P_u = 1,02\text{ kN}$
  * **Vida Nominal Básica (ISO 281):**
    $$L_{10} = \left(\frac{42,3}{6,384}\right)^3 = 290,90 \times 10^6\text{ rev} \implies \mathbf{L_{10h} = 2020,1\text{ horas}}$$
  * **Seguridad Estática (ISO 76, Tabla 11):** $s_0 = C_0 / P_1 = 24,0 / 6,384 = \mathbf{3,76} \ge 1,5$ (Cumple ampliamente).
  * **Vida SKF Modificada (con factor $a_{SKF}$):** Con grasa NLGI 2 a $55^\circ\text{C}$ ($\\kappa = 2,43$) y sellos 2RS1 ($\\eta_c = 0,8$), $a_{SKF} \approx 10,8 \implies \mathbf{L_{10mh} \approx 21.800\text{ horas}}$, cumpliendo la **Tabla 9 del Catálogo SKF** para ventiladores industriales ($20.000$ a $40.000\text{ h}$).

* **Apoyo 2 ($d_2 = 30\text{ mm}$):**
  * **Rodamiento Oficial Seleccionado en Clases:** **SKF `61906`**
  * Dimensiones: $d = 30\text{ mm}$, $D = 47\text{ mm}$, $B = 9\text{ mm}$
  * Capacidades: $C = 7,28\text{ kN}$, $C_0 = 4,55\text{ kN}$, $P_u = 0,20\text{ kN}$
  * **Vida Nominal Básica (ISO 281):**
    $$L_{10} = \left(\frac{7,28}{0,6614}\right)^3 = 1333,5 \times 10^6\text{ rev} \implies \mathbf{L_{10h} = 9260,7\text{ horas}}$$
  * **Seguridad Estática (ISO 76):** $s_0 = 4,55 / 0,6614 = \mathbf{6,88} \ge 1,5$ (Cumple holgadamente).
  * **Vida SKF Modificada ($L_{10mh}$):** Supera las $60.000\text{ horas}$ de funcionamiento continuo libre de mantenimiento.
  * *(Alternativa de catálogo evaluada: **SKF `* 6206`** con $C = 20,3\text{ kN}$, $L_{10h} \approx 200.758\text{ h}$)*.

---

### 🎨 Selector Multi-Vista de Alto Realismo Mecánico
El SCADA incorpora 4 modos visuales conmutables con un solo clic:
1. **🔧 Vista Ensamblaje CAD Fotorrealista (Corte):**
   * Eje cilíndrico escalonado con acabado cromado y reflejos especulares ($d = 35, 38, 40, 44, 36, 30, 28\text{ mm}$).
   * Polea trapezoidal en azul metalizado con garganta seccional normalizada a $38^\circ$.
   * Rodamientos 1 y 2 con casquillos y el **símbolo técnico oficial '✕'** de rodamiento sobre fondo azul.
   * Engranaje impulsor verde dentado con líneas de flancos rectos.
   * Cotas técnicas normalizadas de alto contraste: **100 mm**, **200 mm** y **250 mm**.
2. **🧊 Vista Proyección Isométrica 3D (Cargas Espaciales):**
   * Sólido cilíndrico en perspectiva isométrica con triedro de ejes cartesianos $(x, y, z)$.
   * Crucetas técnicas (`+`) en cada plano transversal de aplicación de cargas.
   * **Los 8 vectores de carga y reacción** en verde neón (`Ftp`, `Frp`, `Ray`, `Raz`, `Fte`, `Fre`, `RBy`, `RBz`) con badges de alto contraste y valores en tiempo real.
3. **📐 Vista DCL Ortogonal Desacoplado (Planos $x\text{-}y$ y $x\text{-}z$):**
   * Dos vigas estructurales en perfil azul independiente.
   * Franja central de cotas exclusiva con badges de alto contraste (**10 cm**, **20 cm**, **25 cm**).
   * Cargas externas en rojo y reacciones de apoyo en verde esmeralda con separación absoluta que evita cualquier solapamiento.
4. **🖼️ Vista Comparador de Láminas de Cátedra:**
   * Despliegue de los facsímiles escaneados originales (`eje_ensamblaje_cad.jpg`, `eje_isometrico_3d.jpg`, `eje_dcl_planos.jpg`) con capacidad de ampliación.

---

### 📐 Plano Técnico Seccional SKF 1.1 y Cinemática de Bolas
* **Simulación cinemática activa:** 8 bolas de acero giran dentro de las pistas a $2400\text{ rpm}$ sincronizadas en 60 FPS.
* **Escalado paramétrico dinámico:** Si se modifica el diámetro de asiento o el rodamiento, el aro interior, aro exterior, espesor $B$ y diámetro medio $d_m$ se reescalan automáticamente.
* **Triángulo vectorial de cargas:** Proyección angular de la resultante en el plano del rodamiento con ángulo de carga $\\theta = \\arctan(R_z / R_y)$.
* **Visor del Catálogo General SKF:** Botón directo para consultar la Tabla 1.1 oficial (págs. 326/328).

---

### 📖 Guía Oficial SKF Paso a Paso y Memoria Técnica
* **Acordeón interactivo estructurado en 7 pasos normativos:**
  1. *Paso 1:* Análisis de Cargas Ortogonales y Carga Equivalente $P$.
  2. *Paso 2:* Búsqueda y Selección en Tabla 1.1 SKF.
  3. *Paso 3:* Vida Nominal Básica $L_{10}$ y $L_{10h}$ (ISO 281).
  4. *Paso 4:* Contrastación con la Vida Requerida por Aplicación (Tabla 9 SKF para ventiladores: $20.000$ a $40.000\text{ h}$).
  5. *Paso 5:* Método Avanzado SKF Explorer ($L_{10m}$ con factor $a_{SKF}$, relación de viscosidad $\\kappa = \\nu / \\nu_1$, factor de contaminación $\\eta_c$ y carga límite de fatiga $P_u$).
  6. *Paso 6:* Verificación de Seguridad Estática $s_0 = C_0 / P_0 \ge 1,5$ (ISO 76, Tabla 11).
  7. *Paso 7:* Verificación de Carga Mínima $F_{rm}$ (prevención de patinado) y Velocidad Límite ($n < n_{lim}$).
* **Generador de Memoria Técnica:** Botón para abrir/imprimir en PDF el reporte formal con membrete universitario completo.

---

## 🔄 Módulo 2: Trabajo Práctico N° 7 — Transmisión por Correas Trapezoidales SKF

### Enunciado Oficial
* **Motor conductor:** Eléctrico trifásico, $P_r = 75\text{ HP} = 55,93\text{ kW}$, $n_1 = 1450\text{ rpm}$, **Arranque Directo** (*Heavy starts*), polea mayor $D = 320\text{ mm}$.
* **Máquina conducida:** Bomba centrífuga (**Clase 1**), $n_2 = 1856\text{ rpm}$, polea menor $d = 250\text{ mm}$.
* **Régimen de operación:** $20\text{ horas diarias}$ (columna **$> 16\text{ h/día}$**).
* **Distancia entre centros preliminar:** $CC_p = 650\text{ mm}$.
* **Relación cinemática:** $i_R = \frac{1856}{1450} = \frac{320}{250} = 1,28$ (Transmisión multiplicadora).

### Memoria de Cálculo Paso a Paso
1. **Factor de Servicio ($C_2$) y Potencia de Diseño ($P_d$):**
   * De la **Tabla 3** (Catálogo SKF pág. 16), para Clase 1, régimen $> 16\text{ h/día}$ y **Heavy starts** (arranque directo):
     $$\mathbf{C_2 = 1,30}$$
   * Potencia de diseño:
     $$P_d = P_r \cdot C_2 = 55,9275\text{ kW} \times 1,30 = \mathbf{72,71\text{ kW}}$$

2. **Selección del Perfil de Correa (Diagrama 2 SKF pág. 17 y Tabla 5a pág. 36):**
   * Con $P_d = 72,71\text{ kW}$ y $n_2 = 1856\text{ rpm}$, el punto de trabajo cae en la zona **`SPB, XPB, SPB-XP`**.
   * Se adopta la gama reforzada **SPB-XP (*eXtra Power*)**:
     * Geometría: $b_o = 16,3\text{ mm}$, $b_d = 14,0\text{ mm}$, $h = 13,0\text{ mm}$.
     * Diámetro mínimo admisible: $d_{\min} = 140\text{ mm} \le 250\text{ mm}$ (Cumple $\checkmark$).

3. **Geometría, Longitud Comercial SKF y Distancia entre Centros Definitiva ($CC$):**
   * Rango admisible: $0,7(D+d) = 399\text{ mm} \le CC_p = 650\text{ mm} \le 2(D+d) = 1140\text{ mm}$ (Cumple $\checkmark$).
   * Longitud primitiva preliminar:
     $$L_{d,\text{prelim}} = 2(650) + 1,57(320+250) + \frac{(320-250)^2}{4(650)} = \mathbf{2196,78\text{ mm}}$$
   * Longitud comercial normalizada adoptada (Catálogo pág. 83 y Tabla 8 pág. 40):
     $$\mathbf{\text{PHG SPB2180XP}} \quad (L_d = 2180\text{ mm} \implies C_1 = \mathbf{0,92})$$
   * Distancia entre centros definitiva por ecuación cuadrática exacta SKF:
     $$CC = \mathbf{641,4\text{ mm}}$$

4. **Cinemática y Factor de Arco ($C_3$):**
   * Velocidad lineal:
     $$v = \frac{\pi \cdot d \cdot n_2}{60\,000} = \frac{\pi \cdot 250 \cdot 1856}{60\,000} = \mathbf{24,30\text{ m/s}} \le 30\text{ m/s} \quad (\text{Cumple } \checkmark)$$
   * Factor de arco (Tabla 7 pág. 40):
     $$\frac{D-d}{CC} = \frac{70}{641,4} = 0,109 \implies \beta = \mathbf{174^\circ} \quad ; \quad C_3 = \mathbf{0,99}$$

5. **Potencia Admisible por Correa ($P_{\text{adm}}$) e Interpolación Tabla 9h:**
   * De la matriz de la Tabla 9h interpolada a $1856\text{ rpm}$ y $d = 250\text{ mm}$:
     $$P_b = 20,89\text{ kW} \qquad ; \qquad \Delta P_b (i_R=1,28) = 0,87\text{ kW} \implies P_{b,\text{total}} = \mathbf{21,75\text{ kW}}$$
   * Potencia admisible corregida:
     $$P_{\text{adm}} = P_{b,\text{total}} \cdot C_1 \cdot C_3 = 21,75 \times 0,92 \times 0,99 = \mathbf{19,81\text{ kW/correa}}$$

6. **Cantidad Definitiva de Correas:**
   $$N = \frac{P_d}{P_{\text{adm}}} = \frac{72,71\text{ kW}}{19,81\text{ kW/correa}} = 3,67 \implies \mathbf{4\text{ correas}}$$

### Selección Comercial Definitiva
> **4 correas trapezoidales estrechas de potencia extra SKF `PHG SPB2180XP`**  
> *(Alternativa superior normalizada: **4 correas SKF `PHG SPB2240XP`** con $CC = 671,6\text{ mm}$)*.

---

## 📈 Diagrama 2 SKF Interactivo (Wedge Belts)
La aplicación web incluye una reconstrucción vectorial interactiva del **Diagrama 2 SKF** en escala doble logarítmica:
* Zonas delimitadas para **SPZ**, **SPA**, **SPB / SPB-XP** y **SPC**.
* Retícula telescópica dinámica con punto pulsante en tiempo real:
  $$(P_d = 72,71\text{ kW}, n = 1856\text{ rpm}) \implies \text{Región SPB-XP (Extra Power)}$$
* Botón de inspección del facsímil escaneado oficial del catálogo (página 17).

---

## 🗄️ Base de Datos Relacional (`skf_catalog.db`)
El catálogo oficial SKF se encuentra estructurado en 7 tablas normalizadas en SQLite:
1. `rodamientos_bolas`: 52 modelos SKF ($d = 25\text{ a }55\text{ mm}$) con $d, D, B, C, C_0, P_u, n_{ref}, n_{lim}, \text{masa}$.
2. `correas_perfiles`: Geometría y límites de perfiles SPZ, SPA, SPB, SPC.
3. `correas_longitudes_c1`: Catálogo de longitudes comerciales normalizadas con factor $C_1$.
4. `correas_servicio_c2`: Matriz de factores de servicio (Clases 1 a 4, arranque normal/pesado, $<10\text{h}$, $10\text{--}16\text{h}$, $>16\text{h}$).
5. `correas_multiplicador_ir`: Multiplicadores por relación de aumento de velocidad de Tabla 1.
6. `correas_arco_c3`: Factores de corrección por ángulo de contacto $\beta$.
7. `correas_potencia_basica`: Matriz de potencias nominales y adicionales de la Tabla 9h.

---

## 📁 Estructura del Repositorio

```
c:\Mecatronica 2026\Mecanica2\ULTIMO\
│
├── index.html                   # Aplicación Web SCADA completa (UI, SVG, SQLite DB en cliente)
├── vercel.json                  # Configuración de despliegue en Vercel
├── .gitignore                   # Exclusiones de Git
├── README.md                    # Memoria y documentación oficial del proyecto
│
├── catalogo_rodamientos_skf.jpg # Escaneo oficial Tabla 1.1 SKF (Págs. 326/328)
├── diagrama2_skf.png            # Escaneo oficial Diagrama 2 SKF (Página 17)
├── eje_ensamblaje_cad.jpg       # Lámina 1: Ensamblaje CAD y cotas del árbol
├── eje_isometrico_3d.jpg        # Lámina 2: Proyección espacial 3D y cargas del árbol
├── eje_dcl_planos.jpg           # Lámina 3: DCL en planos ortogonales x-y y x-z
│
├── skf_catalog.db               # Base de datos relacional SQLite3 con las 7 tablas oficiales
├── db_dump.json                 # Volcado JSON estructurado del catálogo
│
├── ingenieria_skf.py            # Motor de cálculo y clases de ingeniería (Backend Python)
├── cli_ingenieria.py            # Interfaz de consola interactiva para verificación
├── generar_web.py               # Generador automatizado de la web con inyección de datos
│
├── Resolucion_Completa_TP6_y_TP7.md   # Memoria de cálculo exhaustiva con KaTeX
└── Arquitectura_Base_de_Datos_y_Logica_SKF.md # Esquema entidad-relación de la base de datos
```

---

## 🚀 Instrucciones de Ejecución y Despliegue

### 1. Despliegue en Vercel (CI/CD Automático)
El proyecto está configurado con integración continua vinculada a GitHub:
* Cada `git push origin main` activa una compilación y despliegue automático e instantáneo en [mecanicaii-tp6-tp7.vercel.app](https://mecanicaii-tp6-tp7.vercel.app/).

### 2. Ejecución Local de la Web
Simplemente haz **doble clic en `index.html`** para abrirla en cualquier navegador moderno (Chrome, Edge, Firefox, Safari), o bien ejecuta un servidor local:
```bash
python -m http.server 8000
# Abrir en el navegador: http://localhost:8000
```

### 3. Ejecución por Consola del Motor Python (CLI)
Para probar ejercicios adicionales o interactuar mediante terminal con la base de datos:
```bash
python cli_ingenieria.py
```

---

## 👨‍💻 Autor
* **Estudiante:** **Hugo Ariel Martinez**
* **Carrera:** Ingeniería Mecatrónica (Plan 2026)
* **Institución:** Universidad Tecnológica Nacional — Facultad Regional Córdoba (UTN-FRC)
* **Cátedra:** Mecánica II — Prof. Ing. Andrés Lanfranco
* **Fecha de Entrega:** Octubre / Noviembre 2026
