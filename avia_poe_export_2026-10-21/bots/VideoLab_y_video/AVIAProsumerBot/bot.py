# poe: name=VideoProsumerv2

import json
import re
from fastapi_poe.types import (
    SettingsResponse, ParameterControls, Section,
    DropDown, ValueNamePair, ToggleSwitch, Slider
)

# ═══════════════════════════════════════════════════════════════
# VideoProsumerBotv2 — Constelación Económica AVIA Nomada
# Orquestador: AVIA-Clon-Carlosv2
# Producción: AVIA-Studiov2
# Desarrollo: AVIA-Seniorv3.2
#
# Innovaciones:
#   P1: Comandos de edición por chat
#   P2: Auto-detección de escenas
#   P3: Transcripción automática (Whisper)
#   Fase 2.1: Pipeline IA generativa
# ═══════════════════════════════════════════════════════════════

poe.update_settings(SettingsResponse(
    introduction_message=(
        "🎬 **VideoProsumer v2.0** — Constelación AVIA Nomada\n\n"
        "Soy tu estudio de video inteligente con IA generativa. "
        "Puedo editar, analizar y producir contenido multimedia completo.\n\n"
        "**🏆 Comandos de Edición (chat natural):**\n"
        "• `recorta 0:30 a 1:45` — Trim de segmento\n"
        "• `velocidad 2x` / `cámara lenta 0.5x`\n"
        "• `añade subtítulos` — Transcripción auto + .srt\n"
        "• `genera thumbnail` — Thumbnail IA para YouTube\n"
        "• `voz en off: [texto]` — Narración con ElevenLabs\n"
        "• `música [estilo]` — Banda sonora IA\n"
        "• `detecta escenas` — Análisis automático de cortes\n"
        "• `transcribe` — Whisper + contenido derivado\n"
        "• `storyboard [idea]` — Storyboard visual con IA\n"
        "• `genera video [prompt]` — Video IA desde texto\n\n"
        "**🆕 Fase 2.2 — Nuevas herramientas:**\n"
        "• `detecta silencios` — Detectar silencios automáticamente\n"
        "• `transición crossfade` — Transiciones entre clips\n"
        "• `añade texto 'Tu texto'` — Texto overlay en video\n"
        "• `director: [concepto]` — 🎬 Producción IA completa automatizada\n"
        "• `editor` — Abrir editor visual interactivo\n\n"
        "**📎 Adjunta un video/audio/imagen** para trabajar con él, "
        "o escribe un comando directamente.\n\n"
        "⚙️ Ajusta formato de salida y calidad en el icono de configuración."
    ),
    enable_image_comprehension=True,
    allow_attachments=True,
    expand_text_attachments=True,
    parameter_controls=ParameterControls(
        sections=[
            Section(
                name="Formato de Salida",
                controls=[
                    DropDown(
                        label="Aspect Ratio",
                        parameter_name="aspect_ratio",
                        default_value="16:9",
                        options=[
                            ValueNamePair(value="16:9", name="16:9 (YouTube/Landscape)"),
                            ValueNamePair(value="9:16", name="9:16 (Reels/TikTok/Shorts)"),
                            ValueNamePair(value="1:1", name="1:1 (Instagram Feed)"),
                            ValueNamePair(value="4:3", name="4:3 (Presentación)"),
                        ],
                    ),
                    DropDown(
                        label="Idioma de Voz/Subtítulos",
                        parameter_name="language",
                        default_value="es",
                        options=[
                            ValueNamePair(value="es", name="Español"),
                            ValueNamePair(value="en", name="English"),
                            ValueNamePair(value="fr", name="Français"),
                            ValueNamePair(value="pt", name="Português"),
                            ValueNamePair(value="de", name="Deutsch"),
                        ],
                    ),
                    DropDown(
                        label="Voz de Narración",
                        parameter_name="voice",
                        default_value="Jessica",
                        options=[
                            ValueNamePair(value="Jessica", name="Jessica (Femenina EN)"),
                            ValueNamePair(value="Brian", name="Brian (Masculina EN)"),
                            ValueNamePair(value="Sarah", name="Sarah (Femenina EN)"),
                            ValueNamePair(value="George", name="George (Masculina EN)"),
                            ValueNamePair(value="Matilda", name="Matilda (Femenina EN)"),
                            ValueNamePair(value="David Martin", name="David Martin (Masculina ES)"),
                            ValueNamePair(value="Sara Martin", name="Sara Martin (Femenina ES)"),
                        ],
                    ),
                ],
            ),
            Section(
                name="Calidad IA",
                controls=[
                    DropDown(
                        label="Modelo de Video",
                        parameter_name="video_model",
                        default_value="Sora-2",
                        options=[
                            ValueNamePair(value="Sora-2", name="Sora-2 (Estándar)"),
                            ValueNamePair(value="Veo-v3.1", name="Veo-v3.1 (Premium + Audio)"),
                            ValueNamePair(value="Veo-3.1-Fast", name="Veo-3.1-Fast (Rápido)"),
                        ],
                    ),
                    DropDown(
                        label="Modelo de Imagen",
                        parameter_name="image_model",
                        default_value="Imagen-4-Ultra",
                        options=[
                            ValueNamePair(value="Imagen-4-Ultra", name="Imagen-4-Ultra (Calidad)"),
                            ValueNamePair(value="Imagen-4-Fast", name="Imagen-4-Fast (Rápido)"),
                            ValueNamePair(value="GPT-Image-1", name="GPT-Image-1 (Creativo)"),
                        ],
                    ),
                    Slider(
                        label="Duración Video IA (segundos)",
                        parameter_name="video_duration",
                        default_value=8,
                        min_value=4,
                        max_value=12,
                        step=2,
                    ),
                    ToggleSwitch(
                        label="Generar Audio en Video",
                        parameter_name="video_audio",
                        default_value=True,
                    ),
                ],
            ),
        ]
    ),
))


# ═══════════════════════════════════════════════════════════════
# Utilidades
# ═══════════════════════════════════════════════════════════════

def parse_json_from_response(response_text, required_fields=None):
    """Extract and parse JSON from bot response text."""
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


LANG_MAP = {
    "es": {"name": "Español", "whisper": "es", "tts_lang": "es"},
    "en": {"name": "English", "whisper": "en", "tts_lang": "en"},
    "fr": {"name": "Français", "whisper": "fr", "tts_lang": "fr"},
    "pt": {"name": "Português", "whisper": "pt", "tts_lang": "pt"},
    "de": {"name": "Deutsch", "whisper": "de", "tts_lang": "de"},
}


# ═══════════════════════════════════════════════════════════════
# Fase 2.2: Canvas Editor Visual — Timeline + AI Toolbox
# ═══════════════════════════════════════════════════════════════

EDITOR_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VideoProsumer v2.0 — Editor</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
:root{--c-bg:#0a0a1a;--c-surface:#12122a;--c-surface-2:#1a1a3a;--c-surface-3:#242450;--c-primary:#7C3AED;--c-primary-l:#A78BFA;--c-primary-g:rgba(124,58,237,.3);--c-accent:#06B6D4;--c-green:#10B981;--c-red:#EF4444;--c-yellow:#F59E0B;--c-orange:#F97316;--c-text:#E2E8F0;--c-muted:#6B7280;--c-border:rgba(124,58,237,.15);--r:8px;--font:'Segoe UI',system-ui,sans-serif;--ease:cubic-bezier(.4,0,.2,1)}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--font);background:var(--c-bg);color:var(--c-text);overflow:hidden;height:100vh}
.editor{display:grid;grid-template-rows:42px 1fr 140px 32px;height:100vh}

/* ═══ HEADER ═══ */
.hdr{display:flex;align-items:center;justify-content:space-between;padding:0 12px;background:var(--c-surface);border-bottom:1px solid var(--c-border)}
.hdr .logo{display:flex;align-items:center;gap:8px;font-size:.85rem;font-weight:700}
.hdr .logo i{color:var(--c-primary-l)}
.hdr .logo span{background:linear-gradient(135deg,var(--c-primary-l),var(--c-accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hdr .badge{font-size:.6rem;padding:2px 8px;background:var(--c-primary-g);color:var(--c-primary-l);border:1px solid var(--c-border);border-radius:10px}
.hdr-actions{display:flex;gap:6px}
.hdr-btn{background:var(--c-surface-2);border:1px solid var(--c-border);color:var(--c-text);padding:4px 10px;border-radius:var(--r);font-size:.72rem;cursor:pointer;transition:all .2s var(--ease);font-family:var(--font)}
.hdr-btn:hover{background:var(--c-primary);border-color:var(--c-primary)}
.hdr-btn.primary{background:var(--c-primary);border-color:var(--c-primary)}

/* ═══ MAIN (Preview + Toolbox) ═══ */
.main{display:grid;grid-template-columns:1fr 180px;overflow:hidden}
.preview{display:flex;flex-direction:column;background:#000;position:relative}
.preview-area{flex:1;display:flex;align-items:center;justify-content:center;position:relative}
.drop-zone{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;color:var(--c-muted);transition:all .3s}
.drop-zone i{font-size:3rem;opacity:.4}
.drop-zone p{font-size:.82rem}
.drop-zone.drag-over{background:rgba(124,58,237,.15);color:var(--c-primary-l)}
.drop-zone.drag-over i{opacity:1;color:var(--c-primary-l)}
.drop-zone.has-video{display:none}
.preview-area video{width:100%;height:100%;object-fit:contain;display:none}
.preview-area video.visible{display:block}
.controls{display:flex;align-items:center;gap:8px;padding:6px 12px;background:var(--c-surface)}
.ctrl-btn{background:none;border:none;color:var(--c-text);font-size:.9rem;cursor:pointer;padding:4px 6px;border-radius:4px;transition:color .2s}
.ctrl-btn:hover{color:var(--c-primary-l)}
.ctrl-btn.active{color:var(--c-green)}
.time-display{font-size:.7rem;font-family:monospace;color:var(--c-muted);min-width:90px}
.progress-bar{flex:1;height:4px;background:var(--c-surface-3);border-radius:2px;cursor:pointer;position:relative}
.progress-fill{height:100%;background:var(--c-primary);border-radius:2px;width:0%;transition:width .1s linear}
.vol-slider{width:60px;height:4px;-webkit-appearance:none;background:var(--c-surface-3);border-radius:2px;outline:none}
.vol-slider::-webkit-slider-thumb{-webkit-appearance:none;width:10px;height:10px;border-radius:50%;background:var(--c-primary-l);cursor:pointer}

/* ═══ AI TOOLBOX ═══ */
.toolbox{background:var(--c-surface);border-left:1px solid var(--c-border);padding:8px;overflow-y:auto;display:flex;flex-direction:column;gap:4px}
.toolbox h3{font-size:.7rem;color:var(--c-muted);text-transform:uppercase;letter-spacing:1px;padding:4px 6px;margin-bottom:2px}
.tool{display:flex;align-items:center;gap:8px;padding:7px 8px;background:var(--c-surface-2);border:1px solid transparent;border-radius:var(--r);cursor:pointer;transition:all .2s var(--ease);font-size:.75rem;color:var(--c-text);width:100%;text-align:left;font-family:var(--font)}
.tool:hover{border-color:var(--c-primary);background:var(--c-surface-3);transform:translateX(2px)}
.tool i{width:18px;text-align:center;font-size:.8rem}
.tool-divider{height:1px;background:var(--c-border);margin:4px 0}
.tool .badge-new{font-size:.55rem;padding:1px 4px;background:var(--c-green);color:#fff;border-radius:4px;margin-left:auto}

/* ═══ TIMELINE ═══ */
.timeline{background:var(--c-surface);border-top:1px solid var(--c-border);display:flex;flex-direction:column}
.tl-header{display:flex;align-items:center;justify-content:space-between;padding:4px 12px;border-bottom:1px solid var(--c-border)}
.tl-header span{font-size:.7rem;color:var(--c-muted);text-transform:uppercase;letter-spacing:.5px}
.tl-zoom{display:flex;gap:4px}
.tl-zoom button{background:none;border:1px solid var(--c-border);color:var(--c-muted);width:20px;height:20px;border-radius:4px;cursor:pointer;font-size:.65rem;display:flex;align-items:center;justify-content:center}
.tl-zoom button:hover{color:var(--c-text);border-color:var(--c-primary)}
.tracks{flex:1;overflow-y:auto;overflow-x:auto}
.track{display:flex;align-items:center;height:32px;border-bottom:1px solid rgba(255,255,255,.03)}
.track-label{width:60px;flex-shrink:0;font-size:.65rem;color:var(--c-muted);padding:0 8px;display:flex;align-items:center;gap:4px;border-right:1px solid var(--c-border)}
.track-label i{font-size:.6rem}
.track-content{flex:1;position:relative;height:100%;padding:3px 0}
.clip{position:absolute;height:calc(100% - 6px);border-radius:4px;display:flex;align-items:center;padding:0 8px;font-size:.6rem;font-weight:500;cursor:grab;transition:opacity .2s;overflow:hidden;white-space:nowrap}
.clip:hover{opacity:.85}
.clip-video{background:linear-gradient(90deg,rgba(124,58,237,.5),rgba(124,58,237,.3));border:1px solid rgba(124,58,237,.4);color:var(--c-primary-l)}
.clip-audio{background:linear-gradient(90deg,rgba(6,182,212,.5),rgba(6,182,212,.3));border:1px solid rgba(6,182,212,.4);color:var(--c-accent)}
.clip-voice{background:linear-gradient(90deg,rgba(249,115,22,.5),rgba(249,115,22,.3));border:1px solid rgba(249,115,22,.4);color:var(--c-orange)}
.clip-text{background:linear-gradient(90deg,rgba(16,185,129,.5),rgba(16,185,129,.3));border:1px solid rgba(16,185,129,.4);color:var(--c-green)}
.tl-ruler{display:flex;height:18px;border-bottom:1px solid var(--c-border);padding-left:60px}
.ruler-mark{flex:1;font-size:.55rem;color:var(--c-muted);border-left:1px solid rgba(255,255,255,.05);padding-left:4px;line-height:18px}
.tl-playhead{position:absolute;top:0;width:2px;height:100%;background:var(--c-red);z-index:5;pointer-events:none}
.tl-playhead::before{content:'';position:absolute;top:-2px;left:-4px;width:10px;height:6px;background:var(--c-red);clip-path:polygon(0 0,100% 0,50% 100%)}

/* ═══ STATUS BAR ═══ */
.status{display:flex;align-items:center;justify-content:space-between;padding:0 12px;background:var(--c-surface);border-top:1px solid var(--c-border);font-size:.65rem;color:var(--c-muted)}
.status-left,.status-right{display:flex;align-items:center;gap:12px}
.status .dot{width:6px;height:6px;border-radius:50%;background:var(--c-green)}

/* Toast */
.toast{position:fixed;bottom:50px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--c-surface-3);border:1px solid var(--c-primary);color:var(--c-text);padding:8px 18px;border-radius:var(--r);font-size:.8rem;opacity:0;transition:all .3s var(--ease);pointer-events:none;z-index:99}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* Override dialogs */
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:100;align-items:center;justify-content:center}
.modal-overlay.active{display:flex}
.modal-box{background:var(--c-surface);border:1px solid var(--c-border);border-radius:var(--r);padding:20px;max-width:320px;text-align:center}
.modal-box p{margin-bottom:12px;font-size:.85rem}
.modal-box button{background:var(--c-primary);border:none;color:#fff;padding:6px 16px;border-radius:var(--r);cursor:pointer;font-family:var(--font)}

/* Responsive */
@media(max-width:600px){.main{grid-template-columns:1fr}.toolbox{display:none}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition-duration:0ms!important}}
:focus-visible{outline:2px solid var(--c-primary-l);outline-offset:1px}
.toolbox::-webkit-scrollbar{width:4px}.toolbox::-webkit-scrollbar-thumb{background:var(--c-surface-3);border-radius:2px}
.tracks::-webkit-scrollbar{height:4px}.tracks::-webkit-scrollbar-thumb{background:var(--c-surface-3);border-radius:2px}
</style>
</head>
<body>
<div class="editor">

  <!-- HEADER -->
  <header class="hdr">
    <div class="logo"><i class="fas fa-clapperboard"></i><span>VideoProsumer v2.0</span><span class="badge">Fase 2.2</span></div>
    <div class="hdr-actions">
      <button class="hdr-btn" id="btnConsole" title="Consola"><i class="fas fa-terminal"></i></button>
      <button class="hdr-btn" id="btnHelp" title="Ayuda"><i class="fas fa-question"></i></button>
      <button class="hdr-btn primary" id="btnExport" title="Exportar"><i class="fas fa-download"></i> Exportar</button>
    </div>
  </header>

  <!-- MAIN: Preview + Toolbox -->
  <div class="main">
    <div class="preview">
      <div class="preview-area">
        <div class="drop-zone" id="dropZone">
          <i class="fas fa-cloud-arrow-up"></i>
          <p>Arrastra video aquí o adjunta en el chat</p>
          <p style="font-size:.7rem;color:var(--c-primary-l)">Soporta MP4, MOV, WebM, AVI</p>
        </div>
        <video id="videoPlayer" playsinline></video>
      </div>
      <div class="controls">
        <button class="ctrl-btn" id="btnPlay" title="Play/Pause"><i class="fas fa-play"></i></button>
        <button class="ctrl-btn" id="btnStop" title="Stop"><i class="fas fa-stop"></i></button>
        <span class="time-display" id="timeDisplay">00:00 / 00:00</span>
        <div class="progress-bar" id="progressBar"><div class="progress-fill" id="progressFill"></div></div>
        <button class="ctrl-btn" id="btnMute" title="Mute"><i class="fas fa-volume-high"></i></button>
        <input type="range" class="vol-slider" id="volSlider" min="0" max="100" value="80" title="Volumen">
        <button class="ctrl-btn" id="btnFullscreen" title="Pantalla completa"><i class="fas fa-expand"></i></button>
      </div>
    </div>

    <aside class="toolbox" role="toolbar" aria-label="Herramientas IA">
      <h3><i class="fas fa-wand-magic-sparkles"></i> IA Tools</h3>
      <button class="tool" data-cmd="recorta [inicio] a [fin]"><i class="fas fa-scissors" style="color:var(--c-primary-l)"></i>Recortar</button>
      <button class="tool" data-cmd="velocidad 2x"><i class="fas fa-gauge-high" style="color:var(--c-accent)"></i>Velocidad</button>
      <button class="tool" data-cmd="detecta silencios"><i class="fas fa-volume-xmark" style="color:var(--c-yellow)"></i>Silencios<span class="badge-new">NEW</span></button>
      <button class="tool" data-cmd="transición crossfade"><i class="fas fa-shuffle" style="color:var(--c-orange)"></i>Transiciones<span class="badge-new">NEW</span></button>
      <button class="tool" data-cmd="añade texto 'Tu texto aquí'"><i class="fas fa-font" style="color:var(--c-green)"></i>Texto overlay<span class="badge-new">NEW</span></button>
      <div class="tool-divider"></div>
      <h3><i class="fas fa-microphone"></i> Audio</h3>
      <button class="tool" data-cmd="añade subtítulos"><i class="fas fa-closed-captioning" style="color:var(--c-green)"></i>Subtítulos</button>
      <button class="tool" data-cmd="transcribe"><i class="fas fa-file-lines" style="color:var(--c-accent)"></i>Transcribir</button>
      <button class="tool" data-cmd="voz en off: [tu texto]"><i class="fas fa-comment-dots" style="color:var(--c-orange)"></i>Voz en Off</button>
      <button class="tool" data-cmd="música cinematic 30s"><i class="fas fa-music" style="color:var(--c-primary-l)"></i>Música IA</button>
      <div class="tool-divider"></div>
      <h3><i class="fas fa-sparkles"></i> Generativo</h3>
      <button class="tool" data-cmd="genera thumbnail"><i class="fas fa-image" style="color:var(--c-yellow)"></i>Thumbnail</button>
      <button class="tool" data-cmd="storyboard: [tu idea]"><i class="fas fa-table-cells" style="color:var(--c-primary-l)"></i>Storyboard</button>
      <button class="tool" data-cmd="genera video [prompt]"><i class="fas fa-film" style="color:var(--c-accent)"></i>Video IA</button>
      <button class="tool" data-cmd="detecta escenas"><i class="fas fa-clapperboard" style="color:var(--c-green)"></i>Escenas</button>
      <div class="tool-divider"></div>
      <h3><i class="fas fa-crown" style="color:var(--c-yellow)"></i> Premium</h3>
      <button class="tool" data-cmd="director: [describe tu video]" style="border:1px solid rgba(249,115,22,.3);background:rgba(249,115,22,.08)"><i class="fas fa-video" style="color:var(--c-orange)"></i>Director IA<span class="badge-new" style="background:var(--c-orange)">NEW</span></button>
    </aside>
  </div>

  <!-- TIMELINE -->
  <section class="timeline">
    <div class="tl-header">
      <span><i class="fas fa-timeline"></i> Timeline</span>
      <div class="tl-zoom">
        <button id="zoomOut" title="Zoom out"><i class="fas fa-minus"></i></button>
        <button id="zoomIn" title="Zoom in"><i class="fas fa-plus"></i></button>
      </div>
    </div>
    <div class="tl-ruler" id="ruler"></div>
    <div class="tracks" id="tracks" style="position:relative">
      <div class="track"><div class="track-label"><i class="fas fa-video"></i> Video</div><div class="track-content" id="trackVideo"></div></div>
      <div class="track"><div class="track-label"><i class="fas fa-volume-up"></i> Audio</div><div class="track-content" id="trackAudio"></div></div>
      <div class="track"><div class="track-label"><i class="fas fa-microphone"></i> Voz</div><div class="track-content" id="trackVoice"></div></div>
      <div class="track"><div class="track-label"><i class="fas fa-font"></i> Texto</div><div class="track-content" id="trackText"></div></div>
      <div class="tl-playhead" id="playhead" style="left:60px"></div>
    </div>
  </section>

  <!-- STATUS BAR -->
  <div class="status">
    <div class="status-left"><span class="dot"></span><span>Editor listo</span><span id="statusMsg">Arrastra un video o usa los comandos del chat</span></div>
    <div class="status-right"><span id="projectInfo">Sin proyecto</span><span>VideoProsumer v2.0</span></div>
  </div>

</div>

<!-- Toast notification -->
<div class="toast" id="toast"></div>
<!-- Modal -->
<div class="modal-overlay" id="modal"><div class="modal-box"><p id="modalMsg"></p><button id="modalClose">OK</button></div></div>

<script>
(function(){
  /* Override blocked dialogs */
  var mEl=document.getElementById('modal'),mMsg=document.getElementById('modalMsg'),mC=document.getElementById('modalClose');
  function showM(m){if(mEl&&mMsg){mMsg.textContent=String(m);mEl.classList.add('active')}}
  window.alert=function(m){showM(m)};window.confirm=function(m){showM(m);return true};window.prompt=function(m){showM(m);return null};
  if(mC)mC.addEventListener('click',function(){mEl.classList.remove('active')});
  if(mEl)mEl.addEventListener('click',function(e){if(e.target===mEl)mEl.classList.remove('active')});
})();

(function(){
  'use strict';
  var toast=document.getElementById('toast');
  function showToast(msg,ms){toast.textContent=msg;toast.classList.add('show');setTimeout(function(){toast.classList.remove('show')},ms||2500)}

  /* ═══ VIDEO PLAYER ═══ */
  var video=document.getElementById('videoPlayer'),dropZone=document.getElementById('dropZone');
  var btnPlay=document.getElementById('btnPlay'),btnStop=document.getElementById('btnStop');
  var btnMute=document.getElementById('btnMute'),volSlider=document.getElementById('volSlider');
  var progressBar=document.getElementById('progressBar'),progressFill=document.getElementById('progressFill');
  var timeDisplay=document.getElementById('timeDisplay'),btnFullscreen=document.getElementById('btnFullscreen');
  var statusMsg=document.getElementById('statusMsg'),projectInfo=document.getElementById('projectInfo');
  var playhead=document.getElementById('playhead');

  function fmtTime(s){var m=Math.floor(s/60);s=Math.floor(s%60);return(m<10?'0':'')+m+':'+(s<10?'0':'')+s}

  video.volume=0.8;
  btnPlay.addEventListener('click',function(){
    if(!video.src)return;
    if(video.paused){video.play();this.innerHTML='<i class="fas fa-pause"></i>'}
    else{video.pause();this.innerHTML='<i class="fas fa-play"></i>'}
  });
  btnStop.addEventListener('click',function(){if(!video.src)return;video.pause();video.currentTime=0;btnPlay.innerHTML='<i class="fas fa-play"></i>'});
  btnMute.addEventListener('click',function(){video.muted=!video.muted;this.innerHTML=video.muted?'<i class="fas fa-volume-xmark"></i>':'<i class="fas fa-volume-high"></i>'});
  volSlider.addEventListener('input',function(){video.volume=this.value/100});
  video.addEventListener('timeupdate',function(){
    if(!video.duration)return;
    var pct=(video.currentTime/video.duration)*100;
    progressFill.style.width=pct+'%';
    timeDisplay.textContent=fmtTime(video.currentTime)+' / '+fmtTime(video.duration);
    playhead.style.left=(60+((document.getElementById('trackVideo').offsetWidth)*pct/100))+'px';
  });
  video.addEventListener('ended',function(){btnPlay.innerHTML='<i class="fas fa-play"></i>'});
  progressBar.addEventListener('click',function(e){if(!video.duration)return;var r=this.getBoundingClientRect();video.currentTime=(e.clientX-r.left)/r.width*video.duration});
  btnFullscreen.addEventListener('click',function(){if(video.requestFullscreen)video.requestFullscreen()});

  /* ═══ DRAG & DROP ═══ */
  ['dragenter','dragover'].forEach(function(ev){dropZone.addEventListener(ev,function(e){e.preventDefault();dropZone.classList.add('drag-over')})});
  ['dragleave','drop'].forEach(function(ev){dropZone.addEventListener(ev,function(e){e.preventDefault();dropZone.classList.remove('drag-over')})});
  dropZone.addEventListener('drop',function(e){
    var files=e.dataTransfer.files;
    if(files.length>0&&files[0].type.startsWith('video/')){
      loadVideo(files[0]);
    } else {
      showToast('Formato no soportado. Usa MP4, MOV o WebM');
    }
  });

  function loadVideo(file){
    var url=URL.createObjectURL(file);
    video.src=url;video.classList.add('visible');dropZone.classList.add('has-video');
    statusMsg.textContent='Video cargado: '+file.name;
    projectInfo.textContent=file.name+' ('+Math.round(file.size/1024/1024)+'MB)';
    showToast('Video cargado: '+file.name);
    addClip('trackVideo',file.name,'clip-video',0,85);
    /* Generate ruler */
    video.addEventListener('loadedmetadata',function(){
      var dur=video.duration;var ruler=document.getElementById('ruler');ruler.innerHTML='';
      for(var i=0;i<=Math.ceil(dur);i+=Math.max(1,Math.floor(dur/10))){
        var mk=document.createElement('span');mk.className='ruler-mark';mk.textContent=fmtTime(i);ruler.appendChild(mk)}
    },{once:true});
  }

  function addClip(trackId,label,cls,leftPct,widthPct){
    var track=document.getElementById(trackId);
    var clip=document.createElement('div');clip.className='clip '+cls;
    clip.style.left=leftPct+'%';clip.style.width=widthPct+'%';clip.textContent=label;
    track.appendChild(clip);
  }

  /* ═══ TIMELINE ZOOM ═══ */
  var zoomLevel=1;
  document.getElementById('zoomIn').addEventListener('click',function(){zoomLevel=Math.min(zoomLevel*1.3,4);applyZoom()});
  document.getElementById('zoomOut').addEventListener('click',function(){zoomLevel=Math.max(zoomLevel/1.3,0.5);applyZoom()});
  function applyZoom(){document.getElementById('tracks').style.transform='scaleX('+zoomLevel+')';document.getElementById('tracks').style.transformOrigin='left'}

  /* ═══ AI TOOL BUTTONS → Copy command ═══ */
  document.querySelectorAll('.tool').forEach(function(btn){
    btn.addEventListener('click',function(){
      var cmd=this.getAttribute('data-cmd');
      if(navigator.clipboard&&navigator.clipboard.writeText){
        navigator.clipboard.writeText(cmd).then(function(){
          showToast('Copiado: "'+cmd+'" — Pega en el chat de Poe',3000);
        }).catch(function(){showToast('Escribe en el chat: '+cmd,3000)});
      } else {showToast('Escribe en el chat: '+cmd,3000)}
    });
  });

  /* ═══ HEADER BUTTONS ═══ */
  document.getElementById('btnExport').addEventListener('click',function(){showToast('Escribe "exportar" en el chat para generar el video final')});
  document.getElementById('btnHelp').addEventListener('click',function(){showToast('Escribe "ayuda" en el chat para ver todos los comandos',3000)});
  document.getElementById('btnConsole').addEventListener('click',function(){showToast('AVIA Video v2.0 Editor — Fase 2.2 — Constelación AVIA Nomada',3000)});

  /* ═══ DEMO CLIPS ═══ */
  addClip('trackAudio','Banda sonora','clip-audio',5,60);
  addClip('trackVoice','Narración IA','clip-voice',10,35);
  addClip('trackText','Subtítulos','clip-text',0,45);
})();
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════
# Clase Principal: VideoProsumerBotv2
# ═══════════════════════════════════════════════════════════════

class VideoProsumerBot:
    """VideoProsumer v2.0 — Edición, análisis y producción de video con IA."""

    # Constelación AVIA
    ORCHESTRATOR = "AVIA-Clon-Carlosv2"
    PRODUCER = "AVIA-Studiov2"
    SENIOR_DEV = "AVIA-Seniorv3.2"

    # LLMs de apoyo
    ANALYZER = "Claude-Sonnet-4.5"
    FAST_LLM = "Gemini-3-Flash"

    # Prompt de clasificación del orquestador
    CLASSIFY_PROMPT = """Eres el orquestador de VideoProsumer v2.0. Clasifica la intención del usuario.

COMANDOS SOPORTADOS:
- "trim": Recortar video (usuario indica timestamps)
- "speed": Cambiar velocidad del video
- "subtitle": Generar subtítulos automáticos
- "thumbnail": Crear thumbnail con IA
- "voiceover": Generar voz en off con texto
- "music": Generar música de fondo
- "detect_scenes": Analizar y detectar escenas/cortes
- "transcribe": Transcribir audio a texto + contenido derivado
- "storyboard": Crear storyboard visual con IA
- "generate_video": Generar video desde prompt de texto
- "generate_image": Generar imagen desde prompt
- "analyze": Analizar video/imagen adjunto
- "silence_detect": Detectar silencios en audio/video
- "transition": Añadir transición entre clips (crossfade, fade, wipe, etc.)
- "text_overlay": Añadir texto superpuesto al video
- "director": Pipeline completo de producción IA (guión→storyboard→video→voz→música→montaje)
- "editor": Abrir el editor visual interactivo
- "general": Consulta general sobre video/edición

Responde SOLO con JSON:
```json
{"command": "trim|speed|subtitle|thumbnail|voiceover|music|detect_scenes|transcribe|storyboard|generate_video|generate_image|analyze|silence_detect|transition|text_overlay|director|editor|general", "params": {"key": "value"}, "reasoning": "breve explicación"}
```

Extrae parámetros relevantes:
- trim: {"start": "0:30", "end": "1:45"}
- speed: {"factor": "2x"}
- voiceover: {"text": "el texto a narrar"}
- music: {"style": "épica cinematográfica", "duration_ms": 30000}
- storyboard: {"concept": "descripción de la idea"}
- generate_video: {"prompt": "descripción del video"}
- generate_image: {"prompt": "descripción de la imagen"}
- silence_detect: {"threshold": "-30dB", "min_duration": "0.5"}
- transition: {"type": "crossfade", "duration": "1"}
- text_overlay: {"text": "texto a mostrar", "position": "center", "start": "0:00", "duration": "5"}
- director: {"concept": "descripción completa del video a producir"}
- subtitle/transcribe/detect_scenes/analyze/thumbnail/editor: {}"""

    def __init__(self):
        self.params = {}
        self._load_params()

    def _load_params(self):
        """Load user-configured parameters."""
        p = poe.query.parameters if poe.query.parameters else {}
        self.params = {
            "aspect_ratio": p.get("aspect_ratio", "16:9"),
            "language": p.get("language", "es"),
            "voice": p.get("voice", "Jessica"),
            "video_model": p.get("video_model", "Sora-2"),
            "image_model": p.get("image_model", "Imagen-4-Ultra"),
            "video_duration": str(int(p.get("video_duration", 8))),
            "video_audio": p.get("video_audio", True),
        }

    def _get_attachments(self):
        """Get user attachments from query."""
        return list(poe.query.attachments) if poe.query.attachments else []

    # ─────────────────────────────────────────────────
    # P1: COMANDOS DE EDICIÓN POR CHAT
    # ─────────────────────────────────────────────────

    def cmd_trim(self, params):
        """Trim command — recortar video con timestamps."""
        start = params.get("start", "0:00")
        end = params.get("end", "")
        attachments = self._get_attachments()

        with poe.start_message() as msg:
            msg.write("✂️ **Recorte de Video**\n\n")
            if not attachments:
                msg.write(f"📋 **Comando registrado:** Recortar de `{start}` a `{end}`\n\n")
                msg.write("⚠️ Adjunta un video para aplicar el recorte.\n")
                msg.write("Cuando lo adjuntes, usaré `ffmpeg` vía Claude-Code para:\n")
                msg.write(f"1. Extraer el segmento `{start}` → `{end}`\n")
                msg.write("2. Re-codificar sin pérdida de calidad\n")
                msg.write("3. Entregar el clip recortado\n")
                return

            msg.write(f"📋 Recortando: `{start}` → `{end}`\n")
            msg.write(f"📎 Archivo: {attachments[0].name}\n\n")

        # Enviar a Claude-Code para ejecución ffmpeg
        system = (
            "Eres un editor de video profesional. El usuario quiere recortar un video. "
            f"Usa ffmpeg para extraer el segmento desde {start} hasta {end}. "
            "Comando sugerido: ffmpeg -i input -ss START -to END -c copy output.mp4. "
            "Si -c copy da problemas, re-codifica. Entrega el archivo resultante."
        )
        poe.call(
            "Claude-Code",
            poe.Message(text=system, sender="system"),
            poe.query,
            parameters={"thinking_budget": 8000},
            output=poe.default_chat,
        )

    def cmd_speed(self, params):
        """Speed command — cambiar velocidad del video."""
        factor = params.get("factor", "2x")
        factor_num = float(re.sub(r'[xX]', '', factor)) if factor else 2.0
        attachments = self._get_attachments()

        with poe.start_message() as msg:
            msg.write(f"⏩ **Cambio de Velocidad: {factor}**\n\n")
            if not attachments:
                msg.write(f"📋 Preparado para aplicar velocidad **{factor}**\n")
                msg.write("⚠️ Adjunta un video para aplicar el cambio.\n")
                msg.write(f"{'🐢 Cámara lenta' if factor_num < 1 else '🚀 Acelerado'}: "
                          f"el video se reproducirá a {factor_num}x\n")
                return

            msg.write(f"📎 Archivo: {attachments[0].name}\n")
            msg.write(f"{'🐢 Cámara lenta' if factor_num < 1 else '🚀 Acelerado'}\n\n")

        system = (
            f"Eres un editor de video. Cambia la velocidad del video adjunto a {factor_num}x. "
            f"Usa ffmpeg con: -filter:v 'setpts={1/factor_num}*PTS' "
            f"y -filter:a 'atempo={factor_num}' (encadena atempo si >2x). "
            "Entrega el archivo resultante."
        )
        poe.call(
            "Claude-Code",
            poe.Message(text=system, sender="system"),
            poe.query,
            parameters={"thinking_budget": 8000},
            output=poe.default_chat,
        )

    def cmd_subtitle(self, params):
        """Subtitle command — generar subtítulos automáticos."""
        lang = self.params["language"]
        lang_info = LANG_MAP.get(lang, LANG_MAP["es"])

        with poe.start_message() as msg:
            msg.write("📝 **Generación de Subtítulos Automáticos**\n\n")
            msg.write(f"🌍 Idioma: **{lang_info['name']}**\n\n")

        attachments = self._get_attachments()
        if not attachments:
            with poe.start_message() as msg:
                msg.write("⚠️ Adjunta un video o audio para generar subtítulos.\n")
            return

        # Paso 1: Transcribir con Whisper
        with poe.start_message() as msg:
            msg.write("🎙️ **Paso 1/3:** Transcribiendo con Whisper...\n")

        whisper_response = poe.call(
            "Whisper-V3-Large-T",
            poe.query,
        )
        transcript = whisper_response.text

        # Paso 2: Generar SRT con LLM
        with poe.start_message() as msg:
            msg.write("⏱️ **Paso 2/3:** Generando formato SRT con timestamps...\n")

        srt_response = poe.call(
            self.FAST_LLM,
            f"""Convierte esta transcripción en formato SRT (SubRip) con timestamps estimados.
Distribuye el texto en segmentos de 2-3 segundos, máximo 2 líneas por subtítulo.
Idioma: {lang_info['name']}

Transcripción:
{transcript}

Genera SOLO el contenido SRT, sin explicaciones. Empieza con el número 1.""",
        )

        # Paso 3: Entregar resultado
        with poe.start_message() as msg:
            msg.write("✅ **Paso 3/3:** Subtítulos generados\n\n")
            msg.write("**Transcripción:**\n")
            msg.write(f"> {transcript[:500]}{'...' if len(transcript) > 500 else ''}\n\n")
            msg.write("**Archivo SRT:**\n")
            srt_att = msg.attach_file(
                name="subtitulos.srt",
                contents=srt_response.text.encode('utf-8'),
                content_type="text/plain",
            )
            msg.write(f"\n📎 Descarga: `{srt_att.name}`\n\n")
            msg.write("💡 Para incrustar en el video: `añade subtítulos al video`")

    def cmd_thumbnail(self, params):
        """Thumbnail command — generar thumbnail con IA."""
        aspect = self.params["aspect_ratio"]
        image_model = self.params["image_model"]

        with poe.start_message() as msg:
            msg.write("🖼️ **Generación de Thumbnail con IA**\n\n")

        attachments = self._get_attachments()

        # Generar prompt de thumbnail con LLM
        context = poe.query.text
        if attachments:
            context += f"\n[Archivo adjunto: {attachments[0].name}]"

        prompt_response = poe.call(
            self.FAST_LLM,
            f"""Crea un prompt de generación de imagen para un thumbnail de YouTube/redes sociales.
Debe ser visualmente atractivo, con colores vibrantes, composición impactante.
El thumbnail debe comunicar: {context}

Output in ```json format:
```json
{{"prompt": "detailed english image prompt for thumbnail", "title_overlay": "short catchy title text"}}
```""",
        )
        parsed = parse_json_from_response(prompt_response.text, ["prompt"])
        if not parsed:
            parsed = {"prompt": f"Eye-catching YouTube thumbnail about {context}", "title_overlay": ""}

        with poe.start_message() as msg:
            msg.write(f"🎨 Generando con **{image_model}**...\n")
            msg.write(f"📐 Aspect Ratio: `{aspect}`\n\n")

        # Generar thumbnail
        img_params = {"aspect_ratio": aspect} if "Imagen" in image_model else {"aspect": aspect.replace(":", ":")}
        poe.call(
            image_model,
            parsed["prompt"],
            parameters=img_params,
            output=poe.default_chat,
        )

        if parsed.get("title_overlay"):
            with poe.start_message() as msg:
                msg.write(f"\n💡 **Texto sugerido para overlay:** `{parsed['title_overlay']}`\n")
                msg.write("Puedes editar con: `añade texto '[tu texto]' al thumbnail`")

    def cmd_voiceover(self, params):
        """Voiceover command — generar voz en off con ElevenLabs."""
        text = params.get("text", poe.query.text)
        voice = self.params["voice"]
        lang = self.params["language"]

        # Limpiar el texto de comandos
        text = re.sub(r'(?i)^(voz en off|voiceover|narra|narración)[:\s]*', '', text).strip()
        if not text:
            with poe.start_message() as msg:
                msg.write("🎙️ **Voz en Off**\n\n")
                msg.write("⚠️ Indica el texto a narrar:\n")
                msg.write("Ejemplo: `voz en off: Bienvenidos a nuestro canal...`\n")
            return

        # Truncar a 40000 caracteres (límite ElevenLabs-v2.5-Turbo)
        if len(text) > 40000:
            text = text[:40000].rsplit(' ', 1)[0]

        with poe.start_message() as msg:
            msg.write("🎙️ **Generando Voz en Off**\n\n")
            msg.write(f"🗣️ Voz: **{voice}**\n")
            msg.write(f"🌍 Idioma: **{LANG_MAP.get(lang, LANG_MAP['es'])['name']}**\n")
            msg.write(f"📝 Texto: *{text[:100]}{'...' if len(text) > 100 else ''}*\n\n")

        tts_params = {"voice": voice}
        if lang != "en":
            tts_params["language"] = lang

        poe.call(
            "ElevenLabs-v2.5-Turbo",
            text,
            parameters=tts_params,
            output=poe.default_chat,
        )

    def cmd_music(self, params):
        """Music command — generar música con IA."""
        style = params.get("style", "cinematic epic background music")
        duration = int(params.get("duration_ms", 30000))

        with poe.start_message() as msg:
            msg.write("🎵 **Generación de Música con IA**\n\n")
            msg.write(f"🎼 Estilo: **{style}**\n")
            msg.write(f"⏱️ Duración: **{duration // 1000}s**\n\n")

        poe.call(
            "ElevenLabs-Music",
            style,
            parameters={"music_length_ms": duration},
            output=poe.default_chat,
        )

    # ─────────────────────────────────────────────────
    # P2: AUTO-DETECCIÓN DE ESCENAS
    # ─────────────────────────────────────────────────

    def cmd_detect_scenes(self, params):
        """Detect scenes — análisis automático de escenas/cortes."""
        attachments = self._get_attachments()

        with poe.start_message() as msg:
            msg.write("🔍 **Auto-Detección de Escenas**\n\n")

        if not attachments:
            with poe.start_message() as msg:
                msg.write("⚠️ Adjunta un video para analizar sus escenas.\n")
                msg.write("Analizaré:\n")
                msg.write("• 🎬 Cortes y transiciones\n")
                msg.write("• 📊 Duración de cada escena\n")
                msg.write("• 🎭 Tipo de contenido por segmento\n")
                msg.write("• ✂️ Puntos óptimos de corte\n")
            return

        # Usar Claude-Code con ffmpeg para detección de escenas
        system = """Eres un analista de video profesional. Analiza el video adjunto para detectar escenas.

PROCESO:
1. Usa ffprobe para obtener metadatos (duración, resolución, fps, codec)
2. Usa ffmpeg con el filtro 'select=gt(scene\\,0.3)' para detectar cambios de escena
3. Genera un informe estructurado con:
   - Metadatos del video
   - Lista de escenas detectadas con timestamps
   - Duración de cada escena
   - Sugerencias de puntos de corte óptimos

FORMATO DE SALIDA:
Presenta los resultados en una tabla markdown clara y legible.
Incluye un resumen ejecutivo al final con recomendaciones de edición."""

        poe.call(
            "Claude-Code",
            poe.Message(text=system, sender="system"),
            poe.query,
            parameters={"thinking_budget": 12000},
            output=poe.default_chat,
        )

    # ─────────────────────────────────────────────────
    # P3: TRANSCRIPCIÓN AUTOMÁTICA + CONTENIDO DERIVADO
    # ─────────────────────────────────────────────────

    def cmd_transcribe(self, params):
        """Transcribe — Whisper + contenido derivado automático."""
        attachments = self._get_attachments()
        lang = self.params["language"]
        lang_info = LANG_MAP.get(lang, LANG_MAP["es"])

        if not attachments:
            with poe.start_message() as msg:
                msg.write("📝 **Transcripción Automática + Contenido Derivado**\n\n")
                msg.write("⚠️ Adjunta un video o audio para transcribir.\n")
                msg.write("Generaré automáticamente:\n")
                msg.write("• 📝 Transcripción completa\n")
                msg.write("• 📋 Resumen ejecutivo\n")
                msg.write("• ⏱️ Timestamps clave\n")
                msg.write("• 📱 Posts para redes sociales\n")
                msg.write("• 📰 Artículo de blog\n")
                msg.write("• 🏷️ Tags SEO + descripción\n")
            return

        # Paso 1: Transcribir con Whisper
        with poe.start_message() as msg:
            msg.write("📝 **Transcripción + Contenido Derivado**\n\n")
            msg.write(f"🌍 Idioma: **{lang_info['name']}**\n")
            msg.write(f"📎 Archivo: **{attachments[0].name}**\n\n")
            msg.write("🎙️ **Paso 1/3:** Transcribiendo con Whisper...\n")

        whisper_response = poe.call("Whisper-V3-Large-T", poe.query)
        transcript = whisper_response.text

        with poe.start_message() as msg:
            msg.write("✅ Transcripción completada\n\n")
            msg.write(f"📝 **Texto transcrito** ({len(transcript)} caracteres):\n\n")
            msg.write(f"> {transcript[:800]}{'...' if len(transcript) > 800 else ''}\n")

        # Paso 2: Generar archivo de transcripción
        with poe.start_message() as msg:
            msg.write("\n📄 **Paso 2/3:** Generando archivos...\n")
            msg.attach_file(
                name="transcripcion_completa.txt",
                contents=transcript.encode('utf-8'),
                content_type="text/plain",
            )

        # Paso 3: Generar contenido derivado con IA
        with poe.start_message() as msg:
            msg.write("🤖 **Paso 3/3:** Generando contenido derivado con IA...\n\n")

        poe.call(
            self.ANALYZER,
            f"""A partir de esta transcripción de video, genera TODO el contenido derivado.
Idioma de salida: {lang_info['name']}

TRANSCRIPCIÓN:
{transcript}

GENERA (todo en {lang_info['name']}):

## 📋 Resumen Ejecutivo
(3-5 oraciones clave)

## ⏱️ Timestamps Clave
(lista con los momentos más importantes y su timestamp estimado)

## 📱 Posts para Redes Sociales
### Twitter/X (máx 280 caracteres, incluye hashtags)
### Instagram Caption (con emojis y CTA)
### LinkedIn Post (profesional, 2-3 párrafos)

## 📰 Artículo de Blog
(500-800 palabras basado en el contenido)

## 🏷️ SEO
### Título optimizado
### Meta descripción (155 caracteres)
### Tags (10-15 keywords relevantes separados por comas)
### Descripción para YouTube (con timestamps)""",
            parameters={"thinking_budget": 4000},
            output=poe.default_chat,
        )

    # ─────────────────────────────────────────────────
    # FASE 2.1: PIPELINE IA GENERATIVA
    # ─────────────────────────────────────────────────

    def cmd_storyboard(self, params):
        """Storyboard — crear storyboard visual con IA generativa."""
        concept = params.get("concept", poe.query.text)
        concept = re.sub(r'(?i)^storyboard[:\s]*', '', concept).strip()
        if not concept:
            with poe.start_message() as msg:
                msg.write("🎬 **Storyboard Visual con IA**\n\n")
                msg.write("⚠️ Describe tu idea:\n")
                msg.write("Ejemplo: `storyboard: un anuncio de café artesanal en una cafetería vintage`\n")
            return

        image_model = self.params["image_model"]
        aspect = self.params["aspect_ratio"]

        with poe.start_message() as msg:
            msg.write("🎬 **Generando Storyboard Visual**\n\n")
            msg.write(f"💡 Concepto: *{concept}*\n")
            msg.write(f"📐 Formato: `{aspect}`\n\n")
            msg.write("🤖 **Paso 1/2:** Diseñando escenas con IA...\n")

        # Generar descripción de escenas
        scenes_response = poe.call(
            self.ANALYZER,
            f"""Eres un director de cine y storyboard artist. Crea un storyboard de 4 escenas para este concepto:

CONCEPTO: {concept}
FORMATO: {aspect}

Para cada escena genera:
1. Número de escena y título
2. Duración estimada
3. Descripción visual detallada (composición, iluminación, colores, acción)
4. Prompt de imagen en inglés para generar la escena con IA

Output in ```json format:
```json
{{"scenes": [
  {{"number": 1, "title": "Título", "duration": "3s", "description": "Descripción visual", "image_prompt": "english prompt for AI image generation"}},
  {{"number": 2, "title": "Título", "duration": "3s", "description": "Descripción visual", "image_prompt": "english prompt for AI image generation"}},
  {{"number": 3, "title": "Título", "duration": "3s", "description": "Descripción visual", "image_prompt": "english prompt for AI image generation"}},
  {{"number": 4, "title": "Título", "duration": "3s", "description": "Descripción visual", "image_prompt": "english prompt for AI image generation"}}
]}}
```""",
            parameters={"thinking_budget": 4000},
        )

        parsed = parse_json_from_response(scenes_response.text, ["scenes"])
        if not parsed or not parsed.get("scenes"):
            with poe.start_message() as msg:
                msg.write("⚠️ No pude generar las escenas. Intenta con una descripción más detallada.\n")
            return

        scenes = parsed["scenes"]

        with poe.start_message() as msg:
            msg.write(f"✅ {len(scenes)} escenas diseñadas\n\n")
            msg.write("🎨 **Paso 2/2:** Generando imágenes en paralelo...\n\n")

        # Generar imágenes en paralelo
        img_params = {}
        if "Imagen" in image_model:
            img_params = {"aspect_ratio": aspect}
        elif "GPT" in image_model:
            img_params = {"aspect": aspect.replace("16:9", "3:2").replace("9:16", "2:3")}

        image_responses = poe.parallel(*[
            lambda s=scene: poe.call(
                image_model,
                s["image_prompt"],
                parameters=img_params,
            )
            for scene in scenes
        ], return_exceptions=True)

        # Mostrar storyboard completo
        with poe.start_message() as msg:
            msg.write("🎬 **STORYBOARD COMPLETO**\n\n")
            for i, scene in enumerate(scenes):
                msg.write(f"### Escena {scene['number']}: {scene['title']}\n")
                msg.write(f"⏱️ Duración: {scene['duration']}\n")
                msg.write(f"📝 {scene['description']}\n\n")

                # Añadir imagen si se generó correctamente
                if i < len(image_responses) and not isinstance(image_responses[i], Exception):
                    resp = image_responses[i]
                    if resp.last and resp.last.attachments:
                        msg.add_attachment(resp.last.attachments[0])
                msg.write("\n---\n\n")

            msg.write("💡 **Siguiente paso:** `genera video` para convertir este storyboard en clips.\n")

    def cmd_generate_video(self, params):
        """Generate video — video IA desde texto o imagen."""
        prompt = params.get("prompt", poe.query.text)
        prompt = re.sub(r'(?i)^(genera video|generate video|crea video)[:\s]*', '', prompt).strip()
        video_model = self.params["video_model"]
        aspect = self.params["aspect_ratio"]
        duration = self.params["video_duration"]
        audio = self.params["video_audio"]
        attachments = self._get_attachments()

        with poe.start_message() as msg:
            msg.write("🎬 **Generación de Video con IA**\n\n")
            msg.write(f"🤖 Modelo: **{video_model}**\n")
            msg.write(f"📐 Formato: `{aspect}`\n")
            msg.write(f"⏱️ Duración: `{duration}s`\n")
            msg.write(f"🔊 Audio: {'Sí' if audio else 'No'}\n")
            if attachments:
                msg.write(f"📎 Imagen de referencia: {attachments[0].name}\n")
            msg.write(f"\n📝 Prompt: *{prompt[:200]}*\n\n")
            msg.write("⏳ Generando (puede tardar 1-3 minutos)...\n")

        # Configurar parámetros según el modelo
        vid_params = {}
        if video_model == "Sora-2":
            size = "1280x720" if "16" in aspect.split(":")[0] else "720x1280"
            vid_params = {"size": size, "duration": duration}
        elif video_model == "Veo-v3.1":
            vid_params = {
                "aspect": aspect.replace(":", ":"),
                "duration": f"{duration}s",
                "silent": not audio,
            }
        elif video_model == "Veo-3.1-Fast":
            vid_params = {
                "aspect_ratio": aspect.replace(":", ":"),
                "duration": f"{duration}s",
                "silent": not audio,
            }

        # Construir mensaje con imagen de referencia si hay
        if attachments:
            call_msg = poe.Message(
                text=prompt,
                attachments=attachments[:1],
            )
            poe.call(video_model, call_msg, parameters=vid_params, output=poe.default_chat)
        else:
            poe.call(video_model, prompt, parameters=vid_params, output=poe.default_chat)

    def cmd_generate_image(self, params):
        """Generate image — imagen IA desde prompt."""
        prompt = params.get("prompt", poe.query.text)
        prompt = re.sub(r'(?i)^(genera imagen|generate image|crea imagen)[:\s]*', '', prompt).strip()
        image_model = self.params["image_model"]
        aspect = self.params["aspect_ratio"]

        with poe.start_message() as msg:
            msg.write("🖼️ **Generación de Imagen con IA**\n\n")
            msg.write(f"🎨 Modelo: **{image_model}**\n")
            msg.write(f"📐 Formato: `{aspect}`\n\n")

        img_params = {}
        if "Imagen" in image_model:
            img_params = {"aspect_ratio": aspect}
        elif "GPT" in image_model:
            img_params = {"aspect": aspect.replace("16:9", "3:2").replace("9:16", "2:3")}

        poe.call(image_model, prompt, parameters=img_params, output=poe.default_chat)

    def cmd_analyze(self, params):
        """Analyze — analizar video/imagen adjunto."""
        attachments = self._get_attachments()
        if not attachments:
            with poe.start_message() as msg:
                msg.write("🔍 **Análisis de Contenido**\n\n")
                msg.write("⚠️ Adjunta un video, imagen o audio para analizar.\n")
            return

        with poe.start_message() as msg:
            msg.write("🔍 **Analizando contenido adjunto...**\n\n")

        poe.call(
            self.ANALYZER,
            poe.Message(
                text=(
                    "Analiza este contenido multimedia en detalle. Proporciona:\n"
                    "1. Descripción general del contenido\n"
                    "2. Calidad técnica (resolución, iluminación, audio)\n"
                    "3. Composición y encuadre\n"
                    "4. Sugerencias de mejora para producción profesional\n"
                    "5. Ideas de edición y post-producción\n"
                    f"Contexto del usuario: {poe.query.text}"
                ),
                attachments=attachments,
            ),
            parameters={"thinking_budget": 4000},
            output=poe.default_chat,
        )

    def cmd_general(self, params):
        """General — consultas generales sobre video/edición."""
        poe.call(
            self.ANALYZER,
            poe.Message(
                text=(
                    "Eres VideoProsumer v2.0, un asistente experto en producción de video, "
                    "edición, post-producción, y marketing de contenido multimedia. "
                    "Responde de forma práctica y profesional."
                ),
                sender="system",
            ),
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True,
        )

    # ─────────────────────────────────────────────────
    # FASE 2.2: NUEVOS COMANDOS AVANZADOS
    # ─────────────────────────────────────────────────

    def cmd_editor(self, params):
        """Editor — abrir Canvas Editor Visual interactivo."""
        with poe.start_message() as msg:
            msg.write("🎬 **VideoProsumer v2.0 — Editor Visual**\n\n")
            msg.write("Arrastra un video al editor o usa las herramientas del panel lateral.\n")
            msg.write("Haz clic en cualquier herramienta IA para copiar el comando al portapapeles.\n\n")
            # Escape backticks: EDITOR_HTML needs 4+ backtick fence
            msg.write("````html\n" + EDITOR_HTML + "\n````\n")

    def cmd_silence_detect(self, params):
        """Silence detect — detectar silencios en audio/video con ffmpeg."""
        threshold = params.get("threshold", "-30dB")
        min_duration = params.get("min_duration", "0.5")
        attachments = self._get_attachments()

        with poe.start_message() as msg:
            msg.write("🔇 **Detección de Silencios**\n\n")
            msg.write(f"🎚️ Umbral: `{threshold}`\n")
            msg.write(f"⏱️ Duración mínima: `{min_duration}s`\n\n")

        if not attachments:
            with poe.start_message() as msg:
                msg.write("⚠️ Adjunta un video o audio para detectar silencios.\n\n")
                msg.write("Analizaré:\n")
                msg.write("• 🔇 Segmentos de silencio con timestamps\n")
                msg.write("• 📊 Duración de cada silencio\n")
                msg.write("• ✂️ Sugerencias de corte para eliminar silencios\n")
                msg.write("• 📋 Comando ffmpeg listo para ejecutar\n")
            return

        system = (
            "Eres un editor de audio/video profesional. Detecta todos los silencios en el archivo adjunto.\n\n"
            "PROCESO:\n"
            "1. Usa ffprobe para obtener metadatos del archivo\n"
            f"2. Usa ffmpeg con filtro silencedetect: -af silencedetect=noise={threshold}:d={min_duration}\n"
            "3. Parsea la salida y genera una tabla con:\n"
            "   - Timestamp de inicio y fin de cada silencio\n"
            "   - Duración de cada silencio\n"
            "   - Porcentaje del total que son silencios\n"
            "4. Genera un comando ffmpeg listo para eliminar los silencios automáticamente\n"
            "5. Sugiere puntos de corte óptimos para edición\n\n"
            "Presenta TODO en formato markdown con tablas claras."
        )
        poe.call(
            "Claude-Code",
            poe.Message(text=system, sender="system"),
            poe.query,
            parameters={"thinking_budget": 10000},
            output=poe.default_chat,
        )

    def cmd_transition(self, params):
        """Transition — añadir transición entre clips con ffmpeg."""
        tr_type = params.get("type", "crossfade")
        duration = params.get("duration", "1")
        attachments = self._get_attachments()

        with poe.start_message() as msg:
            msg.write("🔀 **Transiciones entre Clips**\n\n")
            msg.write(f"🎭 Tipo: **{tr_type}**\n")
            msg.write(f"⏱️ Duración: **{duration}s**\n\n")

        if not attachments:
            with poe.start_message() as msg:
                msg.write("⚠️ Adjunta uno o más videos para aplicar transiciones.\n\n")
                msg.write("**Transiciones disponibles:**\n")
                msg.write("• `crossfade` — Fundido cruzado (más suave)\n")
                msg.write("• `fade` — Fundido a negro\n")
                msg.write("• `wipeleft` / `wiperight` — Barrido lateral\n")
                msg.write("• `slideup` / `slidedown` — Deslizamiento vertical\n")
                msg.write("• `circleopen` / `circleclose` — Transición circular\n")
                msg.write("• `dissolve` — Disolución\n\n")
                msg.write("**Ejemplo:** `transición crossfade 1.5s entre clip1 y clip2`\n")
            return

        system = (
            f"Eres un editor de video profesional. Aplica una transición '{tr_type}' de {duration}s al video adjunto.\n\n"
            "PROCESO:\n"
            "1. Usa ffprobe para analizar los archivos adjuntos\n"
            f"2. Si hay un solo video, divide en la mitad y aplica transición xfade tipo '{tr_type}'\n"
            "3. Si hay múltiples videos, concatena con transición entre cada par\n"
            f"4. Comando base: ffmpeg -i input1 -i input2 -filter_complex 'xfade=transition={tr_type}:duration={duration}:offset=X'\n"
            "5. Entrega el archivo resultante con la transición aplicada\n\n"
            "IMPORTANTE: Calcula el offset correctamente (duración_video1 - duración_transición)."
        )
        poe.call(
            "Claude-Code",
            poe.Message(text=system, sender="system"),
            poe.query,
            parameters={"thinking_budget": 10000},
            output=poe.default_chat,
        )

    def cmd_text_overlay(self, params):
        """Text overlay — añadir texto superpuesto al video con ffmpeg."""
        text = params.get("text", "")
        position = params.get("position", "center")
        start = params.get("start", "0")
        duration = params.get("duration", "5")
        attachments = self._get_attachments()

        with poe.start_message() as msg:
            msg.write("✏️ **Texto Superpuesto (Overlay)**\n\n")
            if text:
                msg.write(f"📝 Texto: **{text}**\n")
            msg.write(f"📍 Posición: `{position}`\n")
            msg.write(f"⏱️ Desde `{start}s` durante `{duration}s`\n\n")

        if not attachments:
            with poe.start_message() as msg:
                msg.write("⚠️ Adjunta un video para añadir texto superpuesto.\n\n")
                msg.write("**Posiciones disponibles:**\n")
                msg.write("• `center` — Centro de la pantalla\n")
                msg.write("• `top` / `bottom` — Arriba / abajo\n")
                msg.write("• `top-left` / `top-right` — Esquinas superiores\n")
                msg.write("• `bottom-left` / `bottom-right` — Esquinas inferiores\n\n")
                msg.write("**Ejemplo:** `añade texto 'Suscríbete' abajo durante 3s`\n")
            return

        if not text:
            text = re.sub(
                r'(?i)^(añade texto|text overlay|texto|overlay)[:\s]*', '', poe.query.text
            ).strip().strip("'\"")

        system = (
            f"Eres un editor de video profesional. Añade texto superpuesto al video adjunto.\n\n"
            f"TEXTO: {text}\n"
            f"POSICIÓN: {position}\n"
            f"INICIO: {start}s\n"
            f"DURACIÓN: {duration}s\n\n"
            "PROCESO:\n"
            "1. Usa ffprobe para obtener resolución del video\n"
            "2. Calcula coordenadas x/y según la posición solicitada\n"
            "3. Aplica con ffmpeg drawtext:\n"
            f"   ffmpeg -i input -vf \"drawtext=text='{text}':fontsize=48:fontcolor=white:"
            "borderw=2:bordercolor=black:x=X:y=Y:enable='between(t,START,END)'\"\n"
            "4. Usa una fuente legible y con sombra/borde para visibilidad\n"
            "5. Entrega el archivo resultante"
        )
        poe.call(
            "Claude-Code",
            poe.Message(text=system, sender="system"),
            poe.query,
            parameters={"thinking_budget": 10000},
            output=poe.default_chat,
        )

    def cmd_director(self, params):
        """Director IA — pipeline completo de producción automatizada.

        Pipeline: Guión → Storyboard → Imágenes → Videos → Voz en off → Música → Montaje
        """
        concept = params.get("concept", poe.query.text)
        concept = re.sub(r'(?i)^(director|dirección|produce|producción)[:\s]*', '', concept).strip()

        if not concept:
            with poe.start_message() as msg:
                msg.write("🎬 **Director IA — Producción Completa**\n\n")
                msg.write("⚠️ Describe el video que quieres producir:\n\n")
                msg.write("**Ejemplo:** `director: un anuncio de 30s para una app de meditación, "
                          "estilo minimalista con colores pastel y música relajante`\n\n")
                msg.write("El Director IA ejecutará automáticamente:\n")
                msg.write("1. 📝 Guión y escaleta\n")
                msg.write("2. 🎬 Storyboard visual (4-6 escenas)\n")
                msg.write("3. 🖼️ Generación de imágenes por escena\n")
                msg.write("4. 🎥 Generación de video IA por escena\n")
                msg.write("5. 🎙️ Voz en off del guión\n")
                msg.write("6. 🎵 Música de fondo personalizada\n")
                msg.write("7. 🎞️ Montaje final con Claude-Code\n")
            return

        image_model = self.params["image_model"]
        video_model = self.params["video_model"]
        aspect = self.params["aspect_ratio"]
        lang = self.params["language"]
        lang_info = LANG_MAP.get(lang, LANG_MAP["es"])
        voice = self.params["voice"]
        duration = self.params["video_duration"]
        audio_on = self.params["video_audio"]

        # ─── PASO 1: Guión y escaleta ───
        with poe.start_message() as msg:
            msg.write("🎬 **DIRECTOR IA — Producción Completa**\n\n")
            msg.write(f"💡 Concepto: *{concept}*\n")
            msg.write(f"📐 Formato: `{aspect}` | 🌍 Idioma: **{lang_info['name']}**\n")
            msg.write(f"🤖 Modelos: {image_model} + {video_model}\n\n")
            msg.write("━" * 40 + "\n\n")
            msg.write("📝 **Paso 1/7:** Escribiendo guión y escaleta...\n")

        script_response = poe.call(
            self.ANALYZER,
            f"""Eres un director de cine y guionista profesional.
Crea un guión completo para este concepto de video:

CONCEPTO: {concept}
FORMATO: {aspect}
IDIOMA: {lang_info['name']}

Genera un guión con 4 escenas. Para cada escena incluye:
- Número, título y duración estimada
- Descripción visual detallada (composición, iluminación, movimiento de cámara)
- Texto de narración/voz en off en {lang_info['name']}
- Prompt de imagen en inglés para IA generativa

Output in ```json format:
```json
{{
  "title": "título del proyecto",
  "total_duration": "duración total estimada",
  "scenes": [
    {{
      "number": 1,
      "title": "Título de escena",
      "duration": "4s",
      "visual": "Descripción visual detallada",
      "narration": "Texto de narración en {lang_info['name']}",
      "image_prompt": "detailed english prompt for AI image generation, cinematic style",
      "video_prompt": "english prompt describing motion/action for video generation"
    }}
  ],
  "music_style": "descripción del estilo de música ideal"
}}
```""",
            parameters={"thinking_budget": 8000},
        )

        parsed = parse_json_from_response(script_response.text, ["scenes"])
        if not parsed or not parsed.get("scenes"):
            with poe.start_message() as msg:
                msg.write("⚠️ No pude generar el guión. Intenta con una descripción más detallada.\n")
            return

        scenes = parsed["scenes"]
        project_title = parsed.get("title", concept[:50])
        music_style = parsed.get("music_style", "cinematic background music")

        with poe.start_message() as msg:
            msg.write(f"✅ Guión creado: **{project_title}** ({len(scenes)} escenas)\n\n")

        # ─── PASO 2: Mostrar storyboard textual ───
        with poe.start_message() as msg:
            msg.write("📋 **Paso 2/7:** Escaleta del guión\n\n")
            for s in scenes:
                msg.write(f"**Escena {s['number']}: {s['title']}** ({s.get('duration', '4s')})\n")
                msg.write(f"📷 {s['visual'][:120]}...\n")
                msg.write(f"🗣️ *\"{s.get('narration', '')[:80]}...\"*\n\n")

        # ─── PASO 3: Generar imágenes en paralelo ───
        with poe.start_message() as msg:
            msg.write("🖼️ **Paso 3/7:** Generando imágenes de referencia en paralelo...\n\n")

        img_params = {}
        if "Imagen" in image_model:
            img_params = {"aspect_ratio": aspect}
        elif "GPT" in image_model:
            img_params = {"aspect": aspect.replace("16:9", "3:2").replace("9:16", "2:3")}

        image_responses = poe.parallel(*[
            lambda s=scene: poe.call(
                image_model,
                s["image_prompt"],
                parameters=img_params,
            )
            for scene in scenes
        ], return_exceptions=True)

        # Mostrar imágenes generadas
        with poe.start_message() as msg:
            msg.write("✅ **Imágenes de referencia generadas:**\n\n")
            for i, scene in enumerate(scenes):
                msg.write(f"**Escena {scene['number']}: {scene['title']}**\n")
                if i < len(image_responses) and not isinstance(image_responses[i], Exception):
                    resp = image_responses[i]
                    if resp.last and resp.last.attachments:
                        msg.add_attachment(resp.last.attachments[0])
                else:
                    msg.write("*(imagen no disponible)*\n")
                msg.write("\n")

        # ─── PASO 4: Generar voz en off completa ───
        narration_text = " ".join(s.get("narration", "") for s in scenes).strip()
        vo_response = None
        if narration_text:
            with poe.start_message() as msg:
                msg.write(f"🎙️ **Paso 4/7:** Generando voz en off ({voice})...\n\n")

            if len(narration_text) > 40000:
                narration_text = narration_text[:40000].rsplit(' ', 1)[0]

            tts_params = {"voice": voice}
            if lang != "en":
                tts_params["language"] = lang

            vo_response = poe.call(
                "ElevenLabs-v2.5-Turbo",
                narration_text,
                parameters=tts_params,
                output=poe.default_chat,
            )

        # ─── PASO 5: Generar música ───
        with poe.start_message() as msg:
            msg.write(f"🎵 **Paso 5/7:** Generando música ({music_style})...\n\n")

        music_duration = max(10000, len(scenes) * int(duration) * 1000)
        music_duration = min(music_duration, 300000)

        music_response = poe.call(
            "ElevenLabs-Music",
            f"{music_style} - background music for video production",
            parameters={"music_length_ms": music_duration},
            output=poe.default_chat,
        )

        # ─── PASO 6: Generar videos por escena (usando imágenes como referencia) ───
        with poe.start_message() as msg:
            msg.write(f"🎥 **Paso 6/7:** Generando clips de video con {video_model}...\n")
            msg.write("⏳ Esto puede tardar varios minutos por escena...\n\n")

        vid_params = {}
        if video_model == "Sora-2":
            size = "1280x720" if "16" in aspect.split(":")[0] else "720x1280"
            vid_params = {"size": size, "duration": duration}
        elif video_model == "Veo-v3.1":
            vid_params = {"aspect": aspect, "duration": f"{duration}s", "silent": not audio_on}
        elif video_model == "Veo-3.1-Fast":
            vid_params = {"aspect_ratio": aspect, "duration": f"{duration}s", "silent": not audio_on}

        # Generate videos using image references when available
        video_tasks = []
        for i, scene in enumerate(scenes):
            img_att = None
            if i < len(image_responses) and not isinstance(image_responses[i], Exception):
                resp = image_responses[i]
                if resp.last and resp.last.attachments:
                    img_att = resp.last.attachments[0]

            prompt_text = scene.get("video_prompt", scene["image_prompt"])
            if img_att:
                video_tasks.append(
                    lambda p=prompt_text, a=img_att: poe.call(
                        video_model,
                        poe.Message(text=p, attachments=[a]),
                        parameters=vid_params,
                        output=poe.default_chat,
                    )
                )
            else:
                video_tasks.append(
                    lambda p=prompt_text: poe.call(
                        video_model,
                        p,
                        parameters=vid_params,
                        output=poe.default_chat,
                    )
                )

        video_responses = poe.parallel(*video_tasks, return_exceptions=True)

        # ─── PASO 7: Resumen final ───
        successful_videos = sum(1 for r in video_responses if not isinstance(r, Exception))
        has_voiceover = vo_response is not None
        has_music = music_response is not None

        with poe.start_message() as msg:
            msg.write("━" * 40 + "\n\n")
            msg.write("🎬 **PRODUCCIÓN COMPLETADA**\n\n")
            msg.write(f"📽️ **Proyecto:** {project_title}\n\n")
            msg.write("**Resultados:**\n")
            msg.write(f"• 🖼️ {len(scenes)} imágenes de referencia generadas\n")
            msg.write(f"• 🎥 {successful_videos}/{len(scenes)} clips de video generados\n")
            msg.write(f"• 🎙️ Voz en off: {'✅ Generada' if has_voiceover else '⏭️ Omitida'}\n")
            msg.write(f"• 🎵 Música: {'✅ Generada' if has_music else '⏭️ Omitida'}\n\n")
            msg.write("**Próximos pasos:**\n")
            msg.write("• Escribe `editor` para abrir el editor visual y organizar los clips\n")
            msg.write("• Escribe `transición crossfade` para añadir transiciones entre escenas\n")
            msg.write("• Escribe `añade texto 'Tu título'` para overlay de texto\n")

    # ─────────────────────────────────────────────────
    # ORQUESTACIÓN
    # ─────────────────────────────────────────────────

    def classify_command(self):
        """Classify user command using LLM."""
        response = poe.call(
            self.FAST_LLM,
            poe.Message(text=self.CLASSIFY_PROMPT, sender="system"),
            f"Consulta del usuario: {poe.query.text}\n"
            f"Adjuntos: {len(self._get_attachments())} archivo(s)" if self._get_attachments()
            else f"Consulta del usuario: {poe.query.text}\nSin adjuntos.",
        )
        parsed = parse_json_from_response(response.text, ["command"])
        if parsed and parsed.get("command") in (
            "trim", "speed", "subtitle", "thumbnail", "voiceover", "music",
            "detect_scenes", "transcribe", "storyboard", "generate_video",
            "generate_image", "analyze", "general",
            "silence_detect", "transition", "text_overlay", "director", "editor",
        ):
            return parsed
        return {"command": "general", "params": {}, "reasoning": "fallback"}

    def run(self):
        """Main entry point."""
        query_lower = poe.query.text.strip().lower()

        # Comandos directos rápidos (sin LLM)
        quick_commands = {
            "panel": "show_panel",
            "dashboard": "show_panel",
            "editor": "show_editor",
            "ayuda": "show_help",
            "help": "show_help",
            "comandos": "show_help",
        }
        if query_lower in quick_commands:
            action = quick_commands[query_lower]
            if action == "show_help":
                self._show_help()
            elif action == "show_editor":
                self.cmd_editor({})
            return

        # Clasificar con LLM
        with poe.start_message() as msg:
            msg.write("🔄 *Analizando comando...*\n\n")
            classification = self.classify_command()
            command = classification.get("command", "general")
            cmd_params = classification.get("params", {})
            reasoning = classification.get("reasoning", "")
            msg.write(f"🎯 **Comando:** `{command}`\n")
            if reasoning:
                msg.write(f"📋 *{reasoning}*\n")

        # Enrutar al comando
        cmd_map = {
            "trim": self.cmd_trim,
            "speed": self.cmd_speed,
            "subtitle": self.cmd_subtitle,
            "thumbnail": self.cmd_thumbnail,
            "voiceover": self.cmd_voiceover,
            "music": self.cmd_music,
            "detect_scenes": self.cmd_detect_scenes,
            "transcribe": self.cmd_transcribe,
            "storyboard": self.cmd_storyboard,
            "generate_video": self.cmd_generate_video,
            "generate_image": self.cmd_generate_image,
            "analyze": self.cmd_analyze,
            "silence_detect": self.cmd_silence_detect,
            "transition": self.cmd_transition,
            "text_overlay": self.cmd_text_overlay,
            "director": self.cmd_director,
            "editor": self.cmd_editor,
            "general": self.cmd_general,
        }
        handler = cmd_map.get(command, self.cmd_general)
        handler(cmd_params)

    def _show_help(self):
        """Show available commands."""
        with poe.start_message() as msg:
            msg.write("📖 **VideoProsumer v2.0 — Comandos Disponibles**\n\n")
            msg.write("**✂️ Edición:**\n")
            msg.write("• `recorta 0:30 a 1:45` — Trim de segmento\n")
            msg.write("• `velocidad 2x` / `cámara lenta 0.5x` — Cambiar velocidad\n")
            msg.write("• `detecta silencios` — Detectar segmentos de silencio 🆕\n")
            msg.write("• `transición crossfade 1s` — Añadir transiciones entre clips 🆕\n")
            msg.write("• `añade texto 'Tu texto'` — Texto superpuesto al video 🆕\n\n")
            msg.write("**📝 Audio & Texto:**\n")
            msg.write("• `añade subtítulos` — Transcripción auto → SRT\n")
            msg.write("• `transcribe` — Whisper + contenido derivado (SEO, blog, social)\n")
            msg.write("• `voz en off: [texto]` — Narración con ElevenLabs\n")
            msg.write("• `música [estilo]` — Banda sonora IA\n\n")
            msg.write("**🔍 Análisis:**\n")
            msg.write("• `detecta escenas` — Auto-detección de cortes con ffmpeg\n")
            msg.write("• `analiza` — Análisis completo del contenido adjunto\n\n")
            msg.write("**🎨 IA Generativa:**\n")
            msg.write("• `genera thumbnail` — Thumbnail IA para YouTube\n")
            msg.write("• `storyboard [idea]` — Storyboard visual (4 escenas)\n")
            msg.write("• `genera video [prompt]` — Video IA desde texto\n")
            msg.write("• `genera imagen [prompt]` — Imagen IA\n\n")
            msg.write("**👑 Premium:**\n")
            msg.write("• `director: [concepto]` — Producción IA completa automatizada 🆕\n")
            msg.write("  *(guión → storyboard → imágenes → video → voz → música)*\n")
            msg.write("• `editor` — Abrir editor visual interactivo 🆕\n\n")
            msg.write("⚙️ Ajusta modelos, idioma y voz en el icono de configuración.\n")


if __name__ == "__main__":
    bot = VideoProsumerBot()
    bot.run()