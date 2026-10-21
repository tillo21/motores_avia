# poe: name=AVIA-Manager

from fastapi_poe.types import SettingsResponse

poe.update_settings(SettingsResponse(
    introduction_message=(
        "\U0001F30C **AVIA Manager** \u2014 Gestor Permanente del Ecosistema AVIA Senior\n\n"
        "Soy tu bot dedicado para gestionar AVIA Senior sin errores. Comandos:\n\n"
        "\U0001F4CE **Adjunta tu HTML** + escribe qu\u00E9 quieres hacer:\n"
        "- `auditar` \u2014 Auditor\u00EDa at\u00F3mica completa (R1-R12)\n"
        "- `fix [descripci\u00F3n]` \u2014 Aplicar correcci\u00F3n espec\u00EDfica\n"
        "- `estado` \u2014 Verificar salud del sistema\n"
        "- `entregar` \u2014 Canvas preview + HTML descargable (R12)\n"
        "- Cualquier otra instrucci\u00F3n libre\n\n"
        "\u26A1 Anti-crash: retry autom\u00E1tico, scripts modulares, sin timeouts."
    ),
    allow_attachments=True,
    expand_text_attachments=True,
    enable_image_comprehension=True,
))


class AVIAManager:
    """Dedicated AVIA Senior management bot with robust error handling."""

    MAX_RETRIES = 2
    # Rules R1-R12 as system context for the LLM
    RULES_CONTEXT = (
        "REGLAS UNIVERSALES AVIA Senior (R1-R12):\n"
        "R1: ZERO non-ASCII in <script> - use \\uXXXX escapes\n"
        "R2: ZERO spread operators - use Array.prototype.slice.call(x)\n"
        "R3: No optional chaining ?.\n"
        "R4: No nullish coalescing ??\n"
        "R5: No template literals (backticks)\n"
        "R6: No arrow functions =>\n"
        "R7: No const/let - use var\n"
        "R8: No destructuring\n"
        "R9: No for...of\n"
        "R10: No async/await\n"
        "R11: CDN libs must be ES5 compatible (D3 <= v5, marked <= v4)\n"
        "R12: Doble Entrega - Canvas preview (<50KB) + full HTML attachment\n\n"
        "ARQUITECTURA: Capas aditivas v3.2 (sagrada) -> v4.3. "
        "Cada capa: <style>+<script> IIFE. Init escalonado +400ms. "
        "Nunca modificar v3.2 base. Wrapper Pattern para overrides."
    )

    def __init__(self):
        self.query_text = poe.query.text.strip().lower()
        self.has_attachment = len(poe.query.attachments) > 0

    def run(self):
        """Main entry point with automatic error recovery."""
        try:
            self._dispatch()
        except poe.BotError:
            raise  # Let BotError propagate to show user-friendly message
        except Exception as e:
            self._handle_error(e)

    def _dispatch(self):
        """Route to the right handler based on user command."""
        q = self.query_text

        if q.startswith("estado") or q.startswith("status"):
            self._cmd_estado()
        elif q.startswith("auditar") or q.startswith("audit"):
            self._cmd_auditar()
        elif q.startswith("fix") or q.startswith("corregir") or q.startswith("corrige"):
            self._cmd_fix()
        elif q.startswith("entregar") or q.startswith("deliver"):
            self._cmd_entregar()
        else:
            # Free-form instruction -> delegate to Claude with full context
            self._cmd_freeform()

    def _call_with_retry(self, bot, *prompts, **kwargs):
        """Call a bot with automatic retry on failure."""
        last_err = None
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                return poe.call(bot, *prompts, **kwargs)
            except Exception as e:
                last_err = e
                if attempt < self.MAX_RETRIES:
                    with poe.start_message() as msg:
                        msg.write(
                            "\u26A0\uFE0F Reintento "
                            + str(attempt + 1)
                            + "/"
                            + str(self.MAX_RETRIES)
                            + "...\n"
                        )
        raise last_err

    def _get_html_context(self):
        """Extract HTML content from attachment or conversation for analysis."""
        if self.has_attachment:
            att = poe.query.attachments[0]
            try:
                content = att.get_contents().decode("utf-8", errors="replace")
                # Truncate for LLM context if needed (keep first + last sections)
                if len(content) > 80000:
                    head = content[:40000]
                    tail = content[-40000:]
                    return (
                        head
                        + "\n\n[... "
                        + str(len(content) - 80000)
                        + " chars truncated ...]\n\n"
                        + tail
                    )
                return content
            except Exception:
                return "[Error reading attachment]"
        return "[No HTML attachment provided]"

    # ==================== COMMANDS ====================

    def _cmd_estado(self):
        """Health check - verify system status."""
        html = self._get_html_context()

        checks = []
        # R1-R11 quick checks
        r1_ok = "=>" not in html.split("<script")[-1] if "<script" in html else True
        checks.append(("R6 Arrow Functions", r1_ok))

        has_const = "const " in html.split("<script")[-1] if "<script" in html else False
        checks.append(("R7 const/let", not has_const))

        has_d3v5 = "d3@5" in html or "d3.v5" in html or "d3/5" in html
        checks.append(("R11 D3 v5", has_d3v5 or "d3" not in html.lower()))

        has_close = "close" in html.lower() or "times" in html.lower() or "&times;" in html
        checks.append(("Close Buttons", has_close))

        total = len(checks)
        passed = sum(1 for _, ok in checks if ok)

        with poe.start_message() as msg:
            msg.write("## \U0001F3E5 Estado del Sistema AVIA\n\n")
            msg.write("| Check | Estado |\n|---|---|\n")
            for name, ok in checks:
                icon = "\u2705" if ok else "\u274C"
                msg.write("| " + name + " | " + icon + " |\n")
            msg.write("\n**Resultado:** " + str(passed) + "/" + str(total) + " checks OK\n\n")

            if self.has_attachment:
                lines = html.count("\n") + 1
                size_kb = len(html.encode("utf-8")) / 1024
                msg.write("**Archivo:** " + str(lines) + " l\u00EDneas, " + str(round(size_kb, 1)) + " KB\n")
            else:
                msg.write("\u26A0\uFE0F Adjunta tu HTML para un an\u00E1lisis completo.\n")

    def _cmd_auditar(self):
        """Full atomic audit using Claude."""
        if not self.has_attachment:
            raise poe.BotError(
                "Adjunta el archivo HTML para auditar.\n"
                "Ejemplo: arrastra avia_senior_v41.html y escribe 'auditar'"
            )

        html = self._get_html_context()

        with poe.start_message() as msg:
            msg.write("\U0001F50D Auditando con Constelaci\u00F3n de Consenso...\n")

        system = poe.Message(
            text=(
                "Eres el auditor AVIA Senior. "
                + self.RULES_CONTEXT
                + "\n\nRealiza una auditor\u00EDa at\u00F3mica completa del HTML proporcionado. "
                "Estructura tu respuesta as\u00ED:\n"
                "1. **Resumen**: N errores encontrados\n"
                "2. **Violaciones R1-R12**: Lista cada violaci\u00F3n con l\u00EDnea y fix\n"
                "3. **Botones/Paneles**: Verificar que todos tengan bot\u00F3n X cerrar\n"
                "4. **IDs rotos**: getElementById que no matchean\n"
                "5. **Plan de acci\u00F3n**: Pasos priorizados\n"
                "Responde en espa\u00F1ol, conciso, con tablas markdown."
            ),
            sender="system",
        )

        self._call_with_retry(
            "Claude-Sonnet-4",
            system,
            poe.default_chat,
            "Audita este HTML:\n\n" + html[:60000],
            output=poe.default_chat,
            adopt_current_bot_name=True,
        )

    def _cmd_fix(self):
        """Apply specific fix using Claude."""
        if not self.has_attachment:
            raise poe.BotError(
                "Adjunta el archivo HTML + describe el fix.\n"
                "Ejemplo: arrastra el HTML y escribe 'fix BOE API timeout'"
            )

        html = self._get_html_context()
        user_instruction = poe.query.text.strip()

        system = poe.Message(
            text=(
                "Eres el fixer AVIA Senior. "
                + self.RULES_CONTEXT
                + "\n\nEl usuario quiere aplicar un fix. "
                "Genera SOLO el c\u00F3digo corregido necesario (no el HTML completo). "
                "Muestra: (1) qu\u00E9 cambiar, (2) d\u00F3nde, (3) el c\u00F3digo exacto. "
                "TODO el JS debe ser ES5 puro. Responde en espa\u00F1ol."
            ),
            sender="system",
        )

        self._call_with_retry(
            "Claude-Sonnet-4",
            system,
            poe.default_chat,
            "Instrucci\u00F3n: " + user_instruction + "\n\nHTML actual:\n\n" + html[:60000],
            output=poe.default_chat,
            adopt_current_bot_name=True,
        )

    def _cmd_entregar(self):
        """R12 delivery - Canvas preview + download attachment."""
        if not self.has_attachment:
            raise poe.BotError(
                "Adjunta el archivo HTML para entregar.\n"
                "Ejemplo: arrastra el HTML y escribe 'entregar'"
            )

        att = poe.query.attachments[0]

        with poe.start_message() as msg:
            msg.write("## \U0001F680 Entrega R12\n\n")
            msg.write("\U0001F4CE **Archivo recibido:** " + att.name + "\n\n")
            msg.write(
                "\U0001F4E5 **Descarga directa:** ["
                + att.name
                + "]("
                + (att.url or "")
                + ")\n\n"
            )
            msg.write("**Instrucciones:**\n")
            msg.write("1. Descarga el archivo HTML\n")
            msg.write("2. \u00C1brelo en Chrome/Firefox/Safari\n")
            msg.write("3. Bot\u00F3n rojo (esquina sup. izq.) \u2192 Dashboard Unificado\n")
            msg.write("4. Sidebar izquierdo \u2192 Dashboard y Navegaci\u00F3n\n")
            msg.write("5. Bot\u00F3n Exportar \u2192 HTML standalone para Genially\n\n")
            msg.write(
                "\u26A0\uFE0F **Nota:** El Canvas de Poe no puede renderizar archivos >50KB. "
                "Usa siempre la descarga directa para probar la app completa."
            )

    def _cmd_freeform(self):
        """Handle any free-form instruction about AVIA."""
        html_context = ""
        if self.has_attachment:
            html_context = (
                "\n\nEl usuario ha adjuntado un HTML. Primeras l\u00EDneas:\n"
                + self._get_html_context()[:30000]
            )

        system = poe.Message(
            text=(
                "Eres AVIA Manager, el gestor del ecosistema AVIA Senior. "
                + self.RULES_CONTEXT
                + "\n\nResponde a la instrucci\u00F3n del usuario sobre AVIA Senior. "
                "Si necesitas generar c\u00F3digo, SIEMPRE cumple R1-R12. "
                "Responde en espa\u00F1ol, conciso y \u00FAtil."
                + html_context
            ),
            sender="system",
        )

        self._call_with_retry(
            "Claude-Sonnet-4",
            system,
            poe.default_chat,
            poe.query,
            output=poe.default_chat,
            adopt_current_bot_name=True,
        )

    def _handle_error(self, error):
        """Graceful error handling - never crash."""
        error_msg = str(error)
        with poe.start_message() as msg:
            msg.write("## \u26A0\uFE0F Error Capturado\n\n")
            msg.write("**Tipo:** " + type(error).__name__ + "\n")
            msg.write("**Detalle:** " + error_msg[:500] + "\n\n")
            msg.write("**Soluci\u00F3n autom\u00E1tica:**\n")
            if "timeout" in error_msg.lower() or "time" in error_msg.lower():
                msg.write("- El archivo es muy grande. Intenta con un fragmento menor.\n")
                msg.write("- Usa el comando `estado` sin adjunto para un check r\u00E1pido.\n")
            elif "attachment" in error_msg.lower():
                msg.write("- Adjunta el archivo HTML arrastr\u00E1ndolo al chat.\n")
            else:
                msg.write("- Intenta de nuevo. Si persiste, inicia un chat nuevo.\n")
                msg.write("- El contexto acumulado puede causar errores \u2014 un chat limpio lo resuelve.\n")


if __name__ == "__main__":
    bot = AVIAManager()
    bot.run()