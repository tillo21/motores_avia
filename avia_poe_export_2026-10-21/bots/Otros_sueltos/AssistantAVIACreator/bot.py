# poe: name=AVIA-Assistant

import json
import re

class AVIAAssistant:
    """Bot asistente para AVIACreatorHub v4.0 - ayuda a usuarios a gestionar proyectos, tareas y funcionalidades de la aplicación."""

    def __init__(self):
        self.commands = {
            '/help': 'Muestra todos los comandos disponibles',
            '/dashboard': 'Abre el panel de control principal',
            '/tareas': 'Genera tareas con IA desde una descripción de proyecto',
            '/testing': 'Crea un plan de testing de usabilidad',
            '/temas': 'Explica cómo cambiar temas visuales',
            '/github': 'Información sobre la integración con GitHub',
            '/analytics': 'Información sobre el dashboard de analytics'
        }

    def run(self):
        # Detectar si es un comando específico
        query_text = poe.query.text.strip().lower()

        if query_text.startswith('/'):
            self.handle_command(query_text)
        elif any(word in query_text for word in ['tarea', 'proyecto', 'generar', 'organizar']):
            self.handle_task_generation()
        elif any(word in query_text for word in ['test', 'usabilidad', 'testing']):
            self.handle_testing_plan()
        elif any(word in query_text for word in ['tema', 'diseño', 'color', 'apariencia']):
            self.handle_theme_info()
        elif any(word in query_text for word in ['ayuda', 'qué puedes hacer', 'cómo funciona']):
            self.handle_help()
        else:
            # Consulta general - usar Claude para responder con contexto AVIA
            self.handle_general_query()

    def handle_command(self, command):
        """Procesa comandos específicos del sistema AVIA"""
        with poe.start_message() as msg:
            if command == '/help':
                msg.write("📚 **Comandos Disponibles en AVIA**\n\n")
                for cmd, desc in self.commands.items():
                    msg.write(f"• `{cmd}` - {desc}\n")
                msg.write("\n💡 **Tip**: También puedes hacerme preguntas en lenguaje natural sobre cómo usar AVIA.")

            elif command == '/dashboard':
                msg.write("📊 **Dashboard Principal de AVIA**\n\n")
                msg.write("El dashboard te permite:\n")
                msg.write("• Ver todos tus proyectos activos\n")
                msg.write("• Acceder rápidamente a módulos (Gestor de Tareas, Analytics, etc.)\n")
                msg.write("• Monitorear el estado del sistema\n")
                msg.write("• Ver tus logros y progreso\n\n")
                msg.write("🎯 **Cómo acceder**: Usa el botón QuickNav (esquina superior) y selecciona 'Test Dashboard'")

            elif command == '/tareas':
                msg.write("📋 **Generador de Tareas con IA**\n\n")
                msg.write("Esta herramienta te ayuda a desglosar proyectos complejos en tareas accionables.\n\n")
                msg.write("**Niveles de detalle:**\n")
                msg.write("• **Simple**: Lista básica de tareas\n")
                msg.write("• **Detallado**: Con sub-tareas y estimaciones\n\n")
                msg.write("💡 **Ejemplo de uso**: Describe tu proyecto (ej: 'Crear una app de e-commerce') y AVIA generará todas las tareas necesarias con prioridades y estimaciones de tiempo.")

            elif command == '/testing':
                msg.write("🧪 **Plan de Testing de Usabilidad**\n\n")
                msg.write("AVIA puede generar planes completos de testing que incluyen:\n")
                msg.write("• Perfiles de usuarios (personas)\n")
                msg.write("• Escenarios de uso\n")
                msg.write("• Tareas específicas a evaluar\n")
                msg.write("• Métricas de éxito\n\n")
                msg.write("📝 Solo necesitas describir tu producto/app y AVIA creará el plan completo.")

            elif command == '/temas':
                msg.write("🎨 **Temas Visuales de AVIA**\n\n")
                msg.write("Puedes cambiar la apariencia de AVIA entre 4 temas:\n\n")
                msg.write("• 🎬 **Cinematic Mode**: Profundidad y sombras cinematográficas\n")
                msg.write("• ✨ **Affective Gold**: Colores cálidos y emotivos\n")
                msg.write("• 🧘 **Minimal Zen**: Diseño minimalista y sereno\n")
                msg.write("• 🌙 **Dark AVIA**: Modo oscuro profesional\n\n")
                msg.write("🎯 **Cómo cambiar**: Usa QuickNav → 'Temas' o ejecuta `AVIAThemes.switch('nombre_tema')` en la consola")

            elif command == '/github':
                msg.write("🔗 **Integración con GitHub**\n\n")
                msg.write("AVIA incluye funcionalidades de GitHub para:\n")
                msg.write("• Auto-healing: Corrección automática de errores\n")
                msg.write("• Sincronización de proyectos\n")
                msg.write("• Control de versiones\n\n")
                msg.write("⚙️ **Configuración**: Usa el wizard de auto-healing desde QuickNav para conectar tu cuenta de GitHub")

            elif command == '/analytics':
                msg.write("📈 **Analytics Dashboard**\n\n")
                msg.write("El módulo de Analytics te proporciona:\n")
                msg.write("• Métricas de uso de la aplicación\n")
                msg.write("• Tiempo ahorrado con automatizaciones\n")
                msg.write("• Estadísticas visuales de productividad\n")
                msg.write("• Progreso de proyectos\n\n")
                msg.write("📊 Accede desde el Dashboard principal o QuickNav")

            else:
                msg.write(f"❌ Comando `{command}` no reconocido.\n\n")
                msg.write("Usa `/help` para ver todos los comandos disponibles.")

    def handle_task_generation(self):
        """Ayuda al usuario a generar tareas para un proyecto"""
        # Usar Claude para generar las tareas basándose en la descripción del usuario
        task_prompt = f"""Basándote en la siguiente descripción de proyecto, genera un desglose de tareas accionables en formato JSON.

Descripción del proyecto: {poe.query.text}

Genera una estructura con tareas principales, sub-tareas (si aplica), prioridad (alta/media/baja), y estimación de tiempo.

Formato JSON esperado:
```json
{{
  "proyecto": "nombre del proyecto",
  "tareas": [
    {{
      "id": 1,
      "titulo": "título de la tarea",
      "descripcion": "descripción detallada",
      "prioridad": "alta/media/baja",
      "estimacion": "tiempo estimado (ej: 2h, 1d)",
      "subtareas": ["sub-tarea 1", "sub-tarea 2"]
    }}
  ]
}}
```"""

        # Llamar a Claude para generar las tareas
        response = poe.call("Claude-Sonnet-4.5", task_prompt)

        # Parsear el JSON de la respuesta
        try:
            parsed = self.parse_json_from_response(response.text, ["proyecto", "tareas"])

            with poe.start_message() as msg:
                msg.write(f"📋 **Plan de Tareas: {parsed['proyecto']}**\n\n")
                msg.write(f"**Total de tareas**: {len(parsed['tareas'])}\n\n")

                for tarea in parsed['tareas']:
                    prioridad_emoji = {"alta": "🔴", "media": "🟡", "baja": "🟢"}.get(tarea['prioridad'].lower(), "⚪")
                    msg.write(f"### {prioridad_emoji} Tarea {tarea['id']}: {tarea['titulo']}\n")
                    msg.write(f"**Descripción**: {tarea['descripcion']}\n")
                    msg.write(f"**Prioridad**: {tarea['prioridad'].capitalize()} | **Estimación**: {tarea['estimacion']}\n")

                    if tarea.get('subtareas'):
                        msg.write(f"**Sub-tareas**:\n")
                        for subtarea in tarea['subtareas']:
                            msg.write(f"  ☐ {subtarea}\n")
                    msg.write("\n")

                msg.write("\n💡 **Tip**: Puedes copiar estas tareas directamente al Gestor de Tareas de AVIA.")

        except Exception as e:
            # Si falla el parseo, mostrar la respuesta completa de Claude
            poe.call("Claude-Sonnet-4.5", task_prompt, output=poe.default_chat)

    def handle_testing_plan(self):
        """Genera un plan de testing de usabilidad"""
        testing_prompt = f"""Basándote en la siguiente descripción, genera un plan completo de testing de usabilidad en formato JSON.

Descripción: {poe.query.text}

El plan debe incluir:
1. Perfiles de usuarios (personas) con contexto detallado
2. Escenarios de uso realistas
3. Tareas específicas a evaluar
4. Métricas de éxito

Formato JSON esperado:
```json
{{
  "producto": "nombre del producto",
  "usuarios": [
    {{
      "nombre": "nombre del persona",
      "edad": 30,
      "perfil": "descripción detallada del usuario",
      "objetivos": ["objetivo 1", "objetivo 2"]
    }}
  ],
  "escenarios": [
    {{
      "titulo": "título del escenario",
      "descripcion": "descripción del escenario",
      "tareas": ["tarea 1", "tarea 2"]
    }}
  ],
  "metricas": ["métrica 1", "métrica 2"]
}}
```"""

        response = poe.call("Claude-Sonnet-4.5", testing_prompt)

        try:
            parsed = self.parse_json_from_response(response.text, ["producto", "usuarios", "escenarios"])

            with poe.start_message() as msg:
                msg.write(f"🧪 **Plan de Testing: {parsed['producto']}**\n\n")

                # Usuarios/Personas
                msg.write("## 👥 Perfiles de Usuarios\n\n")
                for usuario in parsed['usuarios']:
                    msg.write(f"### {usuario['nombre']} ({usuario.get('edad', 'N/A')} años)\n")
                    msg.write(f"{usuario['perfil']}\n")
                    if usuario.get('objetivos'):
                        msg.write(f"**Objetivos**: {', '.join(usuario['objetivos'])}\n")
                    msg.write("\n")

                # Escenarios
                msg.write("## 📝 Escenarios de Uso\n\n")
                for i, escenario in enumerate(parsed['escenarios'], 1):
                    msg.write(f"### Escenario {i}: {escenario['titulo']}\n")
                    msg.write(f"{escenario['descripcion']}\n")
                    if escenario.get('tareas'):
                        msg.write(f"**Tareas a evaluar**:\n")
                        for tarea in escenario['tareas']:
                            msg.write(f"  • {tarea}\n")
                    msg.write("\n")

                # Métricas
                if parsed.get('metricas'):
                    msg.write("## 📊 Métricas de Éxito\n\n")
                    for metrica in parsed['metricas']:
                        msg.write(f"• {metrica}\n")

                msg.write("\n💡 **Tip**: Puedes usar este plan en el módulo de Testing de AVIA para ejecutar las pruebas.")

        except Exception as e:
            # Si falla el parseo, mostrar la respuesta completa
            poe.call("Claude-Sonnet-4.5", testing_prompt, output=poe.default_chat)

    def handle_theme_info(self):
        """Proporciona información sobre temas y personalización"""
        poe.call(
            "Claude-Sonnet-4.5",
            f"""El usuario está preguntando sobre temas/diseño/personalización en AVIACreatorHub v4.0.

Contexto de AVIA:
- AVIA tiene 4 temas visuales: Cinematic Mode, Affective Gold, Minimal Zen, y Dark AVIA
- Cada tema cambia colores, sombras y el aspecto general de la interfaz
- Se pueden cambiar desde QuickNav o usando AVIAThemes.switch('nombre_tema')

Pregunta del usuario: {poe.query.text}

Responde de manera útil y concisa, explicando cómo el usuario puede personalizar la apariencia de AVIA.""",
            output=poe.default_chat
        )

    def handle_help(self):
        """Muestra ayuda general sobre AVIA"""
        with poe.start_message() as msg:
            msg.write("👋 **Bienvenido al Asistente de AVIA**\n\n")
            msg.write("Soy tu asistente para **AVIACreatorHub v4.0**, un sistema de gestión de proyectos y tareas con IA.\n\n")
            msg.write("**¿Qué puedo hacer por ti?**\n\n")
            msg.write("• 📋 **Generar tareas**: Describe un proyecto y te ayudo a crear un plan de tareas detallado\n")
            msg.write("• 🧪 **Testing de usabilidad**: Creo planes completos de testing para tu producto\n")
            msg.write("• 🎨 **Personalización**: Te explico cómo cambiar temas y personalizar AVIA\n")
            msg.write("• 📊 **Análisis**: Información sobre métricas y analytics\n")
            msg.write("• 🔗 **Integración GitHub**: Ayuda con la configuración de GitHub\n\n")
            msg.write("**Comandos disponibles**: Escribe `/help` para ver todos los comandos.\n\n")
            msg.write("💬 **Pregúntame lo que necesites** en lenguaje natural. Por ejemplo:\n")
            msg.write("  - 'Quiero crear tareas para una app de finanzas'\n")
            msg.write("  - 'Necesito un plan de testing para mi sitio web'\n")
            msg.write("  - 'Cómo cambio el tema a modo oscuro?'\n")

    def handle_general_query(self):
        """Maneja consultas generales usando Claude con contexto de AVIA"""
        context = """Eres el asistente oficial de AVIACreatorHub v4.0, un sistema de gestión de proyectos y tareas con IA.

Funcionalidades principales de AVIA:
- Gestor de Tareas: Desglose de proyectos en tareas accionables con IA
- Analytics Dashboard: Métricas de uso, tiempo ahorrado, estadísticas
- Testing de Usabilidad: Generación de planes de testing completos
- Integración GitHub: Auto-healing y sincronización
- Sistema de Logros: Gamificación de productividad
- Temas Visuales: 4 modos (Cinematic, Gold, Zen, Dark)
- QuickNav: Panel de navegación rápida
- HUD Cognitivo: Información del sistema en tiempo real

Comandos disponibles:
/help - Ayuda general
/dashboard - Panel de control
/tareas - Generador de tareas
/testing - Testing de usabilidad
/temas - Información sobre temas visuales
/github - Integración GitHub
/analytics - Dashboard de analytics"""

        poe.call(
            "Claude-Sonnet-4.5",
            poe.Message(text=context, sender="system"),
            f"Pregunta del usuario: {poe.query.text}\n\nResponde de manera útil, concisa y contextualizada a AVIA. Si la pregunta no está relacionada con AVIA, responde de manera general pero amigable.",
            output=poe.default_chat,
            adopt_current_bot_name=True
        )

    def parse_json_from_response(self, response_text, required_fields=None):
        """Extrae y parsea JSON de la respuesta del bot"""
        # Intentar encontrar bloque ```json primero
        match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
        else:
            # Buscar objeto JSON en cualquier parte de la respuesta
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                json_str = match.group(0).strip()
            else:
                raise Exception(f"No se encontró JSON en la respuesta\n{response_text}")

        try:
            parsed = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise Exception(f"Error al parsear JSON: {e}\nJSON string: {json_str}")

        if required_fields:
            missing_fields = set(required_fields) - set(parsed.keys())
            if missing_fields:
                raise Exception(f"Faltan campos requeridos: {', '.join(missing_fields)}")

        return parsed

if __name__ == "__main__":
    bot = AVIAAssistant()
    bot.run()