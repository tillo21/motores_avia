Procesar la Información con IA
🛠️ Estrategia:
1️⃣ Convertir los documentos a formato texto estructurado (TXT, JSON o Base de Datos).
2️⃣ Utilizar NLP (Procesamiento de Lenguaje Natural) para extraer elementos clave.
3️⃣ Aplicar algoritmos de generación de texto para adaptar cada unidad didáctica.
4️⃣ Implementar un sistema de validación para asegurarse de que cada unidad cumple con la normativa.
Puedes hacer que el bot sea accesible desde:
💻 Una aplicación web (Flask, Streamlit).
📱 Un bot de Telegram.
📂 Un generador de documentos en Google Docs o PDF.Implementar Personalización y Retroalimentación
✍️ El bot debería permitirte:
✅ Elegir niveles educativos y asignaturas. (En este caso se hará según el doc. Plan de Apoyo Antonio y Enrique)
✅ Modificar objetivos, competencias y criterios de evaluación.
✅ Ajustar la redacción y extensión de cada apartado.
### **🚀 Características del Código:**  
✅ Carga una **Unidad Didáctica Base** y extrae su contenido.  
✅ Procesa la **normativa** para asegurarse de que la unidad cumple con los requisitos.  
✅ Genera una **nueva Unidad Didáctica** con IA basada en GPT-4.  
✅ Permite descargar la unidad generada en formato **.txt**.  

---

### **🔧 Requisitos Previos:**  
Instala las librerías necesarias con:  
```bash
pip install openai pdfplumber streamlit python-dotenv
```
Y guarda tu clave API de OpenAI en un archivo `.env` con:  
```
OPENAI_API_KEY=tu_clave_aquí
```

---

### **📜 Código Base del Bot**  
Este código te permite subir un PDF con la unidad base y otro con la normativa. Luego genera una nueva unidad adaptada.  


### **📌 Cómo Usarlo**  
1️⃣ Ejecuta el script con:  
   ```bash
   streamlit run script.py
   ```  
2️⃣ Sube un PDF con tu unidad didáctica base.  
3️⃣ Sube un PDF con la normativa vigente.  
4️⃣ Haz clic en "✍️ Generar Unidad Didáctica".  
5️⃣ Descarga la nueva unidad en `.txt`.  

---

### **🚀 Posibles Mejoras**  
✅ Generar en formato **Word (.docx)** en lugar de `.txt`.  
✅ Personalizar **niveles educativos** y **asignaturas**.  
✅ Añadir opción de **ajustar el lenguaje** y **extensión** de la unidad.  


