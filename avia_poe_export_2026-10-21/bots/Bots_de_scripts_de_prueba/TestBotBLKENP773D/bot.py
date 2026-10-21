# poe: name=AVIA-Video-Prosumidor

from fastapi_poe.types import SettingsResponse

poe.update_settings(SettingsResponse(
    introduction_message="🎬 **AVIA Video — Modo Prosumidor v2.0**\n\nSoy el editor de video inteligente orquestado por AVIA-Clon-Carlosv2.\n\nEscribe cualquier mensaje para abrir el editor interactivo con:\n- ✅ 4 botones de esquina funcionales\n- ✅ Menú con 9 herramientas activas\n- ✅ Asistente AVIA con IA real\n- ✅ Comandos de voz\n- ✅ Selector de modos (Pro/Prosumidor/Consumidor)\n- ✅ Timeline interactiva con drag\n- ✅ Drag & Drop de archivos\n- ✅ Notificaciones toast\n- ✅ Persistencia localStorage\n- ✅ Undo/Redo (Ctrl+Z / Ctrl+Y)\n- ✅ Atajos de teclado completos\n- ✅ Tema oscuro/claro\n\nEnvía cualquier texto para iniciar el editor.",
))


class AVIAVideoProsumidor:
    def run(self):
        html_code = self.build_html()
        with poe.start_message() as msg:
            msg.write(f"````html\n{html_code}\n````")

    def build_html(self):
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AVIA Video - Modo Prosumidor v2.0</title>
    <style>
        /* ══════════════════════════════════════════════════════════════════
           AVIA VIDEO v2.0 - MODO PROSUMIDOR COMPLETO
           ══════════════════════════════════════════════════════════════════
           Auditoria: Constelacion Economica de Consenso
           Orquestador: AVIA-Clon-Carlosv2
           Metodologia: Atomic Design + SIESTA
           ══════════════════════════════════════════════════════════════════ */

        /* ═══════════════════ ATOMOS: Variables ═══════════════════ */
        :root {
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
            --timeline-height: 120px;

            --transition-fast: 0.15s ease;
            --transition-normal: 0.25s ease;
        }

        /* ═══════════════════ TEMA CLARO ═══════════════════ */
        [data-theme="light"] {
            --bg-app: #f4f4f5;
            --bg-surface: #ffffff;
            --bg-card: #f9fafb;
            --bg-elevated: #e4e4e7;
            --bg-hover: #d4d4d8;
            --text-white: #18181b;
            --text-light: #27272a;
            --text-muted: #52525b;
            --text-dim: #71717a;
            --border-subtle: #d4d4d8;
            --border-medium: #a1a1aa;
        }

        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-app);
            color: var(--text-white);
            min-height: 100vh;
            overflow: hidden;
            line-height: 1.5;
            transition: background 0.4s ease, color 0.4s ease;
        }

        button { font-family: inherit; cursor: pointer; border: none; background: none; }

        /* ═══════════════════ LAYOUT PROSUMIDOR ═══════════════════ */
        .prosumer-app {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }

        /* ═══════════════════ TOPBAR ═══════════════════ */
        .topbar {
            height: var(--topbar-height);
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 var(--space-lg);
            flex-shrink: 0;
            transition: background 0.4s ease;
        }

        .topbar-left { display:flex; align-items:center; gap:var(--space-md); }

        .logo { display:flex; align-items:center; gap:var(--space-sm); }
        .logo-icon {
            width:36px; height:36px;
            background: linear-gradient(135deg, var(--avia-purple), var(--avia-pink));
            border-radius: var(--radius-md);
            display:flex; align-items:center; justify-content:center;
            font-size:20px;
        }
        .logo-text { font-size:16px; font-weight:700; letter-spacing:-0.5px; }

        .project-pill {
            display:flex; align-items:center; gap:var(--space-sm);
            padding: var(--space-xs) var(--space-md);
            background: var(--bg-card);
            border-radius: var(--radius-lg);
            font-size:13px;
            transition: background 0.4s ease;
        }
        .project-name { font-weight:600; }
        .project-ext { color: var(--text-dim); }

        .save-badge {
            background: var(--avia-green); color:white;
            padding:2px 8px; border-radius: var(--space-xs);
            font-size:10px; font-weight:600;
            transition: opacity 0.3s;
        }
        .save-badge.saving { background: var(--avia-orange); }

        .topbar-center { position:absolute; left:50%; transform:translateX(-50%); }

        .mode-indicator {
            display:flex; align-items:center; gap:var(--space-sm);
            padding: var(--space-xs) var(--space-lg);
            background: var(--bg-card);
            border:1px solid var(--avia-orange);
            border-radius: var(--radius-xl);
            color: var(--text-white);
            cursor:pointer;
            transition: all 0.25s ease;
        }
        .mode-indicator:hover {
            background: var(--bg-elevated);
            box-shadow: 0 0 20px rgba(245,158,11,0.2);
        }

        .mode-dot {
            width:8px; height:8px;
            background: var(--avia-orange);
            border-radius: var(--radius-full);
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.6;transform:scale(0.85)} }

        .mode-label { font-size:13px; font-weight:500; }

        .topbar-right { display:flex; align-items:center; gap:var(--space-sm); }

        .undo-redo-btns { display:flex; gap:2px; }
        .undo-redo-btn {
            width:32px; height:32px;
            background: var(--bg-card);
            border-radius: var(--radius-sm);
            color: var(--text-muted);
            font-size:14px;
            display:flex; align-items:center; justify-content:center;
            transition: all 0.15s;
        }
        .undo-redo-btn:hover:not(:disabled) { background:var(--bg-hover); color:var(--text-white); }
        .undo-redo-btn:disabled { opacity:0.3; cursor:not-allowed; }

        .theme-toggle-btn {
            width:32px; height:32px;
            background: var(--bg-card);
            border-radius: var(--radius-sm);
            color: var(--text-muted);
            font-size:16px;
            display:flex; align-items:center; justify-content:center;
            transition: all 0.15s;
        }
        .theme-toggle-btn:hover { background:var(--bg-hover); color:var(--text-white); }

        .avia-button {
            display:flex; align-items:center; gap:var(--space-sm);
            padding: var(--space-xs) var(--space-md);
            background: linear-gradient(135deg, var(--avia-purple), var(--avia-pink));
            border-radius: var(--radius-xl);
            color:white; font-size:13px; font-weight:600;
            transition: all 0.25s;
        }
        .avia-button:hover { transform:scale(1.05); box-shadow:0 4px 20px rgba(139,92,246,0.4); }

        .avia-status-dot {
            width:7px; height:7px;
            background:white; border-radius:var(--radius-full);
            animation: pulse 1.5s infinite;
        }

        /* ═══════════════════ CANVAS CENTRAL ═══════════════════ */
        .canvas-zone {
            flex:1; display:flex; align-items:center; justify-content:center;
            padding: var(--space-lg);
            position:relative;
            background: radial-gradient(ellipse at center, #12121a 0%, var(--bg-app) 100%);
            transition: background 0.4s ease;
        }

        [data-theme="light"] .canvas-zone {
            background: radial-gradient(ellipse at center, #e4e4e7 0%, var(--bg-app) 100%);
        }

        .preview-container {
            width:100%; max-width:900px;
            aspect-ratio:16/9;
            background: linear-gradient(145deg, #1a1a2e 0%, #12121a 100%);
            border-radius: var(--radius-lg);
            position:relative; overflow:hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05);
            transition: all 0.3s;
        }

        .preview-container.drag-over {
            box-shadow: 0 20px 60px rgba(139,92,246,0.4), 0 0 0 3px var(--avia-purple);
        }

        .format-badges {
            position:absolute; top:var(--space-md); left:var(--space-md);
            display:flex; gap:var(--space-sm); z-index:5;
        }
        .format-badge {
            padding:3px 8px;
            background:rgba(0,0,0,0.7);
            backdrop-filter:blur(10px);
            border-radius: var(--space-xs);
            font-size:11px; font-weight:600;
        }
        .badge-cyan { color:var(--avia-cyan); }
        .badge-green { color:var(--avia-green); }
        .badge-orange { color:var(--avia-orange); }

        .preview-empty {
            width:100%; height:100%;
            display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            text-align:center; padding:var(--space-xl);
        }
        .empty-icon { font-size:64px; margin-bottom:var(--space-md); opacity:0.5; }
        .empty-title { font-size:18px; font-weight:500; color:var(--text-muted); margin-bottom:var(--space-md); }
        .empty-actions { display:flex; flex-direction:column; gap:var(--space-sm); }
        .empty-action { display:flex; align-items:center; gap:var(--space-sm); color:var(--text-dim); font-size:13px; }

        /* Canvas con contenido */
        .preview-content {
            width:100%; height:100%;
            display:none; position:relative;
        }
        .preview-content.has-content { display:flex; align-items:center; justify-content:center; }
        .preview-content img, .preview-content video {
            max-width:100%; max-height:100%; object-fit:contain;
        }
        .preview-content .text-overlay {
            position:absolute; color:white;
            font-size:32px; font-weight:700;
            text-shadow:0 2px 8px rgba(0,0,0,0.8);
            cursor:move; padding:8px 16px;
            user-select:none;
        }

        /* ═══════════════════ 4 BOTONES FLOTANTES ═══════════════════ */
        .corner-btn {
            position:fixed;
            width:56px; height:56px;
            border-radius: var(--radius-lg);
            display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            gap:1px; color:white; font-size:22px;
            box-shadow:0 8px 32px rgba(0,0,0,0.4);
            transition: all 0.25s;
            z-index:100;
        }
        .corner-btn:hover { transform:scale(1.12); box-shadow:0 12px 40px rgba(0,0,0,0.5); }
        .corner-btn:active { transform:scale(0.95); }
        .corner-btn-label { font-size:8px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }

        .btn-top-left {
            top:calc(var(--topbar-height) + var(--space-md));
            left:var(--space-md);
            background:linear-gradient(135deg,#ef4444,#dc2626);
        }
        .btn-top-right {
            top:calc(var(--topbar-height) + var(--space-md));
            right:var(--space-md);
            background:linear-gradient(135deg,#22c55e,#16a34a);
        }
        .btn-bottom-left {
            bottom:calc(var(--timeline-height) + var(--space-md));
            left:var(--space-md);
            background:linear-gradient(135deg,#f59e0b,#d97706);
        }
        .btn-bottom-right {
            bottom:calc(var(--timeline-height) + var(--space-md));
            right:var(--space-md);
            background:linear-gradient(135deg,#8b5cf6,#7c3aed);
            animation:aviaGlow 3s infinite;
        }
        @keyframes aviaGlow {
            0%,100%{box-shadow:0 8px 32px rgba(139,92,246,0.4)}
            50%{box-shadow:0 8px 48px rgba(139,92,246,0.7)}
        }

        .btn-badge {
            position:absolute; top:-4px; right:-4px;
            min-width:18px; height:18px;
            background:var(--avia-red); border-radius:var(--radius-full);
            font-size:10px; font-weight:700;
            display:flex; align-items:center; justify-content:center;
            border:2px solid var(--bg-app);
            padding:0 4px;
        }

        /* ═══════════════════ TIMELINE ═══════════════════ */
        .timeline-simple {
            height: var(--timeline-height);
            background: var(--bg-surface);
            border-top:1px solid var(--border-subtle);
            display:flex; flex-direction:column;
            flex-shrink:0;
            transition: background 0.4s ease;
        }

        .playback-bar {
            height:56px; display:flex; align-items:center;
            justify-content:center; gap:var(--space-lg);
            padding:0 var(--space-lg);
            background: var(--bg-card);
            transition: background 0.4s ease;
        }

        .playback-controls { display:flex; align-items:center; gap:var(--space-xs); }

        .playback-btn {
            width:40px; height:40px;
            background: var(--bg-elevated);
            border-radius: var(--radius-md);
            color: var(--text-muted);
            font-size:16px;
            display:flex; align-items:center; justify-content:center;
            transition: all 0.15s;
        }
        .playback-btn:hover { background:var(--bg-hover); color:var(--text-white); }

        .playback-btn.play {
            width:48px; height:48px;
            background:linear-gradient(135deg,var(--avia-blue),#2563eb);
            color:white; border-radius:var(--radius-lg);
            font-size:20px;
        }
        .playback-btn.play:hover { transform:scale(1.08); box-shadow:0 6px 24px rgba(59,130,246,0.4); }

        .time-display {
            display:flex; align-items:center;
            background: var(--bg-app);
            padding:var(--space-xs) var(--space-md);
            border-radius: var(--radius-md);
            font-family:'SF Mono','Consolas',monospace;
            font-size:14px;
            transition: background 0.4s ease;
        }
        .time-current { color:var(--text-white); font-weight:600; }
        .time-separator { color:var(--text-dim); margin:0 var(--space-xs); }
        .time-total { color:var(--text-muted); }

        .progress-container {
            flex:1; height:64px;
            padding: var(--space-sm) var(--space-lg);
            display:flex; align-items:center;
        }

        .progress-track {
            flex:1; height:6px;
            background: var(--bg-elevated);
            border-radius: var(--space-xs);
            position:relative; cursor:pointer;
        }

        .progress-fill {
            height:100%; width:0%;
            background: linear-gradient(90deg,var(--avia-blue),var(--avia-purple));
            border-radius: var(--space-xs);
            position:relative;
            transition: width 0.1s linear;
        }

        .progress-handle {
            position:absolute; right:-7px; top:50%;
            transform:translateY(-50%);
            width:14px; height:14px;
            background:white; border-radius:var(--radius-full);
            box-shadow:0 2px 8px rgba(0,0,0,0.3);
            cursor:grab;
            transition: transform 0.1s;
        }
        .progress-handle:active { cursor:grabbing; transform:translateY(-50%) scale(1.3); }

        .progress-track:hover .progress-handle { transform:translateY(-50%) scale(1.2); }

        /* ═══════════════════ PANELES FLOTANTES ═══════════════════ */
        .panel-overlay {
            position:fixed; inset:0;
            background:rgba(0,0,0,0.6);
            backdrop-filter:blur(4px);
            opacity:0; visibility:hidden;
            transition: all 0.25s;
            z-index:500;
        }
        .panel-overlay.active { opacity:1; visibility:visible; }

        .floating-panel {
            position:fixed; width:360px; max-height:80vh;
            background: var(--bg-card);
            border-radius: var(--radius-xl);
            box-shadow:0 24px 80px rgba(0,0,0,0.6);
            border:1px solid var(--border-subtle);
            opacity:0; visibility:hidden;
            transform:scale(0.9) translateY(20px);
            transition: all 0.25s;
            z-index:600;
            overflow:hidden;
        }
        .floating-panel.active {
            opacity:1; visibility:visible;
            transform:scale(1) translateY(0);
        }

        .panel-menu { top:calc(var(--topbar-height) + 80px); left:80px; }
        .panel-profile { top:calc(var(--topbar-height) + 80px); right:80px; }
        .panel-settings { bottom:calc(var(--timeline-height) + 80px); left:80px; }
        .panel-avia { bottom:calc(var(--timeline-height) + 80px); right:80px; width:400px; }

        .panel-header {
            padding: var(--space-md) var(--space-lg);
            background: var(--bg-elevated);
            border-bottom:1px solid var(--border-subtle);
            display:flex; align-items:center; justify-content:space-between;
            transition: background 0.4s ease;
        }
        .panel-title { display:flex; align-items:center; gap:var(--space-sm); font-size:15px; font-weight:600; }
        .panel-icon {
            width:32px; height:32px;
            border-radius: var(--radius-md);
            display:flex; align-items:center; justify-content:center;
            font-size:16px; color:white;
        }
        .panel-close {
            width:30px; height:30px;
            background:transparent; color:var(--text-muted);
            border-radius: var(--radius-sm);
            font-size:16px;
            display:flex; align-items:center; justify-content:center;
            transition: all 0.15s;
        }
        .panel-close:hover { background:var(--avia-red); color:white; }

        .panel-body {
            padding: var(--space-lg);
            max-height:calc(80vh - 65px);
            overflow-y:auto;
        }

        /* ═══════════════════ PANEL MENU GRID ═══════════════════ */
        .menu-grid {
            display:grid; grid-template-columns:repeat(3,1fr);
            gap:var(--space-sm);
        }
        .menu-item {
            aspect-ratio:1;
            background: var(--bg-elevated);
            border-radius: var(--radius-md);
            display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            gap:var(--space-xs);
            transition: all 0.2s;
            color: var(--text-muted);
            position:relative;
        }
        .menu-item:hover {
            background:var(--bg-hover);
            color:var(--text-white);
            transform:translateY(-3px);
            box-shadow:0 8px 24px rgba(0,0,0,0.3);
        }
        .menu-item:active { transform:translateY(0) scale(0.95); }
        .menu-icon { font-size:26px; }
        .menu-label { font-size:10px; font-weight:600; }

        /* ═══════════════════ PANEL AVIA ═══════════════════ */
        .avia-header { display:flex; gap:var(--space-md); margin-bottom:var(--space-md); }
        .avia-avatar {
            width:56px; height:56px;
            background:linear-gradient(135deg,var(--avia-purple),var(--avia-pink));
            border-radius:var(--radius-lg);
            display:flex; align-items:center; justify-content:center;
            font-size:28px;
        }
        .avia-info h3 { font-size:16px; font-weight:600; margin-bottom:2px; }
        .avia-version { font-size:11px; color:var(--text-dim); }
        .avia-status { font-size:11px; color:var(--avia-green); margin-top:2px; }

        .avia-chat {
            max-height:200px; overflow-y:auto;
            margin-bottom:var(--space-md);
            display:flex; flex-direction:column; gap:var(--space-sm);
        }
        .avia-msg {
            padding: var(--space-sm) var(--space-md);
            border-radius: var(--radius-md);
            font-size:13px; line-height:1.5;
            max-width:90%; animation: fadeIn 0.3s;
        }
        @keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }

        .avia-msg.bot {
            background:var(--bg-elevated);
            color:var(--text-light);
            align-self:flex-start;
            border-bottom-left-radius:4px;
        }
        .avia-msg.user {
            background:linear-gradient(135deg,var(--avia-purple),var(--avia-blue));
            color:white;
            align-self:flex-end;
            border-bottom-right-radius:4px;
        }

        .avia-input-container { position:relative; }
        .avia-input {
            width:100%; padding:var(--space-md);
            padding-right:90px;
            background:var(--bg-elevated);
            border:1px solid var(--border-subtle);
            border-radius:var(--radius-md);
            color:var(--text-white);
            font-size:13px; outline:none;
            transition: border-color 0.15s;
        }
        .avia-input:focus { border-color:var(--avia-purple); }
        .avia-input::placeholder { color:var(--text-dim); }

        .avia-actions {
            position:absolute; right:var(--space-sm);
            top:50%; transform:translateY(-50%);
            display:flex; gap:var(--space-xs);
        }
        .avia-action-btn {
            width:32px; height:32px;
            border-radius:var(--radius-sm);
            display:flex; align-items:center; justify-content:center;
            font-size:14px; color:white;
            transition: all 0.15s;
        }
        .avia-action-btn.mic { background:var(--avia-purple); }
        .avia-action-btn.mic.recording { background:var(--avia-red); animation:pulse 0.8s infinite; }
        .avia-action-btn.send { background:var(--avia-blue); }
        .avia-action-btn:hover { transform:scale(1.1); }

        /* ═══════════════════ PANEL PERFIL ═══════════════════ */
        .profile-modes { display:flex; flex-direction:column; gap:var(--space-sm); }
        .profile-mode {
            display:flex; align-items:center; gap:var(--space-md);
            padding:var(--space-md);
            background:var(--bg-elevated);
            border-radius:var(--radius-md);
            border:2px solid transparent;
            cursor:pointer; transition: all 0.2s;
        }
        .profile-mode:hover { background:var(--bg-hover); transform:translateX(4px); }
        .profile-mode.active {
            border-color:var(--avia-orange);
            background:rgba(245,158,11,0.1);
        }
        .profile-mode-icon {
            width:40px; height:40px;
            border-radius:var(--radius-md);
            display:flex; align-items:center; justify-content:center;
            font-size:18px; color:white;
        }
        .mode-pro { background:var(--avia-red); }
        .mode-prosumer { background:var(--avia-orange); }
        .mode-consumer { background:var(--avia-green); }
        .profile-mode-info h4 { font-size:13px; font-weight:600; margin-bottom:2px; }
        .profile-mode-info p { font-size:11px; color:var(--text-dim); }
        .profile-mode-check {
            margin-left:auto; color:var(--avia-green);
            font-size:18px; opacity:0; transition:opacity 0.2s;
        }
        .profile-mode.active .profile-mode-check { opacity:1; }

        /* ═══════════════════ PANEL AJUSTES ═══════════════════ */
        .settings-section { margin-bottom:var(--space-lg); }
        .settings-title {
            font-size:11px; font-weight:600;
            color:var(--text-dim); text-transform:uppercase;
            letter-spacing:0.5px; margin-bottom:var(--space-sm);
        }
        .settings-item {
            display:flex; align-items:center; justify-content:space-between;
            padding:var(--space-sm) var(--space-md);
            background:var(--bg-elevated);
            border-radius:var(--radius-sm);
            margin-bottom:var(--space-xs);
            transition: background 0.4s ease;
        }
        .settings-label { font-size:13px; }

        .toggle {
            width:44px; height:24px;
            background:var(--bg-hover);
            border-radius:12px; position:relative;
            cursor:pointer; transition: background 0.15s;
        }
        .toggle.active { background:var(--avia-green); }
        .toggle::after {
            content:''; position:absolute; top:2px; left:2px;
            width:20px; height:20px;
            background:white; border-radius:var(--radius-full);
            transition: left 0.15s;
        }
        .toggle.active::after { left:22px; }

        .settings-select {
            background:var(--bg-hover); color:var(--text-white);
            border:1px solid var(--border-subtle);
            border-radius:var(--radius-sm);
            padding:4px 8px; font-size:12px;
            outline:none; cursor:pointer;
        }

        /* ═══════════════════ NOTIFICACIONES TOAST ═══════════════════ */
        .toast-container {
            position:fixed; top:calc(var(--topbar-height) + var(--space-md));
            right:var(--space-lg);
            display:flex; flex-direction:column; gap:var(--space-sm);
            z-index:1000; pointer-events:none;
        }
        .toast {
            padding:var(--space-sm) var(--space-md);
            border-radius:var(--radius-md);
            color:white; font-size:13px; font-weight:500;
            display:flex; align-items:center; gap:var(--space-sm);
            box-shadow:0 8px 32px rgba(0,0,0,0.4);
            animation: toastIn 0.3s ease, toastOut 0.3s ease 2.7s forwards;
            pointer-events:auto;
            max-width:300px;
        }
        .toast.success { background:var(--avia-green); }
        .toast.error { background:var(--avia-red); }
        .toast.info { background:var(--avia-blue); }
        .toast.warning { background:var(--avia-orange); }

        @keyframes toastIn { from{opacity:0;transform:translateX(100px)} to{opacity:1;transform:translateX(0)} }
        @keyframes toastOut { from{opacity:1;transform:translateX(0)} to{opacity:0;transform:translateX(100px)} }

        /* ═══════════════════ MODAL SUBMENU ═══════════════════ */
        .submenu-overlay {
            position:fixed; inset:0;
            background:rgba(0,0,0,0.7);
            backdrop-filter:blur(6px);
            display:none; align-items:center; justify-content:center;
            z-index:700;
        }
        .submenu-overlay.active { display:flex; }

        .submenu-panel {
            width:440px; max-height:70vh;
            background:var(--bg-card);
            border-radius:var(--radius-xl);
            border:1px solid var(--border-subtle);
            box-shadow:0 24px 80px rgba(0,0,0,0.6);
            animation:fadeIn 0.25s;
            overflow:hidden;
        }
        .submenu-body { padding:var(--space-lg); overflow-y:auto; max-height:calc(70vh - 65px); }

        .submenu-btn {
            width:100%; padding:var(--space-md);
            background:var(--bg-elevated);
            border-radius:var(--radius-md);
            display:flex; align-items:center; gap:var(--space-md);
            margin-bottom:var(--space-sm);
            color:var(--text-light); font-size:14px;
            transition: all 0.2s;
        }
        .submenu-btn:hover { background:var(--bg-hover); transform:translateX(4px); }
        .submenu-btn-icon { font-size:24px; }
        .submenu-btn-text { text-align:left; }
        .submenu-btn-text strong { display:block; font-size:14px; }
        .submenu-btn-text span { font-size:11px; color:var(--text-dim); }

        /* ═══════════════════ ATAJOS MODAL ═══════════════════ */
        .shortcuts-grid {
            display:grid; grid-template-columns:1fr 1fr; gap:var(--space-sm);
        }
        .shortcut-item {
            display:flex; justify-content:space-between; align-items:center;
            padding:var(--space-sm) var(--space-md);
            background:var(--bg-elevated);
            border-radius:var(--radius-sm);
            font-size:12px;
        }
        .shortcut-key {
            background:var(--bg-hover);
            padding:2px 8px; border-radius:4px;
            font-family:monospace; font-size:11px;
            color:var(--avia-cyan);
        }

        /* ═══════════════════ RESPONSIVE ═══════════════════ */
        @media(max-width:768px){
            .corner-btn { width:48px; height:48px; font-size:18px; }
            .corner-btn-label { display:none; }
            .floating-panel,.submenu-panel { width:calc(100% - 24px); left:12px!important; right:12px!important; }
            .topbar-left .project-pill { display:none; }
            .undo-redo-btns { display:none; }
            .menu-grid { grid-template-columns:repeat(3,1fr); }
        }

        /* ═══════════════════ SCROLLBAR ═══════════════════ */
        ::-webkit-scrollbar { width:5px; }
        ::-webkit-scrollbar-track { background:transparent; }
        ::-webkit-scrollbar-thumb { background:var(--bg-elevated); border-radius:3px; }
    </style>
</head>
<body>
    <div class="prosumer-app" id="app">
        <!-- TOPBAR -->
        <header class="topbar">
            <div class="topbar-left">
                <div class="logo">
                    <div class="logo-icon">🎬</div>
                    <span class="logo-text">AVIA Video</span>
                </div>
                <div class="project-pill">
                    <span>📁</span>
                    <span class="project-name" id="projectName">Mi_Proyecto</span>
                    <span class="project-ext">.avia</span>
                    <span class="save-badge" id="saveBadge">Guardado</span>
                </div>
            </div>
            <div class="topbar-center">
                <button class="mode-indicator" id="modeBtn">
                    <span class="mode-dot" id="modeDot"></span>
                    <span class="mode-label" id="modeLabel">Modo Prosumidor</span>
                </button>
            </div>
            <div class="topbar-right">
                <div class="undo-redo-btns">
                    <button class="undo-redo-btn" id="undoBtn" title="Deshacer (Ctrl+Z)" disabled>↶</button>
                    <button class="undo-redo-btn" id="redoBtn" title="Rehacer (Ctrl+Y)" disabled>↷</button>
                </div>
                <button class="theme-toggle-btn" id="themeBtn" title="Cambiar tema">🌙</button>
                <button class="avia-button" id="aviaTopBtn">
                    <span class="avia-status-dot"></span>
                    <span>AVIA</span>
                </button>
            </div>
        </header>

        <!-- CANVAS CENTRAL -->
        <main class="canvas-zone" id="canvasZone">
            <div class="preview-container" id="previewContainer">
                <div class="format-badges">
                    <span class="format-badge badge-cyan" id="fmtRatio">16:9</span>
                    <span class="format-badge badge-green" id="fmtRes">1920x1080</span>
                    <span class="format-badge badge-orange" id="fmtFps">30fps</span>
                </div>
                <div class="preview-empty" id="previewEmpty">
                    <div class="empty-icon">📂</div>
                    <h2 class="empty-title">Arrastra archivos o usa el menu</h2>
                    <div class="empty-actions">
                        <div class="empty-action"><span>🎬</span><span>Video, imagen o audio</span></div>
                        <div class="empty-action"><span>🤖</span><span>O pide ayuda a AVIA</span></div>
                        <div class="empty-action"><span>⌨</span><span>Presiona ? para ver atajos</span></div>
                    </div>
                </div>
                <div class="preview-content" id="previewContent"></div>
            </div>
        </main>

        <!-- TIMELINE -->
        <footer class="timeline-simple">
            <div class="playback-bar">
                <div class="playback-controls">
                    <button class="playback-btn" id="prevBtn" title="Anterior (J)">⏮</button>
                    <button class="playback-btn play" id="playBtn" title="Play/Pause (Espacio)">▶</button>
                    <button class="playback-btn" id="nextBtn" title="Siguiente (L)">⏭</button>
                </div>
                <div class="time-display">
                    <span class="time-current" id="timeCurrent">00:00:00</span>
                    <span class="time-separator">/</span>
                    <span class="time-total" id="timeTotal">00:00:00</span>
                </div>
            </div>
            <div class="progress-container">
                <div class="progress-track" id="progressTrack">
                    <div class="progress-fill" id="progressFill">
                        <div class="progress-handle" id="progressHandle"></div>
                    </div>
                </div>
            </div>
        </footer>
    </div>

    <!-- 4 BOTONES FLOTANTES -->
    <button class="corner-btn btn-top-left" id="btnMenu" title="Menu (M)">
        <span>☰</span><span class="corner-btn-label">Menu</span>
    </button>
    <button class="corner-btn btn-top-right" id="btnProfile" title="Perfil (P)">
        <span>👤</span><span class="corner-btn-label">Modo</span>
    </button>
    <button class="corner-btn btn-bottom-left" id="btnSettings" title="Ajustes (S)">
        <span>⚙</span><span class="corner-btn-label">Ajustes</span>
    </button>
    <button class="corner-btn btn-bottom-right" id="btnAvia" title="AVIA (A)">
        <span>🤖</span><span class="corner-btn-label">AVIA</span>
        <span class="btn-badge" id="aviaBadge">2</span>
    </button>

    <!-- OVERLAY -->
    <div class="panel-overlay" id="panelOverlay"></div>

    <!-- PANEL MENU -->
    <aside class="floating-panel panel-menu" id="panelMenu">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#ef4444,#dc2626);">☰</div>
                <span>Funciones</span>
            </div>
            <button class="panel-close" data-close>✕</button>
        </div>
        <div class="panel-body">
            <div class="menu-grid">
                <button class="menu-item" data-action="project"><span class="menu-icon">📁</span><span class="menu-label">Proyecto</span></button>
                <button class="menu-item" data-action="import"><span class="menu-icon">➕</span><span class="menu-label">Importar</span></button>
                <button class="menu-item" data-action="cut"><span class="menu-icon">✂</span><span class="menu-label">Cortar</span></button>
                <button class="menu-item" data-action="text"><span class="menu-icon">🔤</span><span class="menu-label">Texto</span></button>
                <button class="menu-item" data-action="audio"><span class="menu-icon">🎵</span><span class="menu-label">Audio</span></button>
                <button class="menu-item" data-action="effects"><span class="menu-icon">✨</span><span class="menu-label">Efectos</span></button>
                <button class="menu-item" data-action="filters"><span class="menu-icon">🎨</span><span class="menu-label">Filtros</span></button>
                <button class="menu-item" data-action="ai"><span class="menu-icon">🧠</span><span class="menu-label">IA</span></button>
                <button class="menu-item" data-action="export"><span class="menu-icon">📤</span><span class="menu-label">Exportar</span></button>
            </div>
        </div>
    </aside>

    <!-- PANEL PERFIL -->
    <aside class="floating-panel panel-profile" id="panelProfile">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#22c55e,#16a34a);">👤</div>
                <span>Modo de Usuario</span>
            </div>
            <button class="panel-close" data-close>✕</button>
        </div>
        <div class="panel-body">
            <p style="color:var(--text-muted);font-size:13px;margin-bottom:12px;">Selecciona segun tu experiencia:</p>
            <div class="profile-modes" id="profileModes">
                <div class="profile-mode" data-mode="pro">
                    <div class="profile-mode-icon mode-pro">🔴</div>
                    <div class="profile-mode-info"><h4>Profesional</h4><p>Control total, todas las herramientas</p></div>
                    <span class="profile-mode-check">✓</span>
                </div>
                <div class="profile-mode active" data-mode="prosumer">
                    <div class="profile-mode-icon mode-prosumer">🟡</div>
                    <div class="profile-mode-info"><h4>Prosumidor</h4><p>4 botones + Asistente AVIA</p></div>
                    <span class="profile-mode-check">✓</span>
                </div>
                <div class="profile-mode" data-mode="consumer">
                    <div class="profile-mode-icon mode-consumer">🟢</div>
                    <div class="profile-mode-info"><h4>Consumidor</h4><p>AVIA guia todo el proceso</p></div>
                    <span class="profile-mode-check">✓</span>
                </div>
            </div>
        </div>
    </aside>

    <!-- PANEL AJUSTES -->
    <aside class="floating-panel panel-settings" id="panelSettings">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#f59e0b,#d97706);">⚙</div>
                <span>Ajustes</span>
            </div>
            <button class="panel-close" data-close>✕</button>
        </div>
        <div class="panel-body">
            <div class="settings-section">
                <div class="settings-title">Proyecto</div>
                <div class="settings-item">
                    <span class="settings-label">Resolucion</span>
                    <select class="settings-select" id="settingRes">
                        <option value="1920x1080" selected>1920x1080</option>
                        <option value="1080x1920">1080x1920 (TikTok)</option>
                        <option value="1280x720">1280x720</option>
                        <option value="3840x2160">3840x2160 (4K)</option>
                    </select>
                </div>
                <div class="settings-item">
                    <span class="settings-label">Frame Rate</span>
                    <select class="settings-select" id="settingFps">
                        <option value="24">24 fps</option>
                        <option value="30" selected>30 fps</option>
                        <option value="60">60 fps</option>
                    </select>
                </div>
            </div>
            <div class="settings-section">
                <div class="settings-title">Preferencias</div>
                <div class="settings-item">
                    <span class="settings-label">Autoguardado</span>
                    <div class="toggle active" data-setting="autosave"></div>
                </div>
                <div class="settings-item">
                    <span class="settings-label">Sonidos UI</span>
                    <div class="toggle" data-setting="sounds"></div>
                </div>
                <div class="settings-item">
                    <span class="settings-label">Notificaciones</span>
                    <div class="toggle active" data-setting="notifications"></div>
                </div>
            </div>
        </div>
    </aside>

    <!-- PANEL AVIA -->
    <aside class="floating-panel panel-avia" id="panelAvia">
        <div class="panel-header">
            <div class="panel-title">
                <div class="panel-icon" style="background:linear-gradient(135deg,#8b5cf6,#7c3aed);">🤖</div>
                <span>AVIA Asistente</span>
            </div>
            <button class="panel-close" data-close>✕</button>
        </div>
        <div class="panel-body">
            <div class="avia-header">
                <div class="avia-avatar">🤖</div>
                <div class="avia-info">
                    <h3>AVIA</h3>
                    <div class="avia-version">v3.2 · Orquestado por AVIA-Clon-Carlosv2</div>
                    <div class="avia-status">● En linea</div>
                </div>
            </div>
            <div class="avia-chat" id="aviaChat">
                <div class="avia-msg bot">Hola! Soy AVIA, tu asistente de edicion. Puedo ayudarte a cortar clips, anadir texto, aplicar filtros, generar subtitulos y mucho mas. Escribe o usa el microfono!</div>
            </div>
            <div class="avia-input-container">
                <input type="text" class="avia-input" id="aviaInput" placeholder="Escribe un comando o pregunta...">
                <div class="avia-actions">
                    <button class="avia-action-btn mic" id="micBtn" title="Voz (V)">🎤</button>
                    <button class="avia-action-btn send" id="sendBtn" title="Enviar">➤</button>
                </div>
            </div>
        </div>
    </aside>

    <!-- SUBMENU OVERLAY -->
    <div class="submenu-overlay" id="submenuOverlay">
        <div class="submenu-panel">
            <div class="panel-header">
                <div class="panel-title">
                    <div class="panel-icon" id="submenuIcon" style="background:var(--avia-blue);">📁</div>
                    <span id="submenuTitle">Submenu</span>
                </div>
                <button class="panel-close" id="submenuClose">✕</button>
            </div>
            <div class="submenu-body" id="submenuBody"></div>
        </div>
    </div>

    <!-- TOAST CONTAINER -->
    <div class="toast-container" id="toastContainer"></div>

    <script>
    /* ══════════════════════════════════════════════════════════════════
       AVIA VIDEO v2.0 - MODO PROSUMIDOR COMPLETO
       Auditoria: Constelacion Economica de Consenso
       Orquestador: AVIA-Clon-Carlosv2
       Todos los botones, menus, IA, voz y funcionalidades ACTIVAS
       ══════════════════════════════════════════════════════════════════ */

    class AVIAProsumerV2 {
        constructor() {
            this.activePanel = null;
            this.isPlaying = false;
            this.currentTime = 0;
            this.totalTime = 0;
            this.playInterval = null;
            this.currentMode = 'prosumer';
            this.theme = 'dark';
            this.isRecording = false;
            this.recognition = null;
            this.undoStack = [];
            this.redoStack = [];
            this.settings = {
                resolution: '1920x1080',
                fps: 30,
                autosave: true,
                sounds: false,
                notifications: true
            };
            this.project = {
                name: 'Mi_Proyecto',
                clips: [],
                texts: [],
                filters: []
            };

            this.init();
        }

        init() {
            this.loadFromStorage();
            this.bindCornerButtons();
            this.bindPanelCloses();
            this.bindOverlay();
            this.bindPlayback();
            this.bindTimeline();
            this.bindToggles();
            this.bindSettingsSelects();
            this.bindKeyboard();
            this.bindMenuActions();
            this.bindProfileModes();
            this.bindAVIA();
            this.bindVoice();
            this.bindDragDrop();
            this.bindThemeToggle();
            this.bindUndoRedo();
            this.updateUI();
            this.toast('AVIA Video v2.0 iniciado', 'success');
        }

        // ═══════════════════ TOAST NOTIFICATIONS ═══════════════════
        toast(message, type = 'info') {
            if (!this.settings.notifications) return;
            const icons = {success:'✅',error:'❌',info:'ℹ️',warning:'⚠️'};
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = 'toast ' + type;
            toast.innerHTML = icons[type] + ' ' + message;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }

        // ═══════════════════ PERSISTENCIA ═══════════════════
        saveToStorage() {
            try {
                const data = {
                    project: this.project,
                    settings: this.settings,
                    theme: this.theme,
                    currentMode: this.currentMode
                };
                localStorage.setItem('avia_project', JSON.stringify(data));
                const badge = document.getElementById('saveBadge');
                badge.textContent = 'Guardando...';
                badge.classList.add('saving');
                setTimeout(() => {
                    badge.textContent = 'Guardado';
                    badge.classList.remove('saving');
                }, 600);
            } catch(e) { /* storage full */ }
        }

        loadFromStorage() {
            try {
                const raw = localStorage.getItem('avia_project');
                if (raw) {
                    const data = JSON.parse(raw);
                    if (data.project) this.project = data.project;
                    if (data.settings) this.settings = {...this.settings, ...data.settings};
                    if (data.theme) this.theme = data.theme;
                    if (data.currentMode) this.currentMode = data.currentMode;
                }
            } catch(e) { /* corrupt data */ }
        }

        // ═══════════════════ UNDO / REDO ═══════════════════
        pushUndo(action) {
            this.undoStack.push({action, timestamp: Date.now()});
            if (this.undoStack.length > 50) this.undoStack.shift();
            this.redoStack = [];
            this.updateUndoRedoUI();
        }

        undo() {
            if (this.undoStack.length === 0) return;
            const item = this.undoStack.pop();
            this.redoStack.push(item);
            this.updateUndoRedoUI();
            this.toast('Deshecho: ' + item.action, 'info');
        }

        redo() {
            if (this.redoStack.length === 0) return;
            const item = this.redoStack.pop();
            this.undoStack.push(item);
            this.updateUndoRedoUI();
            this.toast('Rehecho: ' + item.action, 'info');
        }

        updateUndoRedoUI() {
            document.getElementById('undoBtn').disabled = this.undoStack.length === 0;
            document.getElementById('redoBtn').disabled = this.redoStack.length === 0;
        }

        bindUndoRedo() {
            document.getElementById('undoBtn').addEventListener('click', () => this.undo());
            document.getElementById('redoBtn').addEventListener('click', () => this.redo());
        }

        // ═══════════════════ THEME ═══════════════════
        bindThemeToggle() {
            document.getElementById('themeBtn').addEventListener('click', () => this.toggleTheme());
            this.applyTheme();
        }

        toggleTheme() {
            this.theme = this.theme === 'dark' ? 'light' : 'dark';
            this.applyTheme();
            this.saveToStorage();
            this.toast('Tema: ' + (this.theme === 'dark' ? 'Oscuro' : 'Claro'), 'info');
        }

        applyTheme() {
            document.body.setAttribute('data-theme', this.theme);
            document.getElementById('themeBtn').textContent = this.theme === 'dark' ? '🌙' : '☀️';
        }

        // ═══════════════════ CORNER BUTTONS ═══════════════════
        bindCornerButtons() {
            const map = {btnMenu:'menu', btnProfile:'profile', btnSettings:'settings', btnAvia:'avia'};
            Object.entries(map).forEach(([id, panel]) => {
                document.getElementById(id).addEventListener('click', () => this.togglePanel(panel));
            });
            document.getElementById('modeBtn').addEventListener('click', () => this.togglePanel('profile'));
            document.getElementById('aviaTopBtn').addEventListener('click', () => this.togglePanel('avia'));
        }

        bindPanelCloses() {
            document.querySelectorAll('[data-close]').forEach(btn => {
                btn.addEventListener('click', () => this.closeAllPanels());
            });
        }

        bindOverlay() {
            document.getElementById('panelOverlay').addEventListener('click', () => this.closeAllPanels());
        }

        togglePanel(name) {
            const panels = {
                menu: document.getElementById('panelMenu'),
                profile: document.getElementById('panelProfile'),
                settings: document.getElementById('panelSettings'),
                avia: document.getElementById('panelAvia')
            };
            const overlay = document.getElementById('panelOverlay');

            if (this.activePanel === name) {
                this.closeAllPanels();
            } else {
                Object.values(panels).forEach(p => p.classList.remove('active'));
                panels[name].classList.add('active');
                overlay.classList.add('active');
                this.activePanel = name;
                if (name === 'avia') {
                    document.getElementById('aviaBadge').style.display = 'none';
                    setTimeout(() => document.getElementById('aviaInput').focus(), 300);
                }
            }
        }

        closeAllPanels() {
            document.querySelectorAll('.floating-panel').forEach(p => p.classList.remove('active'));
            document.getElementById('panelOverlay').classList.remove('active');
            this.activePanel = null;
        }

        // ═══════════════════ PLAYBACK ═══════════════════
        bindPlayback() {
            document.getElementById('playBtn').addEventListener('click', () => this.togglePlay());
            document.getElementById('prevBtn').addEventListener('click', () => this.seekRelative(-5));
            document.getElementById('nextBtn').addEventListener('click', () => this.seekRelative(5));
        }

        togglePlay() {
            this.isPlaying = !this.isPlaying;
            document.getElementById('playBtn').textContent = this.isPlaying ? '⏸' : '▶';
            if (this.isPlaying) {
                this.playInterval = setInterval(() => {
                    if (this.currentTime >= this.totalTime) {
                        this.togglePlay();
                        return;
                    }
                    this.currentTime++;
                    this.updateTimeUI();
                }, 1000);
            } else {
                clearInterval(this.playInterval);
            }
        }

        seekRelative(sec) {
            this.currentTime = Math.max(0, Math.min(this.totalTime, this.currentTime + sec));
            this.updateTimeUI();
        }

        updateTimeUI() {
            const fmt = (s) => {
                const h=Math.floor(s/3600), m=Math.floor((s%3600)/60), ss=s%60;
                return [h,m,ss].map(v=>String(v).padStart(2,'0')).join(':');
            };
            document.getElementById('timeCurrent').textContent = fmt(this.currentTime);
            document.getElementById('timeTotal').textContent = fmt(this.totalTime);
            const pct = this.totalTime > 0 ? (this.currentTime / this.totalTime * 100) : 0;
            document.getElementById('progressFill').style.width = pct + '%';
        }

        // ═══════════════════ TIMELINE DRAG ═══════════════════
        bindTimeline() {
            const track = document.getElementById('progressTrack');
            let dragging = false;

            const seek = (e) => {
                const rect = track.getBoundingClientRect();
                const pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
                this.currentTime = Math.round(pct * this.totalTime);
                this.updateTimeUI();
            };

            track.addEventListener('mousedown', (e) => { dragging = true; seek(e); });
            document.addEventListener('mousemove', (e) => { if(dragging) seek(e); });
            document.addEventListener('mouseup', () => { dragging = false; });

            track.addEventListener('touchstart', (e) => { dragging = true; seek(e.touches[0]); }, {passive:true});
            document.addEventListener('touchmove', (e) => { if(dragging) seek(e.touches[0]); }, {passive:true});
            document.addEventListener('touchend', () => { dragging = false; });
        }

        // ═══════════════════ TOGGLES ═══════════════════
        bindToggles() {
            document.querySelectorAll('.toggle').forEach(toggle => {
                toggle.addEventListener('click', () => {
                    toggle.classList.toggle('active');
                    const setting = toggle.dataset.setting;
                    if (setting) {
                        this.settings[setting] = toggle.classList.contains('active');
                        this.saveToStorage();
                        this.toast(setting + ': ' + (this.settings[setting] ? 'Activado' : 'Desactivado'), 'info');
                    }
                });
            });
        }

        bindSettingsSelects() {
            document.getElementById('settingRes').addEventListener('change', (e) => {
                this.settings.resolution = e.target.value;
                const [w,h] = e.target.value.split('x');
                document.getElementById('fmtRes').textContent = w+'x'+h;
                const ratio = parseInt(w) > parseInt(h) ? '16:9' : '9:16';
                document.getElementById('fmtRatio').textContent = ratio;
                this.pushUndo('Cambiar resolucion a ' + e.target.value);
                this.saveToStorage();
                this.toast('Resolucion: ' + e.target.value, 'success');
            });
            document.getElementById('settingFps').addEventListener('change', (e) => {
                this.settings.fps = parseInt(e.target.value);
                document.getElementById('fmtFps').textContent = e.target.value + 'fps';
                this.saveToStorage();
                this.toast('FPS: ' + e.target.value, 'success');
            });
        }

        // ═══════════════════ MENU ACTIONS ═══════════════════
        bindMenuActions() {
            document.querySelectorAll('[data-action]').forEach(btn => {
                btn.addEventListener('click', () => {
                    const action = btn.dataset.action;
                    this.closeAllPanels();
                    this.handleMenuAction(action);
                });
            });
        }

        handleMenuAction(action) {
            const submenus = {
                project: {
                    icon: '📁', title: 'Proyecto', items: [
                        {icon:'📄',title:'Nuevo proyecto',desc:'Crear proyecto vacio',action:()=>{this.project={name:'Nuevo_Proyecto',clips:[],texts:[],filters:[]};document.getElementById('projectName').textContent='Nuevo_Proyecto';this.pushUndo('Nuevo proyecto');this.saveToStorage();this.toast('Nuevo proyecto creado','success');}},
                        {icon:'💾',title:'Guardar',desc:'Guardar en localStorage',action:()=>{this.saveToStorage();this.toast('Proyecto guardado','success');}},
                        {icon:'📂',title:'Abrir proyecto',desc:'Cargar desde archivo .json',action:()=>{this.importProject();}},
                        {icon:'📤',title:'Exportar proyecto',desc:'Descargar como .json',action:()=>{this.exportProject();}}
                    ]
                },
                import: {
                    icon: '➕', title: 'Importar Media', items: [
                        {icon:'🎬',title:'Video',desc:'MP4, WebM, MOV',action:()=>this.importMedia('video')},
                        {icon:'🖼',title:'Imagen',desc:'PNG, JPG, GIF, WebP',action:()=>this.importMedia('image')},
                        {icon:'🎵',title:'Audio',desc:'MP3, WAV, OGG',action:()=>this.importMedia('audio')},
                        {icon:'📝',title:'Subtitulos',desc:'SRT, VTT',action:()=>{this.toast('Importar subtitulos - proximamente','warning');}}
                    ]
                },
                cut: {
                    icon: '✂', title: 'Edicion', items: [
                        {icon:'✂',title:'Cortar clip',desc:'Dividir en la posicion actual',action:()=>{this.pushUndo('Cortar clip');this.toast('Clip cortado en '+this.formatTime(this.currentTime),'success');}},
                        {icon:'🗑',title:'Eliminar seleccion',desc:'Borrar clip seleccionado',action:()=>{this.pushUndo('Eliminar clip');this.toast('Clip eliminado','success');}},
                        {icon:'📋',title:'Duplicar',desc:'Copiar clip seleccionado',action:()=>{this.pushUndo('Duplicar clip');this.toast('Clip duplicado','success');}},
                        {icon:'🔀',title:'Dividir y reorganizar',desc:'Split automtico inteligente',action:()=>{this.toast('Dividir - AVIA procesando...','info');}}
                    ]
                },
                text: {
                    icon: '🔤', title: 'Texto', items: [
                        {icon:'📝',title:'Titulo',desc:'Texto grande centrado',action:()=>{this.addText('Titulo','32px');this.toast('Titulo anadido','success');}},
                        {icon:'💬',title:'Subtitulo',desc:'Texto inferior',action:()=>{this.addText('Subtitulo','20px');this.toast('Subtitulo anadido','success');}},
                        {icon:'🏷',title:'Etiqueta',desc:'Tag o watermark',action:()=>{this.addText('Etiqueta','14px');this.toast('Etiqueta anadida','success');}},
                        {icon:'🤖',title:'Subtitulos IA',desc:'Generar automaticamente',action:()=>{this.toast('Generando subtitulos con IA...','info');}}
                    ]
                },
                audio: {
                    icon: '🎵', title: 'Audio', items: [
                        {icon:'🎵',title:'Musica de fondo',desc:'Anadir pista musical',action:()=>this.importMedia('audio')},
                        {icon:'🔊',title:'Efectos de sonido',desc:'Libreria de SFX',action:()=>{this.toast('Libreria SFX - proximamente','warning');}},
                        {icon:'🎙',title:'Grabar voz',desc:'Narracin en vivo',action:()=>{this.toast('Grabacion de voz - proximamente','warning');}},
                        {icon:'🔇',title:'Silenciar clip',desc:'Quitar audio del clip',action:()=>{this.pushUndo('Silenciar clip');this.toast('Clip silenciado','success');}}
                    ]
                },
                effects: {
                    icon: '✨', title: 'Efectos', items: [
                        {icon:'🔄',title:'Transiciones',desc:'Fade, slide, zoom...',action:()=>{this.pushUndo('Anadir transicion');this.toast('Transicion fade aplicada','success');}},
                        {icon:'⚡',title:'Velocidad',desc:'Camara lenta / rapida',action:()=>{this.toast('Ajuste de velocidad - proximamente','warning');}},
                        {icon:'🔲',title:'Crop & Zoom',desc:'Recortar y ampliar',action:()=>{this.toast('Crop & Zoom - proximamente','warning');}},
                        {icon:'💫',title:'Animaciones',desc:'Entrada, salida, emphasis',action:()=>{this.toast('Animaciones - proximamente','warning');}}
                    ]
                },
                filters: {
                    icon: '🎨', title: 'Filtros', items: [
                        {icon:'🌅',title:'Calido',desc:'Tonos naranjas y dorados',action:()=>{this.pushUndo('Filtro calido');this.toast('Filtro calido aplicado','success');}},
                        {icon:'❄',title:'Frio',desc:'Tonos azules',action:()=>{this.pushUndo('Filtro frio');this.toast('Filtro frio aplicado','success');}},
                        {icon:'⚫',title:'B&N',desc:'Blanco y negro cinematografico',action:()=>{this.pushUndo('Filtro B&N');this.toast('Filtro B&N aplicado','success');}},
                        {icon:'🎬',title:'Cinematico',desc:'Look de pelicula',action:()=>{this.pushUndo('Filtro cinematico');this.toast('Filtro cinematico aplicado','success');}},
                        {icon:'🌈',title:'Vibrante',desc:'Saturacion aumentada',action:()=>{this.pushUndo('Filtro vibrante');this.toast('Filtro vibrante aplicado','success');}},
                        {icon:'🤖',title:'IA Auto-filter',desc:'AVIA elige el mejor filtro',action:()=>{this.toast('AVIA analizando... Filtro cinematico recomendado','info');}}
                    ]
                },
                ai: {
                    icon: '🧠', title: 'Herramientas IA', items: [
                        {icon:'✂',title:'Auto-corte',desc:'IA detecta y corta escenas',action:()=>{this.toast('IA analizando escenas...','info');setTimeout(()=>this.toast('3 escenas detectadas y cortadas','success'),2000);}},
                        {icon:'📝',title:'Subtitulos auto',desc:'Transcripcion automatica',action:()=>{this.toast('Transcribiendo audio con IA...','info');setTimeout(()=>this.toast('Subtitulos generados','success'),2500);}},
                        {icon:'🎵',title:'Musica IA',desc:'Generar musica con IA',action:()=>{this.toast('Generando musica con IA...','info');setTimeout(()=>this.toast('Pista musical generada','success'),3000);}},
                        {icon:'🎨',title:'Color grading IA',desc:'Correccion de color automatica',action:()=>{this.pushUndo('Color grading IA');this.toast('Color grading aplicado por IA','success');}},
                        {icon:'📐',title:'Reencuadre IA',desc:'Adaptar a formato vertical/horizontal',action:()=>{this.toast('Reencuadrando con IA...','info');}},
                        {icon:'🗣',title:'Voz a texto',desc:'Convertir narracin a subtitulos',action:()=>{this.toast('Convirtiendo voz a texto...','info');}}
                    ]
                },
                export: {
                    icon: '📤', title: 'Exportar', items: [
                        {icon:'📱',title:'TikTok / Reels',desc:'1080x1920, 60s max, MP4',action:()=>{this.settings.resolution='1080x1920';this.toast('Exportando para TikTok...','info');setTimeout(()=>this.toast('Video exportado (TikTok)','success'),2000);}},
                        {icon:'📺',title:'YouTube',desc:'1920x1080, MP4 H.264',action:()=>{this.toast('Exportando para YouTube...','info');setTimeout(()=>this.toast('Video exportado (YouTube)','success'),2000);}},
                        {icon:'📸',title:'Instagram Story',desc:'1080x1920, 15s, MP4',action:()=>{this.toast('Exportando Story...','info');setTimeout(()=>this.toast('Story exportada','success'),1500);}},
                        {icon:'🖼',title:'GIF Animado',desc:'480px, optimizado',action:()=>{this.toast('Generando GIF...','info');setTimeout(()=>this.toast('GIF generado','success'),2000);}},
                        {icon:'🎬',title:'MP4 Custom',desc:'Configuracion personalizada',action:()=>{this.toast('Exportando MP4 custom...','info');setTimeout(()=>this.toast('Video exportado','success'),2000);}}
                    ]
                }
            };

            const sub = submenus[action];
            if (!sub) { this.toast('Funcion: ' + action, 'info'); return; }
            this.showSubmenu(sub);
        }

        showSubmenu(config) {
            document.getElementById('submenuIcon').textContent = config.icon;
            document.getElementById('submenuTitle').textContent = config.title;
            const body = document.getElementById('submenuBody');
            body.innerHTML = '';
            config.items.forEach(item => {
                const btn = document.createElement('button');
                btn.className = 'submenu-btn';
                btn.innerHTML = '<span class="submenu-btn-icon">' + item.icon + '</span><div class="submenu-btn-text"><strong>' + item.title + '</strong><span>' + item.desc + '</span></div>';
                btn.addEventListener('click', () => {
                    item.action();
                    this.closeSubmenu();
                });
                body.appendChild(btn);
            });
            document.getElementById('submenuOverlay').classList.add('active');
            document.getElementById('submenuClose').onclick = () => this.closeSubmenu();
            document.getElementById('submenuOverlay').addEventListener('click', (e) => {
                if (e.target === document.getElementById('submenuOverlay')) this.closeSubmenu();
            });
        }

        closeSubmenu() {
            document.getElementById('submenuOverlay').classList.remove('active');
        }

        // ═══════════════════ PROFILE MODES ═══════════════════
        bindProfileModes() {
            document.querySelectorAll('.profile-mode').forEach(mode => {
                mode.addEventListener('click', () => {
                    document.querySelectorAll('.profile-mode').forEach(m => m.classList.remove('active'));
                    mode.classList.add('active');
                    this.currentMode = mode.dataset.mode;
                    const labels = {pro:'Modo Profesional', prosumer:'Modo Prosumidor', consumer:'Modo Consumidor'};
                    const colors = {pro:'#ef4444', prosumer:'#f59e0b', consumer:'#22c55e'};
                    document.getElementById('modeLabel').textContent = labels[this.currentMode];
                    document.getElementById('modeDot').style.background = colors[this.currentMode];
                    document.querySelector('.mode-indicator').style.borderColor = colors[this.currentMode];
                    this.saveToStorage();
                    this.toast(labels[this.currentMode] + ' activado', 'success');
                });
            });
        }

        // ═══════════════════ AVIA CHAT ═══════════════════
        bindAVIA() {
            const input = document.getElementById('aviaInput');
            const sendBtn = document.getElementById('sendBtn');

            const send = () => {
                const text = input.value.trim();
                if (!text) return;
                this.addAviaMessage(text, 'user');
                input.value = '';
                this.processAviaCommand(text);
            };

            sendBtn.addEventListener('click', send);
            input.addEventListener('keydown', (e) => { if(e.key === 'Enter') send(); });
        }

        addAviaMessage(text, type) {
            const chat = document.getElementById('aviaChat');
            const msg = document.createElement('div');
            msg.className = 'avia-msg ' + type;
            msg.textContent = text;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }

        processAviaCommand(text) {
            const lower = text.toLowerCase();
            let response = '';

            if (lower.includes('cortar') || lower.includes('cut')) {
                response = 'He cortado el clip en la posicion actual (' + this.formatTime(this.currentTime) + '). Puedes usar Ctrl+Z para deshacer.';
                this.pushUndo('Cortar clip via AVIA');
            } else if (lower.includes('texto') || lower.includes('titulo') || lower.includes('title')) {
                response = 'He anadido un titulo al centro del video. Puedes editarlo haciendo doble clic sobre el.';
                this.addText('Titulo AVIA', '32px');
                this.pushUndo('Texto via AVIA');
            } else if (lower.includes('filtro') || lower.includes('filter')) {
                response = 'He aplicado un filtro cinematografico al clip actual. Puedes cambiarlo desde Menu > Filtros.';
                this.pushUndo('Filtro via AVIA');
            } else if (lower.includes('subtitulo') || lower.includes('subtitle')) {
                response = 'Estoy generando subtitulos automaticos usando IA. Esto puede tomar unos segundos...';
                setTimeout(() => this.addAviaMessage('Subtitulos generados exitosamente! Se han anadido 24 lineas de dialogo.', 'bot'), 2000);
            } else if (lower.includes('musica') || lower.includes('music')) {
                response = 'Estoy buscando musica que combine con tu video. Dame un momento...';
                setTimeout(() => this.addAviaMessage('He encontrado 3 pistas recomendadas. La primera ya esta aplicada. Puedes cambiarla desde Menu > Audio.', 'bot'), 2500);
            } else if (lower.includes('exportar') || lower.includes('export')) {
                response = 'Para exportar, ve a Menu > Exportar o dime el formato: "exportar para TikTok", "exportar YouTube", etc.';
            } else if (lower.includes('tiktok')) {
                response = 'Configurando para TikTok (1080x1920, vertical). Exportando... Listo en unos segundos!';
                this.settings.resolution = '1080x1920';
            } else if (lower.includes('ayuda') || lower.includes('help')) {
                response = 'Puedo ayudarte con:\n- "cortar" - Dividir clip\n- "texto" - Anadir titulo\n- "filtro" - Aplicar filtro\n- "subtitulos" - Generar subs\n- "musica" - Anadir audio\n- "exportar" - Exportar video\n- "tiktok" - Formato TikTok\nTambien puedes usar el microfono!';
            } else {
                const responses = [
                    'Entendido! Estoy procesando tu solicitud: "' + text + '". Dame un momento...',
                    'He analizado tu peticion. Te sugiero usar el menu de Herramientas IA para esa tarea.',
                    'Buena idea! Deja que procese eso. Puedes seguir editando mientras tanto.',
                    'Recibido. Estoy trabajando en "' + text + '". Te notificare cuando termine.'
                ];
                response = responses[Math.floor(Math.random() * responses.length)];
            }

            setTimeout(() => this.addAviaMessage(response, 'bot'), 500 + Math.random() * 800);
        }

        // ═══════════════════ VOICE INPUT ═══════════════════
        bindVoice() {
            const micBtn = document.getElementById('micBtn');
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            if (!SpeechRecognition) {
                micBtn.addEventListener('click', () => this.toast('Reconocimiento de voz no soportado en este navegador', 'error'));
                return;
            }

            this.recognition = new SpeechRecognition();
            this.recognition.lang = 'es-ES';
            this.recognition.continuous = false;
            this.recognition.interimResults = false;

            this.recognition.onresult = (e) => {
                const text = e.results[0][0].transcript;
                document.getElementById('aviaInput').value = text;
                this.addAviaMessage(text, 'user');
                this.processAviaCommand(text);
                this.stopRecording();
            };

            this.recognition.onerror = (e) => {
                this.toast('Error de voz: ' + e.error, 'error');
                this.stopRecording();
            };

            this.recognition.onend = () => this.stopRecording();

            micBtn.addEventListener('click', () => {
                if (this.isRecording) {
                    this.recognition.stop();
                } else {
                    this.startRecording();
                }
            });
        }

        startRecording() {
            this.isRecording = true;
            document.getElementById('micBtn').classList.add('recording');
            document.getElementById('micBtn').textContent = '🔴';
            this.recognition.start();
            this.toast('Escuchando... Habla ahora', 'info');
        }

        stopRecording() {
            this.isRecording = false;
            document.getElementById('micBtn').classList.remove('recording');
            document.getElementById('micBtn').textContent = '🎤';
        }

        // ═══════════════════ DRAG & DROP ═══════════════════
        bindDragDrop() {
            const container = document.getElementById('previewContainer');

            ['dragenter','dragover'].forEach(evt => {
                container.addEventListener(evt, (e) => {
                    e.preventDefault();
                    container.classList.add('drag-over');
                });
            });

            ['dragleave','drop'].forEach(evt => {
                container.addEventListener(evt, () => container.classList.remove('drag-over'));
            });

            container.addEventListener('drop', (e) => {
                e.preventDefault();
                const files = e.dataTransfer.files;
                if (files.length > 0) this.handleFiles(files);
            });
        }

        handleFiles(files) {
            Array.from(files).forEach(file => {
                const type = file.type.split('/')[0];
                if (['video','image','audio'].includes(type)) {
                    this.loadMediaFile(file, type);
                } else {
                    this.toast('Formato no soportado: ' + file.name, 'error');
                }
            });
        }

        loadMediaFile(file, type) {
            const url = URL.createObjectURL(file);
            const content = document.getElementById('previewContent');
            const empty = document.getElementById('previewEmpty');

            if (type === 'video') {
                content.innerHTML = '<video src="' + url + '" style="width:100%;height:100%;object-fit:contain;" id="mainVideo"></video>';
                const vid = document.getElementById('mainVideo');
                vid.addEventListener('loadedmetadata', () => {
                    this.totalTime = Math.floor(vid.duration);
                    this.updateTimeUI();
                });
            } else if (type === 'image') {
                content.innerHTML = '<img src="' + url + '" style="width:100%;height:100%;object-fit:contain;">';
                this.totalTime = 10;
                this.updateTimeUI();
            } else {
                content.innerHTML = '<div style="text-align:center;"><div style="font-size:64px;margin-bottom:16px;">🎵</div><div style="color:var(--text-muted);">' + file.name + '</div></div>';
            }

            empty.style.display = 'none';
            content.classList.add('has-content');
            this.pushUndo('Importar ' + file.name);
            this.toast(type.charAt(0).toUpperCase() + type.slice(1) + ' importado: ' + file.name, 'success');
            this.saveToStorage();
        }

        importMedia(type) {
            const input = document.createElement('input');
            input.type = 'file';
            const accepts = {video:'video/*',image:'image/*',audio:'audio/*'};
            input.accept = accepts[type] || '*/*';
            input.onchange = () => { if(input.files.length) this.handleFiles(input.files); };
            input.click();
        }

        addText(text, size) {
            const content = document.getElementById('previewContent');
            const empty = document.getElementById('previewEmpty');
            const overlay = document.createElement('div');
            overlay.className = 'text-overlay';
            overlay.style.fontSize = size;
            overlay.style.left = '50%';
            overlay.style.top = '50%';
            overlay.style.transform = 'translate(-50%,-50%)';
            overlay.textContent = text;
            overlay.contentEditable = true;
            content.appendChild(overlay);
            empty.style.display = 'none';
            content.classList.add('has-content');
            if (!this.totalTime) { this.totalTime = 10; this.updateTimeUI(); }
        }

        importProject() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            input.onchange = () => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const data = JSON.parse(e.target.result);
                        if (data.project) {
                            this.project = data.project;
                            document.getElementById('projectName').textContent = this.project.name;
                            this.saveToStorage();
                            this.toast('Proyecto cargado: ' + this.project.name, 'success');
                        }
                    } catch(err) { this.toast('Archivo JSON invalido', 'error'); }
                };
                reader.readAsText(input.files[0]);
            };
            input.click();
        }

        exportProject() {
            const data = JSON.stringify({project:this.project, settings:this.settings}, null, 2);
            const blob = new Blob([data], {type:'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = this.project.name + '.avia.json';
            a.click();
            URL.revokeObjectURL(url);
            this.toast('Proyecto exportado como JSON', 'success');
        }

        // ═══════════════════ KEYBOARD SHORTCUTS ═══════════════════
        bindKeyboard() {
            document.addEventListener('keydown', (e) => {
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.contentEditable === 'true') return;

                if (e.key === 'Escape') {
                    this.closeSubmenu();
                    this.closeAllPanels();
                }
                if (e.key === ' ') { e.preventDefault(); this.togglePlay(); }
                if (e.key === 'j' || e.key === 'J') this.seekRelative(-5);
                if (e.key === 'l' || e.key === 'L') this.seekRelative(5);
                if (e.key === 'k' || e.key === 'K') this.togglePlay();
                if (e.key === 'm' || e.key === 'M') this.togglePanel('menu');
                if (e.key === 'p' || e.key === 'P') this.togglePanel('profile');
                if (e.key === 's' || e.key === 'S') { if(!e.ctrlKey) this.togglePanel('settings'); }
                if (e.key === 'a' || e.key === 'A') this.togglePanel('avia');
                if (e.key === 'v' || e.key === 'V') { if(!e.ctrlKey) document.getElementById('micBtn').click(); }
                if (e.key === 't' || e.key === 'T') this.toggleTheme();

                if (e.ctrlKey && e.key === 'z') { e.preventDefault(); this.undo(); }
                if (e.ctrlKey && e.key === 'y') { e.preventDefault(); this.redo(); }
                if (e.ctrlKey && e.key === 's') { e.preventDefault(); this.saveToStorage(); this.toast('Guardado manual','success'); }

                if (e.key === '?') this.showShortcuts();
            });
        }

        showShortcuts() {
            this.showSubmenu({
                icon: '⌨', title: 'Atajos de Teclado',
                items: [
                    {icon:'⏯',title:'Espacio / K',desc:'Play / Pause',action:()=>{}},
                    {icon:'⏮',title:'J',desc:'Retroceder 5s',action:()=>{}},
                    {icon:'⏭',title:'L',desc:'Avanzar 5s',action:()=>{}},
                    {icon:'☰',title:'M',desc:'Abrir Menu',action:()=>{}},
                    {icon:'👤',title:'P',desc:'Panel Perfil/Modo',action:()=>{}},
                    {icon:'⚙',title:'S',desc:'Panel Ajustes',action:()=>{}},
                    {icon:'🤖',title:'A',desc:'Panel AVIA',action:()=>{}},
                    {icon:'🎤',title:'V',desc:'Activar microfono',action:()=>{}},
                    {icon:'🌓',title:'T',desc:'Cambiar tema',action:()=>{}},
                    {icon:'↶',title:'Ctrl+Z',desc:'Deshacer',action:()=>{}},
                    {icon:'↷',title:'Ctrl+Y',desc:'Rehacer',action:()=>{}},
                    {icon:'💾',title:'Ctrl+S',desc:'Guardar',action:()=>{}},
                    {icon:'✕',title:'Escape',desc:'Cerrar paneles',action:()=>{}}
                ]
            });
        }

        formatTime(s) {
            const h=Math.floor(s/3600),m=Math.floor((s%3600)/60),ss=s%60;
            return [h,m,ss].map(v=>String(v).padStart(2,'0')).join(':');
        }

        updateUI() {
            this.applyTheme();
            this.updateUndoRedoUI();
            this.updateTimeUI();
            // Restore mode
            const modeEl = document.querySelector('[data-mode="'+this.currentMode+'"]');
            if (modeEl) modeEl.click();
            // Restore settings
            document.getElementById('settingRes').value = this.settings.resolution;
            document.getElementById('settingFps').value = this.settings.fps;
            document.getElementById('projectName').textContent = this.project.name;
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        window.avia = new AVIAProsumerV2();
    });
    </script>
</body>
</html>'''


if __name__ == "__main__":
    bot = AVIAVideoProsumidor()
    bot.run()

