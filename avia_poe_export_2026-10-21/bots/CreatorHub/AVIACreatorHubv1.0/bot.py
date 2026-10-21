# poe: name=AVIA-Task-Manager

import json
import re
from datetime import datetime

# In-memory task storage (persists during conversation)
TASKS_DB = {
    "project": "AVIACreatorHub",
    "version": "4.0",
    "tasks": [],
    "last_updated": None
}

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
            raise Exception(f"Could not find JSON in response")

    parsed = json.loads(json_str)
    if required_fields:
        missing = set(required_fields) - set(parsed.keys())
        if missing:
            raise Exception(f"Missing required fields: {', '.join(missing)}")
    return parsed


def get_task_by_id(task_id):
    """Find a task by its ID."""
    for task in TASKS_DB["tasks"]:
        if task["id"].upper() == task_id.upper():
            return task
    return None


def generate_progress_bar(percentage):
    """Generate a visual progress bar."""
    filled = int(percentage / 5)
    empty = 20 - filled
    return f"[{'█' * filled}{'░' * empty}] {percentage}%"


def format_status_icon(status):
    """Return icon based on status."""
    icons = {
        "completada": "✅",
        "en_progreso": "🔄",
        "pendiente": "⏳",
        "bloqueada": "🔒",
        "desbloqueada": "🔓",
        "aprobada": "✅"
    }
    return icons.get(status.lower(), "📌")


class AVIATaskManager:
    def _fallback_intent(self, text):
        """Regex fallback when NLP bot is unavailable (AVIA Autocorrección #005)."""
        lower = text.lower()
        task_id_match = re.search(r'T-[\d.]+', text, re.IGNORECASE)
        task_id = task_id_match.group(0).upper() if task_id_match else None

        # Detect intent from keywords
        if any(kw in lower for kw in ['agregar', 'añadir', 'crear', 'nueva', 'add', 'new']):
            title_match = re.search(r'(?:tarea[:\s]+|crear[:\s]+|add[:\s]+)(.+?)(?:\s+prioridad|\s+asignad|$)', text, re.IGNORECASE)
            return {"intent": "add", "task_id": task_id, "task_title": title_match.group(1).strip() if title_match else "Nueva tarea",
                    "new_status": None, "new_progress": None, "priority": None, "assignee": None}
        elif any(kw in lower for kw in ['actualizar', 'update', 'cambiar', 'marcar', 'progreso']):
            status = None
            for s in ['completada', 'en_progreso', 'pendiente', 'bloqueada']:
                if s in lower: status = s; break
            progress_match = re.search(r'(\d+)\s*%', text)
            return {"intent": "update", "task_id": task_id, "task_title": None,
                    "new_status": status, "new_progress": progress_match.group(1) if progress_match else None, "priority": None, "assignee": None}
        elif any(kw in lower for kw in ['listar', 'mostrar', 'ver', 'list', 'show', 'todas']):
            return {"intent": "list", "task_id": task_id, "task_title": None, "new_status": None, "new_progress": None, "priority": None, "assignee": None}
        elif any(kw in lower for kw in ['reporte', 'report', 'resumen', 'informe']):
            return {"intent": "report", "task_id": None, "task_title": None, "new_status": None, "new_progress": None, "priority": None, "assignee": None}
        elif any(kw in lower for kw in ['eliminar', 'delete', 'borrar', 'quitar']):
            return {"intent": "delete", "task_id": task_id, "task_title": None, "new_status": None, "new_progress": None, "priority": None, "assignee": None}
        elif any(kw in lower for kw in ['exportar', 'export', 'json', 'descargar']):
            return {"intent": "export", "task_id": None, "task_title": None, "new_status": None, "new_progress": None, "priority": None, "assignee": None}
        return {"intent": "help"}

    def run(self):
        global TASKS_DB

        user_input = poe.query.text.strip()

        # Use LLM to understand user intent (with API error fallback)
        NLP_BOT = "Grok-4.1-Fast-Non-Reasoning"
        try:
            intent_response = poe.call(NLP_BOT, f"""Analyze this task manager command and extract the intent.

Valid intents:
- "add": Add a new task
- "update": Update an existing task's status or progress
- "list": List/show all tasks or specific tasks
- "report": Generate a progress report
- "delete": Remove a task
- "help": Show help/instructions
- "export": Export tasks as JSON

Output in ```json format:
```json
{{
    "intent": "the_intent",
    "task_id": "task ID if mentioned (e.g., T-000.1), null otherwise",
    "task_title": "task title if adding new task, null otherwise",
    "new_status": "new status if updating (pendiente/en_progreso/completada/bloqueada), null otherwise",
    "new_progress": "progress percentage 0-100 if mentioned, null otherwise",
    "priority": "alta/media/baja if mentioned, null otherwise",
    "assignee": "person assigned if mentioned, null otherwise"
}}
```

User command: {user_input}""")
            intent_data = parse_json_from_response(intent_response.text, ["intent"])
        except Exception:
            # Fallback: regex-based intent detection when API fails
            intent_data = self._fallback_intent(user_input)

        intent = intent_data.get("intent", "help")

        intent = intent_data.get("intent", "help")

        # Extract task ID directly from user input if LLM missed it
        task_id_match = re.search(r'T-[\d.]+', user_input, re.IGNORECASE)
        if task_id_match and not intent_data.get("task_id"):
            intent_data["task_id"] = task_id_match.group(0).upper()

        with poe.start_message() as msg:
            if intent == "add":
                # Add new task - use extracted ID or generate one
                task_id = intent_data.get("task_id") or f"T-{len(TASKS_DB['tasks'])+1:03d}"

                # Extract title from user input if LLM missed it
                title = intent_data.get("task_title")
                if not title or title == "Nueva tarea":
                    # Try to extract title after task ID or after colon
                    title_match = re.search(r'(?:T-[\d.]+[:\s]+|tarea[:\s]+)(.+?)(?:\s+prioridad|\s+asignad|$)', user_input, re.IGNORECASE)
                    if title_match:
                        title = title_match.group(1).strip()
                    else:
                        title = "Nueva tarea"
                new_task = {
                    "id": task_id,
                    "title": title,
                    "status": intent_data.get("new_status") or "pendiente",
                    "progress": int(intent_data.get("new_progress") or 0),
                    "priority": intent_data.get("priority") or "media",
                    "assignee": intent_data.get("assignee") or "Sin asignar",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "updated": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                TASKS_DB["tasks"].append(new_task)
                TASKS_DB["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

                msg.write(f"""╔═══════════════════════════════════════════════════════════════╗
║  ✅ TAREA AGREGADA EXITOSAMENTE                                ║
╠═══════════════════════════════════════════════════════════════╣
║  ID: {new_task['id']:<54}║
║  Título: {new_task['title']:<50}║
║  Estado: {new_task['status']:<50}║
║  Prioridad: {new_task['priority']:<47}║
║  Asignado a: {new_task['assignee']:<46}║
╚═══════════════════════════════════════════════════════════════╝
""")

            elif intent == "update":
                task_id = intent_data.get("task_id")
                if not task_id:
                    msg.write("⚠️ Por favor especifica el ID de la tarea a actualizar.\n")
                    msg.write("Ejemplo: `Actualizar T-000.1 a completada 100%`")
                else:
                    task = get_task_by_id(task_id)
                    if task:
                        if intent_data.get("new_status"):
                            task["status"] = intent_data["new_status"]
                        if intent_data.get("new_progress"):
                            task["progress"] = int(intent_data["new_progress"])
                        if intent_data.get("assignee"):
                            task["assignee"] = intent_data["assignee"]
                        task["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        TASKS_DB["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

                        icon = format_status_icon(task["status"])
                        msg.write(f"""╔═══════════════════════════════════════════════════════════════╗
║  🔄 TAREA ACTUALIZADA                                          ║
╠═══════════════════════════════════════════════════════════════╣
║  {task['id']}  {generate_progress_bar(task['progress'])} {icon}
║  {task['title']:<58}║
║  Estado: {task['status']:<50}║
║  Asignado: {task['assignee']:<48}║
╚═══════════════════════════════════════════════════════════════╝
""")
                    else:
                        msg.write(f"❌ No se encontró la tarea con ID: {task_id}")

            elif intent == "list":
                if not TASKS_DB["tasks"]:
                    msg.write("""╔═══════════════════════════════════════════════════════════════╗
║  📋 GESTOR DE TAREAS - AVIACreatorHub 4.0                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📭 No hay tareas registradas aún.                            ║
║                                                               ║
║  Usa comandos como:                                           ║
║  • "Agregar tarea: Configurar Dashboard"                      ║
║  • "Nueva tarea T-000.2 Diseñar interfaz"                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
                else:
                    msg.write("""╔═══════════════════════════════════════════════════════════════╗
║  📋 GESTOR DE TAREAS - AVIACreatorHub 4.0                      ║
╠═══════════════════════════════════════════════════════════════╣
""")
                    for task in TASKS_DB["tasks"]:
                        icon = format_status_icon(task["status"])
                        bar = generate_progress_bar(task["progress"])
                        msg.write(f"║  {task['id']}  {bar} {icon}\n")
                        msg.write(f"║  └─ {task['title'][:50]:<50}  ║\n")

                    # Calculate overall progress
                    total = len(TASKS_DB["tasks"])
                    completed = sum(1 for t in TASKS_DB["tasks"] if t["status"] == "completada")
                    overall = int((completed / total) * 100) if total > 0 else 0

                    msg.write(f"""╠═══════════════════════════════════════════════════════════════╣
║  📊 Progreso General: {generate_progress_bar(overall):<36} ║
║  Última actualización: {TASKS_DB.get('last_updated', 'N/A'):<35}║
╚═══════════════════════════════════════════════════════════════╝
""")

            elif intent == "report":
                total = len(TASKS_DB["tasks"])
                if total == 0:
                    msg.write("📊 No hay tareas para generar reporte. Agrega tareas primero.")
                else:
                    completed = sum(1 for t in TASKS_DB["tasks"] if t["status"] == "completada")
                    in_progress = sum(1 for t in TASKS_DB["tasks"] if t["status"] == "en_progreso")
                    pending = sum(1 for t in TASKS_DB["tasks"] if t["status"] == "pendiente")
                    blocked = sum(1 for t in TASKS_DB["tasks"] if t["status"] == "bloqueada")

                    msg.write(f"""╔═══════════════════════════════════════════════════════════════╗
║  📊 REPORTE DE PROGRESO - AVIACreatorHub 4.0                   ║
║  Generado: {datetime.now().strftime("%Y-%m-%d %H:%M"):<48}║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📈 RESUMEN ESTADÍSTICO                                       ║
║  ─────────────────────────────────────────────────────────    ║
║  Total de tareas:     {total:<5}                                  ║
║  ✅ Completadas:      {completed:<5} ({int(completed/total*100) if total else 0}%)                              ║
║  🔄 En progreso:      {in_progress:<5} ({int(in_progress/total*100) if total else 0}%)                              ║
║  ⏳ Pendientes:       {pending:<5} ({int(pending/total*100) if total else 0}%)                              ║
║  🔒 Bloqueadas:       {blocked:<5} ({int(blocked/total*100) if total else 0}%)                              ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  📋 DETALLE POR TAREA                                         ║
║  ─────────────────────────────────────────────────────────    ║
""")
                    for task in TASKS_DB["tasks"]:
                        icon = format_status_icon(task["status"])
                        msg.write(f"║  {icon} {task['id']}: {task['title'][:40]:<40}    ║\n")
                        msg.write(f"║     Progreso: {task['progress']}% | Asignado: {task['assignee'][:20]:<20} ║\n")

                    msg.write("""╚═══════════════════════════════════════════════════════════════╝
""")

            elif intent == "export":
                export_data = json.dumps(TASKS_DB, indent=2, ensure_ascii=False)
                msg.write(f"""📦 **EXPORTACIÓN DE DATOS**

```json
{export_data}
```

✅ Puedes copiar este JSON para sincronización manual con otros sistemas.
""")

            elif intent == "delete":
                task_id = intent_data.get("task_id")
                if not task_id:
                    msg.write("⚠️ Especifica el ID de la tarea a eliminar.\nEjemplo: `Eliminar T-001`")
                else:
                    task = get_task_by_id(task_id)
                    if task:
                        TASKS_DB["tasks"].remove(task)
                        TASKS_DB["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        msg.write(f"🗑️ Tarea **{task_id}** eliminada correctamente.")
                    else:
                        msg.write(f"❌ No se encontró la tarea: {task_id}")

            else:  # help
                msg.write("""╔═══════════════════════════════════════════════════════════════╗
║  📚 AVIA TASK MANAGER - GUÍA DE USO                            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📝 COMANDOS DISPONIBLES                                      ║
║  ─────────────────────────────────────────────────────────    ║
║                                                               ║
║  ➕ AGREGAR TAREAS                                            ║
║     • "Agregar tarea: Configurar Dashboard"                   ║
║     • "Nueva tarea T-000.2 Diseñar interfaz prioridad alta"   ║
║     • "Crear tarea para @Juan: Revisar código"                ║
║                                                               ║
║  🔄 ACTUALIZAR TAREAS                                         ║
║     • "Actualizar T-000.1 a completada 100%"                  ║
║     • "T-000.2 en progreso 50%"                               ║
║     • "Marcar T-001 como bloqueada"                           ║
║                                                               ║
║  📋 VER TAREAS                                                ║
║     • "Listar tareas" / "Mostrar todas"                       ║
║     • "Ver estado del proyecto"                               ║
║                                                               ║
║  📊 REPORTES                                                  ║
║     • "Generar reporte" / "Dame el reporte de progreso"       ║
║                                                               ║
║  📦 EXPORTAR                                                  ║
║     • "Exportar tareas" / "Exportar JSON"                     ║
║                                                               ║
║  🗑️ ELIMINAR                                                  ║
║     • "Eliminar T-001"                                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    bot = AVIATaskManager()
    bot.run()