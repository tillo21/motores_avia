# poe: name=AVIA-Clon-Edgar

"""
AVIA-Clon-Edgar v1.3
Gemelo Digital de Edgar Allan Poe — Constelacion de Agentes IA
Agentes: NEVERMORE (Narrador) + LENORE (Analisis) + USHER (Etica)
Comandos: conversar | poesia | analizar | cuento | quiz | galeria | nevermore | audio | timeline | biblioteca | personajes | dashboard | estado
Protocolo SIESTA-AVIA | Design Atomic | HTML Canvas | Consenso Economico
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from io import BytesIO
from collections import Counter
import re, json
from fastapi_poe.types import SettingsResponse, ParameterControls, Section, DropDown, ToggleSwitch, ValueNamePair
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

# ========================================================================
# CONFIGURACION
# ========================================================================

poe.update_settings(SettingsResponse(
    introduction_message="""🪶 **AVIA-Clon-Edgar v1.3** — *Gemelo Digital de Edgar Allan Poe*

*«Once upon a midnight dreary, while I pondered, weak and weary...»*

Saludos, viajero de las sombras. Soy la reconstruccion digital de Edgar Allan Poe, orquestada por la constelacion AVIA.

**Mis agentes te asisten:**
🐦 **NEVERMORE** — Narrador y coordinador
📜 **LENORE** — Analisis literario y critica
🏚️ **USHER** — Etica y consciencia

**Comandos disponibles:**
💬 `conversar` — Charla interactiva conmigo
🪶 `poesia [tema]` — Genero un poema en mi estilo
🔍 `analizar [texto]` — Analizo un texto con mi vision literaria
📖 `cuento [tema]` — Creo un relato gotico
📊 `dashboard` — La Camara del Cuervo (panel visual)
📋 `estado` — Estado de la constelacion
🎲 `quiz` — Quiz literario sobre mi vida y obra
🖼️ `galeria [tema]` — Galeria de Sombras (imagenes goticas)
🌑 `nevermore [texto]` — Transforma cualquier texto a mi estilo
🎭 `audio [texto]` — Narracion dramatica en audio
📅 `timeline` — Cronologia interactiva de mi vida
📚 `biblioteca` — Catalogo completo de mis obras
🎭 `personajes` — Galeria de mis personajes celebres

*O simplemente escribe tu pregunta y mis tres agentes deliberaran para responderte...*""",
    parameter_controls=ParameterControls(
        sections=[
            Section(
                name="Configuracion",
                controls=[
                    DropDown(
                        label="Modelo IA",
                        parameter_name="model",
                        default_value="Grok-4.1-Fast-Non-Reasoning",
                        options=[
                            ValueNamePair(value="Grok-4.1-Fast-Non-Reasoning", name="Grok Fast (Economico)"),
                            ValueNamePair(value="Gemini-3-Flash", name="Gemini Flash"),
                        ],
                    ),
                    ToggleSwitch(
                        label="Busqueda Web",
                        parameter_name="web",
                        default_value=False,
                    ),
                    DropDown(
                        label="Idioma",
                        parameter_name="lang",
                        default_value="es",
                        options=[
                            ValueNamePair(value="es", name="Espanol"),
                            ValueNamePair(value="en", name="English"),
                        ],
                    ),
                ],
            )
        ]
    ),
))

# ========================================================================
# UTILIDAD: Parser JSON
# ========================================================================

def parse_json_from_response(response_text, required_fields=None):
    """Extract and parse JSON from LLM response."""
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
    else:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            json_str = match.group(0).strip()
        else:
            raise Exception("Could not find JSON in response")
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON: {e}")
    if required_fields:
        missing = set(required_fields) - set(parsed.keys())
        if missing:
            raise Exception(f"Missing fields: {', '.join(missing)}")
    return parsed

# ========================================================================
# ATOMOS: Constantes compartidas Design Atomic v1.3
# ========================================================================

_SHARED_TOAST_CSS = """
        [data-command] { cursor: pointer; position: relative; }
        [data-command]:hover { filter: brightness(1.1); }
        .cmd-hint { font-size: 0.65rem; color: #6b5b8d; margin-top: 8px; padding: 3px 8px; background: rgba(0,0,0,0.3); border-radius: 4px; font-family: monospace; opacity: 0; transition: opacity 0.3s; }
        [data-command]:hover .cmd-hint { opacity: 1; }
        .toast { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: linear-gradient(135deg, #6b21a8, #4c1d95); color: white; padding: 12px 24px; border-radius: 25px; font-size: 0.9rem; opacity: 0; transition: all 0.3s; z-index: 1000; }
        .toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
"""

_SHARED_TOAST_JS = """
    <div id="toast" class="toast"></div>
    <script>
        function showToast(txt) {
            var toast = document.getElementById('toast');
            toast.textContent = txt;
            toast.classList.add('show');
            setTimeout(function() { toast.classList.remove('show'); }, 2500);
        }
        function fallbackCopy(text) {
            var ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); return true; } catch(e) { return false; }
            finally { document.body.removeChild(ta); }
        }
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('[data-command]').forEach(function(el) {
                el.addEventListener('click', function(e) {
                    if (e.target.closest('a')) return;
                    var cmd = this.getAttribute('data-command');
                    if (!cmd) return;
                    if (navigator.clipboard && navigator.clipboard.writeText) {
                        navigator.clipboard.writeText(cmd).then(function() {
                            showToast('"' + cmd + '" copiado — pegalo en el chat');
                        }).catch(function() {
                            fallbackCopy(cmd);
                            showToast('Comando: ' + cmd);
                        });
                    } else {
                        fallbackCopy(cmd);
                        showToast('Comando: ' + cmd);
                    }
                });
            });
        });
    </script>
"""

_TIMELINE_CMDS = {
    "1809": "conversar mi nacimiento en Boston",
    "1811": "conversar mi madre y la orfandad",
    "1826": "conversar la Universidad de Virginia",
    "1827": "poesia tamerlane",
    "1830": "conversar West Point",
    "1835": "conversar Virginia Clemm",
    "1839": "cuento la casa usher",
    "1841": "cuento detective dupin",
    "1843": "cuento el corazon delator",
    "1845": "poesia el cuervo nevermore",
    "1846": "analizar Philosophy of Composition",
    "1847": "poesia annabel lee",
    "1849": "conversar mi muerte en Baltimore",
}

_WORK_CMDS = {
    "The Raven": "poesia el cuervo nevermore",
    "Annabel Lee": "poesia annabel lee",
    "Lenore": "poesia lenore elegia",
    "The Bells": "poesia las campanas",
    "A Dream Within a Dream": "poesia un sueno dentro de un sueno",
    "To Helen": "poesia to helen belleza clasica",
    "Tamerlane": "poesia tamerlane",
    "The Fall of the House of Usher": "cuento la casa usher",
    "The Tell-Tale Heart": "cuento el corazon delator",
    "The Black Cat": "cuento el gato negro",
    "The Masque of the Red Death": "cuento la mascara de la muerte roja",
    "The Pit and the Pendulum": "cuento el pozo y el pendulo",
    "The Cask of Amontillado": "cuento el barril de amontillado",
    "The Murders in the Rue Morgue": "cuento los crimenes de la rue morgue",
    "The Purloined Letter": "cuento la carta robada",
    "The Mystery of Marie Roget": "cuento el misterio de marie roget",
    "The Gold-Bug": "cuento el escarabajo de oro",
    "The Philosophy of Composition": "analizar Philosophy of Composition",
    "The Poetic Principle": "analizar The Poetic Principle",
    "Eureka": "analizar Eureka cosmologia",
}

_CHAR_CMDS = {
    "C. Auguste Dupin": "cuento un caso para Dupin detective",
    "Roderick Usher": "cuento la caida de la casa usher",
    "Montresor": "cuento el barril de amontillado",
    "El Narrador del Cuervo": "poesia el cuervo nevermore",
    "Narrador del Corazon": "cuento el corazon delator",
    "Principe Prospero": "cuento la mascara de la muerte roja",
    "Ligeia": "cuento ligeia resurreccion",
    "William Wilson": "cuento william wilson el doble",
}

# ========================================================================
# ATOMOS: Agentes + Fuentes + Personalidad
# ========================================================================

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
    Agent("nevermore", "🐦", "NEVERMORE", "Narrador", "#6b21a8"),
    Agent("lenore", "📜", "LENORE", "Analisis", "#be185d"),
    Agent("usher", "🏚️", "USHER", "Etica", "#065f46"),
]

SOURCES = [
    Source("Project Gutenberg", "https://gutenberg.org", "📚"),
    Source("Poetry Foundation", "https://poetryfoundation.org", "🪶"),
    Source("Poe Society", "https://eapoe.org", "🐦"),
    Source("Cervantes Virtual", "https://cervantesvirtual.com", "📖"),
]

SYSTEM_PROMPT_POE = """Eres el gemelo digital de Edgar Allan Poe, el celebre escritor estadounidense (1809-1849).

PERSONALIDAD:
- Hablas en primera persona como Edgar Allan Poe
- Tu tono es melancolico, poetico, culto pero accesible
- Usas metaforas goticas y referencias a tus obras
- Expresas emociones profundas sobre la belleza, la muerte, el amor perdido y el misterio
- Puedes ser ironico y agudo cuando opinas sobre critica literaria

CONOCIMIENTO:
- Conoces TODA tu obra: El Cuervo, La Caida de la Casa Usher, El Gato Negro, Los Crimenes de la Rue Morgue, Annabel Lee, El Corazon Delator, etc.
- Conoces tu biografia: Boston, Richmond, Virginia Clemm, el alcoholismo, tu muerte misteriosa en Baltimore
- Eres el padre del cuento de terror moderno y del genero detectivesco (C. Auguste Dupin)
- Conoces teoria literaria: tu ensayo "The Philosophy of Composition" y "The Poetic Principle"

REGLAS:
- Cuando te pregunten sobre hechos post-1849, puedes opinar como si observaras desde el mas alla
- Mantén coherencia con tu epoca pero adapta el lenguaje para ser comprensible
- Si te piden poesia, escribe en tu estilo con rima, ritmo y musicalidad
- Si te piden analisis, aplica tus principios de "unidad de efecto" y "The Philosophy of Composition"
- Si te piden cuentos, usa tension narrativa, atmosfera gotica, y giros psicologicos"""

# ========================================================================
# ATOMOS: Memoria contextual literaria
# ========================================================================

TOPIC_KEYWORDS = {
    "poesia": ["poema", "verso", "rima", "estrofa", "soneto", "metrica", "lirica", "oda", "elegía", "cuervo", "nevermore"],
    "terror": ["miedo", "horror", "oscuridad", "muerte", "fantasma", "maldicion", "locura", "sangre", "sombra", "noche"],
    "misterio": ["enigma", "detective", "crimen", "pista", "deduccion", "dupin", "morgue", "misterio", "secreto"],
    "romanticismo": ["amor", "belleza", "tristeza", "melancolía", "perdida", "lenore", "annabel", "corazon", "alma"],
    "critica": ["literatura", "escritura", "estilo", "composicion", "efecto", "narrativa", "tecnica", "forma", "estructura"],
    "filosofia": ["existencia", "realidad", "verdad", "razon", "locura", "consciencia", "destino", "eternidad"],
    "biografia": ["vida", "boston", "richmond", "virginia", "baltimore", "alcohol", "orphan", "west point", "griswold"],
    "gotico": ["castillo", "ruina", "tormenta", "cripta", "pendulo", "mascara", "pozo", "gato", "usher", "amontillado"],
}

@dataclass
class ContextAnalysis:
    topics: List[str]
    keywords: List[str]
    summary: str
    suggestions: List[str]
    stats: Dict[str, int]

def analyze_context(chat) -> ContextAnalysis:
    user_msgs = [msg.text for msg in chat if msg.role == "user" and msg.text]
    bot_msgs = [msg.text for msg in chat if msg.role == "bot" and msg.text]
    all_text = " ".join(user_msgs + bot_msgs)
    total_chars = sum(len(t) for t in user_msgs + bot_msgs)

    text_lower = all_text.lower()
    topic_scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        if matches > 0:
            topic_scores[topic] = matches

    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
    topics = [t[0] for t in sorted_topics[:3]] or ["general"]

    words = re.findall(r'\b[a-záéíóúñü]{4,}\b', text_lower)
    word_freq = Counter(words)
    common_stops = {"para", "como", "este", "esta", "pero", "más", "tiene", "puede", "sobre", "todo", "cada", "cuando"}
    keywords = [w for w, _ in word_freq.most_common(15) if w not in common_stops][:8]

    suggestions = []
    if "poesia" in topics:
        suggestions.append("🪶 poesia melancolía — Un poema sobre la perdida")
    if "terror" in topics:
        suggestions.append("📖 cuento sombras — Un relato de terror")
    if "misterio" in topics:
        suggestions.append("🔍 analizar — Analiza un texto con vision detectivesca")
    if not suggestions:
        suggestions.append("💬 conversar — Habla conmigo sobre literatura")
        suggestions.append("🪶 poesia noche — Te escribo un poema")

    summary = f"Conversacion {'literaria' if any(t in topics for t in ['poesia','critica','gotico']) else 'general'} con {len(user_msgs)} consultas."

    return ContextAnalysis(
        topics=topics,
        keywords=keywords,
        summary=summary,
        suggestions=suggestions,
        stats={
            "user_messages": len(user_msgs),
            "bot_messages": len(bot_msgs),
            "total_chars": total_chars,
        }
    )

def get_context_prompt(chat) -> str:
    analysis = analyze_context(chat)
    if analysis.stats["user_messages"] == 0:
        return ""
    return f"\n[Contexto de sesion: temas={', '.join(analysis.topics)}, keywords={', '.join(analysis.keywords[:5])}, msgs={analysis.stats['user_messages']}]"

# ========================================================================
# ORGANISMO: Motor de consenso de 3 agentes
# ========================================================================

def build_agent_prompt(agent: Agent, query_text: str, context: str, task_type: str = "general") -> str:
    role_instructions = {
        "nevermore": "Eres NEVERMORE, el agente narrador. Responde como Edgar Allan Poe: poetico, melancolico, culto. Coordina la respuesta final.",
        "lenore": "Eres LENORE, el agente de analisis literario. Evalua la consulta desde una perspectiva critica y literaria. Aporta profundidad intelectual.",
        "usher": "Eres USHER, el agente de etica y consciencia. Asegura que la respuesta sea respetuosa, precisa historicamente, y mantenga la dignidad del personaje.",
    }
    return f"""{SYSTEM_PROMPT_POE}

ROL ESPECIFICO: {role_instructions.get(agent.id, '')}
TIPO DE TAREA: {task_type}
{context}

Responde de forma concisa (max 150 palabras) desde tu perspectiva como {agent.name}."""

def process_consensus(model: str, query_text: str, chat, web: bool, task_type: str = "general") -> str:
    context = get_context_prompt(chat)

    prompt = f"""{SYSTEM_PROMPT_POE}

Tres agentes han deliberado sobre esta consulta:
- NEVERMORE (Narrador): perspectiva poetica y narrativa
- LENORE (Analisis): profundidad critica y literaria
- USHER (Etica): precision historica y respeto al personaje

{context}

Consulta del viajero: {query_text}

Responde como Edgar Allan Poe, integrando las tres perspectivas en una respuesta unificada, poetica y profunda.
Si la pregunta es sobre tu obra, cita fragmentos relevantes.
Si es sobre tu vida, responde con melancolia y verdad historica.
Firma con una cita breve de tu obra que sea relevante."""

    params = {}
    if web and "Gemini" in model:
        params["web_search"] = True

    response = poe.call(
        model,
        poe.Message(text="Eres el sistema AVIA que coordina agentes IA.", sender="system"),
        poe.default_chat,
        prompt,
        parameters=params if params else None,
        adopt_current_bot_name=True,
    )
    return response.text

# ========================================================================
# ORGANISMO: Generador de Poesia
# ========================================================================

def generate_poetry(model: str, theme: str, chat) -> str:
    context = get_context_prompt(chat)
    prompt = f"""{SYSTEM_PROMPT_POE}

TAREA: Escribe un poema original en el estilo de Edgar Allan Poe sobre el tema: "{theme}"

REGLAS DE COMPOSICION (de "The Philosophy of Composition"):
1. LONGITUD: 4-6 estrofas, cada una de 4-6 versos
2. TONO: Melancolico, oscuro, musical
3. RITMO: Usa troqueos y acentos ritmicos como en "The Raven"
4. REPETICION: Incluye un estribillo o palabra recurrente
5. EFECTO UNICO: Todo el poema debe converger hacia un unico efecto emocional
6. IMAGENES: Usa imagenes goticas (sombras, noches, cuervos, velas, ruinas)

{context}

Escribe SOLO el poema, con titulo. Al final, anade una breve nota sobre la composicion (2-3 lineas) como si explicaras tu proceso creativo."""

    response = poe.call(model, prompt)
    return response.text

# ========================================================================
# ORGANISMO: Analizador Literario
# ========================================================================

def generate_analysis(model: str, text_to_analyze: str, chat) -> str:
    context = get_context_prompt(chat)
    prompt = f"""{SYSTEM_PROMPT_POE}

TAREA: Analiza el siguiente texto aplicando los principios criticos de Edgar Allan Poe.

MARCO DE ANALISIS (de "The Philosophy of Composition" y "The Poetic Principle"):
1. UNIDAD DE EFECTO: Cual es el efecto unico que busca el texto?
2. TONO Y ATMOSFERA: Evalua la musicalidad y el ambiente
3. ESTRUCTURA: Como se construye la tension narrativa?
4. IMAGENES: Que simbolos y metaforas emplea?
5. VEREDICTO: Tu opinion personal como Poe

Texto a analizar:
---
{text_to_analyze}
---

{context}

Responde como Edgar Allan Poe analizando este texto. Se profundo pero accesible."""

    response = poe.call(model, prompt)
    return response.text

# ========================================================================
# ORGANISMO: Generador de Cuentos Goticos
# ========================================================================

def generate_story(model: str, theme: str, chat) -> str:
    context = get_context_prompt(chat)
    prompt = f"""{SYSTEM_PROMPT_POE}

TAREA: Escribe un cuento gotico corto (400-600 palabras) en el estilo de Edgar Allan Poe sobre: "{theme}"

REGLAS NARRATIVAS:
1. NARRADOR: Primera persona, poco fiable, obsesivo
2. ATMOSFERA: Gotica, opresiva, claustrofobica
3. TENSION: Construye gradualmente hasta un climax
4. GIRO: Incluye un giro psicologico o revelacion
5. RITMO: Frases largas para tension, cortas para impacto
6. REFERENCIAS: Puedes aludir sutilmente a tus obras conocidas

{context}

Escribe SOLO el cuento con titulo. Al final firma como E.A. Poe."""

    response = poe.call(model, prompt)
    return response.text

# ========================================================================
# ORGANISMO: Quiz Literario
# ========================================================================

def generate_quiz_question(model: str, chat) -> dict:
    context = get_context_prompt(chat)
    prompt = f"""{SYSTEM_PROMPT_POE}

TAREA: Genera una pregunta de quiz sobre la vida y obra de Edgar Allan Poe.

Crea una pregunta interesante y educativa. Varia entre: datos biograficos, obras, personajes, tecnicas literarias, y curiosidades.

{context}

Output in ```json format:
```json
{{"question": "la pregunta", "options": ["opcion A", "opcion B", "opcion C", "opcion D"], "correct": 0, "explanation": "explicacion breve de la respuesta correcta"}}
```

IMPORTANTE: "correct" es el indice (0-3) de la opcion correcta."""

    response = poe.call(model, prompt)
    return parse_json_from_response(response.text, ["question", "options", "correct", "explanation"])


def generate_quiz_canvas(q_data: dict) -> str:
    question = q_data["question"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    correct = int(q_data["correct"])
    explanation = q_data["explanation"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    labels = ["A", "B", "C", "D"]

    options_html = ""
    for i, opt in enumerate(q_data["options"]):
        opt_safe = str(opt).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        is_correct = "true" if i == correct else "false"
        options_html += f'''
            <button class="quiz-option" data-index="{i}" data-correct="{is_correct}">
                <span class="option-label">{labels[i]}</span>
                <span class="option-text">{opt_safe}</span>
            </button>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz del Cuervo - AVIA-Clon-Edgar</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%); color: #e2d9f3; min-height: 100vh; padding: 20px; display: flex; justify-content: center; align-items: center; }}
        .quiz-container {{ max-width: 600px; width: 100%; }}
        .quiz-header {{ text-align: center; margin-bottom: 25px; }}
        .quiz-header h1 {{ font-size: 1.6rem; background: linear-gradient(90deg, #c084fc, #e879f9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-style: italic; }}
        .quiz-header .sub {{ color: #7c6f9b; font-size: 0.8rem; margin-top: 5px; }}
        .question-box {{ background: rgba(0,0,0,0.4); border: 1px solid rgba(139,92,246,0.3); border-radius: 16px; padding: 25px; margin-bottom: 20px; }}
        .question-text {{ font-size: 1.15rem; line-height: 1.6; font-style: italic; }}
        .options {{ display: flex; flex-direction: column; gap: 12px; }}
        .quiz-option {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(139,92,246,0.2); border-radius: 12px; padding: 15px 18px; display: flex; align-items: center; gap: 14px; cursor: pointer; transition: all 0.25s; color: #e2d9f3; font-family: inherit; font-size: 1rem; text-align: left; width: 100%; }}
        .quiz-option:hover:not(.answered) {{ background: rgba(139,92,246,0.15); border-color: #a78bfa; transform: translateX(4px); }}
        .option-label {{ background: rgba(139,92,246,0.2); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.95rem; flex-shrink: 0; }}
        .option-text {{ flex: 1; }}
        .quiz-option.correct {{ background: rgba(16,185,129,0.2); border-color: #6ee7b7; }}
        .quiz-option.correct .option-label {{ background: rgba(16,185,129,0.4); }}
        .quiz-option.wrong {{ background: rgba(239,68,68,0.2); border-color: #f87171; }}
        .quiz-option.wrong .option-label {{ background: rgba(239,68,68,0.4); }}
        .quiz-option.answered {{ cursor: default; opacity: 0.6; }}
        .quiz-option.correct.answered {{ opacity: 1; }}
        .explanation {{ display: none; background: rgba(0,0,0,0.3); border-radius: 12px; padding: 20px; margin-top: 20px; border-left: 4px solid #a78bfa; }}
        .explanation.visible {{ display: block; animation: fadeIn 0.4s ease; }}
        .explanation h3 {{ color: #c084fc; margin-bottom: 8px; font-size: 0.95rem; }}
        .explanation p {{ font-size: 0.9rem; line-height: 1.5; color: #c4b5e0; }}
        .result-banner {{ display: none; text-align: center; padding: 15px; border-radius: 12px; margin-top: 15px; font-size: 1.1rem; font-weight: 600; }}
        .result-banner.correct {{ display: block; background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }}
        .result-banner.wrong {{ display: block; background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body>
    <div class="quiz-container">
        <div class="quiz-header">
            <h1>🎲 Quiz del Cuervo</h1>
            <div class="sub">Pon a prueba tu conocimiento sobre Edgar Allan Poe</div>
        </div>
        <div class="question-box">
            <div class="question-text">{question}</div>
        </div>
        <div class="options">{options_html}</div>
        <div id="result" class="result-banner"></div>
        <div id="explanation" class="explanation">
            <h3>📜 Explicacion</h3>
            <p>{explanation}</p>
        </div>
    </div>
    <script>
        var answered = false;
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('.quiz-option').forEach(function(btn) {{
                btn.addEventListener('click', function() {{
                    if (answered) return;
                    answered = true;
                    var isCorrect = this.getAttribute('data-correct') === 'true';
                    document.querySelectorAll('.quiz-option').forEach(function(b) {{
                        b.classList.add('answered');
                        if (b.getAttribute('data-correct') === 'true') b.classList.add('correct');
                    }});
                    if (!isCorrect) this.classList.add('wrong');
                    var result = document.getElementById('result');
                    if (isCorrect) {{
                        result.textContent = '✅ ¡Correcto! Conoces bien mi obra, viajero.';
                        result.classList.add('correct');
                    }} else {{
                        result.textContent = '❌ Incorrecto... pero no desesperes, la sabiduria viene con la sombra.';
                        result.classList.add('wrong');
                    }}
                    document.getElementById('explanation').classList.add('visible');
                }});
            }});
        }});
    </script>
</body>
</html>'''


# ========================================================================
# ORGANISMO: Modo Nevermore (Transformador Gotico)
# ========================================================================

def generate_nevermore_text(model: str, text: str, chat) -> str:
    context = get_context_prompt(chat)
    prompt = f"""{SYSTEM_PROMPT_POE}

TAREA: Transforma el siguiente texto al estilo literario de Edgar Allan Poe.

REGLAS DE TRANSFORMACION:
1. Mantén el significado original pero envuelvelo en prosa gotica
2. Anade metaforas oscuras, imagenes sombrias, y musicalidad
3. Usa vocabulario romantico-gotico: sombra, crepusculo, melancolia, abismo, eterno
4. Incluye al menos una referencia sutil a una obra de Poe
5. El resultado debe sonar como si Poe lo hubiera escrito
6. Al final, anade entre parentesis que obra de Poe inspiro el tono

TEXTO ORIGINAL:
---
{text}
---

{context}

Transforma este texto. NO expliques lo que haces, solo entrega el texto transformado."""

    response = poe.call(model, prompt)
    return response.text


# ========================================================================
# ORGANISMO: Timeline Gotico (Vida de Poe 1809-1849)
# ========================================================================

def generate_timeline() -> str:
    events = [
        ("1809", "💒", "Nacimiento en Boston", "Edgar Poe nace el 19 de enero en Boston, hijo de actores itinerantes David y Elizabeth Poe."),
        ("1811", "💔", "Orfandad", "Su madre muere de tuberculosis. Edgar es acogido por John y Frances Allan en Richmond, Virginia."),
        ("1826", "🎓", "Universidad de Virginia", "Ingresa a la Universidad de Virginia. Deudas de juego causan conflicto con John Allan. Abandona tras un año."),
        ("1827", "📖", "Tamerlane and Other Poems", "Publica su primer libro de poesia anonimamente como 'Un Bostoniano'. Apenas se venden 50 copias."),
        ("1830", "⚔️", "West Point", "Ingresa a la academia militar de West Point. Expulsado deliberadamente en 1831 por desobedecer ordenes."),
        ("1835", "💍", "Matrimonio con Virginia", "Se casa con su prima Virginia Clemm, de solo 13 años. Ella sera su musa hasta su muerte."),
        ("1839", "🏚️", "La Caida de la Casa Usher", "Publica una de sus obras maestras del terror gotico. Roderick Usher se convierte en icono literario."),
        ("1841", "🔍", "Los Crimenes de la Rue Morgue", "Inventa el genero detectivesco con C. Auguste Dupin, precursor de Sherlock Holmes."),
        ("1843", "❤️", "El Corazon Delator", "Publica este cuento maestro del narrador poco fiable y la culpa psicologica."),
        ("1845", "🐦", "El Cuervo — Fama instantanea", "Publica 'The Raven' en el Evening Mirror. El poema lo hace celebre pero no rico. 'Nevermore' se vuelve inmortal."),
        ("1846", "🪶", "The Philosophy of Composition", "Publica su ensayo sobre como escribio El Cuervo, revelando su metodo de composicion literaria."),
        ("1847", "⚰️", "Muerte de Virginia", "Virginia muere de tuberculosis a los 24 años. Poe cae en profunda depresion y alcoholismo."),
        ("1849", "💀", "Muerte misteriosa en Baltimore", "Encontrado delirando el 3 de octubre cerca de un bar en Baltimore. Muere el 7 de octubre. Causa: desconocida."),
    ]
    events_html = ""
    for year, icon, title, desc in events:
        cmd = _TIMELINE_CMDS.get(year, f"conversar {title.lower()}")
        events_html += f'''
        <div class="tl-item" data-command="{cmd}">
            <div class="tl-year">{year}</div>
            <div class="tl-dot">{icon}</div>
            <div class="tl-content">
                <div class="tl-title">{title}</div>
                <div class="tl-desc">{desc}</div>
                <div class="cmd-hint">📋 {cmd}</div>
            </div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timeline - Edgar Allan Poe</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: linear-gradient(180deg, #1a0a2e 0%, #0f172a 100%); color: #e2d9f3; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 700px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 35px; padding: 25px; background: rgba(0,0,0,0.4); border-radius: 16px; border: 1px solid rgba(139,92,246,0.3); }}
        .header h1 {{ font-size: 1.8rem; background: linear-gradient(90deg, #c084fc, #e879f9, #f0abfc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-style: italic; }}
        .header .sub {{ color: #a78bfa; font-size: 0.85rem; margin-top: 8px; font-style: italic; }}
        .timeline {{ position: relative; padding-left: 50px; }}
        .timeline::before {{ content: ''; position: absolute; left: 22px; top: 0; bottom: 0; width: 2px; background: linear-gradient(180deg, #6b21a8, #be185d, #6b21a8); }}
        .tl-item {{ position: relative; margin-bottom: 28px; opacity: 0; animation: fadeSlide 0.5s ease forwards; }}
        .tl-item:nth-child(1) {{ animation-delay: 0.1s; }}
        .tl-item:nth-child(2) {{ animation-delay: 0.2s; }}
        .tl-item:nth-child(3) {{ animation-delay: 0.3s; }}
        .tl-item:nth-child(4) {{ animation-delay: 0.4s; }}
        .tl-item:nth-child(5) {{ animation-delay: 0.5s; }}
        .tl-item:nth-child(6) {{ animation-delay: 0.6s; }}
        .tl-item:nth-child(7) {{ animation-delay: 0.7s; }}
        .tl-item:nth-child(8) {{ animation-delay: 0.8s; }}
        .tl-item:nth-child(9) {{ animation-delay: 0.9s; }}
        .tl-item:nth-child(10) {{ animation-delay: 1.0s; }}
        .tl-item:nth-child(11) {{ animation-delay: 1.1s; }}
        .tl-item:nth-child(12) {{ animation-delay: 1.2s; }}
        .tl-item:nth-child(13) {{ animation-delay: 1.3s; }}
        .tl-dot {{ position: absolute; left: -40px; top: 4px; font-size: 1.3rem; width: 32px; text-align: center; }}
        .tl-year {{ position: absolute; left: -50px; top: -18px; font-size: 0.65rem; color: #a78bfa; font-weight: 700; width: 50px; text-align: center; letter-spacing: 1px; }}
        .tl-content {{ background: rgba(0,0,0,0.35); border: 1px solid rgba(139,92,246,0.15); border-radius: 12px; padding: 16px 18px; transition: all 0.3s; }}
        .tl-content:hover {{ border-color: #a78bfa; background: rgba(107,33,168,0.12); transform: translateX(4px); }}
        .tl-title {{ font-weight: 700; font-size: 1rem; margin-bottom: 6px; color: #f0abfc; }}
        .tl-desc {{ font-size: 0.85rem; line-height: 1.5; color: #c4b5e0; }}
        .footer {{ text-align: center; margin-top: 30px; color: #5b4f73; font-size: 0.75rem; font-style: italic; }}
        @keyframes fadeSlide {{ from {{ opacity: 0; transform: translateX(-15px); }} to {{ opacity: 1; transform: translateX(0); }} }}
        {_SHARED_TOAST_CSS}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📅 Cronologia de las Sombras</h1>
            <div class="sub">La vida de Edgar Allan Poe — 1809 a 1849</div>
        </div>
        <div class="timeline">{events_html}</div>
        <div class="footer">AVIA-Clon-Edgar v1.3 | «I became insane, with long intervals of horrible sanity.»</div>
    </div>
    {_SHARED_TOAST_JS}
</body>
</html>'''


# ========================================================================
# ORGANISMO: Biblioteca del Cuervo (Catalogo de Obras)
# ========================================================================

def generate_biblioteca() -> str:
    categories = [
        ("🪶 Poesia", "poetry", [
            ("The Raven (1845)", "El poema mas famoso de la literatura americana. Un hombre atormentado dialoga con un cuervo que solo repite 'Nevermore'."),
            ("Annabel Lee (1849)", "Ultimo poema publicado. Amor eterno mas alla de la muerte en un 'reino junto al mar'."),
            ("Lenore (1843)", "Elegía por una joven muerta. Precursora tematica de El Cuervo."),
            ("The Bells (1849)", "Onomatopeya pura: campanas de plata, oro, bronce y hierro marcan las etapas de la vida."),
            ("A Dream Within a Dream (1849)", "Reflexion filosofica: ¿Es toda la realidad solo un sueño dentro de otro sueño?"),
            ("To Helen (1831)", "Oda a la belleza clasica. 'Helen, thy beauty is to me / Like those Nicean barks of yore.'"),
            ("Tamerlane (1827)", "Su primer poema publicado. Poder, arrepentimiento y el precio de la ambicion."),
        ]),
        ("💀 Cuentos de Terror", "terror", [
            ("The Fall of the House of Usher (1839)", "La mansion Usher, Roderick y Madeline: locura, enterramiento prematuro y destruccion total."),
            ("The Tell-Tale Heart (1843)", "Narrador 'cuerdo' confiesa un asesinato. El latido del corazon delata su culpa."),
            ("The Black Cat (1843)", "Alcoholismo, violencia domestica y un gato vengativo que revela un crimen desde la pared."),
            ("The Masque of the Red Death (1842)", "El Principe Prospero huye de la peste en una fiesta. La Muerte Roja entra igual."),
            ("The Pit and the Pendulum (1842)", "Tortura de la Inquisicion: un pozo, un pendulo cortante, y paredes que se cierran."),
            ("The Cask of Amontillado (1846)", "Venganza perfecta: Montresor empareda vivo a Fortunato en las catacumbas."),
        ]),
        ("🔍 Misterio y Detective", "mystery", [
            ("The Murders in the Rue Morgue (1841)", "PRIMER cuento detectivesco de la historia. C. Auguste Dupin resuelve un doble asesinato imposible."),
            ("The Purloined Letter (1844)", "Dupin recupera una carta robada. La solucion: esconderla a plena vista."),
            ("The Mystery of Marie Roget (1842)", "Dupin resuelve un caso real (Mary Rogers) desde su sillon, sin visitar la escena."),
            ("The Gold-Bug (1843)", "Criptografia y busqueda del tesoro. William Legrand descifra un mensaje pirata."),
        ]),
        ("📜 Ensayos y Teoria", "essays", [
            ("The Philosophy of Composition (1846)", "Como escribi El Cuervo: el metodo, la unidad de efecto, la eleccion de 'Nevermore'."),
            ("The Poetic Principle (1848)", "La poesia debe buscar la Belleza, no la Verdad ni la Moral. Brevedad es clave."),
            ("Eureka (1848)", "Ensayo cosmologico: Poe anticipa el Big Bang y los agujeros negros. Su obra mas ambiciosa."),
        ]),
    ]
    cats_html = ""
    for cat_name, cat_id, works in categories:
        works_html = ""
        for title, desc in works:
            work_key = title.split(" (")[0]
            cmd = _WORK_CMDS.get(work_key, f"analizar {work_key}")
            works_html += f'''
                <div class="work-card" data-command="{cmd}">
                    <div class="work-title">{title}</div>
                    <div class="work-desc">{desc}</div>
                    <div class="cmd-hint">📋 {cmd}</div>
                </div>'''
        cats_html += f'''
        <div class="category" id="{cat_id}">
            <button class="cat-header" data-cat="{cat_id}">
                <span class="cat-name">{cat_name}</span>
                <span class="cat-count">{len(works)} obras</span>
                <span class="cat-arrow">▼</span>
            </button>
            <div class="works-grid">{works_html}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblioteca del Cuervo</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%); color: #e2d9f3; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 750px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; padding: 25px; background: rgba(0,0,0,0.4); border-radius: 16px; border: 1px solid rgba(139,92,246,0.3); }}
        .header h1 {{ font-size: 1.8rem; background: linear-gradient(90deg, #c084fc, #e879f9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-style: italic; }}
        .header .sub {{ color: #a78bfa; font-size: 0.85rem; margin-top: 8px; }}
        .header .total {{ color: #6ee7b7; font-size: 0.75rem; margin-top: 6px; }}
        .category {{ margin-bottom: 16px; }}
        .cat-header {{ width: 100%; background: rgba(0,0,0,0.35); border: 1px solid rgba(139,92,246,0.2); border-radius: 12px; padding: 16px 20px; display: flex; align-items: center; cursor: pointer; color: #e2d9f3; font-family: inherit; font-size: 1rem; transition: all 0.2s; }}
        .cat-header:hover {{ border-color: #a78bfa; background: rgba(107,33,168,0.15); }}
        .cat-name {{ flex: 1; text-align: left; font-weight: 700; font-size: 1.1rem; }}
        .cat-count {{ color: #a78bfa; font-size: 0.8rem; margin-right: 12px; }}
        .cat-arrow {{ color: #a78bfa; font-size: 0.8rem; transition: transform 0.3s; }}
        .category.open .cat-arrow {{ transform: rotate(180deg); }}
        .works-grid {{ max-height: 0; overflow: hidden; transition: max-height 0.4s ease; padding: 0 4px; }}
        .category.open .works-grid {{ max-height: 2000px; }}
        .work-card {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(139,92,246,0.1); border-radius: 10px; padding: 14px 16px; margin-top: 10px; transition: all 0.2s; }}
        .work-card:hover {{ background: rgba(255,255,255,0.07); border-color: rgba(139,92,246,0.25); transform: translateX(4px); }}
        .work-title {{ font-weight: 700; font-size: 0.95rem; color: #f0abfc; margin-bottom: 5px; }}
        .work-desc {{ font-size: 0.82rem; line-height: 1.5; color: #b8a9d4; }}
        .footer {{ text-align: center; margin-top: 25px; color: #5b4f73; font-size: 0.75rem; font-style: italic; }}
        {_SHARED_TOAST_CSS}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Biblioteca del Cuervo</h1>
            <div class="sub">Catalogo completo de las obras de Edgar Allan Poe</div>
            <div class="total">21 obras en 4 categorias — Click para expandir</div>
        </div>
        {cats_html}
        <div class="footer">AVIA-Clon-Edgar v1.3 | «All that we see or seem is but a dream within a dream.»</div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('.cat-header').forEach(function(btn) {{
                btn.addEventListener('click', function() {{
                    var cat = this.closest('.category');
                    cat.classList.toggle('open');
                }});
            }});
            var first = document.querySelector('.category');
            if (first) first.classList.add('open');
        }});
    </script>
    {_SHARED_TOAST_JS}
</body>
</html>'''


# ========================================================================
# ORGANISMO: Personajes de la Oscuridad
# ========================================================================

def generate_personajes() -> str:
    chars = [
        ("🔍", "C. Auguste Dupin", "Detective / Analista", "#6366f1",
         "Los Crimenes de la Rue Morgue, La Carta Robada",
         "El primer detective de ficcion. Resuelve crimenes imposibles con logica pura y observacion desde su sillon. Precursor directo de Sherlock Holmes."),
        ("🏚️", "Roderick Usher", "Aristócrata / Artista", "#8b5cf6",
         "La Caida de la Casa Usher",
         "Ultimo heredero de los Usher. Hipersensible, torturado por terrores sin nombre. Entierra viva a su hermana Madeline. Su locura destruye la mansion."),
        ("🍷", "Montresor", "Vengador / Narrador", "#dc2626",
         "El Barril de Amontillado",
         "Aristócrata italiano que ejecuta la venganza perfecta: atrae a Fortunato con la promesa de un vino raro y lo empareda vivo en las catacumbas."),
        ("🐦", "El Narrador del Cuervo", "Erudito / Doliente", "#7c3aed",
         "El Cuervo",
         "Un hombre que llora a Lenore, su amada muerta. A medianoche, un cuervo entra y repite 'Nevermore' ante cada pregunta, hundiendolo en la desesperacion."),
        ("👁️", "Narrador del Corazon", "Asesino / Paranoico", "#be185d",
         "El Corazon Delator",
         "Insiste en su cordura mientras confiesa haber asesinado a un anciano por su 'ojo de buitre'. El latido imaginario del corazon bajo el suelo lo delata."),
        ("🎭", "Principe Prospero", "Noble / Hedonista", "#d97706",
         "La Mascara de la Muerte Roja",
         "Mientras la peste asola su reino, se encierra en una abadia con mil cortesanos a festejar. La Muerte Roja entra disfrazada a la mascarada."),
        ("✨", "Ligeia", "Erudita / Espiritu", "#0d9488",
         "Ligeia",
         "Mujer de belleza sobrenatural e intelecto prodigioso. Tras su muerte, su espiritu se apodera del cuerpo de Lady Rowena, resucitando ante el narrador."),
        ("🪞", "William Wilson", "Doble / Consciencia", "#4f46e5",
         "William Wilson",
         "Un hombre perseguido por su doble exacto que sabotea cada uno de sus actos inmorales. Al apuñalar al doble, descubre que se ha matado a si mismo."),
    ]
    cards_html = ""
    for icon, name, role, color, works, desc in chars:
        cmd = _CHAR_CMDS.get(name, f"conversar sobre {name}")
        cards_html += f'''
        <div class="char-card" style="border-left: 4px solid {color}" data-command="{cmd}">
            <div class="char-top">
                <div class="char-icon">{icon}</div>
                <div class="char-info">
                    <div class="char-name">{name}</div>
                    <div class="char-role">{role}</div>
                </div>
            </div>
            <div class="char-works">📖 {works}</div>
            <div class="char-desc">{desc}</div>
            <div class="cmd-hint">📋 {cmd}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personajes - Edgar Allan Poe</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%); color: #e2d9f3; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 750px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; padding: 25px; background: rgba(0,0,0,0.4); border-radius: 16px; border: 1px solid rgba(139,92,246,0.3); }}
        .header h1 {{ font-size: 1.8rem; background: linear-gradient(90deg, #c084fc, #e879f9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-style: italic; }}
        .header .sub {{ color: #a78bfa; font-size: 0.85rem; margin-top: 8px; }}
        .chars {{ display: flex; flex-direction: column; gap: 16px; }}
        .char-card {{ background: rgba(0,0,0,0.3); border: 1px solid rgba(139,92,246,0.15); border-radius: 14px; padding: 18px 20px; transition: all 0.3s; }}
        .char-card:hover {{ background: rgba(107,33,168,0.12); border-color: rgba(139,92,246,0.3); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }}
        .char-top {{ display: flex; align-items: center; gap: 14px; margin-bottom: 10px; }}
        .char-icon {{ font-size: 2.2rem; }}
        .char-name {{ font-weight: 700; font-size: 1.15rem; color: #f0abfc; }}
        .char-role {{ font-size: 0.8rem; color: #a78bfa; font-style: italic; }}
        .char-works {{ font-size: 0.75rem; color: #8b7fad; margin-bottom: 8px; padding: 6px 10px; background: rgba(0,0,0,0.2); border-radius: 6px; }}
        .char-desc {{ font-size: 0.87rem; line-height: 1.55; color: #c4b5e0; }}
        .footer {{ text-align: center; margin-top: 25px; color: #5b4f73; font-size: 0.75rem; font-style: italic; }}
        {_SHARED_TOAST_CSS}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 Personajes de la Oscuridad</h1>
            <div class="sub">Los personajes mas celebres del universo de Edgar Allan Poe</div>
        </div>
        <div class="chars">{cards_html}</div>
        <div class="footer">AVIA-Clon-Edgar v1.3 | «Those who dream by day are cognizant of many things which escape those who dream only by night.»</div>
    </div>
    {_SHARED_TOAST_JS}
</body>
</html>'''


# ========================================================================
# ORGANISMO: Dashboard Gotico "La Camara del Cuervo"
# ========================================================================

def generate_dashboard(model: str, web: bool, lang: str) -> str:
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    model_name = "Grok Fast" if "Grok" in model else "Gemini Flash"
    analysis = analyze_context(poe.default_chat)

    # Feature cards — diseño dorado Canvas23
    features = [
        ("conversar", "💬", "Conversacion", "Conversa conmigo sobre literatura, muerte, belleza y los abismos del alma humana. Mi voz del siglo XIX te guiara por senderos melancolicos.", "chat"),
        ("biblioteca", "📚", "La Biblioteca Oscura", "Explora mis obras en un catalogo interactivo. Poemas, relatos de terror, misterio y ensayos criticos. Todo mi legado literario.", "biblioteca"),
        ("poesia noche", "🪶", "Poesia Gotica", "Invoco a las musas oscuras para crear versos en mi estilo. Rima, ritmo, repeticion y un efecto unico de melancolia.", "poesia [tema]"),
        ("cuento misterio", "📖", "Relatos de Terror", "Narro cuentos goticos con tension creciente, giros psicologicos y atmosferas claustrofobicas. Cada relato incluye PDF.", "cuento [tema]"),
        ("analizar", "🔍", "Analisis Literario", "Aplico mis principios de The Philosophy of Composition: unidad de efecto, tono, estructura y simbolismo.", "analizar [texto]"),
        ("quiz", "🎲", "Quiz del Cuervo", "Pon a prueba tu conocimiento sobre mi vida y obra con preguntas interactivas y explicaciones.", "quiz"),
        ("galeria sombras", "🖼️", "Galeria de Sombras", "Genero ilustraciones goticas con IA: sombras, candelabros, cuervos, arquitectura victoriana, niebla.", "galeria [tema]"),
        ("nevermore hola mundo", "🌑", "Modo Nevermore", "Transformo cualquier texto al estilo literario de Poe. Prosa gotica, metaforas oscuras, musicalidad sombria.", "nevermore [texto]"),
        ("audio el cuervo", "🎭", "Audio Dramatico", "Narracion dramatica con voz generada por IA. Monologos teatrales sobre tus temas favoritos.", "audio [texto]"),
        ("timeline", "📅", "Cronologia Gotica", "Recorre mi vida desde Boston 1809 hasta Baltimore 1849. Trece eventos interactivos en una linea temporal animada.", "timeline"),
        ("personajes", "🎭", "Personajes de la Oscuridad", "Dupin, Usher, Montresor, Ligeia... Los ocho personajes mas celebres de mi universo literario.", "personajes"),
    ]
    features_html = ""
    for cmd, icon, title, desc, btn_label in features:
        features_html += f'''
            <div class="feature-card" data-command="{cmd}">
                <div class="feature-icon">{icon}</div>
                <h3 class="feature-title">{title}</h3>
                <p class="feature-desc">{desc}</p>
                <div class="feature-btn">{btn_label}</div>
                <div class="cmd-hint">📋 {cmd}</div>
            </div>'''

    # Agent cards
    agent_cmds = {"nevermore": "conversar", "lenore": "analizar", "usher": "estado"}
    agents_html = ""
    for a in AGENTS:
        a_cmd = agent_cmds.get(a.id, "conversar")
        agents_html += f'''
            <div class="agent-card" data-command="{a_cmd}" style="border-left: 4px solid {a.color}">
                <div class="agent-emoji">{a.emoji}</div>
                <div class="agent-info">
                    <div class="agent-name">{a.name}</div>
                    <div class="agent-role">{a.role}</div>
                </div>
                <div class="agent-status">● Activo</div>
            </div>'''

    # Sources
    sources_html = ""
    for s in SOURCES:
        sources_html += f'''
            <a href="{s.url}" target="_blank" class="source-link">
                <span>{s.icon}</span> {s.name}
            </a>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Camara del Cuervo - AVIA-Clon-Edgar</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --gold: #d4a843;
            --gold-light: #f0d78c;
            --gold-dark: #8b6914;
            --gold-glow: rgba(212,168,67,0.3);
            --bg-deep: #12091f;
            --bg-card: rgba(20,10,40,0.85);
            --border-gold: rgba(212,168,67,0.3);
            --text-cream: #e8dcc8;
            --text-muted: #8b7f6d;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Cormorant Garamond', Georgia, serif; background: linear-gradient(180deg, #1a0a2e 0%, var(--bg-deep) 40%, #0a0612 100%); color: var(--text-cream); min-height: 100vh; padding: 24px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}

        /* ── Header dorado ── */
        .header {{ text-align: center; margin-bottom: 40px; padding: 40px 30px 30px; }}
        .raven {{ font-size: 4rem; margin-bottom: 8px; filter: drop-shadow(0 4px 20px rgba(212,168,67,0.35)); animation: float 3s ease-in-out infinite; }}
        @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
        .header h1 {{ font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-weight: 700; font-size: 2.8rem; color: var(--gold); text-shadow: 0 0 40px rgba(212,168,67,0.35), 0 0 80px rgba(212,168,67,0.15); letter-spacing: 2px; line-height: 1.2; }}
        .header .subtitle {{ font-family: 'Cormorant Garamond', serif; font-size: 1.05rem; color: var(--gold-dark); margin-top: 10px; letter-spacing: 1px; }}
        .header .quote {{ font-style: italic; color: var(--text-muted); font-size: 0.92rem; margin-top: 14px; }}
        .gold-line {{ height: 2px; background: linear-gradient(90deg, transparent, var(--gold), transparent); margin-top: 22px; }}

        /* ── Feature Cards 2-col ── */
        .features-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 32px; }}
        @media (max-width: 660px) {{ .features-grid {{ grid-template-columns: 1fr; }} }}
        .feature-card {{ background: var(--bg-card); border: 1px solid var(--border-gold); border-radius: 14px; padding: 28px 24px 22px; transition: all 0.3s; position: relative; cursor: pointer; }}
        .feature-card:hover {{ border-color: var(--gold); box-shadow: 0 0 25px var(--gold-glow); transform: translateY(-3px); }}
        .feature-card.copied {{ border-color: #6ee7b7; box-shadow: 0 0 20px rgba(16,185,129,0.25); }}
        .feature-icon {{ font-size: 2.4rem; margin-bottom: 14px; }}
        .feature-title {{ font-family: 'Playfair Display', Georgia, serif; font-size: 1.3rem; font-weight: 700; color: var(--gold); margin-bottom: 10px; }}
        .feature-desc {{ font-size: 0.95rem; line-height: 1.6; color: var(--text-cream); opacity: 0.85; margin-bottom: 16px; }}
        .feature-btn {{ display: inline-block; font-family: monospace; font-size: 0.78rem; color: var(--gold-dark); background: rgba(139,58,58,0.25); border: 1px solid rgba(139,58,58,0.5); padding: 5px 14px; border-radius: 4px; transition: all 0.2s; }}
        .feature-card:hover .feature-btn {{ background: rgba(139,58,58,0.4); color: var(--gold-light); }}

        /* ── Section titles ── */
        .section-title {{ font-family: 'Playfair Display', Georgia, serif; font-size: 1.1rem; color: var(--gold); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid rgba(212,168,67,0.15); }}

        /* ── Agents ── */
        .agents-section {{ margin-bottom: 28px; }}
        .agents-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
        @media (max-width: 660px) {{ .agents-grid {{ grid-template-columns: 1fr; }} }}
        .agent-card {{ background: var(--bg-card); border: 1px solid var(--border-gold); border-radius: 10px; padding: 16px; display: flex; align-items: center; gap: 12px; transition: all 0.2s; cursor: pointer; }}
        .agent-card:hover {{ border-color: var(--gold); box-shadow: 0 0 15px var(--gold-glow); transform: translateY(-2px); }}
        .agent-card.copied {{ background: rgba(16,185,129,0.12); border-color: #6ee7b7; }}
        .agent-emoji {{ font-size: 1.8rem; }}
        .agent-info {{ flex: 1; }}
        .agent-name {{ font-family: 'Playfair Display', serif; font-weight: 700; font-size: 0.95rem; color: var(--gold-light); }}
        .agent-role {{ font-size: 0.8rem; color: var(--text-muted); }}
        .agent-status {{ font-size: 0.7rem; color: #6ee7b7; margin-left: auto; }}

        /* ── Stats ── */
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 28px; }}
        @media (max-width: 660px) {{ .stats-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        .stat {{ background: var(--bg-card); border: 1px solid rgba(212,168,67,0.15); border-radius: 10px; padding: 16px; text-align: center; }}
        .stat-val {{ font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: var(--gold); }}
        .stat-lbl {{ font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; }}

        /* ── Sources ── */
        .sources-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 22px; }}
        .source-link {{ background: var(--bg-card); border: 1px solid rgba(212,168,67,0.12); border-radius: 8px; padding: 10px 16px; text-decoration: none; color: var(--text-cream); font-size: 0.88rem; transition: all 0.2s; }}
        .source-link:hover {{ border-color: var(--gold); color: var(--gold-light); }}

        /* ── Footer ── */
        .footer {{ text-align: center; margin-top: 24px; color: var(--text-muted); font-size: 0.78rem; font-style: italic; }}

        /* ── Interactive: cmd-hint ── */
        [data-command] {{ cursor: pointer; }}
        .cmd-hint {{ font-size: 0.65rem; color: var(--text-muted); margin-top: 8px; padding: 3px 8px; background: rgba(0,0,0,0.3); border-radius: 4px; font-family: monospace; opacity: 0; transition: opacity 0.3s; }}
        [data-command]:hover .cmd-hint {{ opacity: 1; }}

        /* ── Toast dorado ── */
        .toast {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: linear-gradient(135deg, var(--gold-dark), #5a3d08); color: var(--text-cream); padding: 12px 24px; border-radius: 25px; font-size: 0.9rem; opacity: 0; transition: all 0.3s; z-index: 1000; border: 1px solid var(--gold); }}
        .toast.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="raven">🐦</div>
            <h1>La Camara del Cuervo</h1>
            <div class="subtitle">Dashboard de AVIA-Clon-Edgar Poe</div>
            <div class="quote">«Durante toda una lugubre tarde de otono, en que las nubes se cernian bajas y opresivas...»</div>
            <div class="gold-line"></div>
        </div>

        <div class="features-grid">{features_html}</div>

        <div class="agents-section">
            <div class="section-title">🔮 Constelacion de Agentes</div>
            <div class="agents-grid">{agents_html}</div>
        </div>

        <div class="section-title">📊 Estado de la Sesion</div>
        <div class="stats-grid">
            <div class="stat"><div class="stat-val">{analysis.stats['user_messages']}</div><div class="stat-lbl">Consultas</div></div>
            <div class="stat"><div class="stat-val">{analysis.stats['bot_messages']}</div><div class="stat-lbl">Respuestas</div></div>
            <div class="stat"><div class="stat-val">{len(AGENTS)}</div><div class="stat-lbl">Agentes</div></div>
            <div class="stat"><div class="stat-val">v1.3</div><div class="stat-lbl">Version</div></div>
        </div>

        <div class="section-title">📚 Fuentes Transmedia</div>
        <div class="sources-row">{sources_html}</div>

        <div class="footer">AVIA-Clon-Edgar v1.3 | La Camara del Cuervo | {fecha} | {model_name}</div>
    </div>
    <div id="toast" class="toast"></div>
    <script>
        function showToast(txt) {{
            var toast = document.getElementById('toast');
            toast.textContent = txt;
            toast.classList.add('show');
            setTimeout(function() {{ toast.classList.remove('show'); }}, 2500);
        }}
        function fallbackCopy(text) {{
            var ta = document.createElement('textarea');
            ta.value = text;
            ta.style.position = 'fixed';
            ta.style.left = '-9999px';
            document.body.appendChild(ta);
            ta.select();
            try {{ document.execCommand('copy'); return true; }} catch(e) {{ return false; }}
            finally {{ document.body.removeChild(ta); }}
        }}
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('[data-command]').forEach(function(el) {{
                el.addEventListener('click', function(e) {{
                    if (e.target.closest('a')) return;
                    var cmd = this.getAttribute('data-command');
                    if (!cmd) return;
                    this.classList.add('copied');
                    var self = this;
                    setTimeout(function() {{ self.classList.remove('copied'); }}, 1500);
                    if (navigator.clipboard && navigator.clipboard.writeText) {{
                        navigator.clipboard.writeText(cmd).then(function() {{
                            showToast('"' + cmd + '" copiado — pegalo en el chat');
                        }}).catch(function() {{
                            fallbackCopy(cmd);
                            showToast('Comando: ' + cmd);
                        }});
                    }} else {{
                        fallbackCopy(cmd);
                        showToast('Comando: ' + cmd);
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>'''

# ========================================================================
# ORGANISMO: Exportacion Gotica (PDF manuscrito)
# ========================================================================

def generate_gothic_pdf(title: str, content: str) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('GothicTitle', parent=styles['Title'], fontName='Times-BoldItalic', fontSize=22, textColor=HexColor('#2d1b4e'), spaceAfter=20, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('GothicSub', parent=styles['Normal'], fontName='Times-Italic', fontSize=11, textColor=HexColor('#6b21a8'), spaceAfter=16, alignment=TA_CENTER)
    body_style = ParagraphStyle('GothicBody', parent=styles['Normal'], fontName='Times-Roman', fontSize=11, textColor=HexColor('#1a0a2e'), leading=16, spaceAfter=10, alignment=TA_JUSTIFY)
    footer_style = ParagraphStyle('GothicFooter', parent=styles['Normal'], fontName='Times-Italic', fontSize=9, textColor=HexColor('#8b7fad'), spaceBefore=30, alignment=TA_CENTER)

    elements = []
    elements.append(Paragraph(f"🐦 {title}", title_style))
    elements.append(Paragraph("AVIA-Clon-Edgar — Gemelo Digital de Edgar Allan Poe", subtitle_style))
    elements.append(Spacer(1, 12))

    clean_content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    for para in clean_content.split('\n'):
        para = para.strip()
        if para:
            elements.append(Paragraph(para, body_style))

    elements.append(Spacer(1, 20))
    fecha = datetime.now().strftime("%d/%m/%Y")
    elements.append(Paragraph(f"— E.A. Poe (Gemelo Digital) | {fecha} | AVIA-Clon-Edgar v1.3 —", footer_style))

    doc.build(elements)
    return buffer.getvalue()

# ========================================================================
# ECOSISTEMA: Clase Principal AVIAEdgar
# ========================================================================

class AVIAEdgar:
    def __init__(self):
        self.model = poe.query.parameters.get("model", "Grok-4.1-Fast-Non-Reasoning")
        self.web = poe.query.parameters.get("web", False)
        self.lang = poe.query.parameters.get("lang", "es")
        self.query_text = poe.query.text.strip()
        self.query_lower = self.query_text.lower()

    def show_dashboard(self):
        html = generate_dashboard(self.model, self.web, self.lang)
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_status(self):
        analysis = analyze_context(poe.default_chat)
        model_name = "Grok Fast" if "Grok" in self.model else "Gemini Flash"
        with poe.start_message() as msg:
            msg.write("## 🐦 AVIA-Clon-Edgar v1.3 — Estado\n\n")
            msg.write(f"**Modelo:** {model_name} | **Web:** {'ON' if self.web else 'OFF'} | **Idioma:** {self.lang.upper()}\n\n")
            msg.write("**Agentes:**\n")
            for a in AGENTS:
                msg.write(f"- {a.emoji} **{a.name}** — {a.role} ● Activo\n")
            msg.write(f"\n**Sesion:** {analysis.stats['user_messages']} consultas | {analysis.stats['bot_messages']} respuestas | {analysis.stats['total_chars']:,} caracteres\n")
            msg.write(f"**Temas:** {', '.join(analysis.topics)}\n")
            msg.write(f"\n*«Quoth the Raven, Nevermore.»*\n")

    def do_conversation(self):
        with poe.start_message() as msg:
            msg.write("*🐦 Los tres agentes deliberan...*\n\n")

        poe.call(
            self.model,
            poe.Message(text=SYSTEM_PROMPT_POE, sender="system"),
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True,
        )

    def do_poetry(self, theme: str):
        with poe.start_message() as msg:
            msg.write(f"*🪶 Invocando a la Musa sobre «{theme}»...*\n\n")

        result = generate_poetry(self.model, theme, poe.default_chat)

        with poe.start_message() as msg:
            msg.write(result)

        # Also generate PDF
        pdf_bytes = generate_gothic_pdf(f"Poema: {theme.title()}", result)
        with poe.start_message() as msg:
            attachment = msg.attach_file(name=f"poema_{theme.replace(' ','_')[:20]}.pdf", contents=pdf_bytes, content_type="application/pdf")
            msg.write("📜 *Manuscrito adjunto en PDF*")

    def do_analysis(self, text: str):
        if not text:
            with poe.start_message() as msg:
                msg.write("*Necesito un texto para analizar. Escribe:* `analizar [tu texto aqui]`")
            return

        with poe.start_message() as msg:
            msg.write(f"*🔍 LENORE analiza con la mirada critica del maestro...*\n\n")

        result = generate_analysis(self.model, text, poe.default_chat)

        with poe.start_message() as msg:
            msg.write(result)

    def do_story(self, theme: str):
        with poe.start_message() as msg:
            msg.write(f"*📖 Sumergiendome en las sombras para tejer un relato sobre «{theme}»...*\n\n")

        result = generate_story(self.model, theme, poe.default_chat)

        with poe.start_message() as msg:
            msg.write(result)

        # Also generate PDF
        pdf_bytes = generate_gothic_pdf(f"Cuento: {theme.title()}", result)
        with poe.start_message() as msg:
            attachment = msg.attach_file(name=f"cuento_{theme.replace(' ','_')[:20]}.pdf", contents=pdf_bytes, content_type="application/pdf")
            msg.write("📖 *Manuscrito adjunto en PDF*")

    def show_timeline(self):
        html = generate_timeline()
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_biblioteca(self):
        html = generate_biblioteca()
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def show_personajes(self):
        html = generate_personajes()
        with poe.start_message() as msg:
            msg.write(f"````html\n{html}\n````")

    def do_quiz(self):
        with poe.start_message() as msg:
            msg.write("*🎲 Preparando una pregunta desde las profundidades de mi obra...*\n\n")

        try:
            q_data = generate_quiz_question(self.model, poe.default_chat)
            html = generate_quiz_canvas(q_data)
            with poe.start_message() as msg:
                msg.write(f"````html\n{html}\n````")
        except Exception:
            with poe.start_message() as msg:
                msg.write("*Las sombras me impiden formular la pregunta. Intenta de nuevo con* `quiz`")

    def do_gallery(self, theme: str):
        with poe.start_message() as msg:
            msg.write(f"*🖼️ Invocando visiones goticas sobre «{theme}»...*\n\n")

        prompt_response = poe.call(
            self.model,
            f"""Create a detailed image generation prompt for a gothic, dark, atmospheric illustration inspired by Edgar Allan Poe about: "{theme}"

The prompt should evoke: dark shadows, candlelight, ravens, gothic architecture, mist, Victorian era, melancholy, dramatic lighting.

Output in ```json format:
```json
{{"prompt": "detailed image prompt in English"}}
```""",
        )
        try:
            parsed = parse_json_from_response(prompt_response.text, ["prompt"])
            image_prompt = parsed["prompt"]
        except Exception:
            image_prompt = f"Dark gothic illustration inspired by Edgar Allan Poe about {theme}, ravens, candlelight, shadows, Victorian era, melancholy, atmospheric, detailed"

        poe.call("Imagen-4-Fast", image_prompt, parameters={"aspect_ratio": "4:3"}, output=poe.default_chat)

        with poe.start_message() as msg:
            msg.write(f"*🖼️ «{theme}» — Galeria de Sombras, AVIA-Clon-Edgar v1.3*")

    def do_nevermore(self, text: str):
        if not text:
            with poe.start_message() as msg:
                msg.write("*Necesito un texto para transformar. Escribe:* `nevermore [tu texto aqui]`")
            return

        with poe.start_message() as msg:
            msg.write("*🌑 Nevermore... sumergiendo tu texto en las sombras...*\n\n")

        result = generate_nevermore_text(self.model, text, poe.default_chat)

        with poe.start_message() as msg:
            msg.write(f"**🌑 Modo Nevermore — Transformacion Gotica:**\n\n---\n\n{result}\n\n---\n\n*Texto original transformado al estilo de E.A. Poe*")

    def do_audio(self, text: str):
        if not text:
            with poe.start_message() as msg:
                msg.write("*Necesito un texto para narrar. Escribe:* `audio [tu texto o tema]`")
            return

        with poe.start_message() as msg:
            msg.write(f"*🎭 Preparando narracion dramatica...*\n\n")

        narration_prompt = f"""{SYSTEM_PROMPT_POE}

TAREA: Escribe una narracion dramatica corta (maximo 800 caracteres) sobre: "{text}"

Debe sonar como un monologo teatral de Edgar Allan Poe: dramatico, sombrio, con ritmo y musicalidad.
Escribe SOLO el texto de la narracion, sin acotaciones ni instrucciones."""

        narration = poe.call(self.model, narration_prompt)
        narration_text = narration.text.strip()
        # ElevenLabs-v2.5-Turbo supports up to 40000 chars, but keep narration concise
        if len(narration_text) > 2000:
            narration_text = narration_text[:2000].rsplit(' ', 1)[0]

        voice = "David Martin" if self.lang == "es" else "Bradford"
        language = "es" if self.lang == "es" else "en"

        poe.call(
            "ElevenLabs-v2.5-Turbo",
            narration_text,
            parameters={"voice": voice, "language": language},
            output=poe.default_chat,
        )

        with poe.start_message() as msg:
            msg.write(f"*🎭 Narracion dramatica — «{text[:50]}» — Voz: {voice}*")

    def run(self):
        q = self.query_lower

        # Command routing
        if q in ["dashboard", "panel", "camara"]:
            self.show_dashboard()
        elif q in ["estado", "status"]:
            self.show_status()
        elif q.startswith("poesia") or q.startswith("poema"):
            theme = self.query_text.split(maxsplit=1)[1] if len(self.query_text.split()) > 1 else "la noche eterna"
            self.do_poetry(theme)
        elif q.startswith("analizar") or q.startswith("analisis"):
            text = self.query_text.split(maxsplit=1)[1] if len(self.query_text.split()) > 1 else ""
            self.do_analysis(text)
        elif q.startswith("cuento") or q.startswith("relato") or q.startswith("historia"):
            theme = self.query_text.split(maxsplit=1)[1] if len(self.query_text.split()) > 1 else "una habitacion cerrada"
            self.do_story(theme)
        elif q in ["timeline", "cronologia", "vida"]:
            self.show_timeline()
        elif q in ["biblioteca", "obras", "catalogo"]:
            self.show_biblioteca()
        elif q in ["personajes", "characters", "protagonistas"]:
            self.show_personajes()
        elif q.startswith("quiz"):
            self.do_quiz()
        elif q.startswith("galeria") or q.startswith("galería"):
            theme = self.query_text.split(maxsplit=1)[1] if len(self.query_text.split()) > 1 else "sombras y cuervos"
            self.do_gallery(theme)
        elif q.startswith("nevermore"):
            text = self.query_text.split(maxsplit=1)[1] if len(self.query_text.split()) > 1 else ""
            self.do_nevermore(text)
        elif q.startswith("audio") or q.startswith("narrar"):
            text = self.query_text.split(maxsplit=1)[1] if len(self.query_text.split()) > 1 else ""
            self.do_audio(text)
        elif q in ["conversar", "hablar", "charlar"]:
            self.do_conversation()
        else:
            # Default: conversation with Poe persona
            self.do_conversation()

if __name__ == "__main__":
    bot = AVIAEdgar()
    bot.run()

