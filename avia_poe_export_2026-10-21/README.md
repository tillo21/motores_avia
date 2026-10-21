# Exportación de bots AVIA desde Poe

Cuenta: @carlosdecastrol · Fecha: 21 de octubre de 2026 · 874 bots

## Qué hay aquí

- `catalogo.html` — ábrelo en el navegador: buscador, filtros por tipo y modelo, agrupado por familias, con la última versión marcada y las copias idénticas ocultas.
- `catalogo.csv` — la misma información para Excel o Sheets (separador punto y coma).
- `instrucciones_para_api.jsonl` — los 132 bots de instrucciones con su modelo base y su prompt, una línea por bot, listos para usarse como system prompt con cualquier API compatible con OpenAI.
- `bots/<familia>/<bot>/` — una carpeta por bot: `config.json` (nombre, tipo, modelo base, privacidad, temperatura, descripción, enlaces) y `index.html` (Canvas), `prompt.md` (instrucciones) o `bot.py` (scripts); `bienvenida.md` si hay mensaje de bienvenida.

No se exportó ninguna clave: la clave de servidor que Poe guarda para cada bot queda fuera.

## Resumen

| Tipo | Bots |
| --- | --- |
| canvas | 710 |
| instrucciones | 132 |
| script | 27 |
| imagen | 4 |
| video | 1 |

Familias (agrupadas por nombre; "última" = la creada más recientemente, no necesariamente la mejor):

| Familia | Bots |
| --- | --- |
| Otros (sueltos) | 181 |
| AVIA Senior | 63 |
| CreatorHub | 51 |
| Profesor / educación | 42 |
| SIESTA / SiestaOTT | 41 |
| Turismo y gastronomía Córdoba | 32 |
| Auditor | 31 |
| Gemelo digital | 28 |
| TOOC | 27 |
| CreatorHub Video | 25 |
| VideoLab y vídeo | 25 |
| ControlNextMedIA | 23 |
| Productivity / Design / Mockups | 19 |
| AVIA Hub | 19 |
| IICA y agro | 17 |
| AVIA Nómada | 17 |
| Gestión de proyectos | 16 |
| Constelación AVIA | 15 |
| Bocatti y mapas | 14 |
| AVIA Studio | 14 |
| DIADA | 13 |
| Cáncer y salud | 13 |
| LEID Player y transcripción | 13 |
| Don Simón / García Carrión | 12 |
| SIMPLIT y accesibilidad | 11 |
| Motor de emociones | 9 |
| Orquesta de agentes | 9 |
| Bots de scripts de prueba | 9 |
| AVIA Nexus | 7 |
| Caverna de Platón | 7 |
| AVIA Protocol / AgentOS | 6 |
| Mapa de empatía María | 6 |
| AVIA System | 6 |
| Libro Chispa / Jaima | 6 |
| Pipeline | 5 |
| Eliminar fondos y objetos | 5 |
| AVIA Clon de Carlos | 4 |
| AVIA ODA | 4 |
| AVIA Dashboard | 4 |
| AVIA Autor | 3 |
| Constelación cine | 3 |
| XynapxAI | 3 |
| AVIA-Proyecto | 2 |
| AVIA Care | 2 |
| AVIA Carta Astral | 2 |
| Leonel Fernández | 2 |
| Inscripción UCLM | 2 |
| Lucía fiscal | 2 |
| Procesar docs grandes | 2 |
| Tesis AM | 2 |

## Cómo usarlos fuera de Poe

**Aplicaciones Canvas (index.html).** Se abren en cualquier navegador. Las marcadas como "usa API de Poe" llaman a window.Poe.sendUserMessage: hay que cambiar esas llamadas por una API propia (por ejemplo el enrutador AVIA o la API de Poe a través de un servidor; nunca con la clave dentro del HTML).

**Bots de instrucciones (prompt.md).** El prompt es el system prompt:

```python
import json, openai
bots = [json.loads(l) for l in open("instrucciones_para_api.jsonl", encoding="utf-8")]
bot = next(b for b in bots if b["bot"] == "AVIA-Proyecto")
client = openai.OpenAI(base_url="https://api.poe.com/v1", api_key="TU_CLAVE")
r = client.chat.completions.create(model=bot["modelo_base_en_poe"],
      messages=[{"role": "system", "content": bot["system_prompt"]}, {"role": "user", "content": "Hola"}])
print(r.choices[0].message.content)
```

**Bots de scripts (bot.py).** Código Python con fastapi_poe; fuera de Poe se ejecutan como server bot propio.

## Avisos

- Las familias se asignaron por reglas sobre el nombre; algunas pueden estar mal agrupadas. "Otros (sueltos)" reúne los bots sin familia clara.
- El "estado" sale de tus notas en la descripción (ok, error, final…), no de una prueba real.
- Algunos modelos base están obsoletos en Poe (p. ej. Mixtral-8x7B-Chat-Deprecated).
