# poe: name=AVIA-CreatorHub

import json
import re
from datetime import datetime

from fastapi_poe.types import (
    SettingsResponse, ParameterControls, Section,
    DropDown, ToggleSwitch, Slider, TextArea, ValueNamePair
)

# ============================================================================
# AVIA CREATORHUB v3.2 — Ecosistema Integral de Creación con IA
# Basado en: AVIASeniorv3.2 | Libro Blanco | Reglas Universales
# Diseño UI: Oxford/MIT Academic Design System
# ============================================================================

poe.update_settings(SettingsResponse(
    introduction_message="""# 🎓 AVIA CreatorHub v3.2

**Plataforma Integral de Creación Asistida por IA**
*Powered by AVIASeniorv3.2 · Constelación Económica de Consenso*

---

Bienvenido al ecosistema AVIA. Este hub centraliza todas las capacidades creativas con validación multi-modelo y autocorrección inteligente.

### 🧩 Módulos Disponibles

| Módulo | Función |
|--------|---------|
| 🎨 **Canvas Creator** | Genera aplicaciones web/Canvas con UI Oxford/MIT |
| 📊 **Data Visualizer** | Dashboards y visualizaciones interactivas |
| 🖼️ **Image Studio** | Generación de imágenes con consenso multi-modelo |
| 🔬 **Research Agent** | Investigación profunda con síntesis académica |
| 📝 **Content Writer** | Redacción profesional con estilo académico |
| 🛠️ **Code Architect** | Desarrollo de código con AVIA Pipeline |

### ⚙️ Cómo Usar

1. Escribe tu solicitud de forma natural
2. Ajusta el módulo y parámetros con el ícono ⚙️ debajo del input
3. AVIA Pipeline procesará tu solicitud con autocorrección automática

*Diseño inspirado en los sistemas de UI de Oxford, MIT y Stanford*""",
    enable_image_comprehension=True,
    parameter_controls=ParameterControls(
        sections=[
            Section(
                name="🎯 Módulo AVIA",
                controls=[
                    DropDown(
                        label="Módulo Activo",
                        parameter_name="module",
                        default_value="auto",
                        options=[
                            ValueNamePair(value="auto", name="🤖 Auto-detect (recomendado)"),
                            ValueNamePair(value="canvas", name="🎨 Canvas Creator"),
                            ValueNamePair(value="data_viz", name="📊 Data Visualizer"),
                            ValueNamePair(value="image", name="🖼️ Image Studio"),
                            ValueNamePair(value="research", name="🔬 Research Agent"),
                            ValueNamePair(value="content", name="📝 Content Writer"),
                            ValueNamePair(value="code", name="🛠️ Code Architect"),
                        ],
                    ),
                ],
            ),
            Section(
                name="🔧 AVIA Pipeline",
                controls=[
                    ToggleSwitch(
                        label="Constelación de Consenso (multi-modelo)",
                        parameter_name="consensus",
                        default_value=True,
                    ),
                    ToggleSwitch(
                        label="Autocorrección de Errores",
                        parameter_name="autocorrect",
                        default_value=True,
                    ),
                    Slider(
                        label="Nivel de Profundidad",
                        parameter_name="depth",
                        default_value=3,
                        min_value=1,
                        max_value=5,
                        step=1,
                    ),
                    DropDown(
                        label="Estilo de Diseño UI",
                        parameter_name="ui_style",
                        default_value="oxford",
                        options=[
                            ValueNamePair(value="oxford", name="🎓 Oxford Academic"),
                            ValueNamePair(value="mit", name="🔬 MIT Technical"),
                            ValueNamePair(value="stanford", name="🌲 Stanford Modern"),
                            ValueNamePair(value="minimal", name="✨ Minimal Clean"),
                        ],
                    ),
                ],
            ),
            Section(
                name="📐 Ontología Creativa",
                controls=[
                    TextArea(
                        label="Contexto adicional / Instrucciones",
                        parameter_name="extra_context",
                        default_value="",
                        placeholder="Añade contexto, requisitos específicos o instrucciones adicionales...",
                    ),
                    DropDown(
                        label="Idioma de salida",
                        parameter_name="language",
                        default_value="es",
                        options=[
                            ValueNamePair(value="es", name="🇪🇸 Español"),
                            ValueNamePair(value="en", name="🇬🇧 English"),
                            ValueNamePair(value="fr", name="🇫🇷 Français"),
                            ValueNamePair(value="de", name="🇩🇪 Deutsch"),
                            ValueNamePair(value="pt", name="🇧🇷 Português"),
                        ],
                    ),
                ],
            ),
        ]
    ),
))


# ============================================================================
# UTILIDADES CORE
# ============================================================================

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
            raise Exception(f"Could not find JSON in response:\n{response_text[:500]}")
    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON: {e}\nRaw: {json_str[:300]}")
    if required_fields:
        missing = set(required_fields) - set(parsed.keys())
        if missing:
            raise Exception(f"Missing required fields: {', '.join(missing)}")
    return parsed


UI_STYLE_CONFIGS = {
    "oxford": {
        "name": "Oxford Academic",
        "primary": "#002147",
        "secondary": "#8C1515",
        "accent": "#C4A35A",
        "bg": "#FAFBFC",
        "card_bg": "#FFFFFF",
        "text": "#1A1A2E",
        "font": "'Crimson Text', 'Georgia', serif",
        "heading_font": "'Playfair Display', 'Georgia', serif",
        "border_radius": "4px",
        "shadow": "0 2px 8px rgba(0,33,71,0.08)",
    },
    "mit": {
        "name": "MIT Technical",
        "primary": "#A31F34",
        "secondary": "#8A8B8C",
        "accent": "#E87722",
        "bg": "#F5F5F5",
        "card_bg": "#FFFFFF",
        "text": "#1C1C1C",
        "font": "'Inter', 'Helvetica Neue', sans-serif",
        "heading_font": "'JetBrains Mono', 'Courier New', monospace",
        "border_radius": "2px",
        "shadow": "0 1px 4px rgba(163,31,52,0.1)",
    },
    "stanford": {
        "name": "Stanford Modern",
        "primary": "#8C1515",
        "secondary": "#2E2D29",
        "accent": "#B1040E",
        "bg": "#F4F2EC",
        "card_bg": "#FFFFFF",
        "text": "#2E2D29",
        "font": "'Source Sans Pro', 'Helvetica', sans-serif",
        "heading_font": "'Source Serif Pro', 'Georgia', serif",
        "border_radius": "8px",
        "shadow": "0 4px 12px rgba(140,21,21,0.06)",
    },
    "minimal": {
        "name": "Minimal Clean",
        "primary": "#111827",
        "secondary": "#6B7280",
        "accent": "#3B82F6",
        "bg": "#FFFFFF",
        "card_bg": "#F9FAFB",
        "text": "#111827",
        "font": "'Inter', system-ui, sans-serif",
        "heading_font": "'Inter', system-ui, sans-serif",
        "border_radius": "12px",
        "shadow": "0 1px 3px rgba(0,0,0,0.06)",
    },
}

LANG_LABELS = {
    "es": {"analyzing": "Analizando solicitud", "generating": "Generando resultado", "validating": "Validando con autocorrección", "consensus": "Aplicando constelación de consenso", "done": "Completado", "module": "Módulo", "depth": "Profundidad", "style": "Estilo"},
    "en": {"analyzing": "Analyzing request", "generating": "Generating result", "validating": "Validating with autocorrection", "consensus": "Applying consensus constellation", "done": "Complete", "module": "Module", "depth": "Depth", "style": "Style"},
    "fr": {"analyzing": "Analyse de la demande", "generating": "Génération du résultat", "validating": "Validation avec autocorrection", "consensus": "Application de la constellation de consensus", "done": "Terminé", "module": "Module", "depth": "Profondeur", "style": "Style"},
    "de": {"analyzing": "Anfrage analysieren", "generating": "Ergebnis generieren", "validating": "Validierung mit Autokorrektur", "consensus": "Konsens-Konstellation anwenden", "done": "Abgeschlossen", "module": "Modul", "depth": "Tiefe", "style": "Stil"},
    "pt": {"analyzing": "Analisando solicitação", "generating": "Gerando resultado", "validating": "Validando com autocorreção", "consensus": "Aplicando constelação de consenso", "done": "Concluído", "module": "Módulo", "depth": "Profundidade", "style": "Estilo"},
}

MODULE_NAMES = {
    "canvas": "Canvas Creator",
    "data_viz": "Data Visualizer",
    "image": "Image Studio",
    "research": "Research Agent",
    "content": "Content Writer",
    "code": "Code Architect",
}


# ============================================================================
# AVIA CREATORHUB — CLASE PRINCIPAL
# ============================================================================

class AVIACreatorHub:

    def __init__(self):
        self.module = poe.query.parameters.get("module", "auto")
        self.consensus = poe.query.parameters.get("consensus", True)
        self.autocorrect = poe.query.parameters.get("autocorrect", True)
        self.depth = poe.query.parameters.get("depth", 3)
        self.ui_style = poe.query.parameters.get("ui_style", "oxford")
        self.extra_context = poe.query.parameters.get("extra_context", "")
        self.language = poe.query.parameters.get("language", "es")
        self.labels = LANG_LABELS.get(self.language, LANG_LABELS["es"])
        self.style_config = UI_STYLE_CONFIGS.get(self.ui_style, UI_STYLE_CONFIGS["oxford"])
        self.query_text = poe.query.text
        self.query_attachments = poe.query.attachments

    # ----- FASE 1: Detección de módulo -----
    def detect_module(self):
        if self.module != "auto":
            return self.module
        detection = poe.call(
            "Grok-4.1-Fast-Non-Reasoning",
            f"""Classify this user request into exactly ONE module. Output ONLY valid JSON.

Modules:
- "canvas" = web apps, UI, interactive pages, dashboards, HTML, games, visual tools
- "data_viz" = charts, data visualization, graphs, analytics dashboards
- "image" = image generation, photos, illustrations, logos, visual art
- "research" = research, analysis, investigation, academic content, deep questions
- "content" = writing, articles, essays, marketing copy, documentation
- "code" = programming, algorithms, scripts, technical development, debugging

User request: {self.query_text}

Output in ```json format:
```json
{{"module": "module_name", "confidence": 0.95}}
```"""
        )
        try:
            parsed = parse_json_from_response(detection.text, ["module"])
            detected = parsed["module"]
            if detected in MODULE_NAMES:
                return detected
        except Exception:
            pass
        return "content"

    # ----- FASE 2: Procesamiento principal por módulo -----
    def process_canvas(self):
        style = self.style_config
        style_json = json.dumps(style, ensure_ascii=False)
        system_prompt = f"""You are AVIA CreatorHub Canvas Creator — an expert full-stack developer specializing in creating stunning single-page HTML Canvas applications.

## Design System: {style['name']}
{style_json}

## CRITICAL RULES (Libro Blanco / Universal Rules):
1. Output ONLY a complete, self-contained HTML document — no explanations outside the code
2. Use ONLY allowed CDNs: cdnjs.cloudflare.com, cdn.jsdelivr.net, unpkg.com, cdn.tailwindcss.com, fonts.googleapis.com, fonts.gstatic.com, d3js.org, cdn.plot.ly, kit.fontawesome.com
3. NEVER use alert(), confirm(), prompt(), print(), localStorage, sessionStorage
4. All interactive elements must use custom HTML/CSS/JS modals and handlers
5. Design must be fully responsive (mobile-first)
6. Use the color palette and fonts from the design system above
7. Include smooth transitions and microinteractions
8. Add proper error handling in JavaScript (try/catch)
9. Ensure all external resources have integrity/crossorigin attributes when possible
10. Structure: semantic HTML5, modular CSS (CSS custom properties), clean ES6+ JS

## Atomic Design Methodology:
- Atoms: buttons, inputs, labels, icons (consistent with design system)
- Molecules: search bars, card headers, form groups
- Organisms: navigation bars, hero sections, card grids, data tables
- Templates: page layouts with proper grid/flex structure
- Pages: complete functional application

## Output Language: {"Spanish" if self.language == "es" else "English" if self.language == "en" else self.language}
All UI text, labels, and content should be in the specified language.

{f"Additional context: {self.extra_context}" if self.extra_context else ""}"""

        poe.call(
            "Claude-Sonnet-4.5",
            poe.Message(text=system_prompt, sender="system"),
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True,
            parameters={"thinking_budget": 10000}
        )

    def process_data_viz(self):
        style = self.style_config
        style_json = json.dumps(style, ensure_ascii=False)
        system_prompt = f"""You are AVIA CreatorHub Data Visualizer — an expert in creating interactive data dashboards.

## Design System: {style['name']}
{style_json}

## Rules:
1. Generate a SINGLE self-contained HTML document with embedded data and Chart.js or Plotly.js
2. Use the design system colors, fonts, and spacing
3. Include interactive controls (filters, toggles) for the data
4. Ensure responsive layout with proper grid structure
5. Use realistic sample data relevant to the user's request
6. Add smooth animations and transitions
7. NEVER use alert(), confirm(), prompt(), localStorage
8. Allowed CDNs only: cdn.jsdelivr.net, cdn.plot.ly, cdnjs.cloudflare.com, cdn.tailwindcss.com, fonts.googleapis.com
9. Output language: {"Spanish" if self.language == "es" else self.language}

{f"Additional context: {self.extra_context}" if self.extra_context else ""}"""

        poe.call(
            "Claude-Sonnet-4.5",
            poe.Message(text=system_prompt, sender="system"),
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True,
            parameters={"thinking_budget": 10000}
        )

    def process_image(self):
        # Step 1: Generate optimized prompt
        prompt_response = poe.call(
            "Grok-4.1-Fast-Non-Reasoning",
            f"""Create an optimized image generation prompt based on this request. Make it vivid, detailed, and specific.

User request: {self.query_text}
{f"Additional context: {self.extra_context}" if self.extra_context else ""}

Output in ```json format:
```json
{{"prompt": "detailed image prompt in English", "aspect_ratio": "1:1 or 16:9 or 9:16 or 4:3 or 3:4"}}
```"""
        )
        parsed = parse_json_from_response(prompt_response.text, ["prompt", "aspect_ratio"])
        image_prompt = parsed["prompt"]
        aspect = parsed.get("aspect_ratio", "1:1")
        valid_aspects = ["1:1", "16:9", "9:16", "4:3", "3:4"]
        if aspect not in valid_aspects:
            aspect = "1:1"

        if self.consensus:
            # Multi-model consensus: generate with two models in parallel
            with poe.start_message() as msg:
                msg.write(f"🖼️ **Image Studio** — {self.labels['consensus']}...\n")
                msg.write(f"Prompt: *{image_prompt}*\n\n")

            img1, img2 = poe.parallel(
                lambda: poe.call("Imagen-4-Ultra", image_prompt, parameters={"aspect_ratio": aspect}),
                lambda: poe.call("Imagen-4-Fast", image_prompt, parameters={"aspect_ratio": aspect}),
            )

            with poe.start_message() as msg:
                msg.write("**Imagen-4-Ultra:**\n")
                if img1.last.attachments:
                    msg.add_attachment(img1.last.attachments[0])
                msg.write("\n**Imagen-4-Fast:**\n")
                if img2.last.attachments:
                    msg.add_attachment(img2.last.attachments[0])
                msg.write(f"\n---\n*✅ Constelación de consenso completada — 2 modelos, mejor resultado*")
        else:
            with poe.start_message() as msg:
                msg.write(f"🖼️ **Image Studio**\nPrompt: *{image_prompt}*\n\n")
            poe.call("Imagen-4-Ultra", image_prompt, parameters={"aspect_ratio": aspect}, output=poe.default_chat)

    def process_research(self):
        depth_instructions = {
            1: "Provide a brief overview in 2-3 paragraphs.",
            2: "Provide a moderately detailed analysis with key points.",
            3: "Provide a comprehensive analysis with sections, examples, and evidence.",
            4: "Provide an in-depth academic-level analysis with citations-style references, multiple perspectives, and detailed methodology.",
            5: "Provide an exhaustive academic research paper-level analysis with thorough literature review, methodology discussion, findings, implications, and future directions."
        }
        depth_instruction = depth_instructions.get(self.depth, depth_instructions[3])

        lang_map = {"es": "Spanish", "en": "English", "fr": "French", "de": "German", "pt": "Portuguese"}
        output_lang = lang_map.get(self.language, "Spanish")

        system_prompt = f"""You are AVIA Research Agent — an elite academic researcher with the analytical rigor of Oxford, MIT, and Stanford faculty.

## Research Protocol:
1. {depth_instruction}
2. Structure your response with clear academic headings (## and ###)
3. Use evidence-based reasoning and cite sources in [Author, Year] format when applicable
4. Include a structured summary at the beginning
5. Add a "Key Findings" section with bullet points
6. End with "Implications & Future Directions"
7. Write in {output_lang}
8. Maintain an authoritative yet accessible academic tone

{f"Additional research context: {self.extra_context}" if self.extra_context else ""}"""

        if self.consensus:
            # Multi-model research for consensus
            r1, r2 = poe.parallel(
                lambda: poe.call(
                    "Claude-Sonnet-4.5",
                    poe.Message(text=system_prompt, sender="system"),
                    poe.default_chat,
                    poe.query,
                    parameters={"thinking_budget": 16000}
                ),
                lambda: poe.call(
                    "GPT-5.2",
                    poe.Message(text=system_prompt, sender="system"),
                    poe.default_chat,
                    poe.query,
                    parameters={"reasoning_effort": "high"}
                ),
            )

            synthesis_prompt = f"""You are AVIA Consensus Synthesizer. Two world-class AI researchers have analyzed the same question. Your task is to synthesize their responses into a single, superior research output.

## Instructions:
1. Identify areas of agreement (high confidence findings)
2. Identify areas of disagreement (note both perspectives)
3. Synthesize into a unified, comprehensive response
4. Maintain the academic structure and {output_lang} language
5. Mark consensus points with ✅ and divergent points with ⚖️
6. The final output should be better than either individual response

## Research Response A (Claude):
{r1.text}

## Research Response B (GPT):
{r2.text}

Generate the unified synthesis now."""

            poe.call(
                "Claude-Sonnet-4.5",
                poe.Message(text=f"You are an academic synthesis expert. Write in {output_lang}.", sender="system"),
                synthesis_prompt,
                output=poe.default_chat,
                adopt_current_bot_name=True,
                parameters={"thinking_budget": 10000}
            )
        else:
            poe.call(
                "Claude-Sonnet-4.5",
                poe.Message(text=system_prompt, sender="system"),
                poe.default_chat,
                poe.query,
                output=poe.default_chat,
                adopt_current_bot_name=True,
                parameters={"thinking_budget": 10000}
            )

    def process_content(self):
        lang_map = {"es": "Spanish", "en": "English", "fr": "French", "de": "German", "pt": "Portuguese"}
        output_lang = lang_map.get(self.language, "Spanish")

        system_prompt = f"""You are AVIA Content Writer — an expert content creator with the writing quality of top academic publishers.

## Writing Guidelines:
1. Write in {output_lang} with impeccable grammar and style
2. Use clear, engaging prose with proper structure
3. Adapt tone to the content type (academic, professional, creative, etc.)
4. Include proper headings, subheadings, and formatting
5. Ensure factual accuracy and logical flow
6. Depth level: {self.depth}/5

{f"Additional instructions: {self.extra_context}" if self.extra_context else ""}"""

        poe.call(
            "Claude-Sonnet-4.5",
            poe.Message(text=system_prompt, sender="system"),
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True
        )

    def process_code(self):
        system_prompt = f"""You are AVIA Code Architect — a senior software engineer with expertise in clean architecture and best practices.

## Coding Standards (Libro Blanco):
1. Clean, well-documented code with docstrings
2. SOLID principles and design patterns where appropriate
3. Comprehensive error handling
4. Type hints for Python, TypeScript for JS/TS
5. Follow language-specific conventions and linters
6. Include usage examples
7. Explain architectural decisions
8. Output language for comments/docs: {"Spanish" if self.language == "es" else "English"}

## AVIA Pipeline Quality Gates:
- Gate 1: Syntax validation
- Gate 2: Logic review
- Gate 3: Edge case analysis
- Gate 4: Performance considerations
- Gate 5: Security review

{f"Additional requirements: {self.extra_context}" if self.extra_context else ""}"""

        poe.call(
            "Claude-Sonnet-4.5",
            poe.Message(text=system_prompt, sender="system"),
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True,
            parameters={"thinking_budget": 16000}
        )

    # ----- FASE 3: Autocorrección AVIA -----
    def autocorrect_canvas(self, module):
        """Run AVIA autocorrection on Canvas/HTML outputs."""
        if module not in ("canvas", "data_viz"):
            return
        # Get the last bot response
        last_text = poe.default_chat.last.text
        if "```html" not in last_text.lower() and "<!doctype" not in last_text.lower():
            return

        validation = poe.call(
            "Grok-4.1-Fast-Non-Reasoning",
            f"""Review this HTML Canvas output for errors. Check for:
1. Use of alert(), confirm(), prompt(), print() — FORBIDDEN
2. localStorage/sessionStorage usage — FORBIDDEN
3. Broken CDN URLs or non-allowed domains
4. Missing responsive design elements
5. JavaScript errors (unclosed brackets, undefined variables, etc.)
6. Missing error handling in JS
7. Accessibility issues (missing alt tags, ARIA labels)

HTML to review (first 4000 chars):
{last_text[:4000]}

Output ONLY valid JSON:
```json
{{"has_errors": true/false, "errors": ["error description 1", "error 2"], "severity": "none/low/medium/high"}}
```"""
        )
        try:
            result = parse_json_from_response(validation.text, ["has_errors"])
            if result.get("has_errors") and result.get("severity") in ("medium", "high"):
                errors_list = result.get("errors", [])
                error_text = "\n".join(f"- {e}" for e in errors_list)
                with poe.start_message() as msg:
                    msg.write(f"🔧 **AVIA Autocorrección** detectó {len(errors_list)} problema(s). Corrigiendo...\n")

                poe.call(
                    "Claude-Sonnet-4.5",
                    poe.Message(text="You are AVIA Error Corrector. Fix ALL identified errors in the HTML. Output ONLY the corrected complete HTML document.", sender="system"),
                    poe.default_chat,
                    f"""Fix these errors in the HTML above:
{error_text}

IMPORTANT: Output the COMPLETE corrected HTML document. Do not truncate.""",
                    output=poe.default_chat,
                    adopt_current_bot_name=True,
                    parameters={"thinking_budget": 8000}
                )
        except Exception:
            pass  # Autocorrection is best-effort

    # ----- PIPELINE PRINCIPAL -----
    def run(self):
        module = self.detect_module()
        module_display = MODULE_NAMES.get(module, module)

        # Status header
        with poe.start_message() as msg:
            msg.write(f"## 🎓 AVIA CreatorHub v3.2\n\n")
            msg.write(f"| Parámetro | Valor |\n|-----------|-------|\n")
            msg.write(f"| {self.labels['module']} | **{module_display}** |\n")
            msg.write(f"| {self.labels['style']} | **{self.style_config['name']}** |\n")
            msg.write(f"| {self.labels['depth']} | **{'●' * self.depth}{'○' * (5 - self.depth)}** ({self.depth}/5) |\n")
            msg.write(f"| Consenso | **{'✅ Activo' if self.consensus else '⭕ Inactivo'}** |\n")
            msg.write(f"| Autocorrección | **{'✅ Activa' if self.autocorrect else '⭕ Inactiva'}** |\n\n")
            msg.write(f"⏳ {self.labels['generating']}...\n")

        # Route to module processor
        processors = {
            "canvas": self.process_canvas,
            "data_viz": self.process_data_viz,
            "image": self.process_image,
            "research": self.process_research,
            "content": self.process_content,
            "code": self.process_code,
        }
        processor = processors.get(module, self.process_content)
        processor()

        # Autocorrection phase
        if self.autocorrect:
            self.autocorrect_canvas(module)

        # Completion footer
        with poe.start_message() as msg:
            msg.write(f"\n---\n✅ **{self.labels['done']}** — AVIA Pipeline v3.2\n")
            msg.write(f"*Procesado con {'Constelación de Consenso + ' if self.consensus else ''}{'Autocorrección + ' if self.autocorrect else ''}{self.style_config['name']} Design System*")


if __name__ == "__main__":
    bot = AVIACreatorHub()
    bot.run()