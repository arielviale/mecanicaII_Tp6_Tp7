import json

def build_web():
    with open(r'c:\Mecatronica 2026\Mecanica2\ULTIMO\db_dump.json', 'r', encoding='utf-8') as f:
        db_json_str = f.read()

    template = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SCADA Industrial & Base de Datos SKF — Mecánica II</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      --bg: #090d16;
      --panel: #111827;
      --panel-border: #1f293d;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }
    body {
      background-color: var(--bg);
      color: var(--text-main);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }
    .grid-bg {
      background-image: 
        linear-gradient(to right, rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,0.03) 1px, transparent 1px);
      background-size: 20px 20px;
    }
    .scada-panel {
      background: linear-gradient(145deg, rgba(17,24,39,0.92), rgba(15,23,42,0.85));
      border: 1px solid var(--panel-border);
      backdrop-filter: blur(10px);
      box-shadow: 0 4px 20px -2px rgba(0,0,0,0.5);
    }
    .scada-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.07);
    }
    .active-row {
      background: rgba(16, 185, 129, 0.22) !important;
      border-left: 4px solid #10b981;
      font-weight: 700;
    }
    .pulse-dot {
      animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: .4; transform: scale(1.15); }
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0b1120; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }
  </style>
</head>
<body class="grid-bg min-h-screen text-slate-100">

  <!-- TOP INDUSTRIAL APP HEADER -->
  <header class="border-b border-slate-800 bg-slate-950/80 sticky top-0 z-50 backdrop-blur-md px-4 py-3">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-cyan-500/10 border border-cyan-500/40 flex items-center justify-center text-cyan-400 font-black text-xl">
          ⚙
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-lg font-black tracking-wide bg-gradient-to-r from-cyan-400 via-teal-300 to-emerald-400 bg-clip-text text-transparent">
              SKF ENGINE • SCADA INTERACTIVO
            </h1>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold tracking-wider bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 pulse-dot"></span> SQLite DB ONLINE
            </span>
          </div>
          <p class="text-xs text-slate-400">Plataforma Paramétrica de Transmisiones Mecánicas • TP N° 6 (Rodamientos) & TP N° 7 (Correas)</p>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <button id="btn-anim" onclick="toggleAnim()" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5 cursor-pointer">
          <span id="anim-icon">⏸</span> <span id="anim-text">Pausar Simulación</span>
        </button>
        <button onclick="resetToDefaults()" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-600 hover:bg-cyan-500 text-white shadow transition flex items-center gap-1.5 cursor-pointer">
          <span>↺</span> Restablecer Casos Oficiales
        </button>
      </div>
    </div>

    <!-- MAIN MODULE TABS -->
    <div class="max-w-7xl mx-auto flex gap-2 mt-3 pt-2 border-t border-slate-800/80 overflow-x-auto">
      <button onclick="switchTab('tp6')" id="tab-btn-tp6" class="px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg cursor-pointer">
        <span>🔵</span> MÓDULO 1: Rodamientos SKF (Eje Ventilación)
      </button>
      <button onclick="switchTab('tp7')" id="tab-btn-tp7" class="px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800 cursor-pointer">
        <span>🟠</span> MÓDULO 2: Transmisión por Correas SKF (Bomba Centrífuga)
      </button>
      <button onclick="switchTab('db')" id="tab-btn-db" class="px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800 cursor-pointer">
        <span>🗄️</span> MÓDULO 3: Explorador de Base de Datos SQL SKF
      </button>
    </div>
  </header>

  <main class="max-w-7xl mx-auto p-4 space-y-6">

    <!-- VIEW: TP 6 - RODAMIENTOS -->
    <div id="view-tp6" class="space-y-6">
      
      <!-- KPIs STRIP TP6 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>CARGA APOYO 1 (A)</span>
            <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono font-bold" id="kpi-tp6-d1">d₁ = 40 mm</span>
          </div>
          <div class="text-2xl font-black text-slate-100 mt-1" id="kpi-tp6-p1">6,384 kN</div>
          <div class="text-xs text-slate-400 mt-1">
            Radial: <span class="text-emerald-400 font-semibold" id="kpi-tp6-fr1">650,80 kgf</span>
          </div>
        </div>

        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>RODAMIENTO 1 SELECCIONADO</span>
            <span class="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono font-bold" id="kpi-tp6-desig1">* 6308</span>
          </div>
          <div class="text-2xl font-black text-cyan-400 mt-1" id="kpi-tp6-l10h1">2020 h</div>
          <div class="text-xs text-slate-400 mt-1">
            Capacidad: <span class="text-slate-200 font-semibold" id="kpi-tp6-c1">C = 42,3 kN</span>
          </div>
        </div>

        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>CARGA APOYO 2 (B)</span>
            <span class="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 font-mono font-bold" id="kpi-tp6-d2">d₂ = 30 mm</span>
          </div>
          <div class="text-2xl font-black text-slate-100 mt-1" id="kpi-tp6-p2">0,661 kN</div>
          <div class="text-xs text-slate-400 mt-1">
            Radial: <span class="text-blue-400 font-semibold" id="kpi-tp6-fr2">67,42 kgf</span>
          </div>
        </div>

        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>RODAMIENTO 2 SELECCIONADO</span>
            <span class="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-mono font-bold" id="kpi-tp6-desig2">* 6206</span>
          </div>
          <div class="text-2xl font-black text-indigo-400 mt-1" id="kpi-tp6-l10h2">200.758 h</div>
          <div class="text-xs text-slate-400 mt-1">
            Capacidad: <span class="text-slate-200 font-semibold" id="kpi-tp6-c2">C = 20,3 kN</span>
          </div>
        </div>
      </div>

      <!-- MAIN TP6 WORKSPACE -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- LEFT: SVG SHAFT MODEL -->
        <div class="lg:col-span-8 scada-panel rounded-xl p-5 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div>
              <span class="text-[11px] font-bold uppercase tracking-wider text-emerald-400">Sinóptico Cinemático Industrial</span>
              <h2 class="text-base font-bold text-slate-100">Comportamiento Mecánico y Cargas Ortogonales (n = <span id="lbl-tp6-rpm" class="text-emerald-400">2400</span> rpm)</h2>
            </div>
            <div class="flex items-center gap-2 text-xs font-mono">
              <span class="px-2 py-1 rounded bg-red-500/20 text-red-400 border border-red-500/30 font-semibold">Cargas Externas</span>
              <span class="px-2 py-1 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">Reacciones Apoyo</span>
            </div>
          </div>

          <div class="bg-slate-950/70 rounded-xl border border-slate-800 p-3 overflow-x-auto">
            <svg id="svg-tp6" viewBox="0 0 840 420" class="w-full min-w-[650px] h-auto">
              <line x1="80" y1="25" x2="80" y2="390" stroke="#334155" stroke-dasharray="3 3" stroke-width="1.5"/>
              <line x1="210" y1="25" x2="210" y2="390" stroke="#10b981" stroke-dasharray="3 3" stroke-width="1.5" stroke-opacity="0.6"/>
              <line x1="450" y1="25" x2="450" y2="390" stroke="#334155" stroke-dasharray="3 3" stroke-width="1.5"/>
              <line x1="730" y1="25" x2="730" y2="390" stroke="#3b82f6" stroke-dasharray="3 3" stroke-width="1.5" stroke-opacity="0.6"/>

              <text x="80" y="18" text-anchor="middle" fill="#94a3b8" font-size="11" font-weight="bold">Polea (x = 0)</text>
              <text x="210" y="18" text-anchor="middle" fill="#10b981" font-size="11" font-weight="bold" id="svg-tp6-pos1">Apoyo 1 (x = 10 cm)</text>
              <text x="450" y="18" text-anchor="middle" fill="#94a3b8" font-size="11" font-weight="bold" id="svg-tp6-posgear">Engranaje (x = 30 cm)</text>
              <text x="730" y="18" text-anchor="middle" fill="#3b82f6" font-size="11" font-weight="bold" id="svg-tp6-pos2">Apoyo 2 (x = 55 cm)</text>

              <rect x="55" y="65" width="705" height="24" rx="4" fill="#334155" stroke="#64748b" stroke-width="2"/>
              <g id="tp6-stripes" fill="#94a3b8" opacity="0.4">
                <rect x="110" y="68" width="30" height="6" rx="2"/>
                <rect x="280" y="68" width="40" height="6" rx="2"/>
                <rect x="540" y="68" width="40" height="6" rx="2"/>
              </g>

              <rect x="66" y="30" width="28" height="94" rx="5" fill="#f59e0b" fill-opacity="0.2" stroke="#f59e0b" stroke-width="2.5"/>
              <text x="80" y="138" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="bold">Polea Motriz</text>

              <rect id="svg-b1-box" x="190" y="46" width="40" height="62" rx="6" fill="#10b981" fill-opacity="0.25" stroke="#10b981" stroke-width="2.5"/>
              <circle cx="202" cy="56" r="4" fill="#10b981"/><circle cx="218" cy="56" r="4" fill="#10b981"/>
              <circle cx="202" cy="98" r="4" fill="#10b981"/><circle cx="218" cy="98" r="4" fill="#10b981"/>
              <text x="210" y="125" text-anchor="middle" fill="#10b981" font-size="11" font-weight="bold" id="svg-lbl-b1">Apoyo 1 (* 6308)</text>

              <rect x="436" y="25" width="28" height="104" rx="4" fill="#ec4899" fill-opacity="0.2" stroke="#ec4899" stroke-width="2.5"/>
              <text x="450" y="143" text-anchor="middle" fill="#ec4899" font-size="11" font-weight="bold">Engranaje Impulsor</text>

              <rect id="svg-b2-box" x="712" y="50" width="36" height="54" rx="6" fill="#3b82f6" fill-opacity="0.25" stroke="#3b82f6" stroke-width="2.5"/>
              <circle cx="723" cy="59" r="3.5" fill="#3b82f6"/><circle cx="737" cy="59" r="3.5" fill="#3b82f6"/>
              <circle cx="723" cy="95" r="3.5" fill="#3b82f6"/><circle cx="737" cy="95" r="3.5" fill="#3b82f6"/>
              <text x="730" y="122" text-anchor="middle" fill="#3b82f6" font-size="11" font-weight="bold" id="svg-lbl-b2">Apoyo 2 (* 6206)</text>

              <!-- DCL PLANO X-Y -->
              <text x="15" y="180" fill="#cbd5e1" font-size="11" font-weight="bold">DCL PLANO x-y</text>
              <line x1="60" y1="215" x2="760" y2="215" stroke="#475569" stroke-width="2.5"/>
              <line x1="80" y1="165" x2="80" y2="210" stroke="#ef4444" stroke-width="3"/>
              <polygon points="74,205 86,205 80,215" fill="#ef4444"/>
              <text x="80" y="160" text-anchor="middle" fill="#ef4444" font-size="11" font-weight="bold" id="svg-ftp-val">Ftp = 227 kgf</text>
              <line x1="210" y1="265" x2="210" y2="220" stroke="#10b981" stroke-width="3"/>
              <polygon points="204,225 216,225 210,215" fill="#10b981"/>
              <text x="210" y="280" text-anchor="middle" fill="#10b981" font-size="11" font-weight="bold" id="svg-ray-val">RAy = 390 kgf</text>
              <line x1="450" y1="165" x2="450" y2="210" stroke="#ef4444" stroke-width="3"/>
              <polygon points="444,205 456,205 450,215" fill="#ef4444"/>
              <text x="450" y="160" text-anchor="middle" fill="#ef4444" font-size="11" font-weight="bold" id="svg-fte-val">Fte = 202 kgf</text>
              <line x1="730" y1="260" x2="730" y2="220" stroke="#3b82f6" stroke-width="3"/>
              <polygon points="724,225 736,225 730,215" fill="#3b82f6"/>
              <text x="730" y="275" text-anchor="middle" fill="#3b82f6" font-size="11" font-weight="bold" id="svg-rby-val">RBy = 39 kgf</text>

              <!-- DCL PLANO X-Z -->
              <text x="15" y="315" fill="#cbd5e1" font-size="11" font-weight="bold">DCL PLANO x-z</text>
              <line x1="60" y1="350" x2="760" y2="350" stroke="#475569" stroke-width="2.5"/>
              <line x1="80" y1="395" x2="80" y2="355" stroke="#ef4444" stroke-width="3"/>
              <polygon points="74,360 86,360 80,350" fill="#ef4444"/>
              <text x="80" y="412" text-anchor="middle" fill="#ef4444" font-size="11" font-weight="bold" id="svg-frp-val">Frp = 393 kgf</text>
              <line x1="210" y1="300" x2="210" y2="345" stroke="#10b981" stroke-width="3"/>
              <polygon points="204,340 216,340 210,350" fill="#10b981"/>
              <text x="210" y="295" text-anchor="middle" fill="#10b981" font-size="11" font-weight="bold" id="svg-raz-val">RAz = 521 kgf</text>
              <line x1="450" y1="390" x2="450" y2="355" stroke="#ef4444" stroke-width="3"/>
              <polygon points="444,360 456,360 450,350" fill="#ef4444"/>
              <text x="450" y="408" text-anchor="middle" fill="#ef4444" font-size="11" font-weight="bold" id="svg-fre-val">Fre = 73 kgf</text>
              <line x1="730" y1="390" x2="730" y2="355" stroke="#3b82f6" stroke-width="3"/>
              <polygon points="724,360 736,360 730,350" fill="#3b82f6"/>
              <text x="730" y="408" text-anchor="middle" fill="#3b82f6" font-size="11" font-weight="bold" id="svg-rbz-val">RBz = 55 kgf</text>
            </svg>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
            <div class="p-3 rounded-lg scada-card border-l-4 border-emerald-500">
              <div class="text-emerald-400 font-bold mb-1">APOYO 1 (d₁ = <span id="mem-d1">40</span> mm)</div>
              <div id="mem-fr1">Fr₁ = √(390² + 521²) = 650,80 kgf</div>
              <div id="mem-p1" class="font-bold text-slate-100">P₁ = Fr₁ · 0,00981 = 6,384 kN</div>
              <div id="mem-life1" class="mt-1 text-emerald-300">L₁₀ = (42,3 / 6,384)³ = 290,9 × 10⁶ rev → 2020 h</div>
            </div>

            <div class="p-3 rounded-lg scada-card border-l-4 border-blue-500">
              <div class="text-blue-400 font-bold mb-1">APOYO 2 (d₂ = <span id="mem-d2">30</span> mm)</div>
              <div id="mem-fr2">Fr₂ = √(39² + 55²) = 67,42 kgf</div>
              <div id="mem-p2" class="font-bold text-slate-100">P₂ = Fr₂ · 0,00981 = 0,6614 kN</div>
              <div id="mem-life2" class="mt-1 text-blue-300">L₁₀ = (20,3 / 0,6614)³ = 28.914 × 10⁶ rev → 200.758 h</div>
            </div>
          </div>
        </div>

        <!-- RIGHT: SIMULATION CONTROLS -->
        <div class="lg:col-span-4 scada-panel rounded-xl p-5 space-y-4 flex flex-col justify-between">
          <div>
            <div class="flex justify-between items-center mb-3">
              <h3 class="text-sm font-bold uppercase tracking-wider text-slate-200">Panel de Control TP 6</h3>
              <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">SQL Query Live</span>
            </div>

            <div class="space-y-3 text-xs">
              <div>
                <label class="text-slate-400 font-semibold block mb-1">Modo de Ingreso:</label>
                <select id="tp6-mode" onchange="onTP6ModeToggle()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-100 font-semibold">
                  <option value="direct">1. Ingreso Directo de Reacciones RA y RB</option>
                  <option value="static">2. Calcular Reacciones por Equilibrio (ΣM = 0)</option>
                </select>
              </div>

              <div>
                <label class="text-slate-400 font-semibold block mb-1">Velocidad del Eje n [rpm]:</label>
                <input type="number" id="tp6-rpm" value="2400" step="50" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold text-slate-100">
              </div>

              <!-- Static sub-panel -->
              <div id="tp6-static-sub" class="hidden p-3 rounded-lg bg-slate-950/80 border border-amber-500/30 space-y-2">
                <span class="text-[11px] font-bold text-amber-400 block">Cargas Externas y Cotas del Eje:</span>
                <div class="grid grid-cols-2 gap-2">
                  <div><span class="text-slate-400">Ftp (kgf)</span><input type="number" id="tp6-ftp" value="227" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded p-1 font-bold"></div>
                  <div><span class="text-slate-400">Frp (kgf)</span><input type="number" id="tp6-frp" value="393" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded p-1 font-bold"></div>
                  <div><span class="text-slate-400">Fte (kgf)</span><input type="number" id="tp6-fte" value="202" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded p-1 font-bold"></div>
                  <div><span class="text-slate-400">Fre (kgf)</span><input type="number" id="tp6-fre" value="73" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded p-1 font-bold"></div>
                </div>
                <div class="grid grid-cols-3 gap-1.5 pt-1 text-[11px]">
                  <div><span>L1 (cm)</span><input type="number" id="tp6-l1" value="10" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded p-1 font-bold"></div>
                  <div><span>L2 (cm)</span><input type="number" id="tp6-l2" value="20" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded p-1 font-bold"></div>
                  <div><span>L3 (cm)</span><input type="number" id="tp6-l3" value="25" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded p-1 font-bold"></div>
                </div>
              </div>

              <!-- Reactions fields -->
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="text-emerald-400 font-bold block mb-1">RAy [kgf]:</label>
                  <input type="number" id="tp6-ray" value="390" step="1" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
                <div>
                  <label class="text-emerald-400 font-bold block mb-1">RAz [kgf]:</label>
                  <input type="number" id="tp6-raz" value="521" step="1" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="text-blue-400 font-bold block mb-1">RBy [kgf]:</label>
                  <input type="number" id="tp6-rby" value="39" step="1" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
                <div>
                  <label class="text-blue-400 font-bold block mb-1">RBz [kgf]:</label>
                  <input type="number" id="tp6-rbz" value="55" step="1" oninput="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
              </div>

              <!-- Database selectors for d1 and d2 -->
              <div class="border-t border-slate-800 pt-3 space-y-2">
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <label class="text-emerald-400 font-bold">Diámetro Asiento d₁:</label>
                    <select id="sel-tp6-d1" onchange="onDiameterChange(1)" class="bg-slate-900 border border-slate-700 text-slate-100 rounded px-2 py-0.5 font-bold">
                      <option value="25">25 mm</option>
                      <option value="30">30 mm</option>
                      <option value="35">35 mm</option>
                      <option value="40" selected>40 mm (TP 6)</option>
                      <option value="45">45 mm</option>
                      <option value="50">50 mm</option>
                      <option value="55">55 mm</option>
                    </select>
                  </div>
                  <select id="sel-tp6-bearing1" onchange="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-100 font-mono text-[11px]"></select>
                </div>

                <div>
                  <div class="flex justify-between items-center mb-1">
                    <label class="text-blue-400 font-bold">Diámetro Asiento d₂:</label>
                    <select id="sel-tp6-d2" onchange="onDiameterChange(2)" class="bg-slate-900 border border-slate-700 text-slate-100 rounded px-2 py-0.5 font-bold">
                      <option value="25">25 mm</option>
                      <option value="30" selected>30 mm (TP 6)</option>
                      <option value="35">35 mm</option>
                      <option value="40">40 mm</option>
                      <option value="45">45 mm</option>
                      <option value="50">50 mm</option>
                      <option value="55">55 mm</option>
                    </select>
                  </div>
                  <select id="sel-tp6-bearing2" onchange="computeTP6()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-slate-100 font-mono text-[11px]"></select>
                </div>
              </div>
            </div>
          </div>

          <div class="pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex justify-between">
            <span>Base de datos: <strong class="text-slate-200">52 rodamientos SKF</strong></span>
            <span class="text-emerald-400 font-semibold">Query SQL OK</span>
          </div>
        </div>

      </div>

      <!-- SQL TABLE FOR ACTIVE DIAMETERS -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="scada-panel rounded-xl p-4 space-y-2">
          <div class="flex justify-between items-center">
            <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Catálogo SKF • Opciones para Apoyo 1 (d = <span id="tbl-lbl-d1">40</span> mm)</h4>
            <span class="text-[11px] text-slate-400">Click en fila para elegir</span>
          </div>
          <div class="overflow-x-auto max-h-56">
            <table class="w-full text-left text-xs font-mono border-collapse">
              <thead class="bg-slate-900/80 sticky top-0 text-slate-400">
                <tr>
                  <th class="p-2">Designación</th><th>D [mm]</th><th>B [mm]</th><th>C [kN]</th><th>C0 [kN]</th><th>L10h [h]</th>
                </tr>
              </thead>
              <tbody id="tbody-tp6-d1" class="divide-y divide-slate-800"></tbody>
            </table>
          </div>
        </div>

        <div class="scada-panel rounded-xl p-4 space-y-2">
          <div class="flex justify-between items-center">
            <h4 class="text-xs font-bold text-blue-400 uppercase tracking-wider">Catálogo SKF • Opciones para Apoyo 2 (d = <span id="tbl-lbl-d2">30</span> mm)</h4>
            <span class="text-[11px] text-slate-400">Click en fila para elegir</span>
          </div>
          <div class="overflow-x-auto max-h-56">
            <table class="w-full text-left text-xs font-mono border-collapse">
              <thead class="bg-slate-900/80 sticky top-0 text-slate-400">
                <tr>
                  <th class="p-2">Designación</th><th>D [mm]</th><th>B [mm]</th><th>C [kN]</th><th>C0 [kN]</th><th>L10h [h]</th>
                </tr>
              </thead>
              <tbody id="tbody-tp6-d2" class="divide-y divide-slate-800"></tbody>
            </table>
          </div>
        </div>
      </div>

    </div>

    <!-- VIEW: TP 7 - CORREAS SKF -->
    <div id="view-tp7" class="space-y-6 hidden">
      
      <!-- KPIs STRIP TP7 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>POTENCIA DE DISEÑO</span>
            <span class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono font-bold" id="kpi-tp7-c2">C₂ = 1,300</span>
          </div>
          <div class="text-2xl font-black text-amber-400 mt-1" id="kpi-tp7-pd">72,71 kW</div>
          <div class="text-xs text-slate-400 mt-1">
            Motor: <span class="text-slate-200 font-semibold" id="kpi-tp7-pr">75 HP (55,93 kW)</span>
          </div>
        </div>

        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>PERFIL SELECCIONADO</span>
            <span class="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono font-bold">DIAGRAMA 2</span>
          </div>
          <div class="text-2xl font-black text-cyan-400 mt-1" id="kpi-tp7-perfil">SECCIÓN SPB-XP</div>
          <div class="text-xs text-slate-400 mt-1">
            Dimensiones: <span class="text-slate-200 font-semibold" id="kpi-tp7-profdim">bo=16,3 | h=13 mm</span>
          </div>
        </div>

        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>CINEMÁTICA Y ARCO</span>
            <span class="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 font-mono font-bold" id="kpi-tp7-arc">β = 174°</span>
          </div>
          <div class="text-2xl font-black text-slate-100 mt-1" id="kpi-tp7-v">24,30 m/s</div>
          <div class="text-xs text-slate-400 mt-1">
            Factor Arco: <span class="text-purple-400 font-semibold" id="kpi-tp7-c3">C₃ = 0,99</span>
          </div>
        </div>

        <div class="scada-panel rounded-xl p-4">
          <div class="flex justify-between items-center text-xs text-slate-400">
            <span>SOLUCIÓN FINAL DE TRANSMISIÓN</span>
            <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono font-bold">CUMPLE</span>
          </div>
          <div class="text-2xl font-black text-emerald-400 mt-1" id="kpi-tp7-belts">4 × PHG SPB2180XP</div>
          <div class="text-xs text-slate-400 mt-1">
            Pot. Admisible: <span class="text-emerald-300 font-semibold" id="kpi-tp7-padm">19,81 kW/correa</span>
          </div>
        </div>
      </div>

      <!-- MAIN TP7 WORKSPACE -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- LEFT: DYNAMIC BELT SYNOPTIC -->
        <div class="lg:col-span-8 scada-panel rounded-xl p-5 space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div>
              <span class="text-[11px] font-bold uppercase tracking-wider text-amber-400">Simulador Cinemático de Correas Trapeciales</span>
              <h2 class="text-base font-bold text-slate-100" id="tp7-synoptic-head">Motor (1450 rpm, D=320 mm) → Bomba (1856 rpm, d=250 mm)</h2>
            </div>
            <div class="flex items-center gap-2 font-mono text-xs">
              <span class="px-2 py-1 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold" id="tp7-badge-ir">Ir = 1,28 (Multiplicador)</span>
            </div>
          </div>

          <div class="bg-slate-950/70 rounded-xl border border-slate-800 p-3 overflow-x-auto">
            <svg id="svg-tp7" viewBox="0 0 840 340" class="w-full min-w-[620px] h-auto">
              <line x1="80" y1="160" x2="760" y2="160" stroke="#334155" stroke-dasharray="6 4" stroke-width="1.5"/>

              <path d="M 200 66 L 580 88 A 72 72 0 0 1 580 232 L 200 254 A 94 94 0 0 1 200 66 Z"
                    fill="none" stroke="#f59e0b" stroke-width="9" stroke-opacity="0.35"/>
              <path id="tp7-belt-dash"
                    d="M 200 66 L 580 88 A 72 72 0 0 1 580 232 L 200 254 A 94 94 0 0 1 200 66 Z"
                    fill="none" stroke="#f59e0b" stroke-width="4" stroke-dasharray="15 10"/>

              <circle cx="200" cy="160" r="94" fill="#1e293b" stroke="#10b981" stroke-width="3.5"/>
              <circle cx="200" cy="160" r="76" fill="none" stroke="#10b981" stroke-width="1" stroke-dasharray="4 3"/>
              <g id="tp7-spokes-driver" transform="rotate(0 200 160)">
                <line x1="200" y1="70" x2="200" y2="250" stroke="#10b981" stroke-width="3" stroke-opacity="0.6"/>
                <line x1="110" y1="160" x2="290" y2="160" stroke="#10b981" stroke-width="3" stroke-opacity="0.6"/>
                <line x1="136" y1="96" x2="264" y2="224" stroke="#10b981" stroke-width="2" stroke-opacity="0.4"/>
                <line x1="264" y1="96" x2="136" y2="224" stroke="#10b981" stroke-width="2" stroke-opacity="0.4"/>
              </g>
              <circle cx="200" cy="160" r="16" fill="#10b981"/>
              <text x="200" y="45" text-anchor="middle" fill="#10b981" font-size="12" font-weight="bold">POLEA CONDUCTORA (MOTOR)</text>
              <text x="200" y="278" text-anchor="middle" fill="#e2e8f0" font-size="11" font-weight="bold" id="svg-tp7-motordesc">D = 320 mm • 1450 rpm</text>

              <path d="M 576 83 A 77 77 0 0 1 576 237" fill="none" stroke="#3b82f6" stroke-width="6" stroke-linecap="round"/>
              <text x="675" y="155" fill="#3b82f6" font-size="12" font-weight="bold" id="svg-tp7-arclbl">Arco β = 174°</text>
              <text x="675" y="172" fill="#94a3b8" font-size="11" id="svg-tp7-c3lbl">(C₃ = 0,99)</text>

              <circle cx="580" cy="160" r="72" fill="#1e293b" stroke="#3b82f6" stroke-width="3.5"/>
              <circle cx="580" cy="160" r="55" fill="none" stroke="#3b82f6" stroke-width="1" stroke-dasharray="4 3"/>
              <g id="tp7-spokes-driven" transform="rotate(0 580 160)">
                <line x1="580" y1="92" x2="580" y2="228" stroke="#3b82f6" stroke-width="3" stroke-opacity="0.6"/>
                <line x1="512" y1="160" x2="648" y2="160" stroke="#3b82f6" stroke-width="3" stroke-opacity="0.6"/>
                <line x1="532" y1="112" x2="628" y2="208" stroke="#3b82f6" stroke-width="2" stroke-opacity="0.4"/>
                <line x1="628" y1="112" x2="532" y2="208" stroke="#3b82f6" stroke-width="2" stroke-opacity="0.4"/>
              </g>
              <circle cx="580" cy="160" r="14" fill="#3b82f6"/>
              <text x="580" y="65" text-anchor="middle" fill="#3b82f6" font-size="12" font-weight="bold">POLEA CONDUCIDA</text>
              <text x="580" y="278" text-anchor="middle" fill="#e2e8f0" font-size="11" font-weight="bold" id="svg-tp7-drivenpulley">d = 250 mm • 1856 rpm</text>

              <line x1="200" y1="315" x2="580" y2="315" stroke="#f59e0b" stroke-width="2"/>
              <polygon points="200,315 210,310 210,320" fill="#f59e0b"/>
              <polygon points="580,315 570,310 570,320" fill="#f59e0b"/>
              <text x="390" y="308" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="bold" id="svg-tp7-cctext">
                CC preliminar = 650 mm → CC definitivo = 641,6 mm (PHG SPB2180)
              </text>

              <rect x="320" y="132" width="140" height="52" rx="8" fill="#020617" fill-opacity="0.9" stroke="#f59e0b" stroke-width="1.5"/>
              <text x="390" y="152" text-anchor="middle" fill="#f59e0b" font-size="12" font-weight="bold" id="svg-tp7-vtag">v = 24,30 m/s</text>
              <text x="390" y="171" text-anchor="middle" fill="#10b981" font-size="11" font-weight="bold" id="svg-tp7-beltstag">4 × SPB2180</text>
            </svg>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
            <div class="p-3 rounded-lg scada-card border-t-2 border-amber-500">
              <div class="text-amber-400 font-bold mb-1">1. POTENCIA Y C₂</div>
              <div id="step-pr">Pr = 75 HP (55,93 kW)</div>
              <div id="step-c2">C₂ = 1,30 (Directo Tabla 3)</div>
              <div id="step-pd" class="font-bold text-slate-100">Pd = 72,71 kW</div>
            </div>

            <div class="p-3 rounded-lg scada-card border-t-2 border-cyan-500">
              <div class="text-cyan-400 font-bold mb-1">2 y 3. PERFIL Y CC</div>
              <div id="step-perfil">Perfil SPB (bo=16,3)</div>
              <div id="step-ld">Ld = 2196,8 → 2180 mm</div>
              <div id="step-cc" class="font-bold text-slate-100">CC def = 641,6 mm</div>
            </div>

            <div class="p-3 rounded-lg scada-card border-t-2 border-emerald-500">
              <div class="text-emerald-400 font-bold mb-1">4, 5 y 6. CAPACIDAD Y N</div>
              <div id="step-pb">Pb = 20,89 + 0,87 = 21,75 kW</div>
              <div id="step-padm">Padm = 21,75·0,92·0,99 = 19,81 kW</div>
              <div id="step-nbelts" class="font-bold text-emerald-300">N = 72,71 / 19,81 = 3,67 ⇒ 4</div>
            </div>
          </div>

          <!-- DIAGRAMA 2 SKF: INTERACTIVE CHART & SCAN -->
          <div class="scada-card rounded-xl p-4 border border-cyan-500/30">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></span>
                <h4 class="text-xs font-bold uppercase tracking-wider text-cyan-300">
                  Diagrama 2 SKF — Selección del Perfil de Correas (Wedge Belts)
                </h4>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 font-mono font-bold" id="diag2-badge-point">
                  Pto Operación: Pd = 72,71 kW @ 1856 rpm ➜ SPB-XP
                </span>
                <button type="button" onclick="toggleDiagramScan()" class="text-[11px] text-amber-400 hover:text-amber-300 underline font-semibold cursor-pointer">
                  [Ver Escaneo Catálogo SKF]
                </button>
              </div>
            </div>

            <!-- SVG DIAGRAM 2 LOG-LOG -->
            <div class="bg-slate-950/90 rounded-lg p-2 border border-slate-800 overflow-x-auto">
              <svg id="svg-diag2" viewBox="0 0 660 300" class="w-full min-w-[580px] h-auto font-mono text-[10px]">
                <rect x="70" y="25" width="530" height="205" fill="#090d16" stroke="#334155" stroke-width="1.5"/>
                
                <!-- Grid Horizontal Lines -->
                <line x1="70" y1="230" x2="600" y2="230" stroke="#1e293b" stroke-width="1"/>
                <line x1="70" y1="199" x2="600" y2="199" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="70" y1="158" x2="600" y2="158" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="70" y1="127.5" x2="600" y2="127.5" stroke="#334155" stroke-width="1.2"/>
                <line x1="70" y1="96.6" x2="600" y2="96.6" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="70" y1="55.8" x2="600" y2="55.8" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="70" y1="40.9" x2="600" y2="40.9" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4 2"/>
                <line x1="70" y1="25" x2="600" y2="25" stroke="#334155" stroke-width="1"/>

                <!-- Grid Vertical Lines -->
                <line x1="70" y1="25" x2="70" y2="230" stroke="#334155" stroke-width="1.2"/>
                <line x1="246.7" y1="25" x2="246.7" y2="230" stroke="#334155" stroke-width="1.2"/>
                <line x1="423.3" y1="25" x2="423.3" y2="230" stroke="#334155" stroke-width="1.2"/>
                <line x1="600" y1="25" x2="600" y2="230" stroke="#334155" stroke-width="1.2"/>

                <!-- Intermediate Log Lines -->
                <line x1="123" y1="25" x2="123" y2="230" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="193" y1="25" x2="193" y2="230" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="300" y1="25" x2="300" y2="230" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="370" y1="25" x2="370" y2="230" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="476" y1="25" x2="476" y2="230" stroke="#1e293b" stroke-dasharray="2 3"/>
                <line x1="547" y1="25" x2="547" y2="230" stroke="#1e293b" stroke-dasharray="2 3"/>

                <!-- Zone 1: SPZ, XPZ, SPZ-XP -->
                <polygon points="70,230 70,41 370,41 70,230" fill="#38bdf8" fill-opacity="0.12" stroke="#38bdf8" stroke-width="1.5"/>
                
                <!-- Zone 2: SPA, XPA, SPA-XP -->
                <polygon points="70,230 370,41 573,41 573,86 431,86 185,230" fill="#818cf8" fill-opacity="0.15" stroke="#818cf8" stroke-width="1.5"/>

                <!-- Zone 3: SPB, XPB, SPB-XP (ACTIVE ZONE) -->
                <polygon points="185,230 431,86 573,86 573,155 507,155 261,230" fill="#10b981" fill-opacity="0.25" stroke="#10b981" stroke-width="2"/>

                <!-- Zone 4: SPC, XPC, SPC-XP -->
                <polygon points="261,230 507,155 573,155 573,230" fill="#a855f7" fill-opacity="0.12" stroke="#a855f7" stroke-width="1.5"/>

                <!-- Zone Labels -->
                <text x="135" y="110" fill="#38bdf8" font-size="10" font-weight="bold">SPZ, XPZ, SPZ-XP</text>
                <text x="260" y="145" fill="#818cf8" font-size="10" font-weight="bold">SPA, XPA, SPA-XP</text>
                <text x="390" y="165" fill="#10b981" font-size="11" font-weight="900">SPB, XPB, SPB-XP ★</text>
                <text x="495" y="215" fill="#a855f7" font-size="10" font-weight="bold">SPC, XPC, SPC-XP</text>

                <!-- Axis Numbers -->
                <text x="70" y="246" text-anchor="middle" fill="#94a3b8">1</text>
                <text x="246.7" y="246" text-anchor="middle" fill="#94a3b8">10</text>
                <text x="423.3" y="246" text-anchor="middle" fill="#94a3b8">100</text>
                <text x="600" y="246" text-anchor="middle" fill="#94a3b8">1 000</text>
                <text x="335" y="265" text-anchor="middle" fill="#cbd5e1" font-size="11" font-weight="bold">Potencia de diseño Pd [kW]</text>

                <text x="62" y="233" text-anchor="end" fill="#94a3b8">100</text>
                <text x="62" y="131" text-anchor="end" fill="#94a3b8">1 000</text>
                <text x="62" y="44" text-anchor="end" fill="#38bdf8" font-weight="bold">7 000</text>
                <text x="62" y="28" text-anchor="end" fill="#94a3b8">10 000</text>
                <text x="20" y="130" text-anchor="middle" fill="#cbd5e1" font-size="11" font-weight="bold" transform="rotate(-90 20 130)">Velocidad polea menor [r/min]</text>

                <!-- Operating Point Dynamic Crosshairs and Pin -->
                <g id="diag2-target" transform="translate(399, 100)">
                  <line x1="-399" y1="0" x2="201" y2="0" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="3 3"/>
                  <line x1="0" y1="-100" x2="0" y2="130" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="3 3"/>
                  <circle r="12" fill="#f59e0b" fill-opacity="0.3" class="animate-ping"/>
                  <circle r="5" fill="#f59e0b" stroke="#ffffff" stroke-width="1.5"/>
                  <rect x="10" y="-22" width="180" height="20" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1.2"/>
                  <text id="diag2-target-text" x="16" y="-8" fill="#fef08a" font-size="9" font-weight="bold">72,7 kW @ 1856 rpm ➜ SPB-XP</text>
                </g>
              </svg>
            </div>

            <!-- TOGGLEABLE SCAN VIEW -->
            <div id="diag2-scan-view" class="hidden mt-3 p-3 bg-slate-900/90 rounded-lg border border-slate-700">
              <div class="flex justify-between items-center text-xs text-slate-300 font-semibold mb-2">
                <span>Facsímil Oficial de Catálogo SKF — Página 17 (Diagram 2: Wedge belts)</span>
                <button type="button" onclick="toggleDiagramScan()" class="text-slate-400 hover:text-white px-2 py-0.5 rounded bg-slate-800">Cerrar ✕</button>
              </div>
              <div class="relative bg-white/5 rounded-lg p-2 flex justify-center">
                <img src="diagrama2_skf.png" alt="Diagrama 2 SKF Oficial" class="max-h-80 w-auto rounded border border-slate-800 shadow-xl">
              </div>
              <p class="text-[11px] text-slate-400 mt-2">
                El Diagrama 2 clasifica las correas trapeciales estrechas (Wedge belts) en 4 familias: SPZ, SPA, SPB y SPC (y sus variantes reforzadas <strong>SPB-XP Extra Power</strong>). Con Pd = 72,71 kW y n = 1856 rpm, el punto de trabajo se sitúa exactamente en el centro de la zona <strong>SPB, XPB, SPB-XP</strong>.
              </p>
            </div>
          </div>
        </div>

        <!-- RIGHT: SIMULATOR CONTROLS -->
        <div class="lg:col-span-4 scada-panel rounded-xl p-5 space-y-4">
          <div>
            <div class="flex justify-between items-center mb-3">
              <h3 class="text-sm font-bold uppercase tracking-wider text-slate-200">Panel de Control TP 7</h3>
              <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">Auto-Solver SKF</span>
            </div>

            <div class="space-y-3 text-xs">
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="text-slate-400 font-semibold block mb-1">Potencia Motor [HP]:</label>
                  <input type="number" id="tp7-hp" value="75" step="1" oninput="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold text-slate-100">
                </div>
                <div>
                  <label class="text-slate-400 font-semibold block mb-1">CC Preliminar [mm]:</label>
                  <input type="number" id="tp7-ccp" value="650" step="10" oninput="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold text-slate-100">
                </div>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="text-emerald-400 font-bold block mb-1">D Motor [mm]:</label>
                  <input type="number" id="tp7-D" value="320" step="5" oninput="onPulleyChange('D')" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
                <div>
                  <label class="text-blue-400 font-bold block mb-1">d Conducida [mm]:</label>
                  <input type="number" id="tp7-d" value="250" step="5" oninput="onPulleyChange('d')" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="text-emerald-400 font-bold block mb-1">n₁ Motor [rpm]:</label>
                  <input type="number" id="tp7-n1" value="1450" step="10" oninput="onPulleyChange('n1')" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
                <div>
                  <label class="text-blue-400 font-bold block mb-1">n₂ Conducida [rpm]:</label>
                  <input type="number" id="tp7-n2" value="1856" step="10" oninput="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold">
                </div>
              </div>

              <div class="grid grid-cols-3 gap-1.5 pt-1">
                <div>
                  <label class="text-slate-400 block mb-1 text-[11px]">Clase (Tabla 2):</label>
                  <select id="tp7-clase" onchange="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-slate-100 font-semibold">
                    <option value="1" selected>Clase 1 (Ligero)</option>
                    <option value="2">Clase 2 (Medio)</option>
                    <option value="3">Clase 3 (Pesado)</option>
                    <option value="4">Clase 4 (Extra)</option>
                  </select>
                </div>
                <div>
                  <label class="text-slate-400 block mb-1 text-[11px]">Arranque (Tabla 3):</label>
                  <select id="tp7-arranque" onchange="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-slate-100 font-semibold">
                    <option value="heavy" selected>Heavy starts (Directo)</option>
                    <option value="normal">Soft starts (Suave)</option>
                  </select>
                </div>
                <div>
                  <label class="text-slate-400 block mb-1 text-[11px]">Horas/día:</label>
                  <select id="tp7-horas" onchange="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded p-1.5 text-slate-100 font-semibold">
                    <option value="lt10">&lt; 10 h</option>
                    <option value="10to16">10-16 h</option>
                    <option value="gt16" selected>&gt; 16 h (20h)</option>
                  </select>
                </div>
              </div>

              <!-- MULTIPLICADOR VELOCIDAD TOGGLE -->
              <div class="mt-2 flex items-center justify-between p-2 rounded bg-slate-900/60 border border-slate-800">
                <label class="text-[11px] text-slate-300 flex items-center gap-2 cursor-pointer select-none">
                  <input type="checkbox" id="tp7-chk-mult" onchange="computeTP7()" class="w-4 h-4 rounded border-slate-700 text-amber-500">
                  <span>Factor multiplicador Tabla 1 (i<sub>r</sub> &gt; 1): <strong>+0,05</strong></span>
                </label>
                <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono" id="tp7-badge-mult">Desactivado (1,0)</span>
              </div>

              <div class="grid grid-cols-2 gap-2 pt-1">
                <div>
                  <label class="text-amber-400 font-bold block mb-1">Perfil SKF:</label>
                  <select id="tp7-profsel" onchange="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-bold text-slate-100">
                    <option value="AUTO" selected>Auto (Diag. 2: SPB-XP)</option>
                    <option value="SPB-XP">SPB-XP (Extra Power)</option>
                    <option value="SPZ">SPZ</option>
                    <option value="SPA">SPA</option>
                    <option value="SPB">SPB</option>
                    <option value="SPC">SPC</option>
                  </select>
                </div>
                <div>
                  <label class="text-amber-400 font-bold block mb-1">Longitud Comercial:</label>
                  <select id="tp7-lensel" onchange="computeTP7()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 font-semibold text-slate-100">
                    <option value="AUTO">Automática (Próxima)</option>
                    <option value="1800">1800 mm</option>
                    <option value="2000">2000 mm</option>
                    <option value="2150">2150 mm</option>
                    <option value="2180" selected>2180 mm (TP 7)</option>
                    <option value="2240">2240 mm (ISO Sup)</option>
                    <option value="2360">2360 mm</option>
                    <option value="2500">2500 mm</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <div class="pt-3 border-t border-slate-800 space-y-1 text-[11px]">
            <div class="flex justify-between">
              <span class="text-slate-400">Rango CC admisible:</span>
              <span class="text-emerald-400 font-semibold" id="tp7-chk-ccp">399 a 1140 mm (Cumple ✓)</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Diámetro mín. polea:</span>
              <span class="text-emerald-400 font-semibold" id="tp7-chk-dmin">140 mm ≤ 250 mm (Cumple ✓)</span>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- VIEW: SQL DATABASE EXPLORER -->
    <div id="view-db" class="space-y-6 hidden">
      <div class="scada-panel rounded-xl p-5 space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <span class="text-xs font-bold uppercase tracking-wider text-cyan-400">Explorador Relacional SQL</span>
            <h2 class="text-lg font-bold text-slate-100">Base de Datos de Catálogos Oficiales SKF (`skf_catalog.db`)</h2>
            <p class="text-xs text-slate-400">Consulta directa de tablas cargadas para rodamientos de bolas, correas trapeciales, factores de servicio e interpolaciones.</p>
          </div>
          
          <div class="flex items-center gap-2">
            <label class="text-xs text-slate-300 font-semibold">Seleccionar Tabla:</label>
            <select id="sel-dbtable" onchange="renderDatabaseTable()" class="bg-slate-900 border border-slate-700 text-slate-100 rounded-lg p-2 text-xs font-bold cursor-pointer">
              <option value="rodamientos_bolas">rodamientos_bolas (52 filas)</option>
              <option value="correas_servicio_c2">correas_servicio_c2 (24 filas)</option>
              <option value="correas_longitudes_c1">correas_longitudes_c1 (17 filas)</option>
              <option value="correas_arco_c3">correas_arco_c3 (11 filas)</option>
              <option value="correas_perfiles">correas_perfiles (4 filas)</option>
              <option value="correas_potencia_basica">correas_potencia_basica (20 filas)</option>
              <option value="correas_multiplicador_ir">correas_multiplicador_ir (15 filas)</option>
            </select>
          </div>
        </div>

        <div class="bg-slate-950/80 rounded-xl border border-slate-800 overflow-x-auto max-h-[500px]">
          <table id="db-table-display" class="w-full text-left text-xs font-mono border-collapse">
            <thead class="bg-slate-900 sticky top-0 text-cyan-400">
              <tr id="db-thead-row"></tr>
            </thead>
            <tbody id="db-tbody" class="divide-y divide-slate-800"></tbody>
          </table>
        </div>
      </div>
    </div>

  </main>

  <script>
    const SKF_DATABASE = """ + db_json_str + """;

    function fmt(n, dec=2) {
      return Number(n).toLocaleString("es-AR", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    }

    function switchTab(t) {
      ["tp6", "tp7", "db"].forEach(id => {
        document.getElementById("view-" + id).classList.toggle("hidden", id !== t);
        const btn = document.getElementById("tab-btn-" + id);
        if (id === t) {
          btn.className = "px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-lg cursor-pointer";
        } else {
          btn.className = "px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800 cursor-pointer";
        }
      });
      if (t === "db") renderDatabaseTable();
    }

    function onTP6ModeToggle() {
      const mode = document.getElementById("tp6-mode").value;
      document.getElementById("tp6-static-sub").classList.toggle("hidden", mode !== "static");
      ["tp6-ray", "tp6-raz", "tp6-rby", "tp6-rbz"].forEach(id => {
        document.getElementById(id).readOnly = (mode === "static");
      });
      computeTP6();
    }

    function populateBearingSelect(supportIdx, defDesig) {
      const d = parseFloat(document.getElementById("sel-tp6-d" + supportIdx).value);
      const sel = document.getElementById("sel-tp6-bearing" + supportIdx);
      const rows = SKF_DATABASE.rodamientos_bolas.filter(r => r.d_int === d).sort((a,b) => a.C_din - b.C_din);
      sel.innerHTML = rows.map(r => 
        `<option value="${r.designacion}" ${r.designacion === defDesig ? 'selected' : ''}>${r.designacion} (C=${r.C_din} kN, D=${r.D_ext}, B=${r.B_ancho})</option>`
      ).join("");
      if (!defDesig && rows.length > 0) {
        sel.selectedIndex = Math.min(rows.length - 2, rows.length - 1);
      }
    }

    function onDiameterChange(supportIdx) {
      populateBearingSelect(supportIdx, null);
      computeTP6();
    }

    function computeTP6() {
      const mode = document.getElementById("tp6-mode").value;
      const n = parseFloat(document.getElementById("tp6-rpm").value) || 2400;
      document.getElementById("lbl-tp6-rpm").textContent = n;

      if (mode === "static") {
        const ftp = parseFloat(document.getElementById("tp6-ftp").value) || 0;
        const frp = parseFloat(document.getElementById("tp6-frp").value) || 0;
        const fte = parseFloat(document.getElementById("tp6-fte").value) || 0;
        const fre = parseFloat(document.getElementById("tp6-fre").value) || 0;
        const l1 = parseFloat(document.getElementById("tp6-l1").value) || 10;
        const l2 = parseFloat(document.getElementById("tp6-l2").value) || 20;
        const l3 = parseFloat(document.getElementById("tp6-l3").value) || 25;
        const span = l2 + l3;

        const rayCalc = Math.round((ftp * (l1 + span) + fte * l3) / span);
        const rbyCalc = Math.round(Math.abs(ftp + fte - rayCalc));
        const razCalc = Math.round((frp * (l1 + span) + fre * l3) / span);
        const rbzCalc = Math.round(Math.abs(razCalc - frp - fre));

        document.getElementById("tp6-ray").value = rayCalc;
        document.getElementById("tp6-raz").value = razCalc;
        document.getElementById("tp6-rby").value = rbyCalc;
        document.getElementById("tp6-rbz").value = rbzCalc;

        document.getElementById("svg-tp6-pos1").textContent = `Apoyo 1 (x = ${l1} cm)`;
        document.getElementById("svg-tp6-posgear").textContent = `Engranaje (x = ${l1+l2} cm)`;
        document.getElementById("svg-tp6-pos2").textContent = `Apoyo 2 (x = ${l1+span} cm)`;
      }

      const ray = parseFloat(document.getElementById("tp6-ray").value) || 0;
      const raz = parseFloat(document.getElementById("tp6-raz").value) || 0;
      const rby = parseFloat(document.getElementById("tp6-rby").value) || 0;
      const rbz = parseFloat(document.getElementById("tp6-rbz").value) || 0;

      const fr1 = Math.sqrt(ray*ray + raz*raz);
      const fr2 = Math.sqrt(rby*rby + rbz*rbz);
      const p1 = (fr1 * 9.81) / 1000.0;
      const p2 = (fr2 * 9.81) / 1000.0;

      const d1 = parseFloat(document.getElementById("sel-tp6-d1").value);
      const d2 = parseFloat(document.getElementById("sel-tp6-d2").value);

      const rows1 = SKF_DATABASE.rodamientos_bolas.filter(r => r.d_int === d1).sort((a,b) => a.C_din - b.C_din);
      const rows2 = SKF_DATABASE.rodamientos_bolas.filter(r => r.d_int === d2).sort((a,b) => a.C_din - b.C_din);

      const desig1 = document.getElementById("sel-tp6-bearing1").value || (rows1[rows1.length-2] || rows1[0]).designacion;
      const desig2 = document.getElementById("sel-tp6-bearing2").value || (rows2[4] || rows2[0]).designacion;

      const b1 = rows1.find(r => r.designacion === desig1) || rows1[0];
      const b2 = rows2.find(r => r.designacion === desig2) || rows2[0];

      const l10_1 = Math.pow(b1.C_din / Math.max(p1, 0.001), 3);
      const l10h_1 = (1000000 / (60 * n)) * l10_1;

      const l10_2 = Math.pow(b2.C_din / Math.max(p2, 0.001), 3);
      const l10h_2 = (1000000 / (60 * n)) * l10_2;

      document.getElementById("kpi-tp6-d1").textContent = `d₁ = ${d1} mm`;
      document.getElementById("kpi-tp6-p1").textContent = `${fmt(p1, 3)} kN`;
      document.getElementById("kpi-tp6-fr1").textContent = `${fmt(fr1, 2)} kgf`;
      document.getElementById("kpi-tp6-desig1").textContent = b1.designacion;
      document.getElementById("kpi-tp6-l10h1").textContent = `${fmt(l10h_1, 0)} h`;
      document.getElementById("kpi-tp6-c1").textContent = `C = ${fmt(b1.C_din, 1)} kN`;

      document.getElementById("kpi-tp6-d2").textContent = `d₂ = ${d2} mm`;
      document.getElementById("kpi-tp6-p2").textContent = `${fmt(p2, 4)} kN`;
      document.getElementById("kpi-tp6-fr2").textContent = `${fmt(fr2, 2)} kgf`;
      document.getElementById("kpi-tp6-desig2").textContent = b2.designacion;
      document.getElementById("kpi-tp6-l10h2").textContent = `${fmt(l10h_2, 0)} h`;
      document.getElementById("kpi-tp6-c2").textContent = `C = ${fmt(b2.C_din, 1)} kN`;

      document.getElementById("svg-ray-val").textContent = `RAy = ${ray} kgf`;
      document.getElementById("svg-raz-val").textContent = `RAz = ${raz} kgf`;
      document.getElementById("svg-rby-val").textContent = `RBy = ${rby} kgf`;
      document.getElementById("svg-rbz-val").textContent = `RBz = ${rbz} kgf`;
      document.getElementById("svg-lbl-b1").textContent = `${b1.designacion} (d=${d1})`;
      document.getElementById("svg-lbl-b2").textContent = `${b2.designacion} (d=${d2})`;

      document.getElementById("mem-d1").textContent = d1;
      document.getElementById("mem-fr1").textContent = `Fr₁ = √(${ray}² + ${raz}²) = ${fmt(fr1, 2)} kgf`;
      document.getElementById("mem-p1").textContent = `P₁ = ${fmt(fr1, 2)} · 0,00981 = ${fmt(p1, 3)} kN`;
      document.getElementById("mem-life1").textContent = `L₁₀ = (${b1.C_din} / ${fmt(p1,3)})³ = ${fmt(l10_1,1)} × 10⁶ rev → ${fmt(l10h_1,1)} h`;

      document.getElementById("mem-d2").textContent = d2;
      document.getElementById("mem-fr2").textContent = `Fr₂ = √(${rby}² + ${rbz}²) = ${fmt(fr2, 2)} kgf`;
      document.getElementById("mem-p2").textContent = `P₂ = ${fmt(fr2, 2)} · 0,00981 = ${fmt(p2, 4)} kN`;
      document.getElementById("mem-life2").textContent = `L₁₀ = (${b2.C_din} / ${fmt(p2,4)})³ = ${fmt(l10_2,0)} × 10⁶ rev → ${fmt(l10h_2,0)} h`;

      document.getElementById("tbl-lbl-d1").textContent = d1;
      document.getElementById("tbody-tp6-d1").innerHTML = rows1.map(r => {
        const l = Math.pow(r.C_din / Math.max(p1, 0.001), 3);
        const lh = (1000000 / (60 * n)) * l;
        const sel = r.designacion === b1.designacion;
        return `<tr onclick="selectB(1, '${r.designacion}')" class="cursor-pointer hover:bg-slate-800/80 ${sel ? 'active-row' : ''}">
          <td class="p-2 font-bold">${r.designacion}</td><td>${r.D_ext}</td><td>${r.B_ancho}</td><td>${r.C_din}</td><td>${r.C0_est}</td><td class="text-emerald-400 font-bold">${fmt(lh, 0)} h</td>
        </tr>`;
      }).join("");

      document.getElementById("tbl-lbl-d2").textContent = d2;
      document.getElementById("tbody-tp6-d2").innerHTML = rows2.map(r => {
        const l = Math.pow(r.C_din / Math.max(p2, 0.001), 3);
        const lh = (1000000 / (60 * n)) * l;
        const sel = r.designacion === b2.designacion;
        return `<tr onclick="selectB(2, '${r.designacion}')" class="cursor-pointer hover:bg-slate-800/80 ${sel ? 'active-row' : ''}">
          <td class="p-2 font-bold">${r.designacion}</td><td>${r.D_ext}</td><td>${r.B_ancho}</td><td>${r.C_din}</td><td>${r.C0_est}</td><td class="text-blue-400 font-bold">${fmt(lh, 0)} h</td>
        </tr>`;
      }).join("");
    }

    function selectB(supportIdx, desig) {
      document.getElementById("sel-tp6-bearing" + supportIdx).value = desig;
      computeTP6();
    }

    function onPulleyChange(field) {
      const D = parseFloat(document.getElementById("tp7-D").value) || 320;
      const d = parseFloat(document.getElementById("tp7-d").value) || 250;
      const n1 = parseFloat(document.getElementById("tp7-n1").value) || 1450;
      if (field === "D" || field === "d" || field === "n1") {
        const n2 = Math.round((n1 * D) / Math.max(d, 1));
        document.getElementById("tp7-n2").value = n2;
      }
      computeTP7();
    }

    function computeTP7() {
      const hp = parseFloat(document.getElementById("tp7-hp").value) || 75;
      const ccp = parseFloat(document.getElementById("tp7-ccp").value) || 650;
      const D_in = parseFloat(document.getElementById("tp7-D").value) || 320;
      const d_in = parseFloat(document.getElementById("tp7-d").value) || 250;
      const n1 = parseFloat(document.getElementById("tp7-n1").value) || 1450;
      const n2 = parseFloat(document.getElementById("tp7-n2").value) || 1856;

      const D_large = Math.max(D_in, d_in);
      const d_small = Math.min(D_in, d_in);
      const n_fast = Math.max(n1, n2);
      const isInc = (n2 > n1) || (D_in > d_in);
      const ir = D_large / Math.max(d_small, 1);

      const cl = parseInt(document.getElementById("tp7-clase").value);
      const arr = document.getElementById("tp7-arranque").value;
      const hr = document.getElementById("tp7-horas").value;
      const rowC2 = SKF_DATABASE.correas_servicio_c2.find(r => r.clase_maquina === cl && r.tipo_arranque === arr && r.horas_dia === hr);
      const baseC2 = rowC2 ? rowC2.c2_base : 1.30;

      const chkMult = document.getElementById("tp7-chk-mult");
      const useMult = chkMult ? chkMult.checked : true;
      let multIr = 1.00;
      if (isInc && useMult) {
        const rowMult = SKF_DATABASE.correas_multiplicador_ir.find(r => ir >= r.ir_min && ir <= r.ir_max);
        multIr = rowMult ? rowMult.multiplicador : 1.05;
      }
      const c2 = baseC2 * multIr;
      const pr_kw = hp * 0.7457;
      const pd_kw = pr_kw * c2;

      const badgeMult = document.getElementById("tp7-badge-mult");
      if (badgeMult) {
        badgeMult.textContent = useMult ? `× ${fmt(multIr, 2)}` : "Desactivado (1,0)";
        badgeMult.className = useMult 
          ? "text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono"
          : "text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono";
      }

      let profSel = document.getElementById("tp7-profsel").value;
      if (profSel === "AUTO") {
        if (pd_kw < 12 && d_small < 110) profSel = "SPZ";
        else if (pd_kw < 28 && d_small < 180) profSel = "SPA";
        else if (pd_kw <= 140) profSel = "SPB-XP";
        else profSel = "SPC";
      }
      const baseProf = profSel.includes("SPB") ? "SPB" : profSel;
      const profData = SKF_DATABASE.correas_perfiles.find(p => p.perfil === baseProf) || SKF_DATABASE.correas_perfiles[2];

      const ld_prelim = 2 * ccp + 1.57 * (D_large + d_small) + Math.pow(D_large - d_small, 2) / (4 * ccp);
      let lenChoice = document.getElementById("tp7-lensel").value;
      let chosenLenRow = null;
      if (lenChoice === "AUTO") {
        let minDiff = Infinity;
        SKF_DATABASE.correas_longitudes_c1.forEach(r => {
          const diff = Math.abs(r.Ld - ld_prelim);
          if (diff < minDiff) { minDiff = diff; chosenLenRow = r; }
        });
      } else {
        const target = parseFloat(lenChoice);
        chosenLenRow = SKF_DATABASE.correas_longitudes_c1.find(r => r.Ld === target) || SKF_DATABASE.correas_longitudes_c1[7];
      }
      const commLd = chosenLenRow.Ld;
      const c1 = chosenLenRow.c1;

      const a = 2 * commLd - 3.14 * (D_large + d_small);
      const disc = Math.max(0, a*a - 8*Math.pow(D_large - d_small, 2));
      const cc_def = (a + Math.sqrt(disc)) / 8.0;

      const v = (Math.PI * d_small * n_fast) / 60000.0;
      const ratio = (D_large - d_small) / Math.max(cc_def, 1);

      let closestT7 = SKF_DATABASE.correas_arco_c3[1];
      let minR = Infinity;
      SKF_DATABASE.correas_arco_c3.forEach(r => {
        const diff = Math.abs(r.d_minus_d_over_cc - ratio);
        if (diff < minR) { minR = diff; closestT7 = r; }
      });
      const beta = closestT7.arco_deg;
      const c3 = closestT7.c3;

      const pbRows = SKF_DATABASE.correas_potencia_basica.filter(r => r.d_polea === 250).sort((a,b) => a.rpm_eje_rapido - b.rpm_eje_rapido);
      let pb_base = 20.885, pb_add = 0.868;
      if (pbRows.length >= 2) {
        if (n_fast <= pbRows[0].rpm_eje_rapido) {
          pb_base = pbRows[0].pb_nominal; pb_add = pbRows[0].pb_adicional_ir;
        } else if (n_fast >= pbRows[pbRows.length-1].rpm_eje_rapido) {
          pb_base = pbRows[pbRows.length-1].pb_nominal; pb_add = pbRows[pbRows.length-1].pb_adicional_ir;
        } else {
          for(let i=0; i<pbRows.length-1; i++) {
            if (n_fast >= pbRows[i].rpm_eje_rapido && n_fast <= pbRows[i+1].rpm_eje_rapido) {
              const f = (n_fast - pbRows[i].rpm_eje_rapido) / (pbRows[i+1].rpm_eje_rapido - pbRows[i].rpm_eje_rapido);
              pb_base = pbRows[i].pb_nominal + f * (pbRows[i+1].pb_nominal - pbRows[i].pb_nominal);
              pb_add = pbRows[i].pb_adicional_ir + f * (pbRows[i+1].pb_adicional_ir - pbRows[i].pb_adicional_ir);
              break;
            }
          }
        }
      }
      const scaleProf = profSel === "SPZ" ? 0.32 : (profSel === "SPA" ? 0.62 : (profSel === "SPC" ? 1.65 : 1.0));
      const pb_total = (pb_base + pb_add) * scaleProf;
      const padm = pb_total * c1 * c3;
      const n_exact = pd_kw / Math.max(padm, 0.1);
      const n_belts = Math.max(1, Math.ceil(n_exact));

      document.getElementById("kpi-tp7-c2").textContent = `C₂ = ${fmt(c2, 3)}`;
      document.getElementById("kpi-tp7-pd").textContent = `${fmt(pd_kw, 2)} kW`;
      document.getElementById("kpi-tp7-pr").textContent = `${hp} HP (${fmt(pr_kw, 2)} kW)`;
      document.getElementById("kpi-tp7-perfil").textContent = `SECCIÓN ${profSel} ${profSel.includes("XP") ? "(Extra Power)" : ""}`;
      document.getElementById("kpi-tp7-profdim").textContent = `bo=${profData.bo} | h=${profData.h} mm`;
      document.getElementById("kpi-tp7-arc").textContent = `β = ${beta}°`;
      document.getElementById("kpi-tp7-v").textContent = `${fmt(v, 2)} m/s`;
      document.getElementById("kpi-tp7-c3").textContent = `C₃ = ${fmt(c3, 2)}`;
      const beltCode = profSel.includes("SPB") ? `PHG SPB${commLd}XP` : `PHG ${profSel}${commLd}`;
      document.getElementById("kpi-tp7-belts").textContent = `${n_belts} × ${beltCode}`;
      document.getElementById("kpi-tp7-padm").textContent = `${fmt(padm, 2)} kW/c`;

      document.getElementById("tp7-synoptic-head").textContent = `Motor (${n1} rpm, D=${D_in} mm) → Conducida (${n2} rpm, d=${d_in} mm)`;
      document.getElementById("tp7-badge-ir").textContent = `Ir = ${fmt(ir, 2)} (${isInc ? 'Multiplicador' : 'Reductor'})`;
      document.getElementById("svg-tp7-motordesc").textContent = `D = ${D_in} mm • ${n1} rpm`;
      document.getElementById("svg-tp7-drivenpulley").textContent = `d = ${d_in} mm • ${n2} rpm`;
      document.getElementById("svg-tp7-arclbl").textContent = `Arco β = ${beta}°`;
      document.getElementById("svg-tp7-c3lbl").textContent = `(C₃ = ${fmt(c3, 2)})`;
      document.getElementById("svg-tp7-cctext").textContent = `CC preliminar = ${ccp} mm → CC definitivo = ${fmt(cc_def, 1)} mm (${chosenLenRow.designacion})`;
      document.getElementById("svg-tp7-vtag").textContent = `v = ${fmt(v, 2)} m/s`;
      document.getElementById("svg-tp7-beltstag").textContent = `${n_belts} × ${beltCode.replace("PHG ", "")}`;

      document.getElementById("step-pr").textContent = `Pr = ${hp} HP (${fmt(pr_kw, 2)} kW)`;
      if (multIr > 1.00) {
        document.getElementById("step-c2").textContent = `C₂ = ${fmt(baseC2, 2)} × ${fmt(multIr, 2)} = ${fmt(c2, 3)}`;
      } else {
        document.getElementById("step-c2").textContent = `C₂ = ${fmt(baseC2, 2)} (Directo Tabla 3)`;
      }
      document.getElementById("step-pd").textContent = `Pd = ${fmt(pd_kw, 2)} kW`;
      document.getElementById("step-perfil").textContent = `Perfil ${profSel} (d_mín=${profData.d_min_rec} mm)`;
      document.getElementById("step-ld").textContent = `Ld prelim = ${fmt(ld_prelim, 1)} → ${commLd} mm`;
      document.getElementById("step-cc").textContent = `CC def = ${fmt(cc_def, 1)} mm (C₁=${c1})`;
      document.getElementById("step-pb").textContent = `Pb = ${fmt(pb_base*scaleProf, 2)} + ${fmt(pb_add*scaleProf, 2)} = ${fmt(pb_total, 2)} kW`;
      document.getElementById("step-padm").textContent = `Padm = ${fmt(pb_total, 2)}·${c1}·${c3} = ${fmt(padm, 2)} kW`;
      document.getElementById("step-nbelts").textContent = `N = ${fmt(pd_kw, 2)} / ${fmt(padm, 2)} = ${fmt(n_exact, 2)} ⇒ ${n_belts}`;

      updateDiagram2(pd_kw, n_fast, profSel);

      const minCC = 0.7 * (D_large + d_small);
      const maxCC = 2.0 * (D_large + d_small);
      const ccOk = ccp >= minCC && ccp <= maxCC;
      document.getElementById("tp7-chk-ccp").textContent = `${fmt(minCC, 0)} a ${fmt(maxCC, 0)} mm (${ccOk ? 'Cumple ✓' : 'Alerta ⚠'})`;
      document.getElementById("tp7-chk-dmin").textContent = `${profData.d_min_rec} mm ≤ ${d_small} mm (${d_small >= profData.d_min_rec ? 'Cumple ✓' : 'Bajo el mín ⚠'})`;
    }

        function updateDiagram2(pd_kw, n_fast, perfil) {
      const p = Math.max(1, Math.min(1000, pd_kw));
      const n = Math.max(100, Math.min(10000, n_fast));
      
      const x = 70 + 530 * (Math.log10(p) / 3.0);
      const y = 25 + 205 * ((4.0 - Math.log10(n)) / 2.0);
      
      const targetG = document.getElementById("diag2-target");
      if (targetG) {
        targetG.setAttribute("transform", `translate(${x}, ${y})`);
        const txt = document.getElementById("diag2-target-text");
        if (txt) {
          txt.textContent = `${fmt(p, 1)} kW @ ${Math.round(n)} rpm ➜ ${perfil}`;
        }
      }
      const badge = document.getElementById("diag2-badge-point");
      if (badge) {
        badge.textContent = `Pto Operación: Pd = ${fmt(p, 2)} kW @ ${Math.round(n)} rpm ➜ ${perfil}`;
      }
    }

    function toggleDiagramScan() {
      const el = document.getElementById("diag2-scan-view");
      if (el) el.classList.toggle("hidden");
    }

    function renderDatabaseTable() {
      const tblName = document.getElementById("sel-dbtable").value;
      const data = SKF_DATABASE[tblName] || [];
      const thead = document.getElementById("db-thead-row");
      const tbody = document.getElementById("db-tbody");

      if (data.length === 0) {
        thead.innerHTML = "<th>Sin registros</th>";
        tbody.innerHTML = "<tr><td class='p-3'>Tabla vacía</td></tr>";
        return;
      }

      const cols = Object.keys(data[0]);
      thead.innerHTML = cols.map(c => `<th class="p-2.5 uppercase text-[11px] font-bold border-b border-slate-800">${c}</th>`).join("");
      tbody.innerHTML = data.map(row => {
        const tds = cols.map(c => `<td class="p-2.5 text-slate-300">${row[c]}</td>`).join("");
        return `<tr class="hover:bg-slate-900/60 transition">${tds}</tr>`;
      }).join("");
    }

    function resetToDefaults() {
      document.getElementById("tp6-mode").value = "direct";
      onTP6ModeToggle();
      document.getElementById("tp6-rpm").value = 2400;
      document.getElementById("tp6-ray").value = 390;
      document.getElementById("tp6-raz").value = 521;
      document.getElementById("tp6-rby").value = 39;
      document.getElementById("tp6-rbz").value = 55;
      document.getElementById("sel-tp6-d1").value = "40";
      document.getElementById("sel-tp6-d2").value = "30";
      populateBearingSelect(1, "* 6308");
      populateBearingSelect(2, "* 6206");

      document.getElementById("tp7-hp").value = 75;
      document.getElementById("tp7-ccp").value = 650;
      document.getElementById("tp7-D").value = 320;
      document.getElementById("tp7-d").value = 250;
      document.getElementById("tp7-n1").value = 1450;
      document.getElementById("tp7-n2").value = 1856;
      document.getElementById("tp7-clase").value = "1";
      document.getElementById("tp7-arranque").value = "heavy";
      document.getElementById("tp7-horas").value = "gt16";
      document.getElementById("tp7-chk-mult").checked = false;
      document.getElementById("tp7-profsel").value = "AUTO";
      document.getElementById("tp7-lensel").value = "2180";

      computeTP6();
      computeTP7();
    }

    let animRunning = true;
    let angleD = 0, angleN = 0, bOffset = 0, sPhase = 0;
    function toggleAnim() {
      animRunning = !animRunning;
      document.getElementById("anim-icon").textContent = animRunning ? "⏸" : "▶";
      document.getElementById("anim-text").textContent = animRunning ? "Pausar Simulación" : "Reanudar";
    }

    function animate() {
      if (animRunning) {
        angleD = (angleD + 2.5) % 360;
        angleN = (angleN + 2.5 * 1.28) % 360;
        bOffset = (bOffset - 1.8) % 25;
        sPhase = (sPhase + 1.2) % 15;

        const spk1 = document.getElementById("tp7-spokes-driver");
        const spk2 = document.getElementById("tp7-spokes-driven");
        const dash = document.getElementById("tp7-belt-dash");
        const shStripes = document.getElementById("tp6-stripes");

        if (spk1) spk1.setAttribute("transform", `rotate(${angleD} 200 160)`);
        if (spk2) spk2.setAttribute("transform", `rotate(${angleN} 580 160)`);
        if (dash) dash.setAttribute("stroke-dashoffset", bOffset);
        if (shStripes) shStripes.setAttribute("transform", `translate(${Math.sin(sPhase*0.4)*2}, 0)`);
      }
      requestAnimationFrame(animate);
    }

    populateBearingSelect(1, "* 6308");
    populateBearingSelect(2, "* 6206");
    computeTP6();
    computeTP7();
    requestAnimationFrame(animate);
  </script>
</body>
</html>"""

    with open(r'c:\Mecatronica 2026\Mecanica2\ULTIMO\index.html', 'w', encoding='utf-8') as f:
        f.write(template)


    # Also update brain artifact for inline presentation
    brain_path = r'C:\Users\mhugo\.gemini\antigravity\brain\5f295285-b431-4102-859a-9886db77678b\scada_tp6_tp7.html'
    with open(brain_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print("Successfully built High-Impact SCADA Web Apps!")

if __name__ == '__main__':
    build_web()

