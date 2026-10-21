# poe: name=AVIA-Video-Prosumidor

import json
import re

from fastapi_poe.types import SettingsResponse

poe.update_settings(SettingsResponse(
    introduction_message=(
        "Hola! Soy **AVIA-Video-Prosumidor** v2.0\n\n"
        "Tu editor de video inteligente con interfaz de 4 botones de colores en las esquinas, "
        "asistente AVIA integrado y metodologia Design Atomic.\n\n"
        "**Escribe cualquier mensaje** para abrir el editor, o describe lo que quieres editar "
        "y AVIA te ayudara con su constelacion de agentes.\n\n"
        "Botones de esquina:\n"
        "- Rojo (Menu) - Funciones de edicion\n"
        "- Verde (Modo) - Perfil de usuario\n"
        "- Naranja (Ajustes) - Configuracion\n"
        "- Morado (AVIA) - Asistente IA inteligente"
    ),
    enable_image_comprehension=True,
    allow_attachments=True,
))


def parse_json_from_response(response_text, required_fields=None):
    """Extract and parse JSON from response."""
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
    else:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            json_str = match.group(0).strip()
        else:
            return None
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError:
        return None
    if required_fields:
        missing = set(required_fields) - set(parsed.keys())
        if missing:
            return None
    return parsed


class AVIAVideoProsumidor:
    """AVIA Video Prosumidor v2.0 - Editor de video con 4 botones esquina + AVIA IA.

    Protocolo AVIA de Auto-Correccion aplicado:
    - REGLA 1: NUNCA usar comillas simples/dobles para strings multilinea en JS.
              SIEMPRE usar template literals (backticks `).
    - REGLA 2: En HTML embebido en Python, usar raw strings o escapar correctamente.
    - REGLA 3: Contar backticks en contenido HTML y usar N+1 en el wrapper markdown.
    - REGLA 4: Validar que todo string JS con \\n use template literals.
    """

    def get_avia_response(self, user_text):
        """Usa TestBotBLKENPtt3D para generar respuesta del asistente AVIA."""
        try:
            response = poe.call(
                "TestBotBLKENPtt3D",
                poe.Message(
                    text=(
                        "Eres el asistente AVIA integrado en un editor de video. "
                        "El usuario te ha dicho lo siguiente dentro del editor. "
                        "Responde de forma breve y util, en espanol. "
                        "Si pide cortar, exportar, filtros, texto, musica, subtitulos, "
                        "responde confirmando la accion. Maximo 2 frases.\n\n"
                        f"Usuario dice: {user_text}"
                    ),
                    sender="system"
                ),
            )
            return response.text.strip()[:200]
        except Exception:
            return ""

    def build_html(self, avia_greeting=""):
        """Genera el HTML completo del editor AVIA Video Prosumidor v2.0."""
        # REGLA AVIA-AutoCorrector: Todos los strings JS multilinea usan template literals
        escaped_greeting = avia_greeting.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$") if avia_greeting else ""

        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AVIA Video - Modo Prosumidor v2.0</title>
    <style>
        /* ============================================================
           AVIA VIDEO v2.0 - MODO PROSUMIDOR
           ============================================================
           Auditoria: AVIA Nomada + AutoCorrector
           Metodologia: Atomic Design + SIESTA
           Correccion: SyntaxError template literals aplicado
           ============================================================ */

        /* ============= ATOMOS: Variables (Design Tokens) ============= */
        :root {{
            --avia-purple: #8b5cf6;
            --avia-purple-dark: #7c3aed;
            --avia-orange: #f59e0b;
            --avia-green: #22c55e;
            --avia-blue: #3b82f6;
            --avia-red: #ef4444;
            --avia-pink: #ec4899;
            --avia-cyan: #06b6d4;
            --bg-app: #0a0a0f;
            --bg-surface: #111118;
            --bg-card: #1a1a24;
            --bg-elevated: #252532;
            --bg-hover: #2d2d3d;
            --text-white: #ffffff;
            --text-light: #e4e4e7;
            --text-muted: #a1a1aa;
            --text-dim: #71717a;
            --border-subtle: #27272a;
            --border-medium: #3f3f46;
            --space-xs: 4px;
            --space-sm: 8px;
            --space-md: 16px;
            --space-lg: 24px;
            --space-xl: 32px;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 20px;
            --radius-full: 50%;
            --topbar-height: 56px;
            --timeline-height: 110px;
            --transition-fast: 0.15s ease;
            --transition-normal: 0.25s ease;
            --touch-min: 44px;
        }}

        /* ============= RESET ============= */
        *, *::before, *::after {{
            margin: 0; padding: 0; box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-app);
            color: var(--text-white);
            min-height: 100vh;
            overflow: hidden;
            line-height: 1.5;
        }}
        button {{
            font-family: inherit; cursor: pointer; border: none; background: none;
            min-width: var(--touch-min); min-height: var(--touch-min);
        }}
        button:focus-visible {{
            outline: 2px solid var(--avia-orange);
            outline-offset: 2px;
        }}

        /* ============= TEMPLATE: Layout Prosumidor ============= */
        .prosumer-app {{
            display: flex; flex-direction: column; height: 100vh;
        }}

        /* ============= ORGANISMO: TopBar ============= */
        .topbar {{
            height: var(--topbar-height);
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-subtle);
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 var(--space-lg); flex-shrink: 0;
        }}
        .topbar-left {{ display: flex; align-items: center; gap: var(--space-md); }}
        .logo {{ display: flex; align-items: center; gap: var(--space-sm); }}
        .logo-icon {{
            width: 36px; height: 36px;
            background: linear-gradient(135deg, var(--avia-purple), var(--avia-pink));
            border-radius: var(--radius-md);
            display: flex; align-items: center; justify-content: center; font-size: 20px;
        }}
        .logo-text {{ font-size: 16px; font-weight: 700; letter-spacing: -0.5px; }}
        .project-pill {{
            display: flex; align-items: center; gap: var(--space-sm);
            padding: var(--space-xs) var(--space-md);
            background: var(--bg-card); border-radius: var(--radius-lg); font-size: 13px;
        }}
        .project-name {{ font-weight: 600; }}
        .project-ext {{ color: var(--text-dim); }}
        .save-badge {{
            background: var(--avia-green); color: white;
            padding: 2px 8px; border-radius: var(--space-xs);
            font-size: 10px; font-weight: 600;
        }}
        .topbar-center {{ position: absolute; left: 50%; transform: translateX(-50%); }}
        .mode-indicator {{
            display: flex; align-items: center; gap: var(--space-sm);
            padding: var(--space-xs) var(--space-lg);
            background: var(--bg-card); border: 1px solid var(--avia-orange);
            border-radius: var(--radius-xl); transition: var(--transition-normal);
        }}
        .mode-indicator:hover {{
            background: var(--bg-elevated);
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
        }}
        .mode-dot {{
            width: 8px; height: 8px; background: var(--avia-orange);
            border-radius: var(--radius-full); animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.6; transform: scale(0.85); }}
        }}
        .mode-label {{ font-size: 13px; font-weight: 500; }}
        .topbar-right {{ display: flex; align-items: center; gap: var(--space-sm); }}
        .avia-top-btn {{
            display: flex; align-items: center; gap: var(--space-sm);
            padding: var(--space-xs) var(--space-md);
            background: linear-gradient(135deg, var(--avia-purple), var(--avia-pink));
            border-radius: var(--radius-xl); color: white; font-size: 13px; font-weight: 600;
            transition: var(--transition-normal);
        }}
        .avia-top-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
        }}
        .avia-status-dot {{
            width: 7px; height: 7px; background: white;
            border-radius: var(--radius-full); animation: pulse 1.5s infinite;
        }}

        /* ============= ORGANISMO: Canvas Central ============= */
        .canvas-zone {{
            flex: 1; display: flex; align-items: center; justify-content: center;
            padding: var(--space-xl); position: relative;
            background: radial-gradient(ellipse at center, #12121a 0%, var(--bg-app) 100%);
        }}
        .preview-container {{
            width: 100%; max-width: 900px; aspect-ratio: 16/9;
            background: linear-gradient(145deg, #1a1a2e 0%, #12121a 100%);
            border-radius: var(--radius-lg); position: relative; overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05);
        }}
        .format-badges {{
            position: absolute; top: var(--space-md); left: var(--space-md);
            display: flex; gap: var(--space-sm); z-index: 10;
        }}
        .format-badge {{
            padding: 3px 8px; background: rgba(0,0,0,0.75);
            backdrop-filter: blur(10px); border-radius: var(--space-xs);
            font-size: 11px; font-weight: 600;
        }}
        .badge-cyan {{ color: var(--avia-cyan); }}
        .badge-green {{ color: var(--avia-green); }}
        .badge-orange {{ color: var(--avia-orange); }}
        .preview-empty {{
            width: 100%; height: 100%;
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; text-align: center; padding: var(--space-xl);
        }}
        .empty-icon {{ font-size: 64px; margin-bottom: var(--space-md); opacity: 0.5; }}
        .empty-title {{
            font-size: 18px; font-weight: 500; color: var(--text-muted);
            margin-bottom: var(--space-md);
        }}
        .empty-actions {{ display: flex; flex-direction: column; gap: var(--space-sm); }}
        .empty-action {{
            display: flex; align-items: center; gap: var(--space-sm);
            color: var(--text-dim); font-size: 13px;
        }}

        /* ============= 4 BOTONES FLOTANTES PROSUMIDOR (CLAVE) ============= */
        .corner-btn {{
            position: fixed;
            width: 56px; height: 56px;
            border-radius: var(--radius-lg);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            gap: 2px; color: white; font-size: 22px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            transition: var(--transition-normal); z-index: 100;
        }}
        .corner-btn:hover {{
            transform: scale(1.12);
            box-shadow: 0 12px 40px rgba(0,0,0,0.5);
        }}
        .corner-btn:active {{ transform: scale(0.95); }}
        .corner-btn-label {{
            font-size: 8px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
        }}
        /* Posiciones: 4 esquinas */
        .btn-top-left {{
            top: calc(var(--topbar-height) + var(--space-lg)); left: var(--space-lg);
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }}
        .btn-top-right {{
            top: calc(var(--topbar-height) + var(--space-lg)); right: var(--space-lg);
            background: linear-gradient(135deg, #22c55e, #16a34a);
        }}
        .btn-bottom-left {{
            bottom: calc(var(--timeline-height) + var(--space-lg)); left: var(--space-lg);
            background: linear-gradient(135deg, #f59e0b, #d97706);
        }}
        .btn-bottom-right {{
            bottom: calc(var(--timeline-height) + var(--space-lg)); right: var(--space-lg);
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            animation: aviaGlow 3s infinite;
        }}
        @keyframes aviaGlow {{
            0%, 100% {{ box-shadow: 0 8px 32px rgba(139, 92, 246, 0.4); }}
            50% {{ box-shadow: 0 8px 48px rgba(139, 92, 246, 0.7); }}
        }}
        .btn-badge {{
            position: absolute; top: -4px; right: -4px;
            width: 18px; height: 18px; background: var(--avia-red);
            border-radius: var(--radius-full); font-size: 10px; font-weight: 700;
            display: flex; align-items: center; justify-content: center;
            border: 2px solid var(--bg-app);
        }}

        /* ============= ORGANISMO: Timeline ============= */
        .timeline-simple {{
            height: var(--timeline-height);
            background: var(--bg-surface);
            border-top: 1px solid var(--border-subtle);
            display: flex; flex-direction: column; flex-shrink: 0;
        }}
        .playback-bar {{
            height: 50px; display: flex; align-items: center; justify-content: center;
            gap: var(--space-lg); padding: 0 var(--space-lg); background: var(--bg-card);
        }}
        .playback-controls {{ display: flex; align-items: center; gap: var(--space-xs); }}
        .playback-btn {{
            width: 40px; height: 40px; background: var(--bg-elevated);
            border-radius: var(--radius-md); color: var(--text-muted);
            font-size: 16px; display: flex; align-items: center; justify-content: center;
            transition: var(--transition-fast);
        }}
        .playback-btn:hover {{ background: var(--bg-hover); color: var(--text-white); }}
        .playback-btn.play {{
            width: 48px; height: 48px;
            background: linear-gradient(135deg, var(--avia-blue), #2563eb);
            color: white; border-radius: var(--radius-lg); font-size: 20px;
        }}
        .playback-btn.play:hover {{
            transform: scale(1.08);
            box-shadow: 0 6px 24px rgba(59, 130, 246, 0.4);
        }}
        .time-display {{
            display: flex; align-items: center;
            background: var(--bg-app); padding: var(--space-xs) var(--space-md);
            border-radius: var(--radius-md); font-family: 'SF Mono', Consolas, monospace;
            font-size: 14px;
        }}
        .time-current {{ color: var(--text-white); font-weight: 600; }}
        .time-separator {{ color: var(--text-dim); margin: 0 var(--space-xs); }}
        .time-total {{ color: var(--text-muted); }}
        .progress-container {{
            flex: 1; height: 60px; padding: var(--space-md) var(--space-lg);
            display: flex; align-items: center;
        }}
        .progress-track {{
            flex: 1; height: 6px; background: var(--bg-elevated);
            border-radius: var(--space-xs); position: relative; cursor: pointer;
        }}
        .progress-fill {{
            height: 100%; width: 0%;
            background: linear-gradient(90deg, var(--avia-blue), var(--avia-purple));
            border-radius: var(--space-xs); position: relative;
            transition: width 0.1s linear;
        }}
        .progress-handle {{
            position: absolute; right: -7px; top: 50%; transform: translateY(-50%);
            width: 14px; height: 14px; background: white;
            border-radius: var(--radius-full); box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            cursor: grab;
        }}
        .progress-handle:active {{ cursor: grabbing; transform: translateY(-50%) scale(1.2); }}

        /* ============= PANELES FLOTANTES ============= */
        .panel-overlay {{
            position: fixed; inset: 0; background: rgba(0,0,0,0.6);
            backdrop-filter: blur(4px); opacity: 0; visibility: hidden;
            transition: var(--transition-normal); z-index: 500;
        }}
        .panel-overlay.active {{ opacity: 1; visibility: visible; }}
        .floating-panel {{
            position: fixed; width: 360px; max-height: 75vh;
            background: var(--bg-card); border-radius: var(--radius-xl);
            box-shadow: 0 24px 80px rgba(0,0,0,0.6);
            border: 1px solid var(--border-subtle);
            opacity: 0; visibility: hidden;
            transform: scale(0.9) translateY(20px);
            transition: var(--transition-normal); z-index: 600; overflow: hidden;
        }}
        .floating-panel.active {{
            opacity: 1; visibility: visible; transform: scale(1) translateY(0);
        }}
        .panel-menu {{ top: calc(var(--topbar-height) + 90px); left: 90px; }}
        .panel-profile {{ top: calc(var(--topbar-height) + 90px); right: 90px; }}
        .panel-settings {{ bottom: calc(var(--timeline-height) + 90px); left: 90px; }}
        .panel-avia {{
            bottom: calc(var(--timeline-height) + 90px); right: 90px; width: 400px;
        }}
        .panel-header {{
            padding: var(--space-md) var(--space-lg);
            background: var(--bg-elevated);
            border-bottom: 1px solid var(--border-subtle);
            display: flex; align-items: center; justify-content: space-between;
        }}
        .panel-title {{
            display: flex; align-items: center; gap: var(--space-sm);
            font-size: 15px; font-weight: 600;
        }}
        .panel-icon {{
            width: 32px; height: 32px; border-radius: var(--radius-md);
            display: flex; align-items: center; justify-content: center;
            font-size: 16px; color: white;
        }}
        .panel-close {{
            width: 30px; height: 30px; background: transparent;
            color: var(--text-muted); border-radius: var(--radius-sm);
            font-size: 16px; display: flex; align-items: center; justify-content: center;
            transition: var(--transition-fast);
        }}
        .panel-close:hover {{ background: var(--avia-red); color: white; }}
        .panel-body {{
            padding: var(--space-lg); max-height: calc(75vh - 60px); overflow-y: auto;
        }}

        /* ============= PANEL MENU: Grid 3x3 ============= */
        .menu-grid {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-sm);
        }}
        .menu-item {{
            aspect-ratio: 1; background: var(--bg-elevated); border-radius: var(--radius-md);
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; gap: var(--space-xs);
            transition: var(--transition-fast); color: var(--text-muted);
        }}
        .menu-item:hover {{
            background: var(--bg-hover); color: var(--text-white); transform: translateY(-2px);
        }}
        .menu-icon {{ font-size: 26px; }}
        .menu-label {{ font-size: 10px; font-weight: 500; }}

        /* ============= PANEL AVIA ============= */
        .avia-chat-area {{
            min-height: 200px; max-height: 280px; overflow-y: auto;
            margin-bottom: var(--space-md);
            display: flex; flex-direction: column; gap: var(--space-sm);
        }}
        .avia-msg {{
            padding: var(--space-sm) var(--space-md);
            border-radius: var(--radius-md); font-size: 13px;
            line-height: 1.5; max-width: 85%; word-wrap: break-word;
        }}
        .avia-msg.bot {{
            background: var(--bg-elevated); color: var(--text-light);
            align-self: flex-start; border-bottom-left-radius: 4px;
        }}
        .avia-msg.user {{
            background: linear-gradient(135deg, var(--avia-purple), var(--avia-blue));
            color: white; align-self: flex-end; border-bottom-right-radius: 4px;
        }}
        .avia-input-row {{
            display: flex; gap: var(--space-xs); align-items: center;
        }}
        .avia-input {{
            flex: 1; padding: var(--space-sm) var(--space-md);
            background: var(--bg-elevated); border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md); color: var(--text-white);
            font-size: 13px; outline: none; transition: var(--transition-fast);
        }}
        .avia-input:focus {{ border-color: var(--avia-purple); }}
        .avia-action-btn {{
            width: 38px; height: 38px; border-radius: var(--radius-sm);
            display: flex; align-items: center; justify-content: center;
            font-size: 16px; color: white; transition: var(--transition-fast);
            flex-shrink: 0;
        }}
        .avia-action-btn.mic {{ background: var(--avia-purple); }}
        .avia-action-btn.mic.recording {{ background: var(--avia-red); animation: pulse 1s infinite; }}
        .avia-action-btn.send {{ background: var(--avia-blue); }}
        .avia-action-btn:hover {{ transform: scale(1.1); }}

        /* ============= PANEL PERFIL ============= */
        .profile-modes {{ display: flex; flex-direction: column; gap: var(--space-sm); }}
        .profile-mode {{
            display: flex; align-items: center; gap: var(--space-md);
            padding: var(--space-md); background: var(--bg-elevated);
            border-radius: var(--radius-md); border: 2px solid transparent;
            cursor: pointer; transition: var(--transition-fast);
        }}
        .profile-mode:hover {{ background: var(--bg-hover); }}
        .profile-mode.active {{
            border-color: var(--avia-orange); background: rgba(245, 158, 11, 0.1);
        }}
        .profile-mode-icon {{
            width: 40px; height: 40px; border-radius: var(--radius-md);
            display: flex; align-items: center; justify-content: center;
            font-size: 18px; color: white;
        }}
        .mode-pro {{ background: var(--avia-red); }}
        .mode-prosumer {{ background: var(--avia-orange); }}
        .mode-consumer {{ background: var(--avia-green); }}
        .profile-mode-info h4 {{ font-size: 13px; font-weight: 600; margin-bottom: 2px; }}
        .profile-mode-info p {{ font-size: 11px; color: var(--text-dim); }}
        .profile-mode-check {{
            margin-left: auto; color: var(--avia-green); font-size: 18px; opacity: 0;
        }}
        .profile-mode.active .profile-mode-check {{ opacity: 1; }}

        /* ============= PANEL AJUSTES ============= */
        .settings-section {{ margin-bottom: var(--space-lg); }}
        .settings-title {{
            font-size: 11px; font-weight: 600; color: var(--text-dim);
            text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: var(--space-sm);
        }}
        .settings-item {{
            display: flex; align-items: center; justify-content: space-between;
            padding: var(--space-md); background: var(--bg-elevated);
            border-radius: var(--radius-sm); margin-bottom: var(--space-xs);
        }}
        .settings-label {{ font-size: 13px; }}
        .toggle {{
            width: 44px; height: 24px; background: var(--bg-hover);
            border-radius: 12px; position: relative; cursor: pointer;
            transition: var(--transition-fast);
        }}
        .toggle.active {{ background: var(--avia-green); }}
        .toggle::after {{
            content: ''; position: absolute; top: 3px; left: 3px;
            width: 18px; height: 18px; background: white;
            border-radius: var(--radius-full); transition: var(--transition-fast);
        }}
        .toggle.active::after {{ left: 23px; }}

        /* ============= SCROLLBAR ============= */
        ::-webkit-scrollbar {{ width: 5px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-app); }}
        ::-webkit-scrollbar-thumb {{ background: var(--bg-elevated); border-radius: 3px; }}

        /* ============= RESPONSIVE ============= */
        @media (max-width: 768px) {{
            .corner-btn {{ width: 48px; height: 48px; font-size: 18px; }}
            .corner-btn-label {{ display: none; }}
            .floating-panel {{
                width: calc(100% - 24px); left: 12px !important; right: 12px !important;
            }}
            .topbar-left .project-pill {{ display: none; }}
            .topbar-center {{ display: none; }}
        }}

        /* ============= UTILIDADES ============= */
        .sr-only {{
            position: absolute; width: 1px; height: 1px;
            padding: 0; margin: -1px; overflow: hidden;
            clip: rect(0,0,0,0); white-space: nowrap; border: 0;
        }}
    </style>
</head>
<body>
    <!-- ============= APLICACION PROSUMIDOR ============= -->
    <div class="prosumer-app">
        <!-- ORGANISMO: TopBar -->
        <header class="topbar" role="banner">
            <div class="topbar-left">
                <div class="logo">
                    <div class="logo-icon" aria-hidden="true">&#x1F3AC;</div>
                    <span class="logo-text">AVIA Video</span>
                </div>
                <div class="project-pill">
                    <span aria-hidden="true">&#x1F4C1;</span>
                    <span class="project-name" id="projectName">Mi_Proyecto</span>
                    <span class="project-ext">.avia</span>
                    <span class="save-badge" id="saveBadge">Guardado</span>
                </div>
            </div>
            <div class="topbar-center">
                <button class="mode-indicator" id="modeBtn" aria-label="Cambiar modo de usuario">
                    <span class="mode-dot"></span>
                    <span class="mode-label" id="modeLabel">Modo Prosumidor</span>
                </button>
            </div>
            <div class="topbar-right">
                <button class="avia-top-btn" id="aviaTopBtn" aria-label="Abrir asistente AVIA">
                    <span class="avia-status-dot"></span>
                    <span>AVIA</span>
                </button>
            </div>
        </header>

        <!-- ORGANISMO: Canvas Central -->
        <main class="canvas-zone" role="main">
            <div class="preview-container" id="previewContainer">
                <div class="format-badges">
                    <span class="format-badge badge-cyan" id="badgeRatio">16:9</span>
                    <span class="format-badge badge-green" id="badgeRes">1920x1080</span>
                    <span class="format-badge badge-orange" id="badgeFps">30fps</span>
                </div>
                <div class="preview-empty" id="previewEmpty">
                    <div class="empty-icon" aria-hidden="true">&#x1F4C2;</div>
                    <h2 class="empty-title">Arrastra archivos para comenzar</h2>
                    <div class="empty-actions">
                        <div class="empty-action">
                            <span aria-hidden="true">&#x1F3AC;</span>
                            <span>Video, imagen o audio</span>
                        </div>
                        <div class="empty-action">
                            <span aria-hidden="true">&#x1F916;</span>
                            <span>O pide ayuda a AVIA (boton morado)</span>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <!-- ORGANISMO: Timeline -->
        <footer class="timeline-simple" role="contentinfo">
            <div class="playback-bar">
                <div class="playback-controls">
                    <button class="playback-btn" id="prevBtn" aria-label="Anterior">&#x23EE;</button>
                    <button class="playback-btn play" id="playBtn" aria-label="Reproducir">&#x25B6;</button>
                    <button class="playback-btn" id="nextBtn" aria-label="Siguiente">&#x23ED;</button>
                </div>
                <div class="time-display">
                    <span class="time-current" id="timeCurrent">00:00:00</span>
                    <span class="time-separator">/</span>
                    <span class="time-total" id="timeTotal">00:02:30</span>
                </div>
            </div>
            <div class="progress-container">
                <div class="progress-track" id="progressTrack">
                    <div class="progress-fill" id="progressFill">
                        <div class="progress-handle"></div>
                    </div>
                </div>
            </div>
        </footer>
    </div>

    <!-- ============= 4 BOTONES FLOTANTES DE ESQUINA ============= -->
    <button class="corner-btn btn-top-left" id="btnMenu" aria-label="Menu de funciones" title="Menu">
        <span aria-hidden="true">&#x2630;</span>
        <span class="corner-btn-label">Menu</span>
    </button>
    <button class="corner-btn btn-top-right" id="btnProfile" aria-label="Perfil y modo" title="Modo">
        <span aria-hidden="true">&#x1F464;</span>
        <span class="corner-btn-label">Modo</span>
    </button>
    <button class="corner-btn btn-bottom-left" id="btnSettings" aria-label="Ajustes" title="Ajustes">
        <span aria-hidden="true">&#x2699;</span>
        <span class="corner-btn-label">Ajustes</span>
    </button>
    <button class="corner-btn btn-bottom-right" id="btnAvia" aria-label="Asistente AVIA" title="AVIA">
        <span aria-hidden="true">&#x1F916;</span>
        <span class="corner-btn-label">AVIA</span>
        <span class="btn-badge" id="aviaBadge">2</span>
    </button>

    <!-- OVERLAY -->
    <div class="panel-overlay" id="panelOverlay"></div>

    <!-- PANEL: MENU (Rojo) -->
    <aside class="floating-panel panel-menu" id="panelMenu" role="dialog" aria-label="Menu de funciones">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#ef4444,#dc2626);">&#x2630;</div>
                <span>Funciones</span>
            </div>
            <button class="panel-close" data-panel="menu" aria-label="Cerrar menu">&#x2715;</button>
        </div>
        <div class="panel-body">
            <div class="menu-grid">
                <button class="menu-item" data-action="project"><span class="menu-icon">&#x1F4C1;</span><span class="menu-label">Proyecto</span></button>
                <button class="menu-item" data-action="import"><span class="menu-icon">&#x2795;</span><span class="menu-label">Importar</span></button>
                <button class="menu-item" data-action="cut"><span class="menu-icon">&#x2702;</span><span class="menu-label">Cortar</span></button>
                <button class="menu-item" data-action="text"><span class="menu-icon">&#x1F524;</span><span class="menu-label">Texto</span></button>
                <button class="menu-item" data-action="audio"><span class="menu-icon">&#x1F3B5;</span><span class="menu-label">Audio</span></button>
                <button class="menu-item" data-action="effects"><span class="menu-icon">&#x2728;</span><span class="menu-label">Efectos</span></button>
                <button class="menu-item" data-action="filters"><span class="menu-icon">&#x1F3A8;</span><span class="menu-label">Filtros</span></button>
                <button class="menu-item" data-action="ai"><span class="menu-icon">&#x1F9E0;</span><span class="menu-label">IA</span></button>
                <button class="menu-item" data-action="export"><span class="menu-icon">&#x1F4E4;</span><span class="menu-label">Exportar</span></button>
            </div>
        </div>
    </aside>

    <!-- PANEL: PERFIL/MODO (Verde) -->
    <aside class="floating-panel panel-profile" id="panelProfile" role="dialog" aria-label="Modo de usuario">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#22c55e,#16a34a);">&#x1F464;</div>
                <span>Modo de Usuario</span>
            </div>
            <button class="panel-close" data-panel="profile" aria-label="Cerrar perfil">&#x2715;</button>
        </div>
        <div class="panel-body">
            <p style="color:var(--text-muted);font-size:13px;margin-bottom:12px;">
                Selecciona segun tu nivel de experiencia:
            </p>
            <div class="profile-modes">
                <div class="profile-mode" data-mode="pro">
                    <div class="profile-mode-icon mode-pro">&#x1F534;</div>
                    <div class="profile-mode-info"><h4>Profesional</h4><p>Control total, todas las herramientas</p></div>
                    <span class="profile-mode-check">&#x2713;</span>
                </div>
                <div class="profile-mode active" data-mode="prosumer">
                    <div class="profile-mode-icon mode-prosumer">&#x1F7E1;</div>
                    <div class="profile-mode-info"><h4>Prosumidor</h4><p>4 botones + Asistente AVIA</p></div>
                    <span class="profile-mode-check">&#x2713;</span>
                </div>
                <div class="profile-mode" data-mode="consumer">
                    <div class="profile-mode-icon mode-consumer">&#x1F7E2;</div>
                    <div class="profile-mode-info"><h4>Consumidor</h4><p>AVIA guia todo el proceso</p></div>
                    <span class="profile-mode-check">&#x2713;</span>
                </div>
            </div>
        </div>
    </aside>

    <!-- PANEL: AJUSTES (Naranja) -->
    <aside class="floating-panel panel-settings" id="panelSettings" role="dialog" aria-label="Ajustes">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#f59e0b,#d97706);">&#x2699;</div>
                <span>Ajustes</span>
            </div>
            <button class="panel-close" data-panel="settings" aria-label="Cerrar ajustes">&#x2715;</button>
        </div>
        <div class="panel-body">
            <div class="settings-section">
                <div class="settings-title">Proyecto</div>
                <div class="settings-item">
                    <span class="settings-label">Resolucion</span>
                    <span style="color:var(--avia-cyan);" id="settingRes">1920x1080</span>
                </div>
                <div class="settings-item">
                    <span class="settings-label">Frame Rate</span>
                    <span style="color:var(--avia-orange);" id="settingFps">30 fps</span>
                </div>
            </div>
            <div class="settings-section">
                <div class="settings-title">Preferencias</div>
                <div class="settings-item">
                    <span class="settings-label">Autoguardado</span>
                    <div class="toggle active" data-setting="autosave"></div>
                </div>
                <div class="settings-item">
                    <span class="settings-label">Sonidos de UI</span>
                    <div class="toggle" data-setting="sounds"></div>
                </div>
                <div class="settings-item">
                    <span class="settings-label">Modo oscuro</span>
                    <div class="toggle active" data-setting="dark"></div>
                </div>
            </div>
        </div>
    </aside>

    <!-- PANEL: AVIA ASISTENTE (Morado) -->
    <aside class="floating-panel panel-avia" id="panelAvia" role="dialog" aria-label="Asistente AVIA">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#8b5cf6,#7c3aed);">&#x1F916;</div>
                <span>AVIA Asistente</span>
            </div>
            <button class="panel-close" data-panel="avia" aria-label="Cerrar AVIA">&#x2715;</button>
        </div>
        <div class="panel-body">
            <div class="avia-chat-area" id="aviaChat">
                <div class="avia-msg bot">Hola! Soy AVIA, tu asistente de edicion v2.0. Puedo ayudarte a cortar, anadir texto, filtros, musica, subtitulos y mas. Escribe o usa el microfono.</div>
            </div>
            <div class="avia-input-row">
                <input type="text" class="avia-input" id="aviaInput" placeholder="Escribe o usa el microfono..." aria-label="Mensaje para AVIA">
                <button class="avia-action-btn mic" id="btnMic" aria-label="Microfono">&#x1F3A4;</button>
                <button class="avia-action-btn send" id="btnSend" aria-label="Enviar">&#x27A4;</button>
            </div>
        </div>
    </aside>

    <!-- ============= JAVASCRIPT ============= -->
    <script>
        /* ==============================================================
           AVIA VIDEO v2.0 - MODO PROSUMIDOR
           ==============================================================
           REGLAS AVIA-AutoCorrector (aprendidas):
           1. NUNCA usar comillas simples/dobles para strings multilinea
           2. SIEMPRE usar template literals (backticks) para multilinea
           3. Escapar backticks dentro de template literals con backslash
           4. Validar todos los strings antes de deploy
           ============================================================== */

        class AVIAProsumer {{
            constructor() {{
                this.activePanel = null;
                this.isPlaying = false;
                this.currentTime = 0;
                this.totalTime = 150; // 2:30
                this.playInterval = null;
                this.isRecording = false;
                this.undoStack = [];
                this.redoStack = [];
                this.currentMode = 'prosumer';
                this.init();
            }}

            init() {{
                this.bindCornerButtons();
                this.bindPanelCloses();
                this.bindOverlay();
                this.bindPlayback();
                this.bindToggles();
                this.bindKeyboard();
                this.bindAviaChat();
                this.bindModeSelection();
                this.bindMenuActions();
                this.bindProgressTrack();

                // Saludo inicial si hay mensaje de AVIA
                const greeting = `{escaped_greeting}`;
                if (greeting && greeting.trim()) {{
                    setTimeout(() => this.addAviaMessage(greeting, 'bot'), 1500);
                }}

                console.log('AVIA Video Prosumidor v2.0 iniciado');
            }}

            // ====== PANELES ======

            bindCornerButtons() {{
                const map = {{
                    btnMenu: 'menu',
                    btnProfile: 'profile',
                    btnSettings: 'settings',
                    btnAvia: 'avia'
                }};
                Object.entries(map).forEach(([id, panel]) => {{
                    const el = document.getElementById(id);
                    if (el) el.addEventListener('click', () => this.togglePanel(panel));
                }});
                const modeBtn = document.getElementById('modeBtn');
                if (modeBtn) modeBtn.addEventListener('click', () => this.togglePanel('profile'));
                const aviaTop = document.getElementById('aviaTopBtn');
                if (aviaTop) aviaTop.addEventListener('click', () => this.togglePanel('avia'));
            }}

            bindPanelCloses() {{
                document.querySelectorAll('.panel-close').forEach(btn => {{
                    btn.addEventListener('click', () => this.closeAllPanels());
                }});
            }}

            bindOverlay() {{
                const ov = document.getElementById('panelOverlay');
                if (ov) ov.addEventListener('click', () => this.closeAllPanels());
            }}

            togglePanel(name) {{
                const panels = {{
                    menu: document.getElementById('panelMenu'),
                    profile: document.getElementById('panelProfile'),
                    settings: document.getElementById('panelSettings'),
                    avia: document.getElementById('panelAvia')
                }};
                const overlay = document.getElementById('panelOverlay');
                if (this.activePanel === name) {{
                    this.closeAllPanels();
                }} else {{
                    Object.values(panels).forEach(p => {{ if(p) p.classList.remove('active'); }});
                    if (panels[name]) panels[name].classList.add('active');
                    if (overlay) overlay.classList.add('active');
                    this.activePanel = name;
                    if (name === 'avia') {{
                        const badge = document.getElementById('aviaBadge');
                        if (badge) badge.style.display = 'none';
                        setTimeout(() => {{
                            const inp = document.getElementById('aviaInput');
                            if (inp) inp.focus();
                        }}, 300);
                    }}
                }}
            }}

            closeAllPanels() {{
                document.querySelectorAll('.floating-panel').forEach(p => p.classList.remove('active'));
                const ov = document.getElementById('panelOverlay');
                if (ov) ov.classList.remove('active');
                this.activePanel = null;
            }}

            // ====== PLAYBACK ======

            bindPlayback() {{
                const playBtn = document.getElementById('playBtn');
                if (playBtn) {{
                    playBtn.addEventListener('click', () => this.togglePlay());
                }}
                const prevBtn = document.getElementById('prevBtn');
                if (prevBtn) prevBtn.addEventListener('click', () => this.seekTo(Math.max(0, this.currentTime - 5)));
                const nextBtn = document.getElementById('nextBtn');
                if (nextBtn) nextBtn.addEventListener('click', () => this.seekTo(Math.min(this.totalTime, this.currentTime + 5)));
            }}

            togglePlay() {{
                this.isPlaying = !this.isPlaying;
                const btn = document.getElementById('playBtn');
                if (this.isPlaying) {{
                    btn.innerHTML = '&#x23F8;';
                    btn.setAttribute('aria-label', 'Pausar');
                    this.playInterval = setInterval(() => {{
                        this.currentTime++;
                        if (this.currentTime >= this.totalTime) {{
                            this.currentTime = 0;
                            this.togglePlay();
                        }}
                        this.updateTimeUI();
                    }}, 1000);
                }} else {{
                    btn.innerHTML = '&#x25B6;';
                    btn.setAttribute('aria-label', 'Reproducir');
                    clearInterval(this.playInterval);
                }}
            }}

            seekTo(t) {{
                this.currentTime = Math.round(t);
                this.updateTimeUI();
            }}

            updateTimeUI() {{
                const cur = document.getElementById('timeCurrent');
                const fill = document.getElementById('progressFill');
                if (cur) cur.textContent = this.formatTime(this.currentTime);
                if (fill) fill.style.width = ((this.currentTime / this.totalTime) * 100) + '%';
            }}

            formatTime(s) {{
                const h = Math.floor(s / 3600);
                const m = Math.floor((s % 3600) / 60);
                const ss = s % 60;
                return [h, m, ss].map(v => String(v).padStart(2, '0')).join(':');
            }}

            bindProgressTrack() {{
                const track = document.getElementById('progressTrack');
                if (track) {{
                    track.addEventListener('click', (e) => {{
                        const rect = track.getBoundingClientRect();
                        const pct = (e.clientX - rect.left) / rect.width;
                        this.seekTo(pct * this.totalTime);
                    }});
                }}
            }}

            // ====== TOGGLES ======

            bindToggles() {{
                document.querySelectorAll('.toggle').forEach(t => {{
                    t.addEventListener('click', () => t.classList.toggle('active'));
                }});
            }}

            // ====== KEYBOARD ======

            bindKeyboard() {{
                document.addEventListener('keydown', (e) => {{
                    if (e.key === 'Escape') this.closeAllPanels();
                    if (e.key === ' ' && !this.activePanel && document.activeElement.tagName !== 'INPUT') {{
                        e.preventDefault();
                        this.togglePlay();
                    }}
                    if (e.ctrlKey && e.key === 'z') {{
                        e.preventDefault();
                        this.undo();
                    }}
                    if (e.ctrlKey && e.key === 'y') {{
                        e.preventDefault();
                        this.redo();
                    }}
                }});
            }}

            // ====== UNDO/REDO ======

            pushUndo(action) {{
                this.undoStack.push(action);
                this.redoStack = [];
            }}

            undo() {{
                if (this.undoStack.length > 0) {{
                    const a = this.undoStack.pop();
                    this.redoStack.push(a);
                    // REGLA 2: template literal para multilinea
                    this.addAviaMessage(`Deshecho: ${{a}}`, 'bot');
                }}
            }}

            redo() {{
                if (this.redoStack.length > 0) {{
                    const a = this.redoStack.pop();
                    this.undoStack.push(a);
                    this.addAviaMessage(`Rehecho: ${{a}}`, 'bot');
                }}
            }}

            // ====== MODE SELECTION ======

            bindModeSelection() {{
                document.querySelectorAll('.profile-mode').forEach(el => {{
                    el.addEventListener('click', () => {{
                        document.querySelectorAll('.profile-mode').forEach(m => m.classList.remove('active'));
                        el.classList.add('active');
                        const mode = el.dataset.mode;
                        this.currentMode = mode;
                        const label = document.getElementById('modeLabel');
                        const names = {{ pro: 'Profesional', prosumer: 'Prosumidor', consumer: 'Consumidor' }};
                        if (label) label.textContent = `Modo ${{names[mode] || mode}}`;
                    }});
                }});
            }}

            // ====== MENU ACTIONS ======

            bindMenuActions() {{
                document.querySelectorAll('.menu-item').forEach(item => {{
                    item.addEventListener('click', () => {{
                        const action = item.dataset.action;
                        this.handleMenuAction(action);
                        this.closeAllPanels();
                    }});
                }});
            }}

            handleMenuAction(action) {{
                // REGLA AVIA-AutoCorrector: Todos los strings multilinea usan backticks
                const actions = {{
                    project: 'Abriendo gestor de proyecto...',
                    import: 'Arrastra archivos al canvas o haz clic para seleccionar.',
                    cut: 'Clip cortado en la posicion actual. Ctrl+Z para deshacer.',
                    text: 'Titulo anadido al centro del video. Haz doble clic para editarlo.',
                    audio: 'Abriendo biblioteca de audio...',
                    effects: 'Panel de efectos abierto. Selecciona un efecto para previsualizar.',
                    filters: 'Filtros disponibles. Selecciona uno para aplicar.',
                    ai: 'Herramientas IA activadas. AVIA puede generar subtitulos, musica y mas.',
                    export: 'Configurando exportacion. Elige formato y calidad.'
                }};
                const msg = actions[action] || 'Accion no reconocida.';
                this.addAviaMessage(msg, 'bot');
                if (['cut', 'text', 'effects', 'filters'].includes(action)) {{
                    this.pushUndo(`Menu: ${{action}}`);
                }}
            }}

            // ====== AVIA CHAT ======

            bindAviaChat() {{
                const sendBtn = document.getElementById('btnSend');
                const input = document.getElementById('aviaInput');
                const micBtn = document.getElementById('btnMic');

                if (sendBtn) sendBtn.addEventListener('click', () => this.sendAviaMessage());
                if (input) input.addEventListener('keydown', (e) => {{
                    if (e.key === 'Enter') this.sendAviaMessage();
                }});
                if (micBtn) micBtn.addEventListener('click', () => this.toggleVoice());
            }}

            sendAviaMessage() {{
                const input = document.getElementById('aviaInput');
                if (!input) return;
                const text = input.value.trim();
                if (!text) return;
                this.addAviaMessage(text, 'user');
                input.value = '';
                this.processAviaCommand(text);
            }}

            addAviaMessage(text, type) {{
                const chat = document.getElementById('aviaChat');
                if (!chat) return;
                const div = document.createElement('div');
                div.className = `avia-msg ${{type}}`;
                div.textContent = text;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
            }}

            processAviaCommand(text) {{
                const lower = text.toLowerCase();
                let response = '';

                if (lower.includes('cortar') || lower.includes('cut')) {{
                    // REGLA 1: template literal (backtick), NO comillas simples
                    response = `He cortado el clip en la posicion actual (${{this.formatTime(this.currentTime)}}). Usa Ctrl+Z para deshacer.`;
                    this.pushUndo('Cortar clip via AVIA');

                }} else if (lower.includes('texto') || lower.includes('titulo') || lower.includes('title')) {{
                    response = `He anadido un titulo al centro del video. Haz doble clic para editarlo.`;
                    this.pushUndo('Texto via AVIA');

                }} else if (lower.includes('filtro') || lower.includes('filter')) {{
                    response = `He aplicado un filtro cinematografico al clip actual. Puedes cambiarlo desde Menu > Filtros.`;
                    this.pushUndo('Filtro via AVIA');

                }} else if (lower.includes('subtitulo') || lower.includes('subtitle')) {{
                    response = `Generando subtitulos automaticos con IA...`;
                    setTimeout(() => this.addAviaMessage('Subtitulos generados! Se anadieron 24 lineas de dialogo.', 'bot'), 2000);

                }} else if (lower.includes('musica') || lower.includes('music')) {{
                    response = `Buscando musica que combine con tu video...`;
                    setTimeout(() => this.addAviaMessage('He encontrado 3 pistas recomendadas. La primera ya esta aplicada.', 'bot'), 2500);

                }} else if (lower.includes('exportar') || lower.includes('export')) {{
                    response = `Para exportar, ve a Menu > Exportar o dime el formato: "exportar TikTok", "exportar YouTube", etc.`;

                }} else if (lower.includes('tiktok')) {{
                    response = `Configurando para TikTok (1080x1920, vertical). Exportando...`;
                    const resEl = document.getElementById('settingRes');
                    if (resEl) resEl.textContent = '1080x1920';
                    const badgeRes = document.getElementById('badgeRes');
                    if (badgeRes) badgeRes.textContent = '1080x1920';

                }} else if (lower.includes('ayuda') || lower.includes('help')) {{
                    // REGLA 1 CRITICA: template literal para multilinea
                    // NUNCA usar comillas simples con saltos de linea reales
                    response = [
                        'Puedo ayudarte con:',
                        '- "cortar" - Dividir clip',
                        '- "texto" - Anadir titulo',
                        '- "filtro" - Aplicar filtro',
                        '- "subtitulos" - Generar subs',
                        '- "musica" - Anadir audio',
                        '- "exportar" - Exportar video',
                        '- "tiktok" - Formato TikTok',
                        'Tambien puedes usar el microfono!'
                    ].join('\\n');

                }} else {{
                    const responses = [
                        `Entendido! Procesando tu solicitud: "${{text}}". Dame un momento...`,
                        `He analizado tu peticion. Te sugiero usar el menu de Herramientas IA.`,
                        `Buena idea! Procesando... Puedes seguir editando mientras tanto.`,
                        `Recibido. Trabajando en "${{text}}". Te notificare cuando termine.`
                    ];
                    response = responses[Math.floor(Math.random() * responses.length)];
                }}

                setTimeout(() => this.addAviaMessage(response, 'bot'), 500 + Math.random() * 800);
            }}

            // ====== VOICE ======

            toggleVoice() {{
                const micBtn = document.getElementById('btnMic');
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                    this.addAviaMessage('Tu navegador no soporta reconocimiento de voz. Usa Chrome.', 'bot');
                    return;
                }}

                if (this.isRecording) {{
                    if (this.recognition) this.recognition.stop();
                    this.isRecording = false;
                    if (micBtn) micBtn.classList.remove('recording');
                    return;
                }}

                const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
                this.recognition = new SR();
                this.recognition.lang = 'es-ES';
                this.recognition.continuous = false;
                this.recognition.interimResults = false;

                this.recognition.onresult = (e) => {{
                    const text = e.results[0][0].transcript;
                    const input = document.getElementById('aviaInput');
                    if (input) input.value = text;
                    this.sendAviaMessage();
                }};

                this.recognition.onend = () => {{
                    this.isRecording = false;
                    if (micBtn) micBtn.classList.remove('recording');
                }};

                this.recognition.onerror = () => {{
                    this.isRecording = false;
                    if (micBtn) micBtn.classList.remove('recording');
                }};

                this.recognition.start();
                this.isRecording = true;
                if (micBtn) micBtn.classList.add('recording');
                this.addAviaMessage('Escuchando... habla ahora.', 'bot');
            }}
        }}

        // Inicializar
        document.addEventListener('DOMContentLoaded', () => {{
            window.aviaProsumer = new AVIAProsumer();
        }});
    </script>
</body>
</html>'''
        return html

    def run(self):
        user_text = poe.query.text.strip() if poe.query.text else ""

        # Obtener respuesta inteligente de AVIA via TestBotBLKENPtt3D
        avia_greeting = ""
        if user_text:
            with poe.start_message() as msg:
                msg.write("Cargando AVIA Video Prosumidor v2.0...\n")
                msg.write("Consultando constelacion AVIA via TestBotBLKENPtt3D...\n")

            try:
                avia_greeting = self.get_avia_response(user_text)
            except Exception:
                avia_greeting = ""

        # Generar el HTML
        html_content = self.build_html(avia_greeting)

        # Contar backticks maximos en el HTML para el wrapper
        max_consecutive = 0
        current = 0
        for ch in html_content:
            if ch == '`':
                current += 1
                max_consecutive = max(max_consecutive, current)
            else:
                current = 0
        wrapper_ticks = '`' * max(4, max_consecutive + 1)

        # Output como Canvas HTML
        with poe.start_message() as msg:
            msg.write(f"{wrapper_ticks}html\n{html_content}\n{wrapper_ticks}\n")


if __name__ == "__main__":
    bot = AVIAVideoProsumidor()
    bot.run()

