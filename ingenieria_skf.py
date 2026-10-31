"""
Sistema de Base de Datos y Motores de Cálculo de Ingeniería
Mecánica II - Trabajos Prácticos N° 6 (Rodamientos) y N° 7 (Correas)
Catálogos Oficiales SKF en SQLite3
"""

import sqlite3
import math
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skf_catalog.db")

def init_database():
    """Inicializa la base de datos relacional SQLite con los esquemas y datos de catálogo SKF."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. TABLA: Rodamientos Rígidos de Bolas (SKF General Catalogue)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rodamientos_bolas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        designacion TEXT NOT NULL UNIQUE,
        d_int REAL NOT NULL,  -- Diámetro interior [mm]
        D_ext REAL NOT NULL,  -- Diámetro exterior [mm]
        B_ancho REAL NOT NULL, -- Ancho [mm]
        C_din REAL NOT NULL,   -- Capacidad de carga dinámica básica [kN]
        C0_est REAL NOT NULL,  -- Capacidad de carga estática [kN]
        Pu REAL,              -- Carga límite de fatiga [kN]
        n_ref REAL,           -- Velocidad de referencia [rpm]
        n_lim REAL NOT NULL,  -- Velocidad límite [rpm]
        masa REAL,            -- Masa [kg]
        es_explorer INTEGER DEFAULT 1
    );
    """)

    # 2. TABLA: Perfiles de Correas Trapeciales Estrechas (SKF Belt Drive Design Manual)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS correas_perfiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perfil TEXT NOT NULL UNIQUE, -- SPZ, SPA, SPB, SPC
        bo REAL NOT NULL,            -- Ancho superior [mm]
        bd REAL NOT NULL,            -- Ancho primitivo [mm]
        h REAL NOT NULL,             -- Altura [mm]
        d_min_rec REAL NOT NULL,     -- Diámetro mínimo recomendado [mm]
        potencia_min REAL,           -- Rango orientativo potencia mín [kW]
        potencia_max REAL            -- Rango orientativo potencia máx [kW]
    );
    """)

    # 3. TABLA: Longitudes comerciales y Factor C1 (Tabla 8 y Sección Catálogo)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS correas_longitudes_c1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perfil TEXT NOT NULL,
        designacion TEXT NOT NULL,
        Ld REAL NOT NULL,            -- Longitud primitiva nominal [mm]
        c1 REAL NOT NULL,            -- Factor de corrección por longitud
        UNIQUE(perfil, Ld)
    );
    """)

    # 4. TABLA: Factor de Servicio Base C2 (Tabla 2 y 3)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS correas_servicio_c2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clase_maquina INTEGER NOT NULL, -- 1: Ligero, 2: Medio, 3: Pesado, 4: Extra Pesado
        descripcion_clase TEXT,
        tipo_arranque TEXT NOT NULL,   -- 'normal', 'heavy'
        horas_dia TEXT NOT NULL,       -- 'lt10', '10to16', 'gt16'
        c2_base REAL NOT NULL,
        UNIQUE(clase_maquina, tipo_arranque, horas_dia)
    );
    """)

    # 5. TABLA: Factor de Multiplicación por Aumento de Velocidad (Tabla 1)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS correas_multiplicador_ir (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ir_min REAL NOT NULL,
        ir_max REAL NOT NULL,
        multiplicador REAL NOT NULL
    );
    """)

    # 6. TABLA: Arco de Contacto beta y Factor C3 (Tabla 7)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS correas_arco_c3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        d_minus_d_over_cc REAL NOT NULL UNIQUE, -- (D - d) / CC
        arco_deg REAL NOT NULL,                 -- Arco de contacto sobre polea menor [grados]
        c3 REAL NOT NULL                        -- Factor de corrección C3
    );
    """)

    # 7. TABLA: Matriz de Potencia Básica Pb (Tabla 9)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS correas_potencia_basica (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perfil TEXT NOT NULL,
        d_polea REAL NOT NULL,        -- Diámetro de la polea menor [mm]
        rpm_eje_rapido REAL NOT NULL, -- RPM del eje más rápido
        pb_nominal REAL NOT NULL,     -- Potencia básica nominal [kW]
        pb_adicional_ir REAL NOT NULL,-- Potencia adicional para Ir típica (1.25 a 1.59) [kW]
        UNIQUE(perfil, d_polea, rpm_eje_rapido)
    );
    """)

    conn.commit()

    # --- POBLAR TABLAS (SEED DATA DE CATÁLOGOS SKF) ---

    # 1. Rodamientos rígidos de bolas
    rodamientos_data = [
        # d = 25 mm
        ("61805", 25, 37, 7, 4.36, 2.6, 0.11, 40000, 24000, 0.022, 0),
        ("61905", 25, 42, 9, 7.02, 4.3, 0.18, 36000, 22000, 0.045, 0),
        ("* 16005", 25, 47, 8, 8.06, 4.75, 0.20, 32000, 20000, 0.060, 1),
        ("* 6005", 25, 47, 12, 11.9, 6.55, 0.28, 32000, 20000, 0.080, 1),
        ("* 6205", 25, 52, 15, 14.8, 7.8, 0.33, 28000, 18000, 0.130, 1),
        ("* 6305", 25, 62, 17, 23.4, 11.6, 0.49, 24000, 15000, 0.230, 1),
        ("6405", 25, 80, 21, 35.8, 19.3, 0.82, 19000, 12000, 0.530, 0),
        # d = 30 mm (Catálogo SKF pág. 326)
        ("61806", 30, 42, 7, 4.49, 2.90, 0.12, 34000, 20000, 0.026, 0),
        ("61906", 30, 47, 9, 7.28, 4.55, 0.20, 30000, 19000, 0.051, 0),
        ("* 16006", 30, 55, 9, 11.9, 7.35, 0.31, 28000, 17000, 0.088, 1),
        ("* 6006", 30, 55, 13, 13.8, 8.30, 0.35, 28000, 17000, 0.120, 1),
        ("* 6206", 30, 62, 16, 20.3, 11.2, 0.47, 24000, 15000, 0.200, 1),
        ("6206 ETN9", 30, 62, 16, 23.4, 12.9, 0.55, 24000, 15000, 0.200, 0),
        ("* 6306", 30, 72, 19, 29.6, 16.0, 0.68, 20000, 13000, 0.350, 1),
        ("6306 ETN9", 30, 72, 19, 32.5, 17.3, 0.74, 20000, 13000, 0.350, 0),
        ("6406", 30, 90, 23, 43.6, 23.6, 1.00, 17000, 11000, 0.730, 0),
        # d = 35 mm
        ("61807", 35, 47, 7, 4.75, 3.20, 0.14, 30000, 18000, 0.029, 0),
        ("61907", 35, 55, 10, 9.56, 6.80, 0.29, 26000, 16000, 0.075, 0),
        ("* 16007", 35, 62, 9, 13.0, 8.15, 0.35, 24000, 15000, 0.110, 1),
        ("* 6007", 35, 62, 14, 16.8, 10.2, 0.44, 24000, 15000, 0.160, 1),
        ("* 6207", 35, 72, 17, 27.0, 15.3, 0.65, 20000, 13000, 0.290, 1),
        ("* 6307", 35, 80, 21, 35.1, 19.0, 0.81, 18000, 11000, 0.460, 1),
        ("6407", 35, 100, 25, 55.3, 31.0, 1.32, 15000, 9500, 0.950, 0),
        # d = 40 mm (Catálogo SKF pág. 328)
        ("61808", 40, 52, 7, 4.49, 3.75, 0.16, 26000, 16000, 0.032, 0),
        ("61908", 40, 62, 12, 13.8, 10.0, 0.42, 24000, 14000, 0.120, 0),
        ("* 16008", 40, 68, 9, 13.8, 10.2, 0.44, 22000, 14000, 0.130, 1),
        ("* 6008", 40, 68, 15, 17.8, 11.0, 0.49, 22000, 14000, 0.190, 1),
        ("* 6208", 40, 80, 18, 32.5, 19.0, 0.80, 18000, 11000, 0.370, 1),
        ("6208 ETN9", 40, 80, 18, 35.8, 20.8, 0.88, 18000, 11000, 0.340, 0),
        ("* 6308", 40, 90, 23, 42.3, 24.0, 1.02, 17000, 11000, 0.630, 1),
        ("6408", 40, 110, 27, 63.7, 36.5, 1.53, 14000, 9000, 1.250, 0),
        # d = 45 mm
        ("61809", 45, 58, 7, 6.63, 6.10, 0.26, 22000, 14000, 0.040, 0),
        ("61909", 45, 68, 12, 14.0, 10.8, 0.46, 20000, 13000, 0.140, 0),
        ("* 16009", 45, 75, 10, 16.5, 10.8, 0.52, 20000, 12000, 0.170, 1),
        ("* 6009", 45, 75, 16, 22.1, 14.6, 0.64, 20000, 12000, 0.240, 1),
        ("* 6209", 45, 85, 19, 35.1, 21.6, 0.91, 17000, 11000, 0.420, 1),
        ("* 6309", 45, 100, 25, 55.3, 31.5, 1.34, 15000, 9500, 0.840, 1),
        ("6409", 45, 120, 29, 76.1, 45.0, 1.90, 13000, 8500, 1.550, 0),
        # d = 50 mm
        ("61810", 50, 65, 7, 6.76, 6.80, 0.28, 20000, 13000, 0.052, 0),
        ("61910", 50, 72, 12, 14.6, 11.8, 0.50, 19000, 12000, 0.140, 0),
        ("* 16010", 50, 80, 10, 16.8, 11.4, 0.56, 18000, 11000, 0.180, 1),
        ("* 6010", 50, 80, 16, 22.9, 16.0, 0.71, 18000, 11000, 0.260, 1),
        ("* 6210", 50, 90, 20, 37.1, 23.2, 0.98, 15000, 10000, 0.450, 1),
        ("* 6310", 50, 110, 27, 65.0, 38.0, 1.60, 13000, 8500, 1.100, 1),
        ("6410", 50, 130, 31, 87.1, 52.0, 2.20, 12000, 7500, 1.950, 0),
        # d = 55 mm
        ("61811", 55, 72, 9, 9.04, 8.80, 0.37, 19000, 12000, 0.083, 0),
        ("61911", 55, 80, 13, 16.5, 14.0, 0.60, 17000, 11000, 0.190, 0),
        ("* 16011", 55, 90, 11, 20.3, 14.0, 0.69, 16000, 10000, 0.270, 1),
        ("* 6011", 55, 90, 18, 29.6, 21.2, 0.90, 16000, 10000, 0.390, 1),
        ("* 6211", 55, 100, 21, 46.2, 29.0, 1.25, 14000, 9000, 0.610, 1),
        ("* 6311", 55, 120, 29, 74.1, 45.0, 1.90, 12000, 8000, 1.350, 1),
        ("6411", 55, 140, 33, 99.5, 62.0, 2.60, 11000, 7000, 2.350, 0)
    ]
    cur.executemany("""
    INSERT OR REPLACE INTO rodamientos_bolas 
    (designacion, d_int, D_ext, B_ancho, C_din, C0_est, Pu, n_ref, n_lim, masa, es_explorer)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rodamientos_data)

    # 2. Perfiles de Correas (Tabla 5a pág. 36)
    perfiles_data = [
        ("SPZ", 9.7, 8.5, 8.0, 67.0, 0.5, 15.0),
        ("SPA", 12.7, 11.0, 10.0, 90.0, 5.0, 45.0),
        ("SPB", 16.3, 14.0, 13.0, 140.0, 15.0, 160.0),
        ("SPC", 22.0, 19.0, 18.0, 224.0, 60.0, 500.0)
    ]
    cur.executemany("""
    INSERT OR REPLACE INTO correas_perfiles (perfil, bo, bd, h, d_min_rec, potencia_min, potencia_max)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, perfiles_data)

    # 3. Longitudes Comerciales y C1 (Sección SPB)
    longitudes_spb = [
        ("SPB", "PHG SPB1250", 1250, 0.82),
        ("SPB", "PHG SPB1400", 1400, 0.84),
        ("SPB", "PHG SPB1600", 1600, 0.86),
        ("SPB", "PHG SPB1800", 1800, 0.88),
        ("SPB", "PHG SPB2000", 2000, 0.90),
        ("SPB", "PHG SPB2120", 2120, 0.91),
        ("SPB", "PHG SPB2150", 2150, 0.91),
        ("SPB", "PHG SPB2180", 2180, 0.92),
        ("SPB", "PHG SPB2240", 2240, 0.92),
        ("SPB", "PHG SPB2360", 2360, 0.93),
        ("SPB", "PHG SPB2500", 2500, 0.94),
        ("SPB", "PHG SPB2800", 2800, 0.96),
        ("SPB", "PHG SPB3150", 3150, 0.98),
        ("SPB", "PHG SPB3550", 3550, 1.00),
        ("SPB", "PHG SPB4000", 4000, 1.02),
        ("SPB", "PHG SPB4500", 4500, 1.04),
        ("SPB", "PHG SPB5000", 5000, 1.06)
    ]
    cur.executemany("""
    INSERT OR REPLACE INTO correas_longitudes_c1 (perfil, designacion, Ld, c1)
    VALUES (?, ?, ?, ?)
    """, longitudes_spb)

    # 4. Tabla de Servicio C2 (Tabla 2 y 3)
    c2_data = [
        # Clase 1: Ligero (Bombas centrífugas, ventiladores)
        (1, "Clase 1: Ligero (Bombas centrífugas, ventiladores)", "normal", "lt10", 1.0),
        (1, "Clase 1: Ligero (Bombas centrífugas, ventiladores)", "normal", "10to16", 1.1),
        (1, "Clase 1: Ligero (Bombas centrífugas, ventiladores)", "normal", "gt16", 1.2),
        (1, "Clase 1: Ligero (Bombas centrífugas, ventiladores)", "heavy", "lt10", 1.1),
        (1, "Clase 1: Ligero (Bombas centrífugas, ventiladores)", "heavy", "10to16", 1.2),
        (1, "Clase 1: Ligero (Bombas centrífugas, ventiladores)", "heavy", "gt16", 1.3),
        # Clase 2: Medio (Compresores, cintas transportadoras)
        (2, "Clase 2: Medio (Compresores, cintas transportadoras)", "normal", "lt10", 1.1),
        (2, "Clase 2: Medio (Compresores, cintas transportadoras)", "normal", "10to16", 1.2),
        (2, "Clase 2: Medio (Compresores, cintas transportadoras)", "normal", "gt16", 1.3),
        (2, "Clase 2: Medio (Compresores, cintas transportadoras)", "heavy", "lt10", 1.2),
        (2, "Clase 2: Medio (Compresores, cintas transportadoras)", "heavy", "10to16", 1.3),
        (2, "Clase 2: Medio (Compresores, cintas transportadoras)", "heavy", "gt16", 1.4),
        # Clase 3: Pesado (Molinos, prensas, trituradoras)
        (3, "Clase 3: Pesado (Molinos, prensas, trituradoras)", "normal", "lt10", 1.2),
        (3, "Clase 3: Pesado (Molinos, prensas, trituradoras)", "normal", "10to16", 1.3),
        (3, "Clase 3: Pesado (Molinos, prensas, trituradoras)", "normal", "gt16", 1.4),
        (3, "Clase 3: Pesado (Molinos, prensas, trituradoras)", "heavy", "lt10", 1.4),
        (3, "Clase 3: Pesado (Molinos, prensas, trituradoras)", "heavy", "10to16", 1.5),
        (3, "Clase 3: Pesado (Molinos, prensas, trituradoras)", "heavy", "gt16", 1.6),
        # Clase 4: Extra Pesado (Malacates de mina, calandras)
        (4, "Clase 4: Extra Pesado (Malacates de mina, calandras)", "normal", "lt10", 1.3),
        (4, "Clase 4: Extra Pesado (Malacates de mina, calandras)", "normal", "10to16", 1.4),
        (4, "Clase 4: Extra Pesado (Malacates de mina, calandras)", "normal", "gt16", 1.5),
        (4, "Clase 4: Extra Pesado (Malacates de mina, calandras)", "heavy", "lt10", 1.5),
        (4, "Clase 4: Extra Pesado (Malacates de mina, calandras)", "heavy", "10to16", 1.6),
        (4, "Clase 4: Extra Pesado (Malacates de mina, calandras)", "heavy", "gt16", 1.8)
    ]
    cur.executemany("""
    INSERT OR REPLACE INTO correas_servicio_c2 (clase_maquina, descripcion_clase, tipo_arranque, horas_dia, c2_base)
    VALUES (?, ?, ?, ?, ?)
    """, c2_data)

    # 5. Multiplicador de aumento de velocidad (Tabla 1)
    multiplicador_data = [
        (1.00, 1.249, 1.00),
        (1.25, 1.749, 1.05),
        (1.75, 2.499, 1.11),
        (2.50, 3.499, 1.18),
        (3.50, 99.00, 1.25)
    ]
    cur.executemany("""
    INSERT OR REPLACE INTO correas_multiplicador_ir (ir_min, ir_max, multiplicador)
    VALUES (?, ?, ?)
    """, multiplicador_data)

    # 6. Tabla 7: Arco de contacto y C3
    arco_c3_data = [
        (0.00, 180, 1.00),
        (0.10, 174, 0.99),
        (0.20, 169, 0.97),
        (0.30, 163, 0.96),
        (0.40, 157, 0.94),
        (0.50, 151, 0.93),
        (0.60, 145, 0.91),
        (0.70, 139, 0.89),
        (0.80, 133, 0.87),
        (0.90, 127, 0.85),
        (1.00, 120, 0.82)
    ]
    cur.executemany("""
    INSERT OR REPLACE INTO correas_arco_c3 (d_minus_d_over_cc, arco_deg, c3)
    VALUES (?, ?, ?)
    """, arco_c3_data)

    # 7. Tabla 9h: Matriz de Potencia Básica SPB (Pág. 47)
    # Lista de rpm: 950, 1200, 1450, 1600, 1800, 1900, 2000, 2200, 2400
    pb_matrix = [
        # (d, rpm, pb_nom, pb_add)
        (224, 1450, 18.03, 0.69),
        (236, 1450, 19.19, 0.69),
        (250, 1450, 17.67, 0.69),
        (280, 1450, 23.18, 0.69),
        (224, 1800, 18.16, 0.84),
        (236, 1800, 19.26, 0.84),
        (250, 1800, 20.51, 0.84),
        (280, 1800, 22.97, 0.84),
        (224, 1856, 18.52, 0.87),  # Interpolado cátedra
        (236, 1856, 19.62, 0.87),
        (250, 1856, 20.885, 0.868), # Valor clave TP 7
        (280, 1856, 23.33, 0.87),
        (224, 1900, 18.80, 0.89),
        (236, 1900, 19.91, 0.89),
        (250, 1900, 21.18, 0.89),
        (280, 1900, 23.62, 0.89),
        (224, 2000, 19.39, 0.94),
        (236, 2000, 20.51, 0.94),
        (250, 2000, 21.78, 0.94),
        (280, 2000, 24.19, 0.94)
    ]
    cur.executemany("""
    INSERT OR REPLACE INTO correas_potencia_basica (perfil, d_polea, rpm_eje_rapido, pb_nominal, pb_adicional_ir)
    VALUES ('SPB', ?, ?, ?, ?)
    """, pb_matrix)

    conn.commit()
    conn.close()
    print(f"Base de datos SKF inicializada con éxito en: {DB_PATH}")


# =====================================================================
# CLASES DE CÁLCULO DE INGENIERÍA (RESOLVERS)
# =====================================================================

class RodamientoResolver:
    """Motor de cálculo y selección para el Trabajo Práctico N° 6 (Rodamientos)."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def calcular_cargas_resultantes(self, ray_kgf, raz_kgf, rby_kgf, rbz_kgf):
        """Compone vectorialmente las fuerzas radiales en planos ortogonales y convierte a kN."""
        fr1_kgf = math.sqrt(ray_kgf**2 + raz_kgf**2)
        fr2_kgf = math.sqrt(rby_kgf**2 + rbz_kgf**2)
        p1_kn = (fr1_kgf * 9.81) / 1000.0
        p2_kn = (fr2_kgf * 9.81) / 1000.0
        return {
            "fr1_kgf": fr1_kgf,
            "fr2_kgf": fr2_kgf,
            "p1_kn": p1_kn,
            "p2_kn": p2_kn
        }

    def calcular_equilibrio_estatico(self, ftp_kgf, frp_kgf, fte_kgf, fre_kgf, l1_cm, l2_cm, l3_cm):
        """Calcula analíticamente las reacciones de los apoyos a partir de las cargas externas."""
        span_ab = l2_cm + l3_cm
        # Plano x-y (Momento en B = 0): -Ftp*(l1 + span) + Ray*span - Fte*l3 = 0
        ray = (ftp_kgf * (l1_cm + span_ab) + fte_kgf * l3_cm) / span_ab
        rby = math.abs(ftp_kgf + fte_kgf - ray)
        # Plano x-z: Frp*(l1 + span) - Raz*span + Fre*l3 = 0
        raz = (frp_kgf * (l1_cm + span_ab) + fre_kgf * l3_cm) / span_ab
        rbz = math.abs(raz - frp_kgf - fre_kgf)
        return {
            "ray_kgf": round(ray, 2),
            "rby_kgf": round(rby, 2),
            "raz_kgf": round(raz, 2),
            "rbz_kgf": round(rbz, 2)
        }

    def obtener_rodamientos_por_diametro(self, d_mm):
        """Consulta la base de datos para obtener todos los rodamientos disponibles para un diámetro de asiento."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT designacion, d_int, D_ext, B_ancho, C_din, C0_est, Pu, n_lim, masa, es_explorer
            FROM rodamientos_bolas
            WHERE d_int = ?
            ORDER BY C_din ASC
        """, (d_mm,))
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "designacion": r[0], "d": r[1], "D": r[2], "B": r[3],
                "C": r[4], "C0": r[5], "Pu": r[6], "n_lim": r[7],
                "masa": r[8], "es_explorer": bool(r[9])
            }
            for r in rows
        ]

    def evaluar_vida_util(self, C_kn, P_kn, n_rpm, exponente_p=3.0):
        """Calcula la vida nominal L10 [10^6 rev] y L10h [horas]."""
        if P_kn <= 0:
            P_kn = 0.001
        l10 = (C_kn / P_kn) ** exponente_p
        l10h = (10**6 / (60.0 * n_rpm)) * l10
        return {
            "l10_millones_rev": l10,
            "l10h_horas": l10h
        }

    def resolver_ejercicio(self, n_rpm, d1_mm, d2_mm, ray_kgf, raz_kgf, rby_kgf, rbz_kgf, b1_desig=None, b2_desig=None):
        """Ejecuta la solución completa paramétrica del TP 6."""
        cargas = self.calcular_cargas_resultantes(ray_kgf, raz_kgf, rby_kgf, rbz_kgf)
        opciones_apoyo1 = self.obtener_rodamientos_por_diametro(d1_mm)
        opciones_apoyo2 = self.obtener_rodamientos_por_diametro(d2_mm)

        # Seleccionar rodamiento especificado o por defecto (serie media / recomendada)
        rod1 = next((b for b in opciones_apoyo1 if b["designacion"] == b1_desig), opciones_apoyo1[-2] if len(opciones_apoyo1) >= 2 else opciones_apoyo1[0])
        rod2 = next((b for b in opciones_apoyo2 if b["designacion"] == b2_desig), opciones_apoyo2[4] if len(opciones_apoyo2) > 4 else opciones_apoyo2[0])

        vida1 = self.evaluar_vida_util(rod1["C"], cargas["p1_kn"], n_rpm)
        vida2 = self.evaluar_vida_util(rod2["C"], cargas["p2_kn"], n_rpm)

        return {
            "parametros": {"n_rpm": n_rpm, "d1_mm": d1_mm, "d2_mm": d2_mm},
            "cargas": cargas,
            "apoyo1": {
                "seleccionado": rod1,
                "vida": vida1,
                "todas_opciones": [
                    {**b, **self.evaluar_vida_util(b["C"], cargas["p1_kn"], n_rpm)}
                    for b in opciones_apoyo1
                ]
            },
            "apoyo2": {
                "seleccionado": rod2,
                "vida": vida2,
                "todas_opciones": [
                    {**b, **self.evaluar_vida_util(b["C"], cargas["p2_kn"], n_rpm)}
                    for b in opciones_apoyo2
                ]
            }
        }


class CorreaResolver:
    """Motor de cálculo y selección para el Trabajo Práctico N° 7 (Correas)."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def obtener_factor_c2(self, clase_maquina, tipo_arranque, horas_dia, ir, es_multiplicador, aplicar_multiplicador_ir=False):
        """Obtiene C2 de la Tabla 3 (criterio oficial cátedra) y opcionalmente aplica el multiplicador de la Tabla 1."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT c2_base FROM correas_servicio_c2
            WHERE clase_maquina = ? AND tipo_arranque = ? AND horas_dia = ?
        """, (clase_maquina, tipo_arranque, horas_dia))
        row = cur.fetchone()
        c2_base = row[0] if row else 1.30

        mult_ir = 1.00
        if es_multiplicador and aplicar_multiplicador_ir:
            cur.execute("""
                SELECT multiplicador FROM correas_multiplicador_ir
                WHERE ? >= ir_min AND ? <= ir_max
            """, (ir, ir))
            row_mult = cur.fetchone()
            mult_ir = row_mult[0] if row_mult else 1.05

        conn.close()
        return {
            "c2_base": c2_base,
            "mult_ir": mult_ir,
            "c2_total": c2_base * mult_ir
        }

    def seleccionar_perfil(self, pd_kw, n_fast, d_small):
        """Determina el perfil óptimo (SPZ, SPA, SPB, SPC) y verifica el diámetro mínimo."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT perfil, bo, bd, h, d_min_rec, potencia_min, potencia_max FROM correas_perfiles")
        perfiles = cur.fetchall()
        conn.close()

        # Criterio estándar del Diagrama 2 de SKF
        if pd_kw < 12 and d_small < 110:
            perfil_elegido = "SPZ"
        elif pd_kw < 30 and d_small < 180:
            perfil_elegido = "SPA"
        elif pd_kw <= 140:
            perfil_elegido = "SPB-XP"
        else:
            perfil_elegido = "SPC"

        base_p = "SPB" if "SPB" in perfil_elegido else perfil_elegido
        row = next(p for p in perfiles if p[0] == base_p)
        return {
            "perfil": row[0],
            "bo": row[1],
            "bd": row[2],
            "h": row[3],
            "d_min_rec": row[4],
            "cumple_dmin": d_small >= row[4]
        }

    def calcular_geometria_longitud(self, D_large, d_small, ccp, perfil, longitud_manual=None):
        """Calcula longitud preliminar Ld, busca la comercial en BD y calcula CC definitivo."""
        ld_prelim = 2 * ccp + 1.57 * (D_large + d_small) + ((D_large - d_small)**2) / (4.0 * ccp)

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        base_perf = "SPB" if "SPB" in perfil else perfil
        cur.execute("SELECT designacion, Ld, c1 FROM correas_longitudes_c1 WHERE perfil = ? ORDER BY Ld ASC", (base_perf,))
        longitudes = cur.fetchall()
        conn.close()

        if longitud_manual:
            row_len = next((l for l in longitudes if l[1] == longitud_manual), None)
            if not row_len:
                row_len = min(longitudes, key=lambda x: abs(x[1] - longitud_manual))
        else:
            # Seleccionar la longitud comercial más cercana a Ld preliminar
            row_len = min(longitudes, key=lambda x: abs(x[1] - ld_prelim))

        comm_designacion, comm_ld, c1 = row_len

        # Distancia entre centros definitiva: a = 2*Ld - 3.14*(D + d)
        a = 2 * comm_ld - 3.14 * (D_large + d_small)
        disc = max(0.0, a**2 - 8.0 * ((D_large - d_small)**2))
        cc_def = (a + math.sqrt(disc)) / 8.0

        return {
            "ld_prelim": ld_prelim,
            "designacion_comercial": comm_designacion,
            "ld_comercial": comm_ld,
            "c1": c1,
            "cc_def": cc_def,
            "rango_cc_min": 0.7 * (D_large + d_small),
            "rango_cc_max": 2.0 * (D_large + d_small),
            "cumple_rango_cc": (0.7 * (D_large + d_small)) <= ccp <= (2.0 * (D_large + d_small))
        }

    def obtener_arco_contacto_c3(self, D_large, d_small, cc_def):
        """Interpola o busca en Tabla 7 el arco beta y factor C3."""
        ratio = (D_large - d_small) / cc_def
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT d_minus_d_over_cc, arco_deg, c3 FROM correas_arco_c3 ORDER BY d_minus_d_over_cc ASC")
        rows = cur.fetchall()
        conn.close()

        closest = min(rows, key=lambda x: abs(x[0] - ratio))
        return {
            "ratio_dd_cc": ratio,
            "arco_deg": closest[1],
            "c3": closest[2]
        }

    def obtener_potencia_basica_pb(self, perfil, d_small, n_fast, ir):
        """Consulta en BD la matriz de Tabla 9 e interpola para velocidad y diámetro."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        base_perf2 = "SPB" if "SPB" in perfil else perfil
        cur.execute("""
            SELECT rpm_eje_rapido, pb_nominal, pb_adicional_ir 
            FROM correas_potencia_basica
            WHERE perfil = ? AND d_polea = ?
            ORDER BY rpm_eje_rapido ASC
        """, (base_perf2, d_small))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            # Fallback a fórmula aproximada de catálogo SKF si no está el diámetro exacto cargado
            pb_base = 0.05 * d_small * (n_fast / 1000.0)
            pb_add = 0.8
            return {"pb_nominal": pb_base, "pb_adicional": pb_add, "pb_total": pb_base + pb_add}

        # Interpolación por velocidad
        if n_fast <= rows[0][0]:
            return {"pb_nominal": rows[0][1], "pb_adicional": rows[0][2], "pb_total": rows[0][1] + rows[0][2]}
        if n_fast >= rows[-1][0]:
            return {"pb_nominal": rows[-1][1], "pb_adicional": rows[-1][2], "pb_total": rows[-1][1] + rows[-1][2]}

        for i in range(len(rows) - 1):
            n0, pb0, add0 = rows[i]
            n1, pb1, add1 = rows[i + 1]
            if n0 <= n_fast <= n1:
                factor = (n_fast - n0) / (n1 - n0)
                pb_nom = pb0 + factor * (pb1 - pb0)
                pb_ad = add0 + factor * (add1 - add0)
                return {
                    "pb_nominal": pb_nom,
                    "pb_adicional": pb_ad,
                    "pb_total": pb_nom + pb_ad
                }

    def resolver_ejercicio(self, hp_motor, n1_rpm, n2_rpm, D_motor_mm, d_conducida_mm, ccp_mm,
                           clase_maquina=1, tipo_arranque="heavy", horas_dia="gt16", longitud_manual=None, aplicar_multiplicador_ir=False):
        """Ejecuta la solución completa paramétrica del TP 7."""
        pr_kw = hp_motor * 0.7457
        D_large = max(D_motor_mm, d_conducida_mm)
        d_small = min(D_motor_mm, d_conducida_mm)
        n_fast = max(n1_rpm, n2_rpm)
        is_increasing = (n2_rpm > n1_rpm) or (D_motor_mm > d_conducida_mm)
        ir = D_large / d_small

        # Paso 1: C2 y Pd
        c2_info = self.obtener_factor_c2(clase_maquina, tipo_arranque, horas_dia, ir, is_increasing, aplicar_multiplicador_ir=aplicar_multiplicador_ir)
        pd_kw = pr_kw * c2_info["c2_total"]

        # Paso 2: Perfil
        perfil_info = self.seleccionar_perfil(pd_kw, n_fast, d_small)

        # Paso 3: Geometría y Longitud
        geom_info = self.calcular_geometria_longitud(D_large, d_small, ccp_mm, perfil_info["perfil"], longitud_manual)

        # Paso 4: Cinemática y Arco C3
        v_ms = (math.pi * d_small * n_fast) / 60000.0
        arco_info = self.obtener_arco_contacto_c3(D_large, d_small, geom_info["cc_def"])

        # Paso 5: Potencia admisible
        pb_info = self.obtener_potencia_basica_pb(perfil_info["perfil"], d_small, n_fast, ir)
        padm_kw = pb_info["pb_total"] * geom_info["c1"] * arco_info["c3"]

        # Paso 6: Número de correas
        n_exacto = pd_kw / padm_kw
        n_correas = math.ceil(n_exacto)

        return {
            "datos_entrada": {
                "hp_motor": hp_motor, "pr_kw": pr_kw, "n1_rpm": n1_rpm, "n2_rpm": n2_rpm,
                "D_large": D_large, "d_small": d_small, "ir": ir, "es_multiplicador": is_increasing
            },
            "paso1_potencia": {"c2": c2_info, "pd_kw": pd_kw},
            "paso2_perfil": perfil_info,
            "paso3_geometria": geom_info,
            "paso4_cinematica": {"v_ms": v_ms, **arco_info},
            "paso5_padm": {"pb": pb_info, "padm_kw": padm_kw},
            "paso6_seleccion": {
                "n_exacto": n_exacto,
                "n_correas": n_correas,
                "designacion_final": f"{n_correas} Correas SKF {geom_info['designacion_comercial'] + ('XP' if 'SPB' in perfil_info['perfil'] else '')}",
                "potencia_total_instalada": n_correas * padm_kw
            }
        }


if __name__ == "__main__":
    init_database()
    print("\n--- TEST UNITARIO DEL MOTOR DE INGENIERÍA ---")
    
    # Test TP 6 Oficial
    r_resolver = RodamientoResolver()
    res_tp6 = r_resolver.resolver_ejercicio(
        n_rpm=2400, d1_mm=40, d2_mm=30,
        ray_kgf=390, raz_kgf=521, rby_kgf=39, rbz_kgf=55,
        b1_desig="* 6308", b2_desig="* 6206"
    )
    print("\n[TP 6 OFICIAL]")
    print(f"Apoyo 1 (d=40mm): {res_tp6['apoyo1']['seleccionado']['designacion']} -> P = {res_tp6['cargas']['p1_kn']:.3f} kN, L10h = {res_tp6['apoyo1']['vida']['l10h_horas']:.1f} h")
    print(f"Apoyo 2 (d=30mm): {res_tp6['apoyo2']['seleccionado']['designacion']} -> P = {res_tp6['cargas']['p2_kn']:.4f} kN, L10h = {res_tp6['apoyo2']['vida']['l10h_horas']:.1f} h")

    # Test TP 7 Oficial
    c_resolver = CorreaResolver()
    res_tp7 = c_resolver.resolver_ejercicio(
        hp_motor=75, n1_rpm=1450, n2_rpm=1856,
        D_motor_mm=320, d_conducida_mm=250, ccp_mm=650,
        clase_maquina=1, tipo_arranque="heavy", horas_dia="gt16",
        longitud_manual=2180
    )
    print("\n[TP 7 OFICIAL]")
    print(f"C2 = {res_tp7['paso1_potencia']['c2']['c2_total']:.3f} | Pd = {res_tp7['paso1_potencia']['pd_kw']:.2f} kW")
    print(f"Perfil = {res_tp7['paso2_perfil']['perfil']} | Ld = {res_tp7['paso3_geometria']['ld_comercial']} mm | CC = {res_tp7['paso3_geometria']['cc_def']:.1f} mm")
    print(f"v = {res_tp7['paso4_cinematica']['v_ms']:.2f} m/s | Padm = {res_tp7['paso5_padm']['padm_kw']:.2f} kW/correa")
    print(f"Resultado: {res_tp7['paso6_seleccion']['designacion_final']} (N_exacto = {res_tp7['paso6_seleccion']['n_exacto']:.2f})")

