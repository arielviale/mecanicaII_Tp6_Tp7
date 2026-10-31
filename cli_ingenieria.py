"""
CLI / Interfaz de Usuario de Consola Interactiva para Resolución de Trabajos Prácticos
Permite ingresar cualquier valor o cargar casos de estudio desde la Base de Datos SKF.
"""

import sys
from ingenieria_skf import RodamientoResolver, CorreaResolver, DB_PATH

def menu_tp6():
    resolver = RodamientoResolver()
    print("\n" + "="*60)
    print("  RESOLUCIÓN DE TP 6 — SELECCIÓN Y CÁLCULO DE RODAMIENTOS SKF")
    print("="*60)
    print("1. Ejecutar Caso Oficial TP 6 (n=2400 rpm, d1=40mm, d2=30mm)")
    print("2. Ingresar Nuevas Reacciones y Diámetros Directamente")
    print("3. Calcular Reacciones por Equilibrio Estático (Cargas y Distancias)")
    print("4. Volver al menú principal")
    opc = input("\nSeleccione una opción [1-4]: ").strip()

    if opc == "1":
        res = resolver.resolver_ejercicio(
            n_rpm=2400, d1_mm=40, d2_mm=30,
            ray_kgf=390, raz_kgf=521, rby_kgf=39, rbz_kgf=55,
            b1_desig="* 6308", b2_desig="* 6206"
        )
        mostrar_resultados_tp6(res)
    elif opc == "2":
        try:
            n = float(input("Velocidad de giro n [rpm] (ej. 2400): "))
            d1 = float(input("Diámetro de asiento Apoyo 1 d1 [mm] (ej. 40): "))
            d2 = float(input("Diámetro de asiento Apoyo 2 d2 [mm] (ej. 30): "))
            ray = float(input("Reacción RAy [kgf] (ej. 390): "))
            raz = float(input("Reacción RAz [kgf] (ej. 521): "))
            rby = float(input("Reacción RBy [kgf] (ej. 39): "))
            rbz = float(input("Reacción RBz [kgf] (ej. 55): "))
            res = resolver.resolver_ejercicio(n, d1, d2, ray, raz, rby, rbz)
            mostrar_resultados_tp6(res)
        except Exception as e:
            print(f"Error en datos ingresados: {e}")
    elif opc == "3":
        try:
            n = float(input("Velocidad de giro n [rpm]: "))
            d1 = float(input("Diámetro asiento 1 d1 [mm]: "))
            d2 = float(input("Diámetro asiento 2 d2 [mm]: "))
            ftp = float(input("Fuerza tangencial polea Ftp [kgf]: "))
            frp = float(input("Fuerza radial polea Frp [kgf]: "))
            fte = float(input("Fuerza tangencial engranaje Fte [kgf]: "))
            fre = float(input("Fuerza radial engranaje Fre [kgf]: "))
            l1 = float(input("Longitud voladizo L1 [cm]: "))
            l2 = float(input("Distancia Apoyo 1 a Engranaje L2 [cm]: "))
            l3 = float(input("Distancia Engranaje a Apoyo 2 L3 [cm]: "))
            eq = resolver.calcular_equilibrio_estatico(ftp, frp, fte, fre, l1, l2, l3)
            print(f"\n-> Reacciones calculadas por estática: RAy={eq['ray_kgf']} kgf, RAz={eq['raz_kgf']} kgf | RBy={eq['rby_kgf']} kgf, RBz={eq['rbz_kgf']} kgf")
            res = resolver.resolver_ejercicio(n, d1, d2, eq['ray_kgf'], eq['raz_kgf'], eq['rby_kgf'], eq['rbz_kgf'])
            mostrar_resultados_tp6(res)
        except Exception as e:
            print(f"Error: {e}")

def mostrar_resultados_tp6(res):
    print("\n" + "-"*60)
    print("RESULTADOS DE LA EVALUACIÓN DE RODAMIENTOS")
    print("-"*60)
    c = res["cargas"]
    print(f"• Carga Apoyo 1: Fr1 = {c['fr1_kgf']:.2f} kgf  -->  P1 = {c['p1_kn']:.3f} kN")
    print(f"• Carga Apoyo 2: Fr2 = {c['fr2_kgf']:.2f} kgf  -->  P2 = {c['p2_kn']:.4f} kN")
    
    b1 = res["apoyo1"]["seleccionado"]
    v1 = res["apoyo1"]["vida"]
    print(f"\n[APOYO 1 - d1 = {b1['d']} mm]")
    print(f"  Rodamiento seleccionado: SKF {b1['designacion']} (C = {b1['C']} kN, C0 = {b1['C0']} kN, D={b1['D']} mm, B={b1['B']} mm)")
    print(f"  Vida nominal: L10 = {v1['l10_millones_rev']:.2f} millones de rev  |  L10h = {v1['l10h_horas']:.1f} horas")
    
    b2 = res["apoyo2"]["seleccionado"]
    v2 = res["apoyo2"]["vida"]
    print(f"\n[APOYO 2 - d2 = {b2['d']} mm]")
    print(f"  Rodamiento seleccionado: SKF {b2['designacion']} (C = {b2['C']} kN, C0 = {b2['C0']} kN, D={b2['D']} mm, B={b2['B']} mm)")
    print(f"  Vida nominal: L10 = {v2['l10_millones_rev']:.2f} millones de rev  |  L10h = {v2['l10h_horas']:.1f} horas")

    print("\nOtras opciones de catálogo disponibles en BD para este diámetro:")
    print("  Apoyo 1:", ", ".join([f"{x['designacion']} (L10h={x['l10h_horas']:.0f}h)" for x in res["apoyo1"]["todas_opciones"]]))
    print("  Apoyo 2:", ", ".join([f"{x['designacion']} (L10h={x['l10h_horas']:.0f}h)" for x in res["apoyo2"]["todas_opciones"]]))


def menu_tp7():
    resolver = CorreaResolver()
    print("\n" + "="*60)
    print("  RESOLUCIÓN DE TP 7 — CÁLCULO Y SELECCIÓN DE CORREAS SKF")
    print("="*60)
    print("1. Ejecutar Caso Oficial TP 7 (75 HP, 1450->1856 rpm, Bomba Centrífuga)")
    print("2. Ingresar Nuevo Ejercicio con Parámetros Personalizados")
    print("3. Volver al menú principal")
    opc = input("\nSeleccione una opción [1-3]: ").strip()

    if opc == "1":
        res = resolver.resolver_ejercicio(
            hp_motor=75, n1_rpm=1450, n2_rpm=1856,
            D_motor_mm=320, d_conducida_mm=250, ccp_mm=650,
            clase_maquina=1, tipo_arranque="heavy", horas_dia="gt16",
            longitud_manual=2180
        )
        mostrar_resultados_tp7(res)
    elif opc == "2":
        try:
            hp = float(input("Potencia del motor [HP] (ej. 75 ó 30): "))
            n1 = float(input("Velocidad motor n1 [rpm] (ej. 1450): "))
            n2 = float(input("Velocidad máquina conducida n2 [rpm] (ej. 1856): "))
            D = float(input("Diámetro primitivo polea motor D [mm] (ej. 320): "))
            d = float(input("Diámetro primitivo polea conducida d [mm] (ej. 250): "))
            ccp = float(input("Distancia entre centros preliminar CCp [mm] (ej. 650): "))
            print("\nClase de máquina (1: Bomba centrífuga/ventilador, 2: Compresor/cinta, 3: Molino/trituradora)")
            clase = int(input("Clase [1-4] (default 1): ") or "1")
            arranque = input("Tipo de arranque ('normal' o 'heavy' directo, default 'heavy'): ").strip() or "heavy"
            horas = input("Horas diarias ('lt10', '10to16', 'gt16', default 'gt16'): ").strip() or "gt16"
            
            res = resolver.resolver_ejercicio(hp, n1, n2, D, d, ccp, clase, arranque, horas)
            mostrar_resultados_tp7(res)
        except Exception as e:
            print(f"Error: {e}")

def mostrar_resultados_tp7(res):
    print("\n" + "-"*60)
    print("MEMORIA DE CÁLCULO PASO A PASO (TRANSMISIÓN POR CORREAS)")
    print("-"*60)
    d = res["datos_entrada"]
    p1 = res["paso1_potencia"]
    p2 = res["paso2_perfil"]
    p3 = res["paso3_geometria"]
    p4 = res["paso4_cinematica"]
    p5 = res["paso5_padm"]
    p6 = res["paso6_seleccion"]

    print(f"1. POTENCIA Y FACTOR DE SERVICIO:")
    print(f"   • Pr = {d['hp_motor']} HP = {d['pr_kw']:.2f} kW")
    print(f"   • Factor de servicio (Tabla 3, arranque directo): C2 = {p1['c2']['c2_total']:.2f}")
    print(f"   • Potencia de diseño: Pd = {p1['pd_kw']:.2f} kW")

    print(f"\n2. SELECCIÓN DE PERFIL (DIAGRAMA 2 SKF):")
    print(f"   • Perfil recomendado: SECCIÓN {p2['perfil']} (bo={p2['bo']} mm, h={p2['h']} mm)")
    print(f"   • Diámetro mínimo recomendado: d_min = {p2['d_min_rec']} mm <= {d['d_small']} mm ({'Cumple' if p2['cumple_dmin'] else 'Alerta: bajo el mínimo'})")

    print(f"\n3. GEOMETRÍA Y LONGITUD COMERCIAL:")
    print(f"   • Rango admisible para CCp: [{p3['rango_cc_min']:.0f} mm, {p3['rango_cc_max']:.0f} mm] ({'Cumple' if p3['cumple_rango_cc'] else 'Fuera de rango'})")
    print(f"   • Longitud preliminar calculada: Ld_prelim = {p3['ld_prelim']:.2f} mm")
    print(f"   • Longitud comercial adoptada: {p3['designacion_comercial']} (Ld = {p3['ld_comercial']} mm, C1 = {p3['c1']})")
    print(f"   • Distancia entre centros definitiva: CC = {p3['cc_def']:.1f} mm")

    print(f"\n4. CINEMÁTICA Y ARCO DE CONTACTO:")
    print(f"   • Velocidad lineal: v = {p4['v_ms']:.2f} m/s (Admisible < 33 m/s)")
    print(f"   • Arco de contacto polea menor: beta = {p4['arco_deg']}° (Factor C3 = {p4['c3']})")

    print(f"\n5. POTENCIA ADMISIBLE POR CORREA:")
    print(f"   • Pb nominal = {p5['pb']['pb_nominal']:.2f} kW + Pb adicional = {p5['pb']['pb_adicional']:.2f} kW => Pb total = {p5['pb']['pb_total']:.2f} kW")
    print(f"   • Padm = Pb * C1 * C3 = {p5['pb']['pb_total']:.2f} * {p3['c1']} * {p4['c3']} = {p5['padm_kw']:.2f} kW/correa")

    print(f"\n6. CANTIDAD DE CORREAS Y DESIGNACIÓN:")
    print(f"   • N exacto = Pd / Padm = {p1['pd_kw']:.2f} / {p5['padm_kw']:.2f} = {p6['n_exacto']:.2f} correas")
    print(f"   ============================================================")
    print(f"   --> RESULTADO FINAL: {p6['designacion_final']}")
    print(f"   • Potencia total instalada: {p6['potencia_total_instalada']:.2f} kW >= {p1['pd_kw']:.2f} kW")
    print(f"   ============================================================")


def main():
    while True:
        print("\n" + "#"*60)
        print("  SISTEMA PROFESIONAL DE INGENIERÍA MECÁNICA II (SKF ENGINE)")
        print("  Base de Datos Relacional SQLite3 & Motores Paramétricos")
        print("#"*60)
        print("1. Módulo TP N° 6 — Rodamientos Rígidos de Bolas SKF")
        print("2. Módulo TP N° 7 — Transmisiones por Correas SKF")
        print("3. Salir")
        sel = input("\nSeleccione una opción [1-3]: ").strip()
        if sel == "1":
            menu_tp6()
        elif sel == "2":
            menu_tp7()
        elif sel == "3":
            print("\nFinalizando sistema. ¡Éxitos en la entrega!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()

