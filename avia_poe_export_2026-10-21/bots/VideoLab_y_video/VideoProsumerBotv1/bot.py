# poe: name=AVIA-Asistente

import json
import re
from fastapi_poe.types import SettingsResponse

# ═══════════════════════════════════════════════════════════════
# AVIA Asistente — Constelación Económica AVIA Nomada
# Orquestador: AVIA-Clon-Carlosv2
# Producción: AVIA-Studiov2
# Desarrollo Senior: AVIA-Seniorv3.2
# Principios: Design Atómico | Libro Blanco | Consenso Económico
# ═══════════════════════════════════════════════════════════════

poe.update_settings(SettingsResponse(
    introduction_message=(
        "🌌 **AVIA Asistente — Constelación Económica AVIA Nomada**\n\n"
        "Soy tu asistente inteligente orquestado por **AVIA-Clon-Carlosv2**.\n\n"
        "**Mi constelación de producción:**\n"
        "🧠 **AVIA-Clon-Carlosv2** — Orquestador y coordinador estratégico\n"
        "🎨 **AVIA-Studiov2** — Producción de contenidos, apps y bots\n"
        "👨‍💻 **AVIA-Seniorv3.2** — Desarrollo senior y autocorrección\n\n"
        "📌 **Comandos:**\n"
        "• Escribe **panel** → Dashboard interactivo con micrófono\n"
        "• Cualquier consulta → Se enruta al especialista óptimo\n\n"
        "¡Envía tu primera consulta o escribe **panel** para comenzar!"
    ),
    enable_image_comprehension=True,
))

# ═══════════════════════════════════════════════════════════════
# Dashboard HTML — Design Atómico + Libro Blanco
# ═══════════════════════════════════════════════════════════════

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AVIA Nomada — Constelación</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
/* ═══ DESIGN TOKENS (Átomos — Libro Blanco) ═══ */
:root {
  --c-primary: #7C3AED;
  --c-primary-light: #A78BFA;
  --c-primary-dark: #5B21B6;
  --c-primary-glow: rgba(124,58,237,0.35);
  --c-secondary: #06B6D4;
  --c-success: #10B981;
  --c-warning: #F59E0B;
  --c-error: #EF4444;
  --c-bg: #0B0B19;
  --c-surface: #14142B;
  --c-surface-2: #1E1E3A;
  --c-surface-3: #2A2A4A;
  --c-text: #E2E8F0;
  --c-text-muted: #8892A8;
  --c-border: rgba(124,58,237,0.2);
  --r-sm: 8px; --r-md: 14px; --r-lg: 22px; --r-full: 50%;
  --shadow: 0 4px 24px rgba(0,0,0,0.4);
  --glow: 0 0 30px var(--c-primary-glow);
  --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
}

/* ═══ RESET & BASE ═══ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{font-size:16px;-webkit-font-smoothing:antialiased}
body{font-family:var(--font);background:var(--c-bg);color:var(--c-text);min-height:100vh;overflow-x:hidden;line-height:1.6}

/* ═══ ÁTOMOS ═══ */
.badge{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:var(--r-sm);font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.5px}
.badge-active{background:rgba(16,185,129,.15);color:var(--c-success);border:1px solid rgba(16,185,129,.3)}
.badge-primary{background:rgba(124,58,237,.15);color:var(--c-primary-light);border:1px solid var(--c-border)}
.icon-circle{width:52px;height:52px;border-radius:var(--r-full);display:flex;align-items:center;justify-content:center;font-size:1.3rem;transition:transform .3s var(--ease), box-shadow .3s var(--ease)}
.btn{display:inline-flex;align-items:center;gap:6px;padding:8px 18px;border:none;border-radius:var(--r-sm);font-family:var(--font);font-size:.85rem;font-weight:500;cursor:pointer;transition:all .25s var(--ease)}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-primary{background:var(--c-primary);color:#fff}
.btn-primary:hover:not(:disabled){background:var(--c-primary-dark);box-shadow:var(--glow)}
.btn-ghost{background:var(--c-surface-2);color:var(--c-text-muted);border:1px solid var(--c-border)}
.btn-ghost:hover:not(:disabled){background:var(--c-surface-3);color:var(--c-text)}

/* ═══ MOLÉCULAS ═══ */
.bot-card{background:var(--c-surface);border:1px solid var(--c-border);border-radius:var(--r-md);padding:20px;text-align:center;transition:all .35s var(--ease);position:relative;overflow:hidden}
.bot-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:var(--r-md) var(--r-md) 0 0}
.bot-card:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
.bot-card h3{font-size:.95rem;margin:10px 0 4px;font-weight:600}
.bot-card p{font-size:.78rem;color:var(--c-text-muted);margin-bottom:10px}
.bot-card.orchestrator{border-color:rgba(124,58,237,.4)}
.bot-card.orchestrator::before{background:linear-gradient(90deg,var(--c-primary),var(--c-primary-light))}
.bot-card.orchestrator .icon-circle{background:rgba(124,58,237,.15);color:var(--c-primary-light);box-shadow:0 0 20px var(--c-primary-glow)}
.bot-card.producer{border-color:rgba(6,182,212,.3)}
.bot-card.producer::before{background:linear-gradient(90deg,#06B6D4,#22D3EE)}
.bot-card.producer .icon-circle{background:rgba(6,182,212,.12);color:var(--c-secondary)}
.bot-card.developer{border-color:rgba(16,185,129,.3)}
.bot-card.developer::before{background:linear-gradient(90deg,#10B981,#34D399)}
.bot-card.developer .icon-circle{background:rgba(16,185,129,.12);color:var(--c-success)}

.mic-panel{display:flex;flex-direction:column;align-items:center;gap:14px;padding:28px 20px}
.mic-btn{width:80px;height:80px;border-radius:var(--r-full);border:3px solid var(--c-primary);background:linear-gradient(135deg,var(--c-primary-dark),var(--c-primary));color:#fff;font-size:1.8rem;cursor:pointer;transition:all .3s var(--ease);position:relative;display:flex;align-items:center;justify-content:center}
.mic-btn:hover{transform:scale(1.08);box-shadow:var(--glow)}
.mic-btn.recording{background:linear-gradient(135deg,#DC2626,#EF4444);border-color:#EF4444;animation:pulse-rec 1.5s infinite}
.mic-btn.disabled{opacity:.35;cursor:not-allowed;border-color:var(--c-text-muted)}
.mic-status{font-size:.85rem;color:var(--c-text-muted);transition:color .3s}
.mic-status.active{color:var(--c-error);font-weight:500}
.mic-status.error{color:var(--c-warning)}

/* ═══ ORGANISMOS ═══ */
.header{padding:20px 24px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--c-border);background:linear-gradient(180deg,rgba(124,58,237,.08),transparent)}
.header .logo{display:flex;align-items:center;gap:12px}
.header .logo i{font-size:1.6rem;color:var(--c-primary-light)}
.header .logo h1{font-size:1.15rem;font-weight:700;background:linear-gradient(135deg,var(--c-primary-light),var(--c-secondary));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.header .version{font-size:.72rem;color:var(--c-text-muted)}

.constellation{padding:24px;display:flex;flex-direction:column;align-items:center;gap:16px}
.constellation h2{font-size:.9rem;color:var(--c-text-muted);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:4px}
.constellation .orchestrator-row{display:flex;justify-content:center;width:100%}
.constellation .orchestrator-row .bot-card{flex:0 1 280px}
.constellation .connectors{display:flex;justify-content:center;gap:0;width:200px;height:32px;position:relative}
.constellation .connectors::before,.constellation .connectors::after{content:'';position:absolute;top:0;width:2px;height:100%;background:linear-gradient(180deg,var(--c-primary-glow),transparent)}
.constellation .connectors::before{left:30%}
.constellation .connectors::after{right:30%}
.constellation .sub-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;width:100%;max-width:560px}

.voice-section{margin:0 24px;padding:24px;background:var(--c-surface);border:1px solid var(--c-border);border-radius:var(--r-md)}
.voice-section h2{font-size:.95rem;display:flex;align-items:center;gap:8px;margin-bottom:4px}
.voice-section h2 i{color:var(--c-primary-light)}
.transcript-box{margin-top:14px;min-height:80px;max-height:200px;overflow-y:auto;background:var(--c-bg);border:1px solid var(--c-border);border-radius:var(--r-sm);padding:14px;font-size:.88rem;line-height:1.7}
.transcript-box .placeholder{color:var(--c-text-muted);font-style:italic;font-size:.82rem}
.transcript-box .final{color:var(--c-text)}
.transcript-box .interim{color:var(--c-primary-light);opacity:.7}
.transcript-actions{display:flex;gap:8px;margin-top:12px;justify-content:flex-end}

/* ═══ TEMPLATES ═══ */
.dashboard{max-width:640px;margin:0 auto;display:flex;flex-direction:column;gap:20px;padding-bottom:24px}

.commands{margin:0 24px;display:flex;flex-wrap:wrap;gap:8px}
.cmd-chip{padding:8px 16px;background:var(--c-surface-2);border:1px solid var(--c-border);border-radius:var(--r-lg);font-size:.82rem;cursor:pointer;transition:all .25s var(--ease);user-select:none}
.cmd-chip:hover{background:var(--c-primary);border-color:var(--c-primary);color:#fff;transform:scale(1.04)}

.footer{text-align:center;padding:16px 24px;border-top:1px solid var(--c-border);font-size:.7rem;color:var(--c-text-muted)}

/* ═══ ANIMACIONES ═══ */
@keyframes pulse-rec{0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,.4)}50%{box-shadow:0 0 0 16px rgba(239,68,68,0)}}
@keyframes fade-in{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.bot-card{animation:fade-in .5s var(--ease) both}
.bot-card:nth-child(1){animation-delay:.1s}
.bot-card:nth-child(2){animation-delay:.25s}
.sub-row .bot-card:nth-child(1){animation-delay:.35s}
.sub-row .bot-card:nth-child(2){animation-delay:.45s}

/* ═══ RESPONSIVE (Libro Blanco) ═══ */
@media(max-width:480px){
  .constellation .sub-row{grid-template-columns:1fr}
  .header{padding:14px 16px}
  .constellation,.voice-section,.commands{margin-left:12px;margin-right:12px}
  .mic-btn{width:68px;height:68px;font-size:1.5rem}
}

/* ═══ ACCESSIBILITY (Libro Blanco — WCAG) ═══ */
:focus-visible{outline:2px solid var(--c-primary-light);outline-offset:2px}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}

/* Scrollbar */
.transcript-box::-webkit-scrollbar{width:6px}
.transcript-box::-webkit-scrollbar-track{background:var(--c-bg)}
.transcript-box::-webkit-scrollbar-thumb{background:var(--c-surface-3);border-radius:3px}

/* Custom Modal (No alert/confirm) */
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:100;align-items:center;justify-content:center}
.modal-overlay.active{display:flex}
.modal-box{background:var(--c-surface);border:1px solid var(--c-border);border-radius:var(--r-md);padding:24px;max-width:340px;text-align:center}
.modal-box p{margin-bottom:16px;font-size:.9rem}
.modal-box .btn{margin:0 auto}
</style>
</head>
<body>
<div class="dashboard">

  <!-- ═══ HEADER (Organismo) ═══ -->
  <header class="header" role="banner">
    <div class="logo">
      <i class="fas fa-satellite" aria-hidden="true"></i>
      <h1>AVIA Nomada</h1>
      <span class="badge badge-primary">Constelación</span>
    </div>
    <span class="version">v1.0 · Design Atómico</span>
  </header>

  <!-- ═══ CONSTELACIÓN (Organismo) ═══ -->
  <section class="constellation" aria-label="Mapa de constelación">
    <h2>Constelación Económica</h2>
    <div class="orchestrator-row">
      <article class="bot-card orchestrator" role="article" aria-label="Bot orquestador">
        <div class="icon-circle"><i class="fas fa-brain" aria-hidden="true"></i></div>
        <h3>AVIA-Clon-Carlosv2</h3>
        <p>Orquestador Principal</p>
        <span class="badge badge-active"><i class="fas fa-circle" style="font-size:6px" aria-hidden="true"></i> Activo</span>
      </article>
    </div>
    <div class="connectors" aria-hidden="true"></div>
    <div class="sub-row">
      <article class="bot-card producer" role="article" aria-label="Bot de producción">
        <div class="icon-circle"><i class="fas fa-palette" aria-hidden="true"></i></div>
        <h3>AVIA-Studiov2</h3>
        <p>Producción · Contenidos · Apps</p>
        <span class="badge badge-active"><i class="fas fa-circle" style="font-size:6px" aria-hidden="true"></i> Activo</span>
      </article>
      <article class="bot-card developer" role="article" aria-label="Bot de desarrollo">
        <div class="icon-circle"><i class="fas fa-code" aria-hidden="true"></i></div>
        <h3>AVIA-Seniorv3.2</h3>
        <p>Desarrollo · Corrección · QA</p>
        <span class="badge badge-active"><i class="fas fa-circle" style="font-size:6px" aria-hidden="true"></i> Activo</span>
      </article>
    </div>
  </section>

  <!-- ═══ VOZ (Organismo) ═══ -->
  <section class="voice-section" aria-label="Reconocimiento de voz">
    <h2><i class="fas fa-microphone-alt" aria-hidden="true"></i> Reconocimiento de Voz</h2>
    <div class="mic-panel">
      <button class="mic-btn" id="micBtn" aria-label="Activar micrófono para reconocimiento de voz" type="button">
        <i class="fas fa-microphone" id="micIcon" aria-hidden="true"></i>
      </button>
      <p class="mic-status" id="micStatus" role="status" aria-live="polite">Pulsa el botón para hablar</p>
    </div>
    <div class="transcript-box" id="transcript" role="log" aria-live="polite" aria-label="Transcripción de voz">
      <p class="placeholder">El texto reconocido aparecerá aquí...</p>
    </div>
    <div class="transcript-actions">
      <button class="btn btn-ghost" id="clearBtn" disabled type="button"><i class="fas fa-eraser" aria-hidden="true"></i> Limpiar</button>
      <button class="btn btn-primary" id="copyBtn" disabled type="button"><i class="fas fa-copy" aria-hidden="true"></i> Copiar al portapapeles</button>
    </div>
  </section>

  <!-- ═══ COMANDOS RÁPIDOS ═══ -->
  <nav class="commands" aria-label="Comandos rápidos">
    <span class="cmd-chip" data-text="panel" tabindex="0" role="button">📊 Panel</span>
    <span class="cmd-chip" data-text="Necesito crear contenido" tabindex="0" role="button">🎨 Producción</span>
    <span class="cmd-chip" data-text="Necesito ayuda con código" tabindex="0" role="button">💻 Desarrollo</span>
    <span class="cmd-chip" data-text="Analiza y corrige errores" tabindex="0" role="button">🔧 Autocorrección</span>
  </nav>

  <!-- ═══ FOOTER ═══ -->
  <footer class="footer" role="contentinfo">
    <p>AVIA Nomada v1.0 · Design Atómico · Libro Blanco · Consenso Económico</p>
  </footer>

  <!-- Modal (reemplaza alert/confirm) -->
  <div class="modal-overlay" id="modal" role="dialog" aria-modal="true" aria-labelledby="modalMsg">
    <div class="modal-box">
      <p id="modalMsg"></p>
      <button class="btn btn-primary" id="modalClose" type="button">Entendido</button>
    </div>
  </div>

</div>

<script>
/* ═══ CANVAS SANDBOX FIX: Override blocked native dialogs ═══ */
(function(){
  var _modalEl = document.getElementById('modal');
  var _modalMsgEl = document.getElementById('modalMsg');
  var _modalCloseEl = document.getElementById('modalClose');
  function _safeModal(msg) {
    if (_modalEl && _modalMsgEl) {
      _modalMsgEl.textContent = String(msg);
      _modalEl.classList.add('active');
    }
  }
  window.alert = function(msg){ _safeModal(msg); };
  window.confirm = function(msg){ _safeModal(msg); return true; };
  window.prompt = function(msg){ _safeModal(msg); return null; };
  if (_modalCloseEl) {
    _modalCloseEl.addEventListener('click', function(){ _modalEl.classList.remove('active'); });
  }
  if (_modalEl) {
    _modalEl.addEventListener('click', function(e){ if(e.target===_modalEl) _modalEl.classList.remove('active'); });
  }
})();

(function(){
  'use strict';

  /* ═══ UTILIDADES ═══ */
  var modal = document.getElementById('modal');
  var modalMsg = document.getElementById('modalMsg');
  var modalClose = document.getElementById('modalClose');

  function showModal(msg) {
    modalMsg.textContent = msg;
    modal.classList.add('active');
  }

  /* ═══ ELEMENTOS DOM ═══ */
  var micBtn = document.getElementById('micBtn');
  var micIcon = document.getElementById('micIcon');
  var micStatus = document.getElementById('micStatus');
  var transcript = document.getElementById('transcript');
  var copyBtn = document.getElementById('copyBtn');
  var clearBtn = document.getElementById('clearBtn');

  var isRecording = false;
  var fullTranscript = '';
  var recognition = null;

  /* ═══ WEB SPEECH API — CORRECCIÓN COMPLETA ═══ */
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    micStatus.textContent = 'Tu navegador no soporta reconocimiento de voz. Usa Chrome o Edge.';
    micStatus.classList.add('error');
    micBtn.classList.add('disabled');
    micBtn.setAttribute('aria-disabled', 'true');
  } else {
    try {
      recognition = new SpeechRecognition();
      recognition.lang = 'es-ES';
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;

      recognition.onstart = function() {
        isRecording = true;
        micBtn.classList.add('recording');
        micIcon.className = 'fas fa-stop';
        micStatus.textContent = 'Escuchando... pulsa para detener';
        micStatus.classList.add('active');
        micStatus.classList.remove('error');
      };

      recognition.onresult = function(event) {
        var interim = '';
        var finalText = '';
        for (var i = event.resultIndex; i < event.results.length; i++) {
          var t = event.results[i][0].transcript;
          if (event.results[i].isFinal) { finalText += t; }
          else { interim += t; }
        }
        if (finalText) { fullTranscript += finalText + ' '; }
        renderTranscript(interim);
      };

      recognition.onerror = function(event) {
        var msgs = {
          'not-allowed': 'Permiso de micrófono denegado. Haz clic en el icono de candado en la barra de direcciones y permite el micrófono.',
          'no-speech': 'No se detectó voz. Intenta hablar más cerca del micrófono.',
          'network': 'Error de red. Verifica tu conexión a internet.',
          'aborted': 'Reconocimiento cancelado.',
          'audio-capture': 'No se encontró ningún micrófono conectado.',
          'service-not-allowed': 'Servicio de voz no disponible. Intenta en Chrome o Edge.'
        };
        var msg = msgs[event.error] || 'Error: ' + event.error;
        micStatus.textContent = msg;
        micStatus.classList.add('error');
        micStatus.classList.remove('active');
        stopRec();
      };

      recognition.onend = function() {
        if (isRecording) {
          try { recognition.start(); }
          catch(e) { stopRec(); }
        }
      };
    } catch(e) {
      micStatus.textContent = 'Error al inicializar reconocimiento de voz: ' + e.message;
      micStatus.classList.add('error');
      micBtn.classList.add('disabled');
    }
  }

  function renderTranscript(interim) {
    transcript.innerHTML = '';
    if (fullTranscript.trim()) {
      var pF = document.createElement('p');
      pF.className = 'final';
      pF.textContent = fullTranscript.trim();
      transcript.appendChild(pF);
    }
    if (interim) {
      var pI = document.createElement('p');
      pI.className = 'interim';
      pI.textContent = interim;
      transcript.appendChild(pI);
    }
    if (!fullTranscript.trim() && !interim) {
      transcript.innerHTML = '<p class="placeholder">El texto reconocido aparecerá aquí...</p>';
    }
    transcript.scrollTop = transcript.scrollHeight;
    copyBtn.disabled = !fullTranscript.trim();
    clearBtn.disabled = !fullTranscript.trim();
  }

  function startRec() {
    if (!recognition) {
      showModal('El reconocimiento de voz no está disponible. Usa Google Chrome o Microsoft Edge para esta función.');
      return;
    }
    fullTranscript = '';
    renderTranscript('');
    try { recognition.start(); }
    catch(e) {
      if (e.message && e.message.indexOf('already started') > -1) {
        recognition.stop();
        setTimeout(function(){ try { recognition.start(); } catch(ex){} }, 200);
      } else {
        micStatus.textContent = 'Error al iniciar: ' + e.message;
        micStatus.classList.add('error');
      }
    }
  }

  function stopRec() {
    isRecording = false;
    micBtn.classList.remove('recording');
    micIcon.className = 'fas fa-microphone';
    micStatus.textContent = 'Pulsa el botón para hablar';
    micStatus.classList.remove('active');
    if (recognition) { try { recognition.stop(); } catch(e){} }
  }

  micBtn.addEventListener('click', function() {
    if (micBtn.classList.contains('disabled')) return;
    if (isRecording) { stopRec(); }
    else { startRec(); }
  });

  /* ═══ COPIAR AL PORTAPAPELES ═══ */
  copyBtn.addEventListener('click', function() {
    if (!fullTranscript.trim()) return;
    var text = fullTranscript.trim();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        copyBtn.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i> ¡Copiado!';
        setTimeout(function(){ copyBtn.innerHTML = '<i class="fas fa-copy" aria-hidden="true"></i> Copiar al portapapeles'; }, 2000);
      }).catch(function() { fallbackCopy(text); });
    } else { fallbackCopy(text); }
  });

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.style.cssText = 'position:fixed;left:-9999px';
    document.body.appendChild(ta); ta.select();
    try {
      document.execCommand('copy');
      copyBtn.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i> ¡Copiado!';
      setTimeout(function(){ copyBtn.innerHTML = '<i class="fas fa-copy" aria-hidden="true"></i> Copiar al portapapeles'; }, 2000);
    } catch(e) { showModal('No se pudo copiar. Selecciona el texto manualmente.'); }
    document.body.removeChild(ta);
  }

  /* ═══ LIMPIAR ═══ */
  clearBtn.addEventListener('click', function() {
    fullTranscript = '';
    renderTranscript('');
  });

  /* ═══ COMMAND CHIPS ═══ */
  document.querySelectorAll('.cmd-chip').forEach(function(chip) {
    chip.addEventListener('click', function() {
      var text = this.getAttribute('data-text');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function() {
          showModal('Comando copiado: "' + text + '". Pégalo en el chat de Poe para ejecutarlo.');
        }).catch(function(){ showModal('Escribe en el chat: ' + text); });
      } else { showModal('Escribe en el chat: ' + text); }
    });
    chip.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this.click(); }
    });
  });

})();
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════
# UTILIDAD: Parser JSON robusto
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


# ═══════════════════════════════════════════════════════════════
# CLASE PRINCIPAL: AVIA Asistente
# ═══════════════════════════════════════════════════════════════

class AVIAAsistente:
    """Constelación Económica AVIA Nomada — Orquestada por AVIA-Clon-Carlosv2."""

    ORCHESTRATOR = "AVIA-Clon-Carlosv2"
    PRODUCER = "AVIA-Studiov2"
    SENIOR_DEV = "AVIA-Seniorv3.2"

    SYSTEM_PROMPT = (
        "Eres AVIA-Clon-Carlosv2, el orquestador principal de la Constelación "
        "Económica AVIA Nomada. Tu rol es analizar cada consulta del usuario y "
        "determinar la mejor ruta de acción.\n\n"
        "RUTAS DISPONIBLES:\n"
        '- "production": Crear contenidos, apps, bots, multimedia, diseño, imágenes, '
        "videos, marketing, branding → AVIA-Studiov2\n"
        '- "development": Código, debugging, arquitectura, errores técnicos, HTML, CSS, '
        "JS, Python, corrección de bugs, testing, QA → AVIA-Seniorv3.2\n"
        '- "general": Consultas generales, estrategia, coordinación, planificación, '
        "preguntas de conocimiento → Tú mismo\n\n"
        "Responde SOLO con JSON válido:\n"
        '```json\n{"action": "production|development|general", "reasoning": "explicación breve"}\n```'
    )

    BOT_LABELS = {
        "production": ("🎨", "AVIA-Studiov2", "Producción"),
        "development": ("👨‍💻", "AVIA-Seniorv3.2", "Desarrollo Senior"),
        "general": ("🧠", "AVIA-Clon-Carlosv2", "Coordinación"),
    }

    def show_dashboard(self):
        """Display the interactive Canvas dashboard."""
        with poe.start_message() as msg:
            msg.write("🌌 **Panel de Control — Constelación AVIA Nomada**\n\n")
            msg.write(f"````html\n{DASHBOARD_HTML}\n````\n\n")
            msg.write(
                "💡 **Instrucciones:**\n"
                "- Pulsa el **botón púrpura** 🎙️ para dictar por voz\n"
                "- Usa **Copiar al portapapeles** y pega en el chat\n"
                "- Los **comandos rápidos** se copian al portapapeles al hacer clic\n"
            )

    def classify_query(self):
        """Use AVIA-Clon-Carlosv2 to classify the user's intent."""
        response = poe.call(
            self.ORCHESTRATOR,
            poe.Message(text=self.SYSTEM_PROMPT, sender="system"),
            f"Clasifica esta consulta del usuario:\n\n{poe.query}",
        )
        parsed = parse_json_from_response(response.text, ["action"])
        if parsed and parsed.get("action") in ("production", "development", "general"):
            return parsed
        return {"action": "general", "reasoning": "clasificación por defecto"}

    def route_to_bot(self, action):
        """Route the query to the appropriate constellation bot."""
        bot_map = {
            "production": self.PRODUCER,
            "development": self.SENIOR_DEV,
            "general": self.ORCHESTRATOR,
        }
        target_bot = bot_map.get(action, self.ORCHESTRATOR)
        poe.call(
            target_bot,
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True,
        )

    def run(self):
        """Main entry point for the bot."""
        query_lower = poe.query.text.strip().lower()

        # Dashboard commands
        dashboard_commands = {
            "panel", "dashboard", "menu", "inicio",
            "constelación", "constelacion", "mapa",
        }
        if query_lower in dashboard_commands:
            self.show_dashboard()
            return

        # Orchestrate through constellation
        with poe.start_message() as msg:
            msg.write("🔄 *Orquestador analizando consulta...*\n\n")
            classification = self.classify_query()
            action = classification.get("action", "general")
            reasoning = classification.get("reasoning", "")
            emoji, name, role = self.BOT_LABELS.get(action, self.BOT_LABELS["general"])
            msg.write(f"{emoji} **Ruta:** {name} *({role})*\n")
            if reasoning:
                msg.write(f"📋 *{reasoning}*\n")

        # Execute the routed bot call
        self.route_to_bot(action)


if __name__ == "__main__":
    bot = AVIAAsistente()
    bot.run()

