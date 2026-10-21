# poe: name=Elimina-Objetos

import json
import re
from io import BytesIO

from fastapi_poe.types import SettingsResponse

poe.update_settings(SettingsResponse(
    introduction_message=(
        "¡Hola! 👋 Soy **Elimina-Objetos**, tu eliminador de objetos con IA.\n\n"
        "📌 **Cómo usar:**\n"
        "1. **Envíame una imagen** con marcas de color sólido (rojo, verde, azul, amarillo) "
        "sobre los objetos que quieras eliminar\n"
        "2. O simplemente **envía una imagen** y dime qué quieres eliminar\n\n"
        "✨ 100% Automático — yo me encargo del resto"
    ),
    enable_image_comprehension=True,
))


def parse_json_from_response(response_text, required_fields=None):
    """Extract and parse JSON from a bot response."""
    # Try ```json codeblock first
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
    else:
        match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
        if match:
            json_str = match.group(0).strip()
        else:
            raise Exception("No JSON found in response")
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError:
        # Try to find the first valid JSON object by scanning for balanced braces
        depth = 0
        start = response_text.find('{')
        if start == -1:
            raise Exception("No JSON found in response")
        for i in range(start, len(response_text)):
            if response_text[i] == '{':
                depth += 1
            elif response_text[i] == '}':
                depth -= 1
                if depth == 0:
                    json_str = response_text[start:i + 1]
                    break
        parsed = json.loads(json_str)
    if required_fields:
        missing = set(required_fields) - set(parsed.keys())
        if missing:
            raise Exception(f"Missing fields: {', '.join(missing)}")
    return parsed


CANVAS_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Elimina-Objetos</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f0f1a;
    color: #e0e0e0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-x: hidden;
  }
  .header {
    text-align: center;
    padding: 16px 12px 8px;
    width: 100%;
    max-width: 700px;
  }
  .header h1 { font-size: 1.3em; color: #fff; }
  .header p { font-size: 0.85em; color: #888; margin-top: 4px; }
  .status-bar {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 10px 16px;
    margin: 8px 12px;
    width: calc(100% - 24px);
    max-width: 700px;
    font-size: 0.9em;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .status-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #4CAF50;
    flex-shrink: 0;
  }
  .status-dot.warning { background: #ff9800; }
  .canvas-container {
    position: relative;
    width: calc(100% - 24px);
    max-width: 700px;
    margin: 8px 12px;
    border-radius: 12px;
    overflow: hidden;
    background: #1a1a2e;
    border: 2px dashed #3a3a5a;
    min-height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: crosshair;
    touch-action: none;
  }
  .canvas-container.has-image { border-style: solid; border-color: #4a4a6a; }
  .canvas-container canvas {
    display: block;
    max-width: 100%;
    max-height: 70vh;
  }
  .upload-prompt {
    text-align: center;
    padding: 40px 20px;
    color: #666;
  }
  .upload-prompt .icon { font-size: 3em; margin-bottom: 12px; }
  .upload-prompt p { margin: 4px 0; }
  .toolbar {
    display: flex;
    gap: 8px;
    padding: 8px 12px;
    width: calc(100% - 24px);
    max-width: 700px;
    flex-wrap: wrap;
    justify-content: center;
  }
  .btn {
    padding: 10px 18px;
    border: none;
    border-radius: 8px;
    font-size: 0.85em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .btn:active { transform: scale(0.96); }
  .btn-primary { background: #6C63FF; color: #fff; }
  .btn-primary:hover { background: #5a52e0; }
  .btn-danger { background: #e74c3c; color: #fff; }
  .btn-danger:hover { background: #c0392b; }
  .btn-secondary { background: #2a2a4a; color: #ccc; }
  .btn-secondary:hover { background: #3a3a5a; }
  .btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .brush-size {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #1a1a2e;
    padding: 6px 14px;
    border-radius: 8px;
    border: 1px solid #2a2a4a;
  }
  .brush-size input[type=range] { width: 80px; accent-color: #e74c3c; }
  .brush-size span { font-size: 0.8em; color: #aaa; min-width: 30px; }
  .instructions {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 12px;
    width: calc(100% - 24px);
    max-width: 700px;
    font-size: 0.82em;
    color: #999;
    line-height: 1.6;
  }
  .instructions strong { color: #e74c3c; }
  input[type=file] { display: none; }

  /* Custom modal — replaces window.confirm / alert */
  .modal-overlay {
    display: none;
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.7);
    z-index: 1000;
    align-items: center;
    justify-content: center;
  }
  .modal-overlay.active { display: flex; }
  .modal-box {
    background: #1e1e32;
    border: 1px solid #3a3a5a;
    border-radius: 14px;
    padding: 24px;
    max-width: 360px;
    width: 90%;
    text-align: center;
  }
  .modal-box h3 { margin-bottom: 10px; color: #fff; font-size: 1.1em; }
  .modal-box p { color: #aaa; font-size: 0.9em; margin-bottom: 18px; }
  .modal-actions { display: flex; gap: 10px; justify-content: center; }
  .modal-actions .btn { min-width: 100px; justify-content: center; }
</style>
</head>
<body>

<div class="header">
  <h1>🎯 Eliminador de Objetos con IA</h1>
  <p>Marca lo que quieras eliminar y la IA lo restaurará</p>
</div>

<div class="status-bar">
  <div class="status-dot" id="statusDot"></div>
  <span id="statusText">✅ Listo — Sube una imagen para empezar</span>
</div>

<div class="canvas-container" id="canvasContainer">
  <div class="upload-prompt" id="uploadPrompt">
    <div class="icon">📷</div>
    <p><strong>Toca aquí</strong> o arrastra una imagen</p>
    <p style="font-size:0.85em; margin-top:8px;">JPG, PNG, WEBP</p>
  </div>
  <canvas id="mainCanvas" style="display:none;"></canvas>
  <canvas id="drawCanvas" style="display:none; position:absolute; top:0; left:0;"></canvas>
</div>

<div class="toolbar">
  <div class="brush-size">
    <span>🖌️</span>
    <input type="range" id="brushSize" min="5" max="80" value="25">
    <span id="brushLabel">25px</span>
  </div>
  <button class="btn btn-danger" id="btnUndo" disabled>↩️ Deshacer</button>
  <button class="btn btn-secondary" id="btnClear" disabled>🗑️ Limpiar</button>
  <button class="btn btn-primary" id="btnDownload" disabled>💾 Descargar marcada</button>
  <button class="btn btn-secondary" id="btnNewImage">📷 Nueva imagen</button>
</div>

<div class="instructions">
  <strong>📌 Instrucciones:</strong><br>
  1. Sube una imagen tocando el área superior<br>
  2. <strong>Pinta en rojo</strong> sobre los objetos a eliminar<br>
  3. Pulsa <strong>💾 Descargar marcada</strong> para obtener la imagen con marcas sólidas<br>
  4. Envía esa imagen descargada al bot y ¡la IA restaurará todo!
</div>

<input type="file" id="fileInput" accept="image/*">

<!-- Custom modal (replaces window.confirm) -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal-box">
    <h3 id="modalTitle">Confirmar</h3>
    <p id="modalMsg">¿Estás seguro?</p>
    <div class="modal-actions">
      <button class="btn btn-secondary" id="modalCancel">Cancelar</button>
      <button class="btn btn-danger" id="modalConfirm">Confirmar</button>
    </div>
  </div>
</div>

<script>
(function(){
  const mainCanvas  = document.getElementById('mainCanvas');
  const drawCanvas  = document.getElementById('drawCanvas');
  const mainCtx     = mainCanvas.getContext('2d');
  const drawCtx     = drawCanvas.getContext('2d');
  const container   = document.getElementById('canvasContainer');
  const uploadPrompt= document.getElementById('uploadPrompt');
  const fileInput   = document.getElementById('fileInput');
  const brushSlider = document.getElementById('brushSize');
  const brushLabel  = document.getElementById('brushLabel');
  const btnUndo     = document.getElementById('btnUndo');
  const btnClear    = document.getElementById('btnClear');
  const btnDownload = document.getElementById('btnDownload');
  const btnNewImage = document.getElementById('btnNewImage');
  const statusDot   = document.getElementById('statusDot');
  const statusText  = document.getElementById('statusText');

  let originalImage = null;
  let drawing = false;
  let strokes = []; // for undo
  let currentStroke = [];

  function setStatus(text, ok) {
    statusText.textContent = text;
    statusDot.className = 'status-dot' + (ok ? '' : ' warning');
  }

  /* ---- Custom modal (replaces window.confirm) ---- */
  function showModal(title, msg) {
    return new Promise(resolve => {
      document.getElementById('modalTitle').textContent = title;
      document.getElementById('modalMsg').textContent   = msg;
      const overlay = document.getElementById('modalOverlay');
      overlay.classList.add('active');
      document.getElementById('modalConfirm').onclick = () => { overlay.classList.remove('active'); resolve(true);  };
      document.getElementById('modalCancel').onclick  = () => { overlay.classList.remove('active'); resolve(false); };
    });
  }

  /* ---- Image loading ---- */
  function loadImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = new Image();
      img.onload = function() {
        // Fit to container
        const maxW = Math.min(700, container.clientWidth);
        const maxH = window.innerHeight * 0.65;
        let w = img.width, h = img.height;
        if (w > maxW) { h = h * maxW / w; w = maxW; }
        if (h > maxH) { w = w * maxH / h; h = maxH; }
        w = Math.round(w); h = Math.round(h);

        mainCanvas.width = w; mainCanvas.height = h;
        drawCanvas.width = w; drawCanvas.height = h;
        mainCtx.drawImage(img, 0, 0, w, h);
        originalImage = mainCtx.getImageData(0, 0, w, h);

        mainCanvas.style.display = 'block';
        drawCanvas.style.display = 'block';
        uploadPrompt.style.display = 'none';
        container.classList.add('has-image');
        strokes = [];
        drawCtx.clearRect(0, 0, w, h);
        updateButtons();
        setStatus('🎨 Pinta sobre los objetos que quieras eliminar', true);
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  /* ---- Drawing ---- */
  function getBrush() { return parseInt(brushSlider.value); }
  brushSlider.oninput = () => { brushLabel.textContent = brushSlider.value + 'px'; };

  function getPos(e) {
    const rect = drawCanvas.getBoundingClientRect();
    const t = e.touches ? e.touches[0] : e;
    return {
      x: (t.clientX - rect.left) * (drawCanvas.width  / rect.width),
      y: (t.clientY - rect.top)  * (drawCanvas.height / rect.height)
    };
  }

  function startDraw(e) {
    if (!originalImage) return;
    e.preventDefault();
    drawing = true;
    currentStroke = [];
    const p = getPos(e);
    currentStroke.push({ x: p.x, y: p.y, size: getBrush() });
    drawDot(p.x, p.y, getBrush());
  }
  function moveDraw(e) {
    if (!drawing) return;
    e.preventDefault();
    const p = getPos(e);
    currentStroke.push({ x: p.x, y: p.y, size: getBrush() });
    drawDot(p.x, p.y, getBrush());
  }
  function endDraw(e) {
    if (!drawing) return;
    drawing = false;
    if (currentStroke.length > 0) {
      strokes.push([...currentStroke]);
      currentStroke = [];
      updateButtons();
    }
  }

  function drawDot(x, y, size) {
    drawCtx.beginPath();
    drawCtx.arc(x, y, size / 2, 0, Math.PI * 2);
    drawCtx.fillStyle = 'rgba(255, 0, 0, 0.55)';
    drawCtx.fill();
  }

  function redrawAllStrokes() {
    drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    for (const stroke of strokes) {
      for (const p of stroke) {
        drawDot(p.x, p.y, p.size);
      }
    }
  }

  drawCanvas.addEventListener('mousedown',  startDraw);
  drawCanvas.addEventListener('mousemove',  moveDraw);
  drawCanvas.addEventListener('mouseup',    endDraw);
  drawCanvas.addEventListener('mouseleave', endDraw);
  drawCanvas.addEventListener('touchstart', startDraw, { passive: false });
  drawCanvas.addEventListener('touchmove',  moveDraw,  { passive: false });
  drawCanvas.addEventListener('touchend',   endDraw);

  /* ---- Buttons ---- */
  function updateButtons() {
    btnUndo.disabled    = strokes.length === 0;
    btnClear.disabled   = strokes.length === 0;
    btnDownload.disabled = strokes.length === 0;
  }

  btnUndo.addEventListener('click', () => {
    strokes.pop();
    redrawAllStrokes();
    updateButtons();
  });

  btnClear.addEventListener('click', async () => {
    const ok = await showModal('Limpiar marcas', '¿Seguro que quieres borrar todas las marcas?');
    if (ok) {
      strokes = [];
      drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
      updateButtons();
    }
  });

  btnNewImage.addEventListener('click', async () => {
    if (originalImage) {
      const ok = await showModal('Nueva imagen', '¿Cargar una nueva imagen? Se perderán las marcas actuales.');
      if (ok) fileInput.click();
    } else {
      fileInput.click();
    }
  });

  /* ---- Download merged image with solid red marks ---- */
  btnDownload.addEventListener('click', () => {
    const dataUrl = window.getMarkedImage();
    if (!dataUrl) return;
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = 'imagen_marcada.png';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setStatus('💾 Imagen descargada — envíala al bot para procesarla', true);
  });

  /* ---- File input ---- */
  container.addEventListener('click', (e) => {
    if (!originalImage && e.target !== drawCanvas) fileInput.click();
  });
  fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) loadImage(e.target.files[0]);
  });

  /* Drag & drop */
  container.addEventListener('dragover', (e) => { e.preventDefault(); container.style.borderColor = '#6C63FF'; });
  container.addEventListener('dragleave', ()  => { container.style.borderColor = ''; });
  container.addEventListener('drop', (e) => {
    e.preventDefault();
    container.style.borderColor = '';
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith('image/')) loadImage(f);
  });

  /* ---- Compose final image: original + red marks merged ---- */
  window.getMarkedImage = function() {
    if (!originalImage || strokes.length === 0) return null;
    const tmpCanvas = document.createElement('canvas');
    tmpCanvas.width  = mainCanvas.width;
    tmpCanvas.height = mainCanvas.height;
    const tmpCtx = tmpCanvas.getContext('2d');
    tmpCtx.putImageData(originalImage, 0, 0);
    // Draw red marks on top with full opacity
    for (const stroke of strokes) {
      for (const p of stroke) {
        tmpCtx.beginPath();
        tmpCtx.arc(p.x, p.y, p.size / 2, 0, Math.PI * 2);
        tmpCtx.fillStyle = 'rgba(255, 0, 0, 1)';
        tmpCtx.fill();
      }
    }
    return tmpCanvas.toDataURL('image/png');
  };

  setStatus('✅ Listo — Sube una imagen para empezar', true);
})();
</script>
</body>
</html>"""


class EliminaObjetos:

    def has_image_attachment(self):
        """Check if the user sent an image."""
        for att in poe.query.attachments:
            ct = (att.content_type or "").lower()
            name = (att.name or "").lower()
            if ct.startswith("image/") or any(name.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".heic"]):
                return True
        return False

    def run(self):
        user_text = poe.query.text.strip()

        # If the user sends an image with marks → process it
        if self.has_image_attachment():
            self.process_image()
        else:
            # Show the Canvas UI for marking objects
            self.show_canvas()

    def show_canvas(self):
        """Display the interactive Canvas for the user to mark objects."""
        with poe.start_message() as msg:
            msg.write("🎯 **Eliminador de Objetos con IA**\n\n")
            msg.write("Abre el editor de abajo para marcar los objetos a eliminar, ")
            msg.write("luego envíame la imagen marcada.\n\n")
            msg.write("````html\n")
            msg.write(CANVAS_HTML)
            msg.write("\n````\n\n")
            msg.write("📌 **Instrucciones:** Sube una imagen, pinta en rojo sobre lo que quieras eliminar, ")
            msg.write("descárgala y envíamela aquí. ¡Yo me encargo del resto!")

    def process_image(self):
        """Process an image with colored marks — detect, analyze, and inpaint."""
        import cv2
        import numpy as np
        from pillow_heif import register_heif_opener
        from PIL import Image

        register_heif_opener()

        img_attachment = None
        for att in poe.query.attachments:
            ct = (att.content_type or "").lower()
            name = (att.name or "").lower()
            if ct.startswith("image/") or any(name.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".heic"]):
                img_attachment = att
                break

        if not img_attachment:
            raise poe.BotError("📷 No se encontró una imagen válida.")

        img_bytes = img_attachment.get_contents()

        with poe.start_message() as msg:
            msg.write("🔍 Detectando marcas de color en la imagen...")

        # Detect colored marks
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        img_array = np.array(img)
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        total_pixels = img_array.shape[0] * img_array.shape[1]

        # Lowered S/V thresholds (80) to catch semi-transparent / blended marks
        color_ranges = {
            "rojo": [
                (np.array([0, 80, 80]), np.array([12, 255, 255])),
                (np.array([155, 80, 80]), np.array([180, 255, 255])),
            ],
            "azul": [(np.array([95, 80, 80]), np.array([135, 255, 255]))],
            "verde": [(np.array([35, 120, 100]), np.array([85, 255, 255]))],
            "amarillo": [(np.array([18, 80, 80]), np.array([35, 255, 255]))],
        }

        detected_colors = []
        combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        for color_name, ranges in color_ranges.items():
            color_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
            for lower, upper in ranges:
                color_mask |= cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            min_area = total_pixels * 0.002
            for contour in contours:
                if cv2.contourArea(contour) >= min_area:
                    cv2.drawContours(combined_mask, [contour], -1, 255, -1)
                    if color_name not in detected_colors:
                        detected_colors.append(color_name)

        mark_pct = (np.sum(combined_mask > 0) / total_pixels) * 100

        if not detected_colors:
            # No marks found by OpenCV → fall back to vision AI
            user_text = poe.query.text.strip()

            if not user_text:
                # No text either → ask GPT-5.2 to look for drawn marks or objects to remove
                with poe.start_message() as msg:
                    msg.write("🔍 No detecté marcas por color. Analizando la imagen con IA...\n")

                vision_check = poe.call(
                    "GPT-5.2",
                    poe.Message(
                        text=(
                            "Look at this image. The user wants to remove something. "
                            "Check if there are any hand-drawn marks, scribbles, highlights, "
                            "or colored overlays indicating areas to erase. "
                            "If yes, describe them. If not, describe the most likely "
                            "unwanted element (watermark, logo, text overlay, person, etc.).\n\n"
                            "Output in ```json format:\n"
                            "```json\n"
                            '{"found_marks": true/false, '
                            '"description": "what to remove and where"}\n'
                            "```"
                        ),
                        attachments=[img_attachment],
                    ),
                )
                parsed_vision = parse_json_from_response(vision_check.text, ["description"])
                user_text = parsed_vision["description"]

            with poe.start_message() as msg:
                msg.write(f"🎯 Eliminaré: **{user_text}**\n")
                msg.write("🎨 Procesando...\n")

            poe.call(
                "Nano-Banana",
                poe.Message(
                    text=(
                        f"Remove the following from this image: {user_text}\n\n"
                        "Fill the removed area naturally, matching the surrounding style and textures. "
                        "Do NOT change anything else in the image."
                    ),
                    attachments=[img_attachment],
                    parameters={"image_only": True},
                ),
                output=poe.default_chat,
            )
            return

        colors_text = ", ".join(detected_colors)

        with poe.start_message() as msg:
            msg.write(f"✅ Marcas detectadas: **{colors_text}** ({mark_pct:.1f}% de la imagen)\n")
            msg.write("🧠 Analizando contenido bajo las marcas...\n")

        # Vision analysis — what's under the marks?
        analysis = poe.call(
            "GPT-5.2",
            poe.Message(
                text=(
                    f"Analyze this image. There are solid **{colors_text}** colored marks/overlays "
                    "that someone drew on top to indicate objects to remove or areas to restore.\n\n"
                    "Study the context and determine:\n"
                    "1. What is hidden under the colored marks\n"
                    "2. What should replace the marked areas to look natural\n\n"
                    "Output in ```json format:\n"
                    "```json\n"
                    '{"hidden_content": "what is under the marks or what should fill the area", '
                    '"objects_to_remove": "what the user wants removed", '
                    '"mark_location": "where in the image"}\n'
                    "```"
                ),
                attachments=[img_attachment],
            ),
        )

        parsed = parse_json_from_response(
            analysis.text, ["hidden_content", "mark_location"]
        )
        hidden = parsed["hidden_content"]
        location = parsed["mark_location"]
        objects_to_remove = parsed.get("objects_to_remove", "the marked objects")

        user_hint = poe.query.text.strip()
        extra = (
            f"\nAdditional user instruction: {user_hint}"
            if user_hint
            else ""
        )

        with poe.start_message() as msg:
            msg.write(f"🎯 Análisis: {hidden}\n")
            msg.write("🎨 Restaurando imagen...\n")

        # Inpaint with Nano-Banana
        poe.call(
            "Nano-Banana",
            poe.Message(
                text=(
                    f"Remove ONLY the solid {colors_text} colored marks/paint overlays "
                    "from this image and restore the area underneath.\n\n"
                    f"What should appear where the marks are: {hidden}\n"
                    f"Mark location: {location}\n"
                    f"{extra}\n\n"
                    "CRITICAL RULES:\n"
                    "1. Remove ONLY the bright colored paint marks\n"
                    "2. Restore the content underneath naturally\n"
                    "3. Match the exact art style, colors, lighting and textures\n"
                    "4. The restored area must blend perfectly\n"
                    "5. Do NOT change anything outside the marked areas"
                ),
                attachments=[img_attachment],
                parameters={"image_only": True},
            ),
            output=poe.default_chat,
        )


if __name__ == "__main__":
    bot = EliminaObjetos()
    bot.run()

