# poe: name=AVIA-Constellation

"""
AVIA CONSTELLATION HUB v1.6
Sistema SIESTA-AVIA con Dashboard Canvas + Libro Blanco PDF
Comandos: "dashboard" | "estado" | "libro" | consulta normal
"""

from dataclasses import dataclass
from typing import List
from datetime import datetime
from io import BytesIO
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
    introduction_message="""🌟 **AVIA Constellation v1.6**

**Agentes:** 🤖TILLO | 🎭SEMIA | ⚖️DIGNA

**Comandos:**
• `dashboard` → Panel visual interactivo
• `libro [tema]` → Genera Libro Blanco PDF
• `estado` → Resumen rápido
• Tu consulta → Respuesta de la constelación

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
            AVIA Constellation Hub v1.5 | Protocolo SIESTA-AVIA
        </div>
    </div>
</body>
</html>'''

# ═══════════════════════════════════════════════════════════════════════════════
# BOT PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

class AVIABot:
    def __init__(self):
        self.model = poe.query.parameters.get("model", "Grok-4.1-Fast-Non-Reasoning")
        self.web = poe.query.parameters.get("web", False)

    def show_dashboard(self):
        """Muestra el Dashboard Canvas"""
        html = generate_dashboard(self.model, self.web)
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_status(self):
        """Muestra estado rápido en texto"""
        agents_str = " | ".join([f"{a.emoji}{a.name}" for a in AGENTS])
        web_str = "🌐 ON" if self.web else "📴 OFF"
        model_str = "Grok" if "Grok" in self.model else "Gemini"
        mode = "💚 Económico" if "Grok" in self.model else "💙 Estándar"

        with poe.start_message() as msg:
            msg.write(f"**🌟 AVIA Constellation v1.6 - Estado**\n\n")
            msg.write(f"**Agentes:** {agents_str}\n")
            msg.write(f"**Modelo:** {model_str} | **Web:** {web_str}\n")
            msg.write(f"**Modo:** {mode}\n\n")
            msg.write("_Comandos: `dashboard` | `libro [tema]` | `estado`_")

    def generate_libro(self, tema: str):
        """Genera Libro Blanco PDF sobre un tema"""
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
        """Procesa consulta normal"""
        agents_str = " ".join([f"{a.emoji}{a.name}" for a in AGENTS])
        with poe.start_message() as msg:
            msg.write(f"🌟 {agents_str} | 📡 {self.model.split('-')[0]}")
            if self.web:
                msg.write(" 🌐")
            msg.write("\n\n")

        prompt = f"Eres AVIA con agentes {agents_str}. Responde integrando perspectivas.\n\nConsulta: {query}"

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
                msg.write("👋 Envía una consulta, `dashboard`, `libro [tema]` o `estado`")
            return

        # Comandos especiales
        if query in ["dashboard", "panel", "canvas"]:
            self.show_dashboard()
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

