# Arquitectura Profesional de Ingeniería: Base de Datos Relacional y Motores Paramétricos SKF

Este documento detalla la estructura formal de base de datos relacional (SQLite), el análisis de variables de entrada/salida y la lógica matemática implementada en Python para resolver de manera universal cualquier variante de los **Trabajos Prácticos N° 6 y N° 7**.

---

## 1. Análisis de Variables del Problema

### A) Trabajo Práctico N° 6 — Eje y Rodamientos SKF
El problema consiste en determinar la carga dinámica equivalente sobre los apoyos de un eje rotatorio sometido a flexión en dos planos ortogonales ($x\text{-}y$ y $x\text{-}z$), seleccionar rodamientos normalizados de catálogo para cada diámetro de asiento y verificar su vida nominal $L_{10}$ y $L_{10h}$.

| Tipo de Variable | Parámetro | Símbolo | Unidad | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| **Entrada (Cinemática)** | Velocidad de rotación | $n$ | $\text{rpm}$ | Régimen de giro constante del eje |
| **Entrada (Geometría)** | Diámetros de asiento | $d_1, d_2$ | $\text{mm}$ | Diámetros de los muñones para Apoyo 1 y Apoyo 2 |
| **Entrada (Modo Directo)** | Reacciones ortogonales | $R_{Ay}, R_{Az}, R_{By}, R_{Bz}$ | $\text{kgf}$ o $\text{kN}$ | Reacciones de los apoyos obtenidas del DCL |
| **Entrada (Modo Estático)** | Fuerzas externas | $F_{tp}, F_{rp}, F_{te}, F_{re}$ | $\text{kgf}$ | Componentes tangenciales y radiales en polea y engranaje |
| **Entrada (Modo Estático)** | Distancias axiales | $L_1, L_2, L_3$ | $\text{cm}$ o $\text{mm}$ | Posición de polea en voladizo, engranaje y apoyos |
| **Intermedia** | Carga radial resultante | $F_r = \sqrt{R_y^2 + R_z^2}$ | $\text{kgf}$ / $\text{kN}$ | Carga resultante en cada rodamiento ($P = F_r$) |
| **Catálogo SKF** | Parámetros del rodamiento | $C, C_0, D, B, n_{\lim}$ | $\text{kN, mm, rpm}$ | Capacidad dinámica, estática, dimensiones y velocidad límite |
| **Salida (Duración)** | Vida nominal en revoluciones | $L_{10} = (C / P)^3$ | $10^6\text{ rev}$ | Millones de ciclos con 90% de confiabilidad ($p=3$ para bolas) |
| **Salida (Duración)** | Vida nominal en horas | $L_{10h} = \frac{10^6}{60 \cdot n} L_{10}$ | $\text{horas}$ | Tiempo de servicio proyectado continuo |

---

### B) Trabajo Práctico N° 7 — Transmisión por Correas Trapeciales SKF
El problema consiste en diseñar una transmisión de potencia por correas en V estrechas según la metodología SKF / ISO, partiendo de las máquinas motriz y conducida, sus velocidades y la distancia entre ejes.

| Tipo de Variable | Parámetro | Símbolo | Unidad | Descripción / Fuente |
| :--- | :--- | :---: | :---: | :--- |
| **Entrada (Potencia)** | Potencia nominal motriz | $P_r$ | $\text{HP}$ o $\text{kW}$ | Potencia entregada por el motor conductor |
| **Entrada (Cinemática)** | Velocidades | $n_1, n_2$ | $\text{rpm}$ | Velocidades del motor y de la máquina conducida |
| **Entrada (Geometría)** | Diámetros de poleas | $D, d$ | $\text{mm}$ | Diámetro primitivo polea mayor ($D$) y menor ($d$) |
| **Entrada (Geometría)** | Distancia entre centros | $CC_p$ | $\text{mm}$ | Distancia tentativa inicial entre ejes |
| **Entrada (Servicio)** | Condiciones de servicio | Clase, Arranque, Horas | — | Clase 1–4, arranque normal/pesado, régimen diario |
| **Intermedia (Cinemática)** | Relación de transmisión | $I_r = \frac{D}{d} = \frac{n_{\text{rápido}}}{n_{\text{lento}}}$ | — | Factor de multiplicación o reducción |
| **Catálogo (Tablas 1, 2, 3)** | Factor de servicio | $C_2 = C_{2,\text{base}} \times f(I_r)$ | — | Sobrediseño según severidad y sentido de transmisión |
| **Intermedia** | Potencia de diseño | $P_d = P_r \cdot C_2$ | $\text{kW}$ | Carga demandada corregida para dimensionar correas |
| **Catálogo (Diag. 2 / Tab. 5a)**| Perfil óptimo | SPZ, SPA, SPB, SPC | — | Sección transversal y verificación $d \ge d_{\min}$ |
| **Intermedia (Geometría)** | Longitud preliminar | $L_d = 2CC_p + 1,57(D+d) + \frac{(D-d)^2}{4CC_p}$ | $\text{mm}$ | Longitud teórica del lazo cerrado |
| **Catálogo (Tabla 8 / p. 83)** | Longitud comercial | $L_{d,\text{comercial}}, C_1$ | $\text{mm}$, — | Longitud estandarizada de catálogo y factor por longitud |
| **Intermedia (Geometría)** | Distancia $CC$ definitiva | $CC = \frac{a + \sqrt{a^2 - 8(D-d)^2}}{8}$ | $\text{mm}$ | Distancia real entre ejes ajustada a la correa comercial |
| **Intermedia (Cinemática)** | Velocidad periférica | $v = \frac{\pi \cdot d \cdot n_{\text{rápido}}}{60\,000}$ | $\text{m/s}$ | Velocidad tangencial (límite $< 33\text{ a } 35\text{ m/s}$) |
| **Catálogo (Tabla 7)** | Arco y factor de contacto | $\beta, C_3$ | $^\circ$, — | Ángulo abrazado sobre polea menor y factor reductor |
| **Catálogo (Tabla 9)** | Potencia básica por correa | $P_b = P_{b,\text{nom}} + P_{b,\text{adicional}}$ | $\text{kW}$ | Capacidad unitaria de la correa a esas RPM y diámetro |
| **Intermedia** | Potencia admisible | $P_{\text{adm}} = P_b \cdot C_1 \cdot C_3$ | $\text{kW/correa}$ | Potencia neta transmitible por cada correa |
| **Salida Final** | Cantidad de correas | $N = \lceil P_d / P_{\text{adm}} \rceil$ | entero | Número de correas a montar en la transmisión |

---

## 2. Esquema Relacional de la Base de Datos (`skf_catalog.db`)

La base de datos SQLite implementada contiene las siguientes entidades normalizadas:

```
┌───────────────────────────────────────┐         ┌───────────────────────────────────────┐
│          rodamientos_bolas            │         │           correas_perfiles            │
├───────────────────────────────────────┤         ├───────────────────────────────────────┤
│ id (PK)                               │         │ id (PK)                               │
│ designacion (TEXT UNIQUE)             │         │ perfil (TEXT UNIQUE) [SPZ,SPA,SPB,SPC]│
│ d_int (REAL) [Diámetro interior mm]   │         │ bo, bd, h (REAL) [Dimensiones mm]     │
│ D_ext (REAL) [Diámetro exterior mm]   │         │ d_min_rec (REAL) [Diám. mín. polea]   │
│ B_ancho (REAL) [Ancho mm]             │         │ potencia_min, potencia_max (REAL)     │
│ C_din (REAL) [Carga dinámica kN]      │         └───────────────────────────────────────┘
│ C0_est (REAL) [Carga estática kN]     │                            ▲
│ Pu (REAL), n_ref (REAL), n_lim (REAL) │                            │ perfil
│ masa (REAL), es_explorer (INTEGER)    │         ┌──────────────────┴────────────────────┐
└───────────────────────────────────────┘         │        correas_longitudes_c1          │
                                                  ├───────────────────────────────────────┤
┌───────────────────────────────────────┐         │ id (PK)                               │
│          correas_servicio_c2          │         │ perfil (TEXT), designacion (TEXT)     │
├───────────────────────────────────────┤         │ Ld (REAL) [Longitud comercial mm]     │
│ id (PK)                               │         │ c1 (REAL) [Factor corrección]         │
│ clase_maquina (INT) [1 a 4]           │         └───────────────────────────────────────┘
│ tipo_arranque (TEXT) [normal, heavy]  │
│ horas_dia (TEXT) [lt10, 10to16, gt16] │         ┌───────────────────────────────────────┐
│ c2_base (REAL)                        │         │        correas_potencia_basica        │
└───────────────────────────────────────┘         ├───────────────────────────────────────┤
                                                  │ id (PK)                               │
┌───────────────────────────────────────┐         │ perfil (TEXT), d_polea (REAL)         │
│       correas_multiplicador_ir        │         │ rpm_eje_rapido (REAL)                 │
├───────────────────────────────────────┤         │ pb_nominal (REAL), pb_adicional_ir    │
│ id (PK)                               │         └───────────────────────────────────────┘
│ ir_min, ir_max (REAL)                 │
│ multiplicador (REAL) [1.00 a 1.25]    │         ┌───────────────────────────────────────┐
└───────────────────────────────────────┘         │           correas_arco_c3             │
                                                  ├───────────────────────────────────────┤
                                                  │ id (PK)                               │
                                                  │ d_minus_d_over_cc (REAL)              │
                                                  │ arco_deg (REAL), c3 (REAL)            │
                                                  └───────────────────────────────────────┘
```

---

## 3. Scripts y Archivos Creados en el Proyecto

1. **`skf_catalog.db`**: Base de datos SQLite que almacena los catálogos de rodamientos de bolas SKF (páginas 326 a 333) y las tablas de diseño de transmisiones por correas en V (Tablas 1, 2, 3, 5a, 7, 8, 9h y longitudes comerciales).
2. **`ingenieria_skf.py`**: Módulo central de clases y métodos de ingeniería (`RodamientoResolver` y `CorreaResolver`). Realiza consultas SQL a la base de datos, interpolaciones matemáticas y cálculo de vida útil o selección de componentes.
3. **`cli_ingenieria.py`**: Interfaz interactiva de terminal en Python para ejecutar y ensayar cualquier combinación de datos.
4. **`index.html` / `Entrega_Final_SCADA_TP6_TP7.html`**: Interfaz visual web interactiva SCADA con sinóptico animado que refleja estas mismas fórmulas y tablas en tiempo real.

