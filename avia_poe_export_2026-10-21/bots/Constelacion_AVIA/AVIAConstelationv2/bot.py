# poe: name=AVIA-Constellation

"""
AVIA CONSTELLATION HUB v2.1
Sistema SIESTA-AVIA con Dashboard + Panel + Visor Memoria + Gemelo Digital JE Beta2 + Libro Blanco
Comandos: "dashboard" | "panel" | "visor" | "gemelo" | "libro" | "memoria" | "estado" | consulta
Protocolo Auto-corrección + Design Atomic + Botones con Copy-to-Clipboard
"""

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from io import BytesIO
from collections import Counter
import re
from fastapi_poe.types import SettingsResponse, ParameterControls, Section, DropDown, ToggleSwitch, ValueNamePair
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

poe.update_settings(SettingsResponse(
    introduction_message="""🌟 **AVIA Constellation v2.1**

**Agentes:** 🤖TILLO | 🎭SEMIA | ⚖️DIGNA

**Comandos:**
• `dashboard` → Panel visual (HTML 1)
• `panel` → Centro de control (HTML 2)
• `visor` → Visor de Memoria gráfico (HTML 3)
• `gemelo` → **🧬 Gemelo Digital JE Beta2** ✨ NUEVO
• `libro [tema]` → Genera Libro Blanco PDF
• `memoria` → Análisis contextual texto
• `estado` → Resumen rápido

✨ **v2.1:** Gemelo Digital con avatar, personalidad, logros y timeline

Ajusta opciones en ⚙️""",
    parameter_controls=ParameterControls(
        sections=[
            Section(
                name="⚙️ Opciones",
                controls=[
                    DropDown(
                        label="Modelo",
                        parameter_name="model",
                        default_value="Grok-4.1-Fast-Non-Reasoning",
                        options=[
                            ValueNamePair(value="Grok-4.1-Fast-Non-Reasoning", name="Grok (Económico)"),
                            ValueNamePair(value="Gemini-3-Flash", name="Gemini Flash"),
                        ],
                    ),
                    ToggleSwitch(label="🌐 Web Search", parameter_name="web", default_value=False),
                ],
            ),
        ]
    ),
))

# ═══════════════════════════════════════════════════════════════════════════════
# DATOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Agent:
    id: str
    emoji: str
    name: str
    role: str
    color: str

@dataclass
class Source:
    name: str
    url: str
    icon: str

AGENTS = [
    Agent("tillo", "🤖", "TILLO", "Coordinador", "#3b82f6"),
    Agent("semia", "🎭", "SEMIA", "Análisis", "#8b5cf6"),
    Agent("digna", "⚖️", "DIGNA", "Ética", "#10b981"),
]

SOURCES = [
    Source("arXiv", "https://arxiv.org", "📄"),
    Source("TIM Analytics", "https://ec.europa.eu", "🇪🇺"),
    Source("Stanford HAI", "https://hai.stanford.edu", "🎓"),
    Source("UNESCO", "https://unesco.org", "🌍"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORIA CONTEXTUAL - ÁTOMOS (funciones base)
# ═══════════════════════════════════════════════════════════════════════════════

# Palabras clave por categoría temática
TOPIC_KEYWORDS = {
    "tecnología": ["ia", "inteligencia artificial", "digital", "tecnología", "software", "datos", "algoritmo", "machine learning", "robot", "automatización"],
    "ética": ["ética", "moral", "valores", "responsabilidad", "derechos", "justicia", "equidad", "dignidad", "privacidad"],
    "educación": ["educación", "aprendizaje", "enseñanza", "formación", "estudiante", "profesor", "escuela", "universidad", "conocimiento"],
    "salud": ["salud", "medicina", "paciente", "tratamiento", "diagnóstico", "bienestar", "mental", "enfermedad"],
    "sociedad": ["sociedad", "comunidad", "social", "ciudadano", "inclusión", "accesibilidad", "diversidad", "cultura"],
    "trabajo": ["trabajo", "empleo", "laboral", "profesional", "carrera", "habilidades", "competencias"],
    "investigación": ["investigación", "estudio", "análisis", "evidencia", "metodología", "hipótesis", "experimento"],
}

# Stopwords en español para filtrar
STOPWORDS = {"el", "la", "los", "las", "un", "una", "de", "del", "en", "y", "que", "es", "por", "para", "con", "se", "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o", "este", "sí", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "tú", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosotros", "vosotras", "os", "mío", "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", "esas", "estoy", "estás", "está", "estamos", "estáis", "están", "esté", "estés", "estemos", "estéis", "estén", "estaré", "estarás", "estará", "estaremos", "estaréis", "estarán", "estaría", "estarías", "estaríamos", "estaríais", "estarían", "estaba", "estabas", "estábamos", "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "hola", "gracias", "por favor", "ok", "sí", "no", "bien", "mal"}

def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """Átomo: Extrae palabras clave de un texto"""
    words = re.findall(r'\b[a-záéíóúñü]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(top_n)]

def detect_topics(text: str) -> List[str]:
    """Átomo: Detecta temas principales en el texto"""
    text_lower = text.lower()
    detected = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        if matches >= 2:
            detected.append(topic)
    return detected if detected else ["general"]

def count_interactions(chat) -> Dict[str, int]:
    """Átomo: Cuenta interacciones por tipo"""
    stats = {"user_messages": 0, "bot_messages": 0, "total_chars": 0}
    for msg in chat:
        if msg.role == "user":
            stats["user_messages"] += 1
        else:
            stats["bot_messages"] += 1
        stats["total_chars"] += len(msg.text)
    return stats

# ═══════════════════════════════════════════════════════════════════════════════
# MEMORIA CONTEXTUAL - MOLÉCULAS (analizadores)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ContextAnalysis:
    """Molécula: Resultado del análisis contextual"""
    keywords: List[str]
    topics: List[str]
    stats: Dict[str, int]
    suggestions: List[str]
    summary: str

def analyze_context(chat) -> ContextAnalysis:
    """Molécula: Analiza el contexto completo de la conversación"""
    # Concatenar todo el texto de la conversación
    all_text = " ".join([msg.text for msg in chat if msg.text])

    # Extraer componentes
    keywords = extract_keywords(all_text, 8)
    topics = detect_topics(all_text)
    stats = count_interactions(chat)

    # Generar sugerencias basadas en el análisis
    suggestions = []
    if "tecnología" in topics:
        suggestions.append("💡 libro Transformación Digital")
    if "ética" in topics:
        suggestions.append("💡 libro Ética en IA")
    if "educación" in topics:
        suggestions.append("💡 libro Educación del Futuro")
    if stats["user_messages"] > 3 and not suggestions:
        suggestions.append("💡 libro " + (keywords[0].capitalize() if keywords else "Resumen"))
    if not suggestions:
        suggestions.append("💡 Prueba: libro [tema de tu interés]")

    # Generar resumen
    topic_str = ", ".join(topics) if topics else "general"
    summary = f"Conversación sobre {topic_str} con {stats['user_messages']} consultas."

    return ContextAnalysis(
        keywords=keywords,
        topics=topics,
        stats=stats,
        suggestions=suggestions,
        summary=summary
    )

def get_context_prompt(chat) -> str:
    """Molécula: Genera un prompt enriquecido con contexto"""
    if len(chat) < 2:
        return ""

    analysis = analyze_context(chat)
    if not analysis.keywords:
        return ""

    context_lines = []
    if analysis.topics and analysis.topics != ["general"]:
        context_lines.append(f"Temas de la conversación: {', '.join(analysis.topics)}")
    if analysis.keywords:
        context_lines.append(f"Conceptos clave mencionados: {', '.join(analysis.keywords[:5])}")

    if context_lines:
        return "Contexto previo: " + ". ".join(context_lines) + ".\n\n"
    return ""

# ═══════════════════════════════════════════════════════════════════════════════
# LIBRO BLANCO PDF - ÁTOMOS (funciones base)
# ═══════════════════════════════════════════════════════════════════════════════

AVIA_COLORS = {
    "primary": HexColor("#3b82f6"),
    "secondary": HexColor("#8b5cf6"),
    "accent": HexColor("#10b981"),
    "dark": HexColor("#1e293b"),
    "light": HexColor("#f1f5f9"),
}

def get_pdf_styles():
    """Átomo: Estilos base del documento"""
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='AVIATitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=AVIA_COLORS["primary"],
        alignment=TA_CENTER,
        spaceAfter=20,
    ))
    styles.add(ParagraphStyle(
        name='AVIASubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=AVIA_COLORS["dark"],
        alignment=TA_CENTER,
        spaceAfter=30,
    ))
    styles.add(ParagraphStyle(
        name='AVIASection',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=AVIA_COLORS["secondary"],
        spaceBefore=20,
        spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name='AVIABody',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    ))
    return styles

# ═══════════════════════════════════════════════════════════════════════════════
# LIBRO BLANCO PDF - MOLÉCULAS (generadores de secciones)
# ═══════════════════════════════════════════════════════════════════════════════

def build_header(styles, title: str) -> list:
    """Molécula: Cabecera del documento"""
    elements = []
    elements.append(Paragraph("AVIA CONSTELLATION", styles['AVIATitle']))
    elements.append(Paragraph("Sistema Integrado de e-Servicios y Tecnologías de Ayuda", styles['AVIASubtitle']))
    elements.append(Paragraph(f"LIBRO BLANCO: {title.upper()}", styles['AVIASection']))
    elements.append(Spacer(1, 0.5*cm))
    return elements

def build_agents_section(styles) -> list:
    """Molécula: Sección de agentes activos"""
    elements = []
    elements.append(Paragraph("CONSTELACIÓN DE AGENTES", styles['AVIASection']))

    data = [["Agente", "Rol", "Función"]]
    for a in AGENTS:
        data.append([f"{a.emoji} {a.name}", a.role, f"Especialista en {a.role.lower()}"])

    table = Table(data, colWidths=[4*cm, 3*cm, 8*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AVIA_COLORS["primary"]),
        ('TEXTCOLOR', (0, 0), (-1, 0), AVIA_COLORS["light"]),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, AVIA_COLORS["dark"]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))
    return elements

def build_sources_section(styles) -> list:
    """Molécula: Sección de fuentes transmedia"""
    elements = []
    elements.append(Paragraph("FUENTES TRANSMEDIA", styles['AVIASection']))

    data = [["Fuente", "URL"]]
    for s in SOURCES:
        data.append([f"{s.icon} {s.name}", s.url])

    table = Table(data, colWidths=[5*cm, 10*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AVIA_COLORS["secondary"]),
        ('TEXTCOLOR', (0, 0), (-1, 0), AVIA_COLORS["light"]),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, AVIA_COLORS["dark"]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))
    return elements

def build_content_section(styles, content: str) -> list:
    """Molécula: Sección de contenido principal"""
    elements = []
    elements.append(Paragraph("ANÁLISIS DE LA CONSTELACIÓN", styles['AVIASection']))

    # Dividir contenido en párrafos
    paragraphs = content.split('\n\n')
    for p in paragraphs:
        if p.strip():
            clean_text = p.replace('**', '').replace('*', '').replace('#', '').strip()
            elements.append(Paragraph(clean_text, styles['AVIABody']))

    elements.append(Spacer(1, 0.5*cm))
    return elements

def build_footer(styles) -> list:
    """Molécula: Pie del documento"""
    elements = []
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f"Generado por AVIA Constellation v1.6 | {fecha}", styles['AVIASubtitle']))
    elements.append(Paragraph("Protocolo SIESTA-AVIA | Metodología Design Atomic", styles['AVIASubtitle']))
    return elements

# ═══════════════════════════════════════════════════════════════════════════════
# LIBRO BLANCO PDF - ORGANISMO (compositor completo)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_libro_blanco(title: str, content: str) -> bytes:
    """Organismo: Genera el PDF completo del Libro Blanco"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = get_pdf_styles()
    elements = []

    # Ensamblar moléculas
    elements.extend(build_header(styles, title))
    elements.extend(build_agents_section(styles))
    elements.extend(build_sources_section(styles))
    elements.extend(build_content_section(styles, content))
    elements.extend(build_footer(styles))

    doc.build(elements)
    return buffer.getvalue()

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD HTML
# ═══════════════════════════════════════════════════════════════════════════════

def generate_dashboard(model: str, web: bool) -> str:
    agents_html = ""
    for a in AGENTS:
        agents_html += f'''
        <div class="agent-card" style="border-left: 4px solid {a.color}">
            <div class="agent-emoji">{a.emoji}</div>
            <div class="agent-info">
                <div class="agent-name">{a.name}</div>
                <div class="agent-role">{a.role}</div>
            </div>
            <div class="agent-status active">● Activo</div>
        </div>'''

    sources_html = ""
    for s in SOURCES:
        sources_html += f'''
        <a href="{s.url}" target="_blank" class="source-card">
            <span class="source-icon">{s.icon}</span>
            <span class="source-name">{s.name}</span>
        </a>'''

    web_status = "ON" if web else "OFF"
    web_class = "active" if web else "inactive"
    model_short = "Grok Fast" if "Grok" in model else "Gemini Flash"
    mode_text = "ECONÓMICO" if "Grok" in model else "ESTÁNDAR"
    mode_color = "#10b981" if "Grok" in model else "#3b82f6"

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AVIA Constellation Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .header h1 {{
            font-size: 1.8rem;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        .header p {{ color: #94a3b8; font-size: 0.9rem; }}
        .section {{
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .section-title {{
            font-size: 0.85rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .agents-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}
        .agent-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: transform 0.2s, background 0.2s;
        }}
        .agent-card:hover {{
            transform: translateY(-2px);
            background: rgba(255,255,255,0.08);
        }}
        .agent-emoji {{ font-size: 2rem; }}
        .agent-info {{ flex: 1; }}
        .agent-name {{ font-weight: 600; font-size: 1rem; }}
        .agent-role {{ color: #94a3b8; font-size: 0.8rem; }}
        .agent-status {{
            font-size: 0.75rem;
            padding: 4px 8px;
            border-radius: 20px;
        }}
        .agent-status.active {{
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
        }}
        .sources-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .source-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 10px 15px;
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: #e2e8f0;
            transition: background 0.2s;
            font-size: 0.9rem;
        }}
        .source-card:hover {{ background: rgba(255,255,255,0.1); }}
        .source-icon {{ font-size: 1.2rem; }}
        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
        }}
        .config-item {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 15px;
        }}
        .config-label {{ color: #64748b; font-size: 0.8rem; margin-bottom: 5px; }}
        .config-value {{ font-weight: 600; font-size: 1.1rem; }}
        .status-bar {{
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .status-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.9rem;
        }}
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}
        .status-dot.active {{ background: #10b981; }}
        .status-dot.inactive {{ background: #64748b; }}
        .mode-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            background: {mode_color}22;
            color: {mode_color};
            margin-top: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #64748b;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 AVIA Constellation</h1>
            <p>Sistema Integrado de e-Servicios y Tecnologías de Ayuda</p>
            <div class="mode-badge">💡 Modo {mode_text}</div>
        </div>

        <div class="section">
            <div class="section-title">🔮 Agentes Activos</div>
            <div class="agents-grid">{agents_html}</div>
        </div>

        <div class="section">
            <div class="section-title">📚 Fuentes Transmedia</div>
            <div class="sources-grid">{sources_html}</div>
        </div>

        <div class="section">
            <div class="section-title">⚙️ Configuración Actual</div>
            <div class="config-grid">
                <div class="config-item">
                    <div class="config-label">Modelo</div>
                    <div class="config-value">📡 {model_short}</div>
                </div>
                <div class="config-item">
                    <div class="config-label">Web Search</div>
                    <div class="config-value">🌐 {web_status}</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📊 Estado del Sistema</div>
            <div class="status-bar">
                <div class="status-item">
                    <div class="status-dot active"></div>
                    <span>Constelación Online</span>
                </div>
                <div class="status-item">
                    <div class="status-dot {web_class}"></div>
                    <span>Web Search {web_status}</span>
                </div>
                <div class="status-item">
                    <div class="status-dot active"></div>
                    <span>3 Agentes Activos</span>
                </div>
            </div>
        </div>

        <div class="footer">
            AVIA Constellation Hub v2.0 | Protocolo SIESTA-AVIA
        </div>
    </div>
</body>
</html>'''

# ═══════════════════════════════════════════════════════════════════════════════
# PANEL INTERACTIVO HTML 2 - ÁTOMOS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_panel_interactivo(model: str, web: bool) -> str:
    """Organismo: Genera el Panel Interactivo (HTML 2) con botones funcionales"""
    agents_cards = ""
    for a in AGENTS:
        agents_cards += f'''
            <div class="agent-chip" style="--agent-color: {a.color}">
                <span class="chip-emoji">{a.emoji}</span>
                <span class="chip-name">{a.name}</span>
                <span class="chip-badge">Activo</span>
            </div>'''

    sources_list = ""
    for s in SOURCES:
        sources_list += f'''
            <a href="{s.url}" target="_blank" class="quick-link">
                <span>{s.icon}</span> {s.name}
            </a>'''

    model_name = "Grok Fast" if "Grok" in model else "Gemini Flash"
    mode_icon = "💚" if "Grok" in model else "💙"
    web_icon = "🌐" if web else "📴"
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Definir acciones con sus comandos
    actions = [
        {"icon": "📊", "label": "Dashboard", "desc": "Panel visual", "cmd": "dashboard"},
        {"icon": "📚", "label": "Libro Blanco", "desc": "Generar PDF", "cmd": "libro [tema]"},
        {"icon": "🧠", "label": "Memoria", "desc": "Contexto", "cmd": "memoria"},
        {"icon": "💬", "label": "Estado", "desc": "Info rápida", "cmd": "estado"},
    ]

    actions_html = ""
    for act in actions:
        actions_html += f'''
                        <button class="action-btn" data-command="{act['cmd']}" onclick="copyCommand(this)">
                            <div class="action-icon">{act['icon']}</div>
                            <div class="action-label">{act['label']}</div>
                            <div class="action-desc">{act['desc']}</div>
                            <div class="action-cmd">📋 {act['cmd']}</div>
                        </button>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AVIA Panel Interactivo</title>
    <style>
        :root {{
            --primary: #3b82f6;
            --secondary: #8b5cf6;
            --accent: #10b981;
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
        }}
        .app {{
            display: grid;
            grid-template-rows: auto 1fr auto;
            min-height: 100vh;
        }}
        .topbar {{
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .topbar h1 {{
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .topbar-status {{
            display: flex;
            gap: 15px;
            font-size: 0.85rem;
        }}
        .status-pill {{
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .main {{
            display: grid;
            grid-template-columns: 1fr 280px;
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }}
        @media (max-width: 768px) {{
            .main {{ grid-template-columns: 1fr; }}
        }}
        .content {{ display: flex; flex-direction: column; gap: 20px; }}
        .card {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .card-title {{
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .agents-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .agent-chip {{
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--agent-color);
            border-radius: 25px;
            padding: 8px 15px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }}
        .agent-chip:hover {{
            background: rgba(255,255,255,0.1);
            transform: translateY(-2px);
        }}
        .chip-emoji {{ font-size: 1.2rem; }}
        .chip-name {{ font-weight: 500; }}
        .chip-badge {{
            background: var(--accent);
            color: white;
            font-size: 0.65rem;
            padding: 2px 6px;
            border-radius: 10px;
        }}
        .actions-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
        }}
        .action-btn {{
            background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(139,92,246,0.2));
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--text);
            text-decoration: none;
            display: block;
            font-family: inherit;
        }}
        .action-btn:hover {{
            transform: translateY(-3px);
            background: linear-gradient(135deg, rgba(59,130,246,0.3), rgba(139,92,246,0.3));
            border-color: var(--primary);
        }}
        .action-btn:active {{
            transform: scale(0.95);
        }}
        .action-btn.copied {{
            background: linear-gradient(135deg, rgba(16,185,129,0.3), rgba(16,185,129,0.2));
            border-color: var(--accent);
        }}
        .action-icon {{ font-size: 1.8rem; margin-bottom: 8px; }}
        .action-label {{ font-size: 0.85rem; font-weight: 500; }}
        .action-desc {{ font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; }}
        .action-cmd {{
            font-size: 0.65rem;
            color: var(--text-muted);
            margin-top: 8px;
            padding: 4px 8px;
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
            font-family: monospace;
        }}
        .toast {{
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: linear-gradient(135deg, var(--accent), #059669);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 4px 20px rgba(16,185,129,0.4);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .toast.show {{
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }}
        .toast-icon {{ font-size: 1.2rem; }}
        .sidebar {{ display: flex; flex-direction: column; gap: 20px; }}
        .quick-links {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .quick-link {{
            background: rgba(255,255,255,0.03);
            padding: 10px 12px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--text);
            transition: background 0.2s;
            font-size: 0.9rem;
        }}
        .quick-link:hover {{ background: rgba(255,255,255,0.08); }}
        .metrics {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        .metric {{
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .metric-label {{ font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; }}
        .config-list {{ display: flex; flex-direction: column; gap: 8px; }}
        .config-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .config-row:last-child {{ border-bottom: none; }}
        .config-key {{ font-size: 0.85rem; color: var(--text-muted); }}
        .config-val {{ font-size: 0.85rem; font-weight: 500; }}
        .bottombar {{
            background: var(--bg-card);
            padding: 10px 20px;
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255,255,255,0.05);
        }}
        .theme-toggle {{
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 20px;
            padding: 5px 12px;
            color: white;
            cursor: pointer;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="app">
        <div class="topbar">
            <h1>🌟 AVIA Control Center</h1>
            <div class="topbar-status">
                <div class="status-pill">{mode_icon} {model_name}</div>
                <div class="status-pill">{web_icon} Web</div>
                <div class="status-pill">🟢 Online</div>
            </div>
        </div>

        <div class="main">
            <div class="content">
                <div class="card">
                    <div class="card-title">🔮 Constelación de Agentes</div>
                    <div class="agents-row">{agents_cards}</div>
                </div>

                <div class="card">
                    <div class="card-title">⚡ Acciones Rápidas <span style="font-size:0.7rem;color:var(--accent)">(click para copiar)</span></div>
                    <div class="actions-grid">{actions_html}
                    </div>
                </div>

                <div class="card">
                    <div class="card-title">📈 Métricas del Sistema</div>
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value">3</div>
                            <div class="metric-label">Agentes Activos</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">4</div>
                            <div class="metric-label">Fuentes</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">v2.0</div>
                            <div class="metric-label">Versión</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">✓</div>
                            <div class="metric-label">Estado</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="sidebar">
                <div class="card">
                    <div class="card-title">📚 Fuentes Transmedia</div>
                    <div class="quick-links">{sources_list}</div>
                </div>

                <div class="card">
                    <div class="card-title">⚙️ Configuración</div>
                    <div class="config-list">
                        <div class="config-row">
                            <span class="config-key">Modelo</span>
                            <span class="config-val">{model_name}</span>
                        </div>
                        <div class="config-row">
                            <span class="config-key">Web Search</span>
                            <span class="config-val">{"Activo" if web else "Inactivo"}</span>
                        </div>
                        <div class="config-row">
                            <span class="config-key">Modo</span>
                            <span class="config-val">{"Económico" if "Grok" in model else "Estándar"}</span>
                        </div>
                        <div class="config-row">
                            <span class="config-key">Protocolo</span>
                            <span class="config-val">SIESTA-AVIA</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bottombar">
            AVIA Constellation v2.0 | Panel Interactivo | {fecha} | Metodología Design Atomic
        </div>

        <div id="toast" class="toast">
            <span class="toast-icon">✓</span>
            <span id="toast-text">Comando copiado</span>
        </div>
    </div>

    <script>
        function copyCommand(btn) {{
            const cmd = btn.getAttribute('data-command');
            navigator.clipboard.writeText(cmd).then(() => {{
                // Visual feedback en botón
                btn.classList.add('copied');
                setTimeout(() => btn.classList.remove('copied'), 1500);

                // Mostrar toast
                const toast = document.getElementById('toast');
                const toastText = document.getElementById('toast-text');
                toastText.textContent = `"${{cmd}}" copiado - pégalo en el chat`;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2500);
            }}).catch(() => {{
                // Fallback si clipboard no disponible
                const toast = document.getElementById('toast');
                const toastText = document.getElementById('toast-text');
                toastText.textContent = `Escribe: ${{cmd}}`;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2500);
            }});
        }}
    </script>
</body>
</html>'''

# ═══════════════════════════════════════════════════════════════════════════════
# GEMELO DIGITAL HTML 4 - ÁTOMOS
# ═══════════════════════════════════════════════════════════════════════════════

# Rasgos de personalidad del Gemelo Digital (Átomo: configuración)
PERSONALITY_TRAITS = {
    "curiosidad": {"icon": "🔍", "color": "#3b82f6", "keywords": ["qué", "cómo", "por qué", "explica", "pregunta"]},
    "creatividad": {"icon": "🎨", "color": "#8b5cf6", "keywords": ["crea", "genera", "diseña", "imagina", "idea"]},
    "analítico": {"icon": "📊", "color": "#10b981", "keywords": ["analiza", "compara", "datos", "estadística", "evalúa"]},
    "comunicativo": {"icon": "💬", "color": "#f59e0b", "keywords": ["escribe", "mensaje", "carta", "texto", "comunicación"]},
    "técnico": {"icon": "⚙️", "color": "#06b6d4", "keywords": ["código", "programa", "sistema", "tecnología", "software"]},
    "estratégico": {"icon": "🎯", "color": "#ef4444", "keywords": ["plan", "estrategia", "objetivo", "meta", "proyecto"]},
}

# Logros desbloqueables (Átomo: configuración de badges)
ACHIEVEMENT_BADGES = {
    "primera_consulta": {"icon": "🌟", "name": "Primera Conexión", "desc": "Realizaste tu primera consulta", "threshold": 1},
    "explorador": {"icon": "🧭", "name": "Explorador", "desc": "5+ consultas en la sesión", "threshold": 5},
    "conversador": {"icon": "💎", "name": "Gran Conversador", "desc": "10+ mensajes intercambiados", "threshold": 10},
    "curioso": {"icon": "🔮", "name": "Mente Curiosa", "desc": "3+ temas diferentes explorados", "threshold": 3},
    "creador": {"icon": "📚", "name": "Creador", "desc": "Generaste un Libro Blanco", "threshold": 1},
    "analista": {"icon": "🧠", "name": "Analista", "desc": "Usaste el visor de memoria", "threshold": 1},
}

def calculate_personality(chat) -> Dict[str, int]:
    """Átomo: Calcula perfil de personalidad basado en la conversación (0-100)"""
    all_text = " ".join([msg.text.lower() for msg in chat if msg.role == "user" and msg.text])

    scores = {}
    for trait, config in PERSONALITY_TRAITS.items():
        matches = sum(1 for kw in config["keywords"] if kw in all_text)
        scores[trait] = min(100, matches * 15 + 20)  # Base de 20 + matches

    return scores

def calculate_energy_level(stats: Dict[str, int]) -> Dict[str, any]:
    """Átomo: Calcula nivel de energía/actividad de la sesión"""
    total_msgs = stats["user_messages"] + stats["bot_messages"]
    chars = stats["total_chars"]

    # Nivel de energía (0-100)
    msg_score = min(50, total_msgs * 5)
    char_score = min(50, chars // 200)
    energy = msg_score + char_score

    # Estado basado en energía
    if energy >= 80:
        state = {"level": energy, "label": "🔥 Alta Energía", "color": "#ef4444"}
    elif energy >= 50:
        state = {"level": energy, "label": "⚡ Activo", "color": "#f59e0b"}
    elif energy >= 25:
        state = {"level": energy, "label": "🌿 Moderado", "color": "#10b981"}
    else:
        state = {"level": energy, "label": "🌙 Inicio", "color": "#64748b"}

    return state

def get_unlocked_achievements(stats: Dict[str, int], topics: List[str], commands_used: List[str]) -> List[Dict]:
    """Átomo: Determina logros desbloqueados"""
    unlocked = []
    total_msgs = stats["user_messages"] + stats["bot_messages"]

    # Primera consulta
    if stats["user_messages"] >= 1:
        unlocked.append(ACHIEVEMENT_BADGES["primera_consulta"])

    # Explorador (5+ consultas)
    if stats["user_messages"] >= 5:
        unlocked.append(ACHIEVEMENT_BADGES["explorador"])

    # Conversador (10+ mensajes)
    if total_msgs >= 10:
        unlocked.append(ACHIEVEMENT_BADGES["conversador"])

    # Curioso (3+ temas)
    if len(topics) >= 3:
        unlocked.append(ACHIEVEMENT_BADGES["curioso"])

    # Creador (usó libro)
    if "libro" in commands_used:
        unlocked.append(ACHIEVEMENT_BADGES["creador"])

    # Analista (usó visor)
    if "visor" in commands_used:
        unlocked.append(ACHIEVEMENT_BADGES["analista"])

    return unlocked

def validate_gemelo_data(personality: Dict[str, int], energy: Dict, achievements: List) -> Dict[str, any]:
    """Átomo: Protocolo auto-corrección para datos del gemelo"""
    validation = {"is_valid": True, "warnings": [], "corrections": []}

    # Validar personalidad
    for trait, score in personality.items():
        if score < 0 or score > 100:
            personality[trait] = max(0, min(100, score))
            validation["corrections"].append(f"{trait} normalizado a rango válido")

    # Validar energía
    if energy["level"] < 0 or energy["level"] > 100:
        energy["level"] = max(0, min(100, energy["level"]))
        validation["corrections"].append("Nivel de energía normalizado")

    # Validar al menos un rasgo dominante
    if all(v < 30 for v in personality.values()):
        validation["warnings"].append("Perfil aún en desarrollo - más interacción revelará tu estilo")

    return validation

# ═══════════════════════════════════════════════════════════════════════════════
# GEMELO DIGITAL HTML 4 - MOLÉCULAS
# ═══════════════════════════════════════════════════════════════════════════════

def build_avatar_section(personality: Dict[str, int], energy: Dict) -> str:
    """Molécula: Genera el avatar visual con estado"""
    # Determinar rasgo dominante para el avatar
    dominant_trait = max(personality.items(), key=lambda x: x[1])
    trait_config = PERSONALITY_TRAITS.get(dominant_trait[0], PERSONALITY_TRAITS["curiosidad"])

    return f'''
        <div class="avatar-container">
            <div class="avatar-ring" style="--ring-color: {energy['color']}">
                <div class="avatar-inner">
                    <div class="avatar-icon">{trait_config['icon']}</div>
                </div>
            </div>
            <div class="avatar-info">
                <div class="avatar-name">Gemelo Digital JE</div>
                <div class="avatar-status" style="color: {energy['color']}">{energy['label']}</div>
                <div class="avatar-trait">Rasgo dominante: {dominant_trait[0].capitalize()}</div>
            </div>
        </div>'''

def build_personality_radar(personality: Dict[str, int]) -> str:
    """Molécula: Genera gráfico de radar de personalidad (CSS puro)"""
    bars_html = ""
    for trait, score in sorted(personality.items(), key=lambda x: x[1], reverse=True):
        config = PERSONALITY_TRAITS.get(trait, {"icon": "📊", "color": "#64748b"})
        bars_html += f'''
            <div class="trait-bar">
                <div class="trait-info">
                    <span class="trait-icon">{config['icon']}</span>
                    <span class="trait-name">{trait.capitalize()}</span>
                    <span class="trait-score">{score}%</span>
                </div>
                <div class="trait-progress">
                    <div class="trait-fill" style="width: {score}%; background: {config['color']}"></div>
                </div>
            </div>'''

    return bars_html

def build_timeline_html(chat) -> str:
    """Molécula: Genera timeline visual de la sesión"""
    items_html = ""
    events = []

    # Extraer eventos del chat (simplificado)
    msg_count = 0
    for msg in chat:
        msg_count += 1
        if msg.role == "user" and msg.text:
            text_preview = msg.text[:30] + "..." if len(msg.text) > 30 else msg.text
            events.append({"type": "user", "text": text_preview, "num": msg_count})
        elif msg.role == "bot":
            events.append({"type": "bot", "text": "Respuesta", "num": msg_count})

    # Limitar a los últimos 6 eventos
    for event in events[-6:]:
        icon = "💬" if event["type"] == "user" else "🤖"
        color = "#3b82f6" if event["type"] == "user" else "#8b5cf6"
        items_html += f'''
            <div class="timeline-item" style="--item-color: {color}">
                <div class="timeline-dot">{icon}</div>
                <div class="timeline-content">{event['text']}</div>
            </div>'''

    if not items_html:
        items_html = '<div class="empty-state">Timeline vacío - ¡Comienza a interactuar!</div>'

    return items_html

def build_achievements_html(achievements: List[Dict]) -> str:
    """Molécula: Genera badges de logros desbloqueados"""
    if not achievements:
        return '<div class="empty-state">Sin logros aún - ¡Sigue explorando!</div>'

    badges_html = ""
    for badge in achievements:
        badges_html += f'''
            <div class="achievement-badge unlocked">
                <div class="badge-icon">{badge['icon']}</div>
                <div class="badge-info">
                    <div class="badge-name">{badge['name']}</div>
                    <div class="badge-desc">{badge['desc']}</div>
                </div>
            </div>'''

    # Añadir badges bloqueados
    all_badges = list(ACHIEVEMENT_BADGES.values())
    unlocked_names = [a['name'] for a in achievements]
    for badge in all_badges:
        if badge['name'] not in unlocked_names:
            badges_html += f'''
            <div class="achievement-badge locked">
                <div class="badge-icon">🔒</div>
                <div class="badge-info">
                    <div class="badge-name">???</div>
                    <div class="badge-desc">{badge['desc']}</div>
                </div>
            </div>'''

    return badges_html

def build_energy_meter(energy: Dict) -> str:
    """Molécula: Genera medidor visual de energía"""
    return f'''
        <div class="energy-meter">
            <div class="energy-label">{energy['label']}</div>
            <div class="energy-bar-container">
                <div class="energy-bar-fill" style="width: {energy['level']}%; background: {energy['color']}"></div>
            </div>
            <div class="energy-value">{energy['level']}%</div>
        </div>'''

# ═══════════════════════════════════════════════════════════════════════════════
# GEMELO DIGITAL HTML 4 - ORGANISMO
# ═══════════════════════════════════════════════════════════════════════════════

def generate_gemelo_digital(chat, model: str, web: bool, commands_used: List[str]) -> str:
    """Organismo: Genera el Gemelo Digital JE Beta2 completo (HTML 4)"""

    # Calcular datos con átomos
    analysis = analyze_context(chat)
    personality = calculate_personality(chat)
    energy = calculate_energy_level(analysis.stats)
    achievements = get_unlocked_achievements(analysis.stats, analysis.topics, commands_used)

    # Auto-corrección
    validation = validate_gemelo_data(personality, energy, achievements)

    # Construir moléculas
    avatar_section = build_avatar_section(personality, energy)
    personality_radar = build_personality_radar(personality)
    timeline = build_timeline_html(chat)
    achievements_html = build_achievements_html(achievements)
    energy_meter = build_energy_meter(energy)

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    model_name = "Grok Fast" if "Grok" in model else "Gemini Flash"

    # Validation HTML
    validation_html = ""
    if validation["warnings"] or validation["corrections"]:
        validation_html = '<div class="validation-panel">'
        for warning in validation["warnings"]:
            validation_html += f'<div class="validation-warning">⚠️ {warning}</div>'
        for correction in validation["corrections"]:
            validation_html += f'<div class="validation-correction">🔧 {correction}</div>'
        validation_html += '</div>'

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemelo Digital JE Beta2</title>
    <style>
        :root {{
            --primary: #3b82f6;
            --secondary: #8b5cf6;
            --accent: #10b981;
            --energy: {energy['color']};
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
        }}
        .app {{
            display: grid;
            grid-template-rows: auto 1fr auto;
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
            padding: 25px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.5;
        }}
        .header h1 {{
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            position: relative;
            z-index: 1;
        }}
        .header-subtitle {{
            font-size: 0.85rem;
            opacity: 0.9;
            margin-top: 5px;
            position: relative;
            z-index: 1;
        }}
        .beta-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.25);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: 8px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        .main {{
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .card-title {{
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        @media (max-width: 700px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
        /* Avatar */
        .avatar-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
            padding: 20px;
        }}
        .avatar-ring {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: conic-gradient(var(--ring-color) 0%, transparent 70%);
            padding: 4px;
            animation: spin 8s linear infinite;
        }}
        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        .avatar-inner {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: var(--bg-card);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .avatar-icon {{
            font-size: 3.5rem;
        }}
        .avatar-info {{ text-align: center; }}
        .avatar-name {{
            font-size: 1.3rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .avatar-status {{
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 4px;
        }}
        .avatar-trait {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 4px;
        }}
        /* Energy Meter */
        .energy-meter {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 15px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            margin-top: 15px;
        }}
        .energy-label {{ font-size: 0.85rem; min-width: 100px; }}
        .energy-bar-container {{
            flex: 1;
            height: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            overflow: hidden;
        }}
        .energy-bar-fill {{
            height: 100%;
            border-radius: 5px;
            transition: width 1s ease-out;
        }}
        .energy-value {{
            font-weight: 600;
            min-width: 45px;
            text-align: right;
        }}
        /* Personality Traits */
        .trait-bar {{ margin-bottom: 12px; }}
        .trait-info {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
        }}
        .trait-icon {{ font-size: 1.1rem; }}
        .trait-name {{ flex: 1; font-size: 0.85rem; }}
        .trait-score {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--accent);
        }}
        .trait-progress {{
            height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            overflow: hidden;
        }}
        .trait-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 1s ease-out;
        }}
        /* Timeline */
        .timeline {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .timeline-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 15px;
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            border-left: 3px solid var(--item-color);
            transition: transform 0.2s;
        }}
        .timeline-item:hover {{
            transform: translateX(5px);
            background: rgba(255,255,255,0.06);
        }}
        .timeline-dot {{ font-size: 1.2rem; }}
        .timeline-content {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        /* Achievements */
        .achievements-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 12px;
        }}
        .achievement-badge {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            border-radius: 12px;
            transition: all 0.3s;
        }}
        .achievement-badge.unlocked {{
            background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(139,92,246,0.2));
            border: 1px solid rgba(59,130,246,0.3);
        }}
        .achievement-badge.unlocked:hover {{
            transform: scale(1.02);
            background: linear-gradient(135deg, rgba(59,130,246,0.3), rgba(139,92,246,0.3));
        }}
        .achievement-badge.locked {{
            background: rgba(255,255,255,0.03);
            border: 1px dashed rgba(255,255,255,0.1);
            opacity: 0.6;
        }}
        .badge-icon {{ font-size: 1.8rem; }}
        .badge-name {{ font-size: 0.85rem; font-weight: 600; }}
        .badge-desc {{ font-size: 0.7rem; color: var(--text-muted); }}
        /* Validation */
        .validation-panel {{
            padding: 12px;
            background: rgba(251,191,36,0.1);
            border-radius: 8px;
            border: 1px solid rgba(251,191,36,0.3);
            margin-bottom: 15px;
        }}
        .validation-warning {{ color: #fbbf24; font-size: 0.85rem; margin-bottom: 4px; }}
        .validation-correction {{ color: #10b981; font-size: 0.85rem; margin-bottom: 4px; }}
        .empty-state {{
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-style: italic;
        }}
        .footer {{
            background: var(--bg-card);
            padding: 12px 20px;
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255,255,255,0.05);
        }}
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 8px;
        }}
        .footer-link {{
            color: var(--primary);
            text-decoration: none;
            font-size: 0.75rem;
            cursor: pointer;
            transition: color 0.2s;
        }}
        .footer-link:hover {{ color: var(--accent); }}
    </style>
</head>
<body>
    <div class="app">
        <div class="header">
            <h1>🧬 Gemelo Digital JE <span class="beta-badge">Beta2</span></h1>
            <div class="header-subtitle">Tu representación digital en AVIA Constellation</div>
        </div>

        <div class="main">
            {validation_html}

            <div class="grid-2">
                <div class="card">
                    <div class="card-title">👤 Tu Avatar Digital</div>
                    {avatar_section}
                    {energy_meter}
                </div>

                <div class="card">
                    <div class="card-title">🎭 Perfil de Personalidad</div>
                    {personality_radar}
                </div>
            </div>

            <div class="card">
                <div class="card-title">🏆 Logros Desbloqueados ({len(achievements)}/{len(ACHIEVEMENT_BADGES)})</div>
                <div class="achievements-grid">{achievements_html}</div>
            </div>

            <div class="card">
                <div class="card-title">📅 Timeline de Sesión</div>
                <div class="timeline">{timeline}</div>
            </div>
        </div>

        <div class="footer">
            AVIA Constellation v2.1 | Gemelo Digital JE Beta2 | {fecha} | Modelo: {model_name}
            <div class="footer-links">
                <span class="footer-link" onclick="location.reload()">🔄 Actualizar</span>
            </div>
        </div>
    </div>

    <script>
        // Animación de barras al cargar
        document.addEventListener('DOMContentLoaded', () => {{
            document.querySelectorAll('.trait-fill, .energy-bar-fill').forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => bar.style.width = width, 100);
            }});
        }});
    </script>
</body>
</html>'''

# ═══════════════════════════════════════════════════════════════════════════════
# VISOR DE MEMORIA HTML 3 - ÁTOMOS
# ═══════════════════════════════════════════════════════════════════════════════

# Colores e iconos para temas (Átomo: configuración visual)
TOPIC_VISUALS = {
    "tecnología": {"color": "#3b82f6", "icon": "💻", "gradient": "from-blue-500"},
    "ética": {"color": "#8b5cf6", "icon": "⚖️", "gradient": "from-purple-500"},
    "educación": {"color": "#10b981", "icon": "📚", "gradient": "from-green-500"},
    "salud": {"color": "#ef4444", "icon": "🏥", "gradient": "from-red-500"},
    "sociedad": {"color": "#f59e0b", "icon": "👥", "gradient": "from-amber-500"},
    "trabajo": {"color": "#06b6d4", "icon": "💼", "gradient": "from-cyan-500"},
    "investigación": {"color": "#ec4899", "icon": "🔬", "gradient": "from-pink-500"},
    "general": {"color": "#64748b", "icon": "📋", "gradient": "from-slate-500"},
}

def calculate_topic_scores(text: str) -> Dict[str, int]:
    """Átomo: Calcula puntuación de cada tema (0-100)"""
    text_lower = text.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        # Normalizar a 0-100 (max matches esperados ~5)
        scores[topic] = min(100, matches * 20)
    return scores

def validate_analysis(analysis: ContextAnalysis) -> Dict[str, any]:
    """Átomo: Protocolo auto-corrección - valida el análisis"""
    validation = {
        "is_valid": True,
        "warnings": [],
        "corrections": []
    }

    # Validar estadísticas
    if analysis.stats["user_messages"] < 0:
        validation["is_valid"] = False
        validation["corrections"].append("user_messages corregido a 0")
        analysis.stats["user_messages"] = 0

    # Validar keywords
    if not analysis.keywords:
        validation["warnings"].append("Sin palabras clave detectadas")

    # Validar topics
    if not analysis.topics:
        analysis.topics = ["general"]
        validation["corrections"].append("Topic por defecto: general")

    return validation

# ═══════════════════════════════════════════════════════════════════════════════
# VISOR DE MEMORIA HTML 3 - MOLÉCULAS
# ═══════════════════════════════════════════════════════════════════════════════

def build_topic_bars_html(scores: Dict[str, int]) -> str:
    """Molécula: Genera barras de progreso CSS para temas"""
    bars_html = ""
    # Ordenar por puntuación descendente
    sorted_topics = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for topic, score in sorted_topics:
        if score > 0:
            visual = TOPIC_VISUALS.get(topic, TOPIC_VISUALS["general"])
            bars_html += f'''
                <div class="topic-bar">
                    <div class="topic-info">
                        <span class="topic-icon">{visual["icon"]}</span>
                        <span class="topic-name">{topic.capitalize()}</span>
                        <span class="topic-score">{score}%</span>
                    </div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: {score}%; background: {visual["color"]}"></div>
                    </div>
                </div>'''

    if not bars_html:
        bars_html = '<div class="empty-state">No hay suficientes datos para analizar</div>'

    return bars_html

def build_keywords_cloud_html(keywords: List[str]) -> str:
    """Molécula: Genera tags/nube de palabras clave"""
    if not keywords:
        return '<div class="empty-state">Sin palabras clave detectadas</div>'

    tags_html = ""
    sizes = ["tag-xl", "tag-lg", "tag-md", "tag-sm", "tag-xs"]
    colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#06b6d4", "#ec4899"]

    for i, keyword in enumerate(keywords[:10]):
        size = sizes[min(i, len(sizes)-1)]
        color = colors[i % len(colors)]
        tags_html += f'<span class="keyword-tag {size}" style="--tag-color: {color}">{keyword}</span>'

    return tags_html

def build_stats_cards_html(stats: Dict[str, int]) -> str:
    """Molécula: Genera tarjetas de estadísticas animadas"""
    return f'''
        <div class="stat-card">
            <div class="stat-icon">💬</div>
            <div class="stat-value" data-target="{stats['user_messages']}">{stats['user_messages']}</div>
            <div class="stat-label">Consultas</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-value" data-target="{stats['bot_messages']}">{stats['bot_messages']}</div>
            <div class="stat-label">Respuestas</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🔤</div>
            <div class="stat-value" data-target="{stats['total_chars']}">{stats['total_chars']:,}</div>
            <div class="stat-label">Caracteres</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">{stats['user_messages'] + stats['bot_messages']}</div>
            <div class="stat-label">Total Msgs</div>
        </div>'''

def build_suggestions_html(suggestions: List[str]) -> str:
    """Molécula: Genera lista de sugerencias con botones copiables"""
    if not suggestions:
        return '<div class="empty-state">Sin sugerencias disponibles</div>'

    html = ""
    for suggestion in suggestions:
        # Extraer comando si existe
        cmd = ""
        if "libro " in suggestion.lower():
            parts = suggestion.split("libro ", 1)
            if len(parts) > 1:
                cmd = f"libro {parts[1]}"

        if cmd:
            html += f'''
                <button class="suggestion-btn" data-command="{cmd}" onclick="copyCommand(this)">
                    <span class="suggestion-text">{suggestion}</span>
                    <span class="copy-hint">📋</span>
                </button>'''
        else:
            html += f'<div class="suggestion-item">{suggestion}</div>'

    return html

# ═══════════════════════════════════════════════════════════════════════════════
# VISOR DE MEMORIA HTML 3 - ORGANISMO
# ═══════════════════════════════════════════════════════════════════════════════

def generate_visor_memoria(analysis: ContextAnalysis, model: str, web: bool) -> str:
    """Organismo: Genera el Visor de Memoria completo (HTML 3)"""

    # Auto-corrección
    validation = validate_analysis(analysis)

    # Calcular scores para barras
    all_text = " ".join([msg.text for msg in poe.default_chat if msg.text])
    topic_scores = calculate_topic_scores(all_text)

    # Construir moléculas
    topic_bars = build_topic_bars_html(topic_scores)
    keywords_cloud = build_keywords_cloud_html(analysis.keywords)
    stats_cards = build_stats_cards_html(analysis.stats)
    suggestions = build_suggestions_html(analysis.suggestions)

    # Tema dominante para gradiente
    dominant_topic = analysis.topics[0] if analysis.topics else "general"
    dominant_visual = TOPIC_VISUALS.get(dominant_topic, TOPIC_VISUALS["general"])

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    model_name = "Grok Fast" if "Grok" in model else "Gemini Flash"

    # Generar warnings/corrections HTML si existen
    validation_html = ""
    if validation["warnings"] or validation["corrections"]:
        validation_html = '<div class="validation-panel">'
        for warning in validation["warnings"]:
            validation_html += f'<div class="validation-warning">⚠️ {warning}</div>'
        for correction in validation["corrections"]:
            validation_html += f'<div class="validation-correction">🔧 {correction}</div>'
        validation_html += '</div>'

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AVIA Visor de Memoria</title>
    <style>
        :root {{
            --primary: #3b82f6;
            --secondary: #8b5cf6;
            --accent: #10b981;
            --dominant: {dominant_visual["color"]};
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
        }}
        .app {{
            display: grid;
            grid-template-rows: auto 1fr auto;
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(135deg, var(--dominant), var(--secondary));
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .header-subtitle {{
            font-size: 0.85rem;
            opacity: 0.9;
            margin-top: 5px;
        }}
        .dominant-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.2);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-top: 10px;
        }}
        .main {{
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        .card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .card-title {{
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }}
        @media (max-width: 600px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: transform 0.2s, background 0.2s;
        }}
        .stat-card:hover {{
            transform: translateY(-3px);
            background: rgba(255,255,255,0.08);
        }}
        .stat-icon {{ font-size: 1.5rem; margin-bottom: 8px; }}
        .stat-value {{
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stat-label {{ font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; }}
        .topic-bar {{
            margin-bottom: 12px;
        }}
        .topic-info {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
        }}
        .topic-icon {{ font-size: 1.1rem; }}
        .topic-name {{ flex: 1; font-size: 0.9rem; }}
        .topic-score {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--accent);
        }}
        .bar-container {{
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 1s ease-out;
        }}
        .keywords-cloud {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .keyword-tag {{
            background: rgba(255,255,255,0.08);
            border: 1px solid var(--tag-color);
            color: var(--tag-color);
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 500;
            transition: all 0.2s;
            cursor: default;
        }}
        .keyword-tag:hover {{
            background: var(--tag-color);
            color: white;
            transform: scale(1.05);
        }}
        .tag-xl {{ font-size: 1rem; padding: 8px 16px; }}
        .tag-lg {{ font-size: 0.9rem; }}
        .tag-md {{ font-size: 0.8rem; }}
        .tag-sm {{ font-size: 0.75rem; padding: 4px 10px; }}
        .tag-xs {{ font-size: 0.7rem; padding: 3px 8px; opacity: 0.8; }}
        .suggestions-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .suggestion-btn {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15));
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 12px 16px;
            color: var(--text);
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
            font-size: 0.9rem;
            width: 100%;
            text-align: left;
        }}
        .suggestion-btn:hover {{
            background: linear-gradient(135deg, rgba(59,130,246,0.25), rgba(139,92,246,0.25));
            border-color: var(--primary);
            transform: translateX(5px);
        }}
        .suggestion-btn.copied {{
            background: linear-gradient(135deg, rgba(16,185,129,0.3), rgba(16,185,129,0.2));
            border-color: var(--accent);
        }}
        .copy-hint {{ opacity: 0.5; transition: opacity 0.2s; }}
        .suggestion-btn:hover .copy-hint {{ opacity: 1; }}
        .suggestion-item {{
            padding: 10px 16px;
            background: rgba(255,255,255,0.03);
            border-radius: 8px;
            font-size: 0.9rem;
        }}
        .summary-text {{
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text);
            padding: 15px;
            background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1));
            border-radius: 12px;
            border-left: 4px solid var(--dominant);
        }}
        .validation-panel {{
            margin-bottom: 15px;
            padding: 12px;
            background: rgba(251,191,36,0.1);
            border-radius: 8px;
            border: 1px solid rgba(251,191,36,0.3);
        }}
        .validation-warning {{
            color: #fbbf24;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }}
        .validation-correction {{
            color: #10b981;
            font-size: 0.85rem;
            margin-bottom: 4px;
        }}
        .empty-state {{
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-style: italic;
        }}
        .footer {{
            background: var(--bg-card);
            padding: 12px 20px;
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-muted);
            border-top: 1px solid rgba(255,255,255,0.05);
        }}
        .toast {{
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: linear-gradient(135deg, var(--accent), #059669);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 4px 20px rgba(16,185,129,0.4);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 1000;
        }}
        .toast.show {{
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        @media (max-width: 700px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="app">
        <div class="header">
            <h1>🧠 AVIA Visor de Memoria</h1>
            <div class="header-subtitle">Análisis Contextual de la Sesión</div>
            <div class="dominant-badge">
                <span>{dominant_visual["icon"]}</span>
                <span>Tema dominante: {dominant_topic.capitalize()}</span>
            </div>
        </div>

        <div class="main">
            {validation_html}

            <div class="card">
                <div class="card-title">📊 Estadísticas de Sesión</div>
                <div class="stats-grid">{stats_cards}</div>
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="card-title">🎯 Análisis Temático</div>
                    {topic_bars}
                </div>

                <div class="card">
                    <div class="card-title">🔑 Palabras Clave</div>
                    <div class="keywords-cloud">{keywords_cloud}</div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">💡 Sugerencias Inteligentes <span style="font-size:0.65rem;color:var(--accent)">(click para copiar)</span></div>
                <div class="suggestions-list">{suggestions}</div>
            </div>

            <div class="card">
                <div class="card-title">📝 Resumen de Contexto</div>
                <div class="summary-text">{analysis.summary}</div>
            </div>
        </div>

        <div class="footer">
            AVIA Constellation v2.0 | Visor de Memoria | {fecha} | Modelo: {model_name} | Protocolo SIESTA-AVIA
        </div>

        <div id="toast" class="toast">✓ Comando copiado</div>
    </div>

    <script>
        function copyCommand(btn) {{
            const cmd = btn.getAttribute('data-command');
            navigator.clipboard.writeText(cmd).then(() => {{
                btn.classList.add('copied');
                setTimeout(() => btn.classList.remove('copied'), 1500);

                const toast = document.getElementById('toast');
                toast.textContent = `"${{cmd}}" copiado - pégalo en el chat`;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2500);
            }}).catch(() => {{
                const toast = document.getElementById('toast');
                toast.textContent = `Escribe: ${{cmd}}`;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2500);
            }});
        }}

        // Animación de barras al cargar
        document.addEventListener('DOMContentLoaded', () => {{
            document.querySelectorAll('.bar-fill').forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => bar.style.width = width, 100);
            }});
        }});
    </script>
</body>
</html>'''

# ═══════════════════════════════════════════════════════════════════════════════
# BOT PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

class AVIABot:
    def __init__(self):
        self.model = poe.query.parameters.get("model", "Grok-4.1-Fast-Non-Reasoning")
        self.web = poe.query.parameters.get("web", False)
        self.commands_used = []  # Rastrear comandos usados para logros

    def show_dashboard(self):
        """Muestra el Dashboard Canvas (HTML 1)"""
        html = generate_dashboard(self.model, self.web)
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_panel(self):
        """Muestra el Panel Interactivo (HTML 2)"""
        html = generate_panel_interactivo(self.model, self.web)
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_visor(self):
        """Muestra el Visor de Memoria (HTML 3)"""
        self.commands_used.append("visor")
        analysis = analyze_context(poe.default_chat)
        html = generate_visor_memoria(analysis, self.model, self.web)
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_gemelo(self):
        """Muestra el Gemelo Digital JE Beta2 (HTML 4)"""
        self.commands_used.append("gemelo")
        html = generate_gemelo_digital(poe.default_chat, self.model, self.web, self.commands_used)
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_status(self):
        """Muestra estado rápido en texto"""
        agents_str = " | ".join([f"{a.emoji}{a.name}" for a in AGENTS])
        web_str = "🌐 ON" if self.web else "📴 OFF"
        model_str = "Grok" if "Grok" in self.model else "Gemini"
        mode = "💚 Económico" if "Grok" in self.model else "💙 Estándar"

        with poe.start_message() as msg:
            msg.write(f"**🌟 AVIA Constellation v2.1 - Estado**\n\n")
            msg.write(f"**Agentes:** {agents_str}\n")
            msg.write(f"**Modelo:** {model_str} | **Web:** {web_str}\n")
            msg.write(f"**Modo:** {mode}\n\n")
            msg.write("_Comandos: `dashboard` | `panel` | `visor` | `gemelo` | `memoria` | `libro [tema]` | `estado`_")

    def show_memoria(self):
        """Muestra el análisis de memoria contextual de la sesión"""
        analysis = analyze_context(poe.default_chat)

        # Iconos para temas
        topic_icons = {
            "tecnología": "💻", "ética": "⚖️", "educación": "📚",
            "salud": "🏥", "sociedad": "👥", "trabajo": "💼",
            "investigación": "🔬", "general": "📋"
        }

        with poe.start_message() as msg:
            msg.write("🧠 **AVIA Memoria Contextual**\n\n")

            # Estadísticas
            msg.write("**📊 Estadísticas de Sesión:**\n")
            msg.write(f"• Consultas del usuario: {analysis.stats['user_messages']}\n")
            msg.write(f"• Respuestas del bot: {analysis.stats['bot_messages']}\n")
            msg.write(f"• Total caracteres: {analysis.stats['total_chars']:,}\n\n")

            # Temas detectados
            msg.write("**🎯 Temas Detectados:**\n")
            for topic in analysis.topics:
                icon = topic_icons.get(topic, "📋")
                msg.write(f"• {icon} {topic.capitalize()}\n")
            msg.write("\n")

            # Palabras clave
            if analysis.keywords:
                msg.write("**🔑 Conceptos Clave:**\n")
                msg.write(f"• {' • '.join(analysis.keywords)}\n\n")

            # Sugerencias
            msg.write("**💡 Sugerencias:**\n")
            for suggestion in analysis.suggestions:
                msg.write(f"• {suggestion}\n")
            msg.write("\n")

            # Resumen
            msg.write(f"**📝 Resumen:** {analysis.summary}")

    def generate_libro(self, tema: str):
        """Genera Libro Blanco PDF sobre un tema"""
        self.commands_used.append("libro")
        with poe.start_message() as msg:
            msg.write(f"📚 **Generando Libro Blanco: {tema}**\n\n")
            msg.write("⏳ Consultando a la constelación...\n")

        # Obtener análisis de la constelación
        agents_str = " ".join([f"{a.emoji}{a.name}" for a in AGENTS])
        prompt = f"""Eres AVIA Constellation con agentes {agents_str}.
Genera un análisis detallado sobre: {tema}

Estructura:
1. Introducción y contexto
2. Análisis desde cada perspectiva de agente
3. Conclusiones y recomendaciones

Responde de forma clara y estructurada."""

        try:
            response = poe.call(self.model, prompt)
            content = response.text
        except:
            try:
                response = poe.call("Grok-4.1-Fast-Non-Reasoning", prompt)
                content = response.text
            except:
                content = f"Análisis sobre {tema} pendiente de desarrollo."

        with poe.start_message() as msg:
            msg.write("📄 Generando documento PDF...\n")

        # Generar PDF
        pdf_bytes = generate_libro_blanco(tema, content)

        # Crear attachment y mostrar
        with poe.start_message() as msg:
            attachment = msg.attach_file(
                name=f"Libro_Blanco_{tema.replace(' ', '_')[:20]}.pdf",
                contents=pdf_bytes,
                content_type="application/pdf"
            )
            msg.write(f"✅ **Libro Blanco generado exitosamente**\n\n")
            msg.write(f"📖 **Tema:** {tema}\n")
            msg.write(f"🤖 **Agentes:** {agents_str}\n")
            msg.write(f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            msg.write("_Descarga el PDF adjunto arriba_")

    def process_query(self, query: str):
        """Procesa consulta normal con memoria contextual"""
        agents_str = " ".join([f"{a.emoji}{a.name}" for a in AGENTS])

        # Obtener contexto de la conversación
        context = get_context_prompt(poe.default_chat)
        has_context = bool(context)

        with poe.start_message() as msg:
            msg.write(f"🌟 {agents_str} | 📡 {self.model.split('-')[0]}")
            if self.web:
                msg.write(" 🌐")
            if has_context:
                msg.write(" 🧠")  # Indicador de memoria activa
            msg.write("\n\n")

        prompt = f"Eres AVIA con agentes {agents_str}. Responde integrando perspectivas.\n\n{context}Consulta: {query}"

        try:
            params = {"web_search": True} if self.web and "Gemini" in self.model else None
            poe.call(
                self.model,
                prompt,
                parameters=params,
                output=poe.default_chat,
                adopt_current_bot_name=True
            )
        except:
            try:
                poe.call("Grok-4.1-Fast-Non-Reasoning", prompt, output=poe.default_chat, adopt_current_bot_name=True)
            except:
                with poe.start_message() as msg:
                    msg.write("⚠️ Error temporal. Intenta de nuevo.")

    def run(self):
        query = poe.query.text.strip().lower() if poe.query.text else ""
        query_original = poe.query.text.strip() if poe.query.text else ""

        if not query:
            with poe.start_message() as msg:
                msg.write("👋 Envía una consulta, `dashboard`, `panel`, `visor`, `gemelo`, `memoria`, `libro [tema]` o `estado`")
            return

        # Comandos especiales
        if query in ["dashboard", "canvas", "html1"]:
            self.show_dashboard()
        elif query in ["panel", "control", "centro", "html2"]:
            self.show_panel()
        elif query in ["visor", "analisis", "html3", "visual"]:
            self.show_visor()
        elif query in ["gemelo", "digital", "avatar", "html4", "twin"]:
            self.show_gemelo()
        elif query in ["memoria", "contexto", "memory", "context"]:
            self.show_memoria()
        elif query in ["estado", "status", "info"]:
            self.show_status()
        elif query.startswith("libro ") or query.startswith("pdf ") or query.startswith("whitepaper "):
            # Extraer tema del comando
            tema = query_original.split(" ", 1)[1] if " " in query_original else "General"
            self.generate_libro(tema)
        elif query in ["libro", "pdf", "whitepaper"]:
            with poe.start_message() as msg:
                msg.write("📚 **Uso:** `libro [tema]`\n\n")
                msg.write("Ejemplo: `libro Inteligencia Artificial Ética`")
        else:
            self.process_query(query_original)


if __name__ == "__main__":
    bot = AVIABot()
    bot.run()