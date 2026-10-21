# poe: name=AppEliminaObjetos

import json
import re

from fastapi_poe.types import SettingsResponse

poe.update_settings(SettingsResponse(
    introduction_message="¡Hola! Soy **AppEliminaObjetos** 🧹\n\nEnvíame una imagen y te abriré un editor donde podrás **pintar sobre los objetos que quieras eliminar**. Luego la IA rellenará esas áreas automáticamente.\n\n📌 **Cómo usar:**\n1. Envía una imagen\n2. Pinta con el pincel rojo sobre lo que quieras eliminar\n3. Haz clic en \"Eliminar objetos\"\n4. ¡Listo! La IA hará el resto",
    enable_image_comprehension=True,
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
            raise Exception(f"Could not find JSON in response\n{response_text}")
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON: {e}\nJSON string: {json_str}")
    if required_fields:
        missing_fields = set(required_fields) - set(parsed.keys())
        if missing_fields:
            raise Exception(f"Missing required fields: {', '.join(missing_fields)}")
    return parsed


EDITOR_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Eliminar Objetos</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #1a1a2e;
    color: #eee;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 12px;
    overflow-x: hidden;
  }
  h2 { font-size: 18px; margin-bottom: 8px; color: #e94560; }
  .instructions {
    font-size: 13px;
    color: #aaa;
    margin-bottom: 12px;
    text-align: center;
    line-height: 1.4;
  }
  .canvas-container {
    position: relative;
    display: inline-block;
    border: 2px solid #e94560;
    border-radius: 8px;
    overflow: hidden;
    cursor: crosshair;
    touch-action: none;
    max-width: 100%;
  }
  canvas {
    display: block;
    max-width: 100%;
  }
  #maskCanvas {
    position: absolute;
    top: 0;
    left: 0;
  }
  .toolbar {
    display: flex;
    gap: 10px;
    margin: 12px 0;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
  }
  .toolbar label {
    font-size: 13px;
    color: #ccc;
  }
  .toolbar input[type=range] {
    width: 100px;
    accent-color: #e94560;
  }
  button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.1s, opacity 0.2s;
  }
  button:active { transform: scale(0.96); }
  .btn-clear {
    background: #333;
    color: #eee;
  }
  .btn-undo {
    background: #555;
    color: #eee;
  }
  .btn-submit {
    background: #e94560;
    color: #fff;
    font-size: 16px;
    padding: 12px 32px;
    margin-top: 8px;
  }
  .btn-submit:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  .brush-preview {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid #e94560;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .brush-dot {
    background: rgba(233, 69, 96, 0.6);
    border-radius: 50%;
  }
  #status {
    margin-top: 10px;
    font-size: 13px;
    color: #aaa;
    min-height: 20px;
  }
</style>
</head>
<body>
<h2>🎨 Pinta sobre lo que quieras eliminar</h2>
<p class="instructions">Usa el pincel rojo para marcar los objetos. Ajusta el tamaño del pincel abajo.</p>

<div class="canvas-container" id="canvasContainer">
  <canvas id="imgCanvas"></canvas>
  <canvas id="maskCanvas"></canvas>
</div>

<div class="toolbar">
  <label>Pincel:</label>
  <input type="range" id="brushSize" min="5" max="100" value="30">
  <div class="brush-preview">
    <div class="brush-dot" id="brushDot"></div>
  </div>
  <button class="btn-undo" id="undoBtn">↩ Deshacer</button>
  <button class="btn-clear" id="clearBtn">🗑 Limpiar</button>
</div>

<button class="btn-submit" id="submitBtn">✨ Eliminar objetos</button>
<div id="status"></div>

<script>
const IMAGE_URL = "IMAGE_URL_PLACEHOLDER";
const imgCanvas = document.getElementById('imgCanvas');
const maskCanvas = document.getElementById('maskCanvas');
const imgCtx = imgCanvas.getContext('2d');
const maskCtx = maskCanvas.getContext('2d');
const brushSlider = document.getElementById('brushSize');
const brushDot = document.getElementById('brushDot');
const submitBtn = document.getElementById('submitBtn');
const undoBtn = document.getElementById('undoBtn');
const clearBtn = document.getElementById('clearBtn');
const status = document.getElementById('status');

let painting = false;
let history = [];
let maxW = Math.min(window.innerWidth - 30, 800);
let maxH = Math.min(window.innerHeight - 250, 700);
let scaleRatio = 1;
let origW, origH;

function updateBrushPreview() {
  const s = Math.min(brushSlider.value * 0.6, 36);
  brushDot.style.width = s + 'px';
  brushDot.style.height = s + 'px';
}
brushSlider.addEventListener('input', updateBrushPreview);
updateBrushPreview();

const img = new Image();
img.crossOrigin = 'anonymous';
img.onload = function() {
  origW = img.naturalWidth;
  origH = img.naturalHeight;
  scaleRatio = Math.min(maxW / origW, maxH / origH, 1);
  const dw = Math.round(origW * scaleRatio);
  const dh = Math.round(origH * scaleRatio);
  imgCanvas.width = dw;
  imgCanvas.height = dh;
  maskCanvas.width = dw;
  maskCanvas.height = dh;
  imgCtx.drawImage(img, 0, 0, dw, dh);
  saveState();
  status.textContent = 'Imagen cargada. ¡Pinta sobre los objetos!';
};
img.onerror = function() {
  status.textContent = 'Error al cargar la imagen.';
};
img.src = IMAGE_URL;

function saveState() {
  history.push(maskCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height));
  if (history.length > 30) history.shift();
}

function getPos(e) {
  const rect = maskCanvas.getBoundingClientRect();
  const sx = maskCanvas.width / rect.width;
  const sy = maskCanvas.height / rect.height;
  if (e.touches) {
    return { x: (e.touches[0].clientX - rect.left) * sx, y: (e.touches[0].clientY - rect.top) * sy };
  }
  return { x: (e.clientX - rect.left) * sx, y: (e.clientY - rect.top) * sy };
}

function startPaint(e) {
  e.preventDefault();
  painting = true;
  const pos = getPos(e);
  maskCtx.beginPath();
  maskCtx.arc(pos.x, pos.y, brushSlider.value * scaleRatio / 2, 0, Math.PI * 2);
  maskCtx.fillStyle = 'rgba(233, 69, 96, 0.5)';
  maskCtx.fill();
  maskCtx.beginPath();
  maskCtx.moveTo(pos.x, pos.y);
}

function paint(e) {
  if (!painting) return;
  e.preventDefault();
  const pos = getPos(e);
  maskCtx.lineWidth = brushSlider.value * scaleRatio;
  maskCtx.lineCap = 'round';
  maskCtx.lineJoin = 'round';
  maskCtx.strokeStyle = 'rgba(233, 69, 96, 0.5)';
  maskCtx.lineTo(pos.x, pos.y);
  maskCtx.stroke();
  maskCtx.beginPath();
  maskCtx.moveTo(pos.x, pos.y);
}

function stopPaint(e) {
  if (painting) {
    painting = false;
    maskCtx.beginPath();
    saveState();
  }
}

maskCanvas.addEventListener('mousedown', startPaint);
maskCanvas.addEventListener('mousemove', paint);
maskCanvas.addEventListener('mouseup', stopPaint);
maskCanvas.addEventListener('mouseleave', stopPaint);
maskCanvas.addEventListener('touchstart', startPaint, { passive: false });
maskCanvas.addEventListener('touchmove', paint, { passive: false });
maskCanvas.addEventListener('touchend', stopPaint);

undoBtn.addEventListener('click', () => {
  if (history.length > 1) {
    history.pop();
    maskCtx.putImageData(history[history.length - 1], 0, 0);
  }
});

clearBtn.addEventListener('click', () => {
  maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
  saveState();
});

submitBtn.addEventListener('click', () => {
  // Build full-res mask
  const fullMask = document.createElement('canvas');
  fullMask.width = origW;
  fullMask.height = origH;
  const fCtx = fullMask.getContext('2d');
  fCtx.fillStyle = '#000';
  fCtx.fillRect(0, 0, origW, origH);
  // Get painted pixels
  const maskData = maskCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height);
  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = maskCanvas.width;
  tempCanvas.height = maskCanvas.height;
  const tCtx = tempCanvas.getContext('2d');
  const tData = tCtx.createImageData(maskCanvas.width, maskCanvas.height);
  for (let i = 0; i < maskData.data.length; i += 4) {
    if (maskData.data[i + 3] > 10) {
      tData.data[i] = 255;
      tData.data[i+1] = 255;
      tData.data[i+2] = 255;
      tData.data[i+3] = 255;
    }
  }
  tCtx.putImageData(tData, 0, 0);
  fCtx.drawImage(tempCanvas, 0, 0, origW, origH);

  const maskDataUrl = fullMask.toDataURL('image/png');

  // Build combined image (original + mask side by side) for the LLM
  const combined = document.createElement('canvas');
  combined.width = origW;
  combined.height = origH;
  const cCtx = combined.getContext('2d');
  cCtx.drawImage(img, 0, 0, origW, origH);
  // Overlay mask regions as red tint
  const redOverlay = document.createElement('canvas');
  redOverlay.width = origW;
  redOverlay.height = origH;
  const rCtx = redOverlay.getContext('2d');
  rCtx.drawImage(tempCanvas, 0, 0, origW, origH);
  const roData = rCtx.getImageData(0, 0, origW, origH);
  for (let i = 0; i < roData.data.length; i += 4) {
    if (roData.data[i] > 128) {
      roData.data[i] = 255;
      roData.data[i+1] = 0;
      roData.data[i+2] = 0;
      roData.data[i+3] = 160;
    } else {
      roData.data[i+3] = 0;
    }
  }
  rCtx.putImageData(roData, 0, 0);
  cCtx.drawImage(redOverlay, 0, 0);

  submitBtn.disabled = true;
  status.textContent = '⏳ Enviando máscara...';

  const payload = JSON.stringify({
    action: "inpaint",
    mask_data_url: maskDataUrl
  });

  window.parent.postMessage(payload, '*');
  status.textContent = '✅ Máscara enviada. Espera el resultado...';
});
</script>
</body>
</html>
"""


class AppEliminaObjetos:
    def run(self):
        # Check if this is a mask submission from the canvas
        try:
            data = json.loads(poe.query.text)
            if data.get("action") == "inpaint":
                self.process_inpaint(data)
                return
        except (json.JSONDecodeError, TypeError):
            pass

        # Check if user sent an image
        image_attachments = [a for a in poe.query.attachments if a.content_type and a.content_type.startswith("image/")]

        if not image_attachments:
            raise poe.BotError("Por favor, envíame una imagen para poder editarla. 📷")

        image_att = image_attachments[0]
        image_url = image_att.url

        # Show the painting editor
        html = EDITOR_HTML.replace("IMAGE_URL_PLACEHOLDER", image_url)
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def process_inpaint(self, data):
        """Process the mask and generate the inpainted image."""
        import base64

        mask_data_url = data.get("mask_data_url", "")

        # Get the original image from conversation history
        original_image = None
        for m in reversed(list(poe.default_chat)):
            for a in m.attachments:
                if a.content_type and a.content_type.startswith("image/"):
                    original_image = a
                    break
            if original_image:
                break

        if not original_image:
            raise poe.BotError("No pude encontrar la imagen original. Por favor, envía la imagen de nuevo.")

        # Create mask attachment from data URL
        mask_bytes = base64.b64decode(mask_data_url.split(",")[1])
        mask_attachment = poe.Attachment(
            name="mask.png",
            contents=mask_bytes,
            content_type="image/png"
        )

        with poe.start_message() as msg:
            msg.write("⏳ Procesando... La IA está eliminando los objetos marcados.\n\n")

        # Use GPT-Image-1 with mask for inpainting
        inpaint_message = poe.Message(
            text="Remove the masked/white areas from this image. Fill those areas naturally with the surrounding background so it looks like the objects were never there. Keep the rest of the image exactly as is.",
            attachments=[original_image, mask_attachment],
            parameters={"use_mask": True, "quality": "high"}
        )
        poe.call("GPT-Image-1", inpaint_message, output=poe.default_chat)


if __name__ == "__main__":
    bot = AppEliminaObjetos()
    bot.run()

