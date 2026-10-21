# poe: name=AVIA-Clon-Edgar

"""
AVIA-Clon-Edgar v1.1
Gemelo Digital de Edgar Allan Poe — Constelacion de Agentes IA
Agentes: NEVERMORE (Narrador) + LENORE (Analisis) + USHER (Etica)
Comandos: conversar | poesia | analizar | cuento | quiz | galeria | nevermore | audio | dashboard | estado
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
    introduction_message="""🪶 **AVIA-Clon-Edgar v1.0** — *Gemelo Digital de Edgar Allan Poe*

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
# ORGANISMO: Dashboard Gotico "La Camara del Cuervo"
# ========================================================================

def generate_dashboard(model: str, web: bool, lang: str) -> str:
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    model_name = "Grok Fast" if "Grok" in model else "Gemini Flash"
    analysis = analyze_context(poe.default_chat)

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

    # Functional action cards
    commands = [
        ("conversar", "💬", "Conversar", "Charla con Poe"),
        ("poesia noche", "🪶", "Poesia", "Generar poema"),
        ("cuento misterio", "📖", "Cuento", "Relato gotico"),
        ("analizar", "🔍", "Analizar", "Critica literaria"),
        ("quiz", "🎲", "Quiz", "Trivia literaria"),
        ("galeria sombras", "🖼️", "Galeria", "Imagenes goticas"),
        ("nevermore hola mundo", "🌑", "Nevermore", "Transformar texto"),
        ("audio el cuervo", "🎭", "Audio", "Narracion dramatica"),
    ]
    actions_html = ""
    for cmd, icon, label, desc in commands:
        actions_html += f'''
        <button class="action-btn" data-command="{cmd}">
            <div class="action-icon">{icon}</div>
            <div class="action-label">{label}</div>
            <div class="action-desc">{desc}</div>
            <div class="action-cmd">📋 {cmd}</div>
        </button>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La Camara del Cuervo - AVIA-Clon-Edgar</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', 'Times New Roman', serif; background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%); color: #e2d9f3; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 850px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; padding: 30px; background: rgba(0,0,0,0.4); border-radius: 16px; border: 1px solid rgba(139,92,246,0.3); position: relative; overflow: hidden; }}
        .header::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at 50% 0%, rgba(139,92,246,0.15) 0%, transparent 70%); pointer-events: none; }}
        .header h1 {{ font-size: 2rem; background: linear-gradient(90deg, #c084fc, #e879f9, #f0abfc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; font-style: italic; }}
        .header .subtitle {{ color: #a78bfa; font-size: 0.95rem; font-style: italic; }}
        .header .quote {{ color: #7c6f9b; font-size: 0.8rem; margin-top: 12px; font-style: italic; }}
        .section {{ background: rgba(0,0,0,0.3); border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(139,92,246,0.15); }}
        .section-title {{ font-size: 0.85rem; color: #a78bfa; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }}
        .agents-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }}
        .agent-card {{ background: rgba(255,255,255,0.04); border-radius: 10px; padding: 15px; display: flex; align-items: center; gap: 12px; transition: transform 0.2s; }}
        .agent-card:hover {{ transform: translateY(-2px); background: rgba(255,255,255,0.07); }}
        .agent-emoji {{ font-size: 2rem; }}
        .agent-info {{ flex: 1; }}
        .agent-name {{ font-weight: 700; font-size: 1rem; }}
        .agent-role {{ color: #8b7fad; font-size: 0.8rem; }}
        .agent-status {{ font-size: 0.7rem; padding: 4px 8px; border-radius: 20px; }}
        .agent-status.active {{ background: rgba(16,185,129,0.15); color: #6ee7b7; }}
        .sources-grid {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .source-card {{ background: rgba(255,255,255,0.04); border-radius: 8px; padding: 10px 15px; display: flex; align-items: center; gap: 8px; text-decoration: none; color: #e2d9f3; font-size: 0.9rem; transition: background 0.2s; }}
        .source-card:hover {{ background: rgba(255,255,255,0.08); }}
        .actions-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; }}
        .action-btn {{ background: linear-gradient(135deg, rgba(107,33,168,0.3), rgba(190,24,93,0.2)); border: 1px solid rgba(139,92,246,0.2); border-radius: 12px; padding: 18px; text-align: center; cursor: pointer; transition: all 0.2s; color: #e2d9f3; font-family: inherit; }}
        .action-btn:hover {{ transform: translateY(-3px); border-color: #a78bfa; box-shadow: 0 8px 25px rgba(139,92,246,0.2); }}
        .action-btn:active {{ transform: scale(0.95); }}
        .action-btn.copied {{ background: linear-gradient(135deg, rgba(16,185,129,0.3), rgba(6,95,70,0.3)); border-color: #6ee7b7; }}
        .action-icon {{ font-size: 2rem; margin-bottom: 8px; }}
        .action-label {{ font-size: 0.9rem; font-weight: 600; }}
        .action-desc {{ font-size: 0.75rem; color: #8b7fad; margin-top: 4px; }}
        .action-cmd {{ font-size: 0.65rem; color: #6b5b8d; margin-top: 10px; padding: 4px 8px; background: rgba(0,0,0,0.3); border-radius: 4px; font-family: monospace; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
        @media (max-width: 600px) {{ .stats-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        .stat {{ background: rgba(255,255,255,0.04); border-radius: 10px; padding: 15px; text-align: center; }}
        .stat-val {{ font-size: 1.5rem; font-weight: 700; background: linear-gradient(90deg, #c084fc, #e879f9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .stat-lbl {{ font-size: 0.7rem; color: #8b7fad; margin-top: 4px; }}
        .toast {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: linear-gradient(135deg, #6b21a8, #4c1d95); color: white; padding: 12px 24px; border-radius: 25px; font-size: 0.9rem; opacity: 0; transition: all 0.3s; z-index: 1000; }}
        .toast.show {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
        .footer {{ text-align: center; margin-top: 20px; color: #5b4f73; font-size: 0.8rem; font-style: italic; }}
        .badge-new {{ background: linear-gradient(90deg, #e879f9, #c084fc); color: #1a0a2e; font-size: 0.55rem; padding: 2px 6px; border-radius: 8px; font-weight: 700; margin-left: 6px; vertical-align: middle; letter-spacing: 0.5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 La Camara del Cuervo</h1>
            <div class="subtitle">AVIA-Clon-Edgar — Gemelo Digital de Edgar Allan Poe</div>
            <div class="quote">«Deep into that darkness peering, long I stood there wondering, fearing...»</div>
        </div>
        <div class="section">
            <div class="section-title">🔮 Constelacion de Agentes</div>
            <div class="agents-grid">{agents_html}</div>
        </div>
        <div class="section">
            <div class="section-title">⚡ Invocaciones <span style="font-size:0.7rem;color:#6ee7b7">(click para copiar)</span></div>
            <div class="actions-grid">{actions_html}</div>
        </div>
        <div class="section">
            <div class="section-title">📊 Estado de la Sesion</div>
            <div class="stats-grid">
                <div class="stat"><div class="stat-val">{analysis.stats['user_messages']}</div><div class="stat-lbl">Consultas</div></div>
                <div class="stat"><div class="stat-val">{analysis.stats['bot_messages']}</div><div class="stat-lbl">Respuestas</div></div>
                <div class="stat"><div class="stat-val">{len(AGENTS)}</div><div class="stat-lbl">Agentes</div></div>
                <div class="stat"><div class="stat-val">v1.0</div><div class="stat-lbl">Version</div></div>
            </div>
        </div>
        <div class="section">
            <div class="section-title">📚 Fuentes Transmedia</div>
            <div class="sources-grid">{sources_html}</div>
        </div>
        <div class="footer">AVIA-Clon-Edgar v1.1 | La Camara del Cuervo | {fecha} | {model_name}</div>
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
            document.querySelectorAll('.action-btn').forEach(function(btn) {{
                btn.addEventListener('click', function() {{
                    var cmd = this.getAttribute('data-command');
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
    elements.append(Paragraph(f"— E.A. Poe (Gemelo Digital) | {fecha} | AVIA-Clon-Edgar v1.0 —", footer_style))

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
            msg.write("## 🐦 AVIA-Clon-Edgar v1.0 — Estado\n\n")
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
            msg.write(f"*🖼️ «{theme}» — Galeria de Sombras, AVIA-Clon-Edgar v1.1*")

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

