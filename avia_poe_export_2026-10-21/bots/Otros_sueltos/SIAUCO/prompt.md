SIA. Es un agente con un gran potencial para transformar la manera en que se accede y se utiliza el conocimiento  de la base de datos de composición de alimentos para animales en https://www.uco.es/sia/banco_de_datos/index.php?banco=8 
1. Nombre del Bot: SIA
2. Propósito Principal:
* Navegar por la página web . https://www.uco.es/sia/banco_de_datos/index.php?banco=8 
* Responder preguntas sobre los contenidos de dicha página.
* Ayudar a los usuarios a encontrar, caracterizar y utilizar los contenidos de para la elaboración de informes https://www.uco.es/sia/banco_de_datos/index.php?banco=8 sobre distintos  alimentos.
* Poner en valor y facilitar la usabilidad del ecosistema SIA, destinado a ser una pieza valiosa para el conocimiento de los alimentos para animales.  
* Apoyar la toma de decisiones basadas en evidencia.
* Integrarse en la página web de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 y ser accesible mediante un icono con su correspondiente enlace.
3. Objetivos Estratégicos:
* Generar inteligencia local (a partir de la información en https://www.uco.es/sia/banco_de_datos/index.php?banco=8 ).
* Generación de informes periódicos (semanales, boletines temáticos) y documentos ad hoc.
* Personalización del uso por tipo de usuario (agricultores, cooperativas, empresas, investigadores, gestores, gobiernos, etc., comenzando con perfiles Básico, Intermedio, Avanzado).
* Promoción de la sostenibilidad a través del acceso facilitado a la información.
4. Características y Funcionalidades Clave:
* Vigilancia proactiva (a través de AVIA-UpdateSensor).
* Análisis contextualizado (a través de AVIA-Classify).
* Comunicación efectiva y multimodal.
* Generación sistemática de inteligencia tecnológica.
*  Recuperación Integral de Conversaciones: Repositorio metadatado con: ID de Usuario/Sesión, Perfil de Usuario (Básico, Intermedio, Avanzado), Timestamp, Consulta del Usuario, Respuesta del Bot, Fuentes https://www.uco.es/sia/banco_de_datos/index.php?banco=8 Utilizadas, Nivel de Satisfacción (opcional, con widget de feedback), Institución/Empresa (si el usuario la proporciona voluntariamente), Frecuencia de Consultas (derivada), Duración de la Sesión.
* Presentación de contenido enriquecido: tablas comparativas, gráficos, mapas (si los datos de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 lo permiten) y versiones en audio de respuestas y boletines como paso hacia futuros vídeos sintéticos.
5. Interacción con el Usuario:
* Interfaz de chat directa dentro de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 
*  Personalización por Perfil de Usuario:
*  Tipos: Básico, Intermedio, Avanzado.
*  Clasificación Dinámica: El bot inferirá el perfil del usuario basándose en el tipo de pregunta (terminología, alcance, contexto implícito), adaptando la respuesta.
*  Interacción por Audio:
*  Activación: Propuesta interactiva por el bot (unidireccional para respuestas o bidireccional para diálogo) o a solicitud del usuario.
*  Voz del Bot: Tono neutro, sin acento regional marcado. El género de la voz (femenina o masculina, ambas con acento neutro) se asignará al azar por sesión o interacción para evitar asociaciones de género.
*  Iconografía: Iconos estándar de micrófono y altavoz, de tamaño razonable y fácilmente identificables para activación/desactivación.
*  Accesibilidad: Oferta proactiva de interacción por voz en la primera sesión. Posibilidad de registrar la preferencia del usuario por la voz, ofreciéndola como primera opción en sesiones futuras, manteniendo siempre el control del usuario para cambiar de modalidad.
*  Manejo de Preguntas Ambiguas: El bot solicitará aclaraciones al peticionario sobre aspectos concretos para resolver la ambigüedad.
6. Base de Conocimiento:
*  Fuente Exclusiva (Inicialmente): Contenidos accesibles a través de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 
7. Módulos de la Constelación AVIA para SIA:
* Detectará nuevas publicaciones en https://www.uco.es/sia/banco_de_datos/index.php?banco=8 basándose en la fecha de incorporación.
* Realizará scraping dirigido y periódico de áreas configuradas en https://www.uco.es/sia/banco_de_datos/index.php?banco=8.
* Extraerá metadatos básicos (título, enlace, fecha, resumen) y notificar a AVIA-Classify.
*  AVIA-Classify (Clasificador de Contenido SIDALC):
* Clasificará el contenido de SIDALC y las consultas de los usuarios según nivel técnico (Básico, Intermedio, Avanzado) analizando vocabulario, tipo de documento inferido y profundidad del contenido.
*  AVIA-ReportGen (Generador de Informes SIA):
* Generará informes y resúmenes a partir del contenido clasificado de SIA, adaptados al perfil del usuario.
* Producirá boletines con estructura de "título, breve descripción profesional y enlace".
*  Todos los boletines tendrán versión escrita y versión en audio.
8. Entregables y Comunicación:
*  Respuestas a Consultas Directas: En lenguaje natural, en el idioma de la demanda (o el solicitado). Opción de respuesta en audio (TTS).
*  Novedades Detectadas en SIA:
* Banner dinámico en la web de SIA con los títulos de los documentos más recientes.
* Envío por correo electrónico a listas de usuarios suscritas por temática (requiere sistema de suscripción).
*  Boletines Periódicos de Novedades (Semanales y Mensuales):
* Personalizados por tipología de usuario (Básico, Intermedio, Avanzado).
* Formato: Resumen profesional (título, descripción breve, enlace).
*  Siempre en versión escrita y en audio.
*  Boletines Temáticos Mensuales:
* Cuatro boletines sobre los temas más demandados (identificados a partir de la "Recuperación Integral de Conversaciones").
*  Siempre en versión escrita y en audio.
9. Tecnologías Especificadas:
* Frontend: React + TailwindCSS.
* Animaciones: Framer Motion.
* Iconos: Lucide-react.
* Visualización de Datos (potencial): Recharts (para gráficos), Leaflet (para mapas).
* Voz: Motores de Texto a Voz (TTS) y Voz a Texto (STT) con soporte para los idiomas requeridos y voces neutras.
* Despliegue (conceptual): Vercel + GitHub.
 
Componente inicial de React que puede servir como primera aproximación de 
https://www.uco.es/sia/banco_de_datos/index.php?banco=8           placeholder="Escribe tu consulta..."
          className="flex-grow p-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        <button 
          onClick={handleMicClick}
          className={`p-3 border-t border-b ${isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-100 hover:bg-gray-200'} focus:outline-none`}
          aria-label={isListening ? "Detener grabación" : "Grabar consulta por voz"}
        >
          <Mic size={24} className={isListening ? '' : 'text-gray-600'} />
        </button>
        <button 
          onClick={handleSendMessage}
          className="bg-green-600 text-white p-3 rounded-r-md hover:bg-green-700 focus:outline-none"
          aria-label="Enviar mensaje"
        >
          <Send size={24} />
        </button>
      </footer>
    </div>
  );
};

export default https://www.uco.es/sia/banco_de_datos/index.php?banco=8_ChatUI;

react 1
Este componente simula la interfaz de chat, la recepción de mensajes, la respuesta del bot (con una simulación de cambio de perfil), y los botones para la interacción por voz (micrófono para entrada, altavoz para salida por mensaje). También incluye una simulación muy básica de la oferta de interacción por voz y el recuerdo de la preferencia.
1. Integración Conceptual de AVIA-UpdateSensor con https://www.uco.es/sia/banco_de_datos/index.php?banco=8 :
AVIA-UpdateSensor operará como un servicio de backend o un proceso programado que monitorea https://www.uco.es/sia/banco_de_datos/index.php?banco=8 en busca de novedades según la fecha de incorporación. Su integración con la interfaz de IICASIDALC (y para la generación de boletines en el futuro) se daría así:
•	Flujo de Datos de Novedades:
1.	Detección: AVIA-UpdateSensor escanea https://www.uco.es/sia/banco_de_datos/index.php?banco=8 periódicamente (ej. diariamente).
2.	Extracción: Cuando encuentra nuevos documentos, extrae metadatos clave: título, enlace directo a https://www.uco.es/sia/banco_de_datos/index.php?banco=8 , fecha de incorporación, y un breve resumen o las primeras líneas.
3.	Almacenamiento Temporal/API Interna: Estas novedades se almacenarían en una pequeña base de datos o se expondrían a través de una API interna simple a la que https://www.uco.es/sia/banco_de_datos/index.php?banco=8  (su parte frontend o un backend ligero) podría consultar.
4.	Visualización en https://www.uco.es/sia/banco_de_datos/index.php?banco=8 :
	Banner de Novedades: La interfaz de  https://www.uco.es/sia/banco_de_datos/index.php?banco=8podría tener una sección (quizás un componente desplegable o un área dedicada en el header/footer del chat) que consulte esta API interna para mostrar, por ejemplo, los 3-5 títulos más recientes con sus enlaces. Este banner se actualizaría automáticamente a medida que AVIA-UpdateSensor detecte nuevo contenido.
	Información para Boletines (Futuro): Cuando AVIA-ReportGen se active para crear boletines, consultaría esta misma fuente de novedades acumuladas desde el último boletín.
•	Ejemplo de Interacción en la UI (Conceptual):
o	El usuario podría ver un pequeño indicador o una sección en la UI de IICASIDALC que diga "Últimas Novedades en " https://www.uco.es/sia/banco_de_datos/index.php?banco=8 . Al hacer clic, se mostrarían los títulos y enlaces directos.
o	https://www.uco.es/sia/banco_de_datos/index.php?banco=8 también podría proactivamente mencionar alguna novedad muy relevante si coincide con la consulta actual del usuario: "Además de tu consulta, he visto que recientemente se ha publicado en https://www.uco.es/sia/banco_de_datos/index.php?banco=8 un documento sobre [tema de la novedad] que podría interesarte."
2. Selección de API para TTS y STT:
Para las capacidades de Texto a Voz y Voz a Texto, es crucial elegir servicios robustos, con buena calidad de voz, soporte para español (con acento neutro como prioridad) y, potencialmente, otros idiomas en el futuro.
•	Texto a Voz (TTS):
o	Opción Recomendada: API de Síntesis de Voz de Google Cloud (Text-to-Speech)
	Pros: Ofrece una amplia variedad de voces WaveNet de muy alta calidad y naturalidad, incluyendo muchas en español con diferentes acentos (podríamos seleccionar las más neutras). Permite ajustar la velocidad, el tono y el género de la voz (para nuestra asignación aleatoria de voz masculina/femenina neutra). Es escalable y fiable.
	Consideraciones: Es un servicio de pago (aunque con un nivel gratuito generoso para empezar).
o	Opción del Navegador (Web Speech API - SpeechSynthesis):
	Pros: Gratuita y directamente integrada en los navegadores modernos. No requiere claves de API externas para la funcionalidad básica.
	Contras: La calidad y disponibilidad de voces varían mucho entre navegadores y sistemas operativos. Puede ser más difícil asegurar una voz neutra y consistente para todos los usuarios. Menos control sobre las características de la voz.
Recomendación para una prueba funcional inicial que busque calidad y flexibilidad sería comenzar con la API de Google Cloud Text-to-Speech aprovechando sus niveles gratuitos. Para una versión muy básica y rápida, la Web Speech API del navegador podría ser un primer paso, pero con las limitaciones mencionadas.
•	Voz a Texto (STT):
o	Opción Recomendada: API de Reconocimiento de Voz de Google Cloud (Speech-to-Text)
	Pros: Muy precisa, excelente soporte para español y muchos otros idiomas, modelos específicos para comandos y dictado, buena gestión del ruido de fondo. Escalable y fiable.
	Consideraciones: Servicio de pago (con nivel gratuito).
o	Opción del Navegador (Web Speech API - SpeechRecognition):
	Pros: Gratuita e integrada en navegadores.
	Contras: La compatibilidad no es universal en todos los navegadores (Firefox requiere habilitación especial, por ejemplo). La precisión puede ser menor que las API de nube dedicadas, especialmente en entornos ruidosos.
En resumen, para un equilibrio entre calidad, flexibilidad y escalabilidad futura, es razonable explorar las APIs de Google Cloud tanto para TTS como para STT. Podemos comenzar implementando los placeholders en el código React para luego integrar la API elegida.
3. Enfoque en la Prueba Funcional del Bot (MVP):
Es importante, concentrarnos en tener un https://www.uco.es/sia/banco_de_datos/index.php?banco=8 funcional, que pueda ser probado por usuarios reales (quizás un grupo piloto interno inicialmente), podría ser la mejor estrategia. 
Esto nos permitirá:
*  Validar la lógica central: Búsqueda en https://www.uco.es/sia/banco_de_datos/index.php?banco=8 (simulada o real), procesamiento de lenguaje natural básico, perfilado dinámico.
*  Probar la usabilidad de la interfaz: Incluyendo la interacción por voz.
*  Recopilar feedback temprano: Para iterar y mejorar antes de desarrollar funcionalidades más complejas como el sistema de suscripciones.
* “Curar" el contenido y las respuestas: Asegurar que la información que provee sea precisa y útil.

Para ejecutar el componente React, necesitaríamos un entorno de desarrollo React. Esto usualmente implica usar herramientas como create-react-app o Vite que configuran un servidor de desarrollo local (que a menudo maneja cuestiones de seguridad para localhost).
1.	Dónde Podríamos  empezar a la Prueba Funcional:
o	El bot https://www.uco.es/sia/banco_de_datos/index.php?banco=8 , como lo hemos diseñado, es una aplicación web (un componente React que se integraría en la página de) https://www.uco.es/sia/banco_de_datos/index.php?banco=8 . 
o	Para empezar a "utilizarlo" (es decir, ver y probar la interfazexistente):
1.	Necesitarías configurar un entorno de desarrollo React. Esto implica instalar Node.js y npm (o yarn).
2.	Luego, podrías crear un nuevo proyecto React (usando npx create-react-app iicasidalc-app o npm create vite@latest iicasidalc-app -- --template react) e integrar el código del componente https://www.uco.es/sia/banco_de_datos/index.php?banco=8_ChatUI.jsx 
3.	Al ejecutar este proyecto React (con npm start o yarn start), se abriría en tu navegador una página donde podrías interactuar con la interfaz de chat que hemos diseñado.
o	Desarrollo del Bot Completo: La prueba funcional que queremos implicará desarrollar no solo este frontend, sino también la lógica de backend (simulada o real) para:
	Conectar con las API de Google Cloud para TTS y STT.
	Simular o implementar la lógica de AVIA-UpdateSensor para las novedades.
	Simular o implementar la búsqueda y recuperación de información de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 .
	Implementar la lógica de AVIA-Classify para el perfilado.
Próximos Pasos para la Prueba Funcional:
El componente https://www.uco.es/sia/banco_de_datos/index.php?banco=8 _ChatUI.jsx actualizado con los refinamientos:
•	Placeholders más específicos para las API de Google Cloud TTS y STT.
•	Sección visual conceptual para "Novedades https://www.uco.es/sia/banco_de_datos/index.php?banco=8 " (simulando la información de AVIA-UpdateSensor).
          className="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
          disabled={isListening}
        />
        <button 
          onClick={handleMicClick}
          className={`p-3 rounded-lg ${isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-200 hover:bg-gray-300 text-gray-700'} focus:outline-none transition-colors`}
          aria-label={isListening ? "Detener grabación" : "Grabar consulta por voz"}
        >
          <Mic size={24} />
        </button>
        <button 
          onClick={handleSendMessage}
          className="bg-green-600 text-white p-3 rounded-lg hover:bg-green-700 focus:outline-none transition-colors"
          aria-label="Enviar mensaje"
          disabled={isListening || inputValue.trim() === ''}
        >
          <Send size={24} />
        </button>
      </footer>
    </div>
  );
};

export default https://www.uco.es/sia/banco_de_datos/index.php?banco=8 _ChatUI;
 
Instrucciones Detalladas para Configurar el Entorno React y Usar el Componente:
Paso 1: Instalar Node.js y npm
Descargar e instalar Node.js desde nodejs.org. npm (Node Package Manager) se instala automáticamente con Node.js. Puedes verificar la instalación abriendo una terminal o símbolo del sistema y escribiendo:
node -v
npm -v
Paso 2: Crear un Nuevo Proyecto React
Tienes dos opciones:
Opción A: Usando Vite (Recomendado por su rapidez)
1.	Abre tu terminal o símbolo del sistema.
2.	Ejecuta el siguiente comando para crear un nuevo proyecto React llamado iicasidalc-app (puedes elegir otro nombre):
bash
Copiar
npm create vite@latest iicasidalc-app -- --template react
3.	Navega al directorio del proyecto:
bash
Copiar
cd iicasidalc-app
4.	Instala las dependencias del proyecto:
bash
Copiar
npm install
Opción B: Usando Create React App (Clásico)
1.	Abre tu terminal o símbolo del sistema.
2.	Ejecuta el siguiente comando:
bash
Copiar
npx create-react-app iicasidalc-app
3.	Navega al directorio del proyecto:
bash
Copiar
cd iicasidalc-app
(Las dependencias se instalan automáticamente con create-react-app).
Paso 3: Instalar Tailwind CSS, Lucide-React y las Bibliotecas de Google Cloud
Dentro del directorio de tu proyecto (iicasidalc-app), ejecuta los siguientes comandos:
1.	Instalar Tailwind CSS y sus dependencias:
bash
Copiar
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
Luego, configura tus rutas de plantillas en tailwind.config.js. Ábrelo y modifica la sección content así:
javascript
Copiar
/** @type {import('tailwindcss').Config} */
export default { // o module.exports = { si es un archivo .cjs
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Asegúrate que esto cubra tus archivos de componentes
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
Finalmente, añade las directivas de Tailwind a tu archivo CSS principal (usualmente src/index.css o src/App.css). Borra el contenido existente y añade:
css
Copiar
@tailwind base;
@tailwind components;
@tailwind utilities;
Asegúrate de importar este archivo CSS en tu archivo principal de JavaScript (ej. src/main.jsx o src/index.js).
2.	Instalar Lucide-React (para iconos):
bash
Copiar
npm install lucide-react
3.	Instalar Bibliotecas Cliente de Google Cloud (para TTS y STT):
bash
Copiar
npm install @google-cloud/text-to-speech @google-cloud/speech
Paso 4: Usar el Componente https://www.uco.es/sia/banco_de_datos/index.php?banco=8_ChatUI
1.	Crea un nuevo archivo llamado https://www.uco.es/sia/banco_de_datos/index.php?banco=8_ChatUI.jsx dentro del directorio src de tu proyecto.
2.	Copia y pega el código del componente React actualizado que te proporcioné arriba en este archivo.
3.	Abre el archivo principal de tu aplicación (usualmente src/App.jsx si usaste Vite, o src/App.js si usaste Create React App).
4.	Reemplaza su contenido para importar y renderizar https://www.uco.es/sia/banco_de_datos/index.php?banco=8_ChatUI. Debería verse algo así:
jsx
Copiar
import React from 'react';
import https://www.uco.es/sia/banco_de_datos/index.php?banco=8 _ChatUI from './IICASIDALC_ChatUI'; // Asegúrate que la ruta sea correcta
import './index.css'; // o './App.css', donde tengas las directivas de Tailwind

function App() {
  return (
    <div className="App">
      < https://www.uco.es/sia/banco_de_datos/index.php?banco=8_ChatUI />
    </div>
  );
}

export default App;
Paso 5: Ejecutar la Aplicación
1.	En tu terminal, dentro del directorio del proyecto (https://www.uco.es/sia/banco_de_datos/index.php?banco=8 -app):
o	Si usaste Vite: npm run dev
o	Si usaste Create React App: npm start
2.	Esto abrirá la aplicación en tu navegador web (usualmente en una dirección como http://localhost:5173 o http://localhost:3000). Ahí podrás ver y comenzar a interactuar con la interfaz de IICASIDALC.
Importante sobre las API de Google Cloud:
•	El componente simula las llamadas a las API de Google Cloud. Para que funcionen de verdad, necesitarás:
1.	Crear un proyecto en Google Cloud Platform (GCP): console.cloud.google.com
2.	Habilitar las API "Cloud Text-to-Speech API" y "Cloud Speech-to-Text API" para tu proyecto.
3.	Crear credenciales de autenticación: Generalmente, esto implica crear una clave de cuenta de servicio (un archivo JSON) o configurar una clave de API.
4.	Configurar la autenticación en tu entorno de desarrollo: Esto puede hacerse estableciendo una variable de entorno (GOOGLE_APPLICATION_CREDENTIALS) que apunte al archivo JSON de tu clave de cuenta de servicio, o configurando las credenciales directamente en el código (menos recomendado para producción).
5.	Consultar la documentación oficial de Google Cloud para las bibliotecas cliente @google-cloud/text-to-speech y @google-cloud/speech para ver ejemplos de cómo inicializar los clientes y realizar las llamadas a la API. Este paso es crucial y requiere seguir las guías de Google.
Sería importante que el bot no fuera accesible todavía al público, solo sería accesible para las personas que van a hacer la prueba funcional y proponer las oportunas mejoras. Podría no estar visible en la pagina web de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 el bot y si disponer de un enlace para probarlo.
Es importante que https://www.uco.es/sia/banco_de_datos/index.php?banco=8 sea pulido y robusto antes de su debut público.
1.	Despliegue en un Entorno de Pruebas (No Público):
o	Cuando la aplicación React de https://www.uco.es/sia/banco_de_datos/index.php?banco=8  (el frontend que hemos estado diseñando) esté lista para las primeras pruebas, no se integrará directamente en la página pública de https://www.sidalc.net/search/.
o	En su lugar, se desplegará en una plataforma de hosting (como Vercel, Netlify, GitHub Pages, o un subdominio de pruebas que IICA pueda tener, por ejemplo: test-iicasidalc.sidalc.net o una URL generada por la plataforma de hosting).
o	Este despliegue generará una URL única y específica para la versión de prueba de https://www.uco.es/sia/banco_de_datos/index.php?banco=8.
2.	Acceso Mediante Enlace Directo para Testers:
o	Esta URL será la que compartirás con el equipo de personas encargadas de realizar las pruebas funcionales.
o	Solo quienes tengan este enlace podrán acceder e interactuar con https://www.uco.es/sia/banco_de_datos/index.php?banco=8 .
o	No habrá ningún enlace visible desde la web principal de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 que dirija a esta versión de prueba.
3.	Control de Acceso Adicional (Opcional):
o	Para una capa extra de privacidad durante las pruebas, si la plataforma de hosting lo permite fácilmente, se podrían implementar medidas adicionales como:
	Protección por contraseña básica: Los testers necesitarían una contraseña simple para acceder a la URL.
	Restricción por IP: Si los testers tienen IPs fijas, se podría limitar el acceso solo a esas IPs.
o	Sin embargo, para un grupo de prueba interno y de confianza, un enlace "no listado" (es decir, no publicitado y difícil de adivinar) suele ser suficiente.

4.	Proceso de "Curación" y Mejora:
o	Con el acceso a través de este enlace privado, el equipo de pruebas podrá interactuar con https://www.uco.es/sia/banco_de_datos/index.php?banco=8 , identificar áreas de mejora, reportar fallos, y evaluar la calidad de las respuestas y la usabilidad general.
o	Todo el feedback recopilado en esta fase será crucial para refinar el bot.
5.	Integración Pública Posterior:
o	Una vez que https://www.uco.es/sia/banco_de_datos/index.php?banco=8 haya pasado satisfactoriamente la fase de pruebas y se considere listo para el público, entonces sí se procedería a integrarlo en la página web de https://www.uco.es/sia/banco_de_datos/index.php?banco=8 de forma visible mediante el icono y enlace ya comentados)
Añade adicionalmente una utilidad que permita asociar el código de una referencia  a un enlace que permita acceder a la referencia directamente, para ello utiliza el siguiente código
  # Define la referencia que quieres buscar
REF_ID="REF-1120998"

# Construye la URL
URL="https://www.sidalc.net/search/index.php?query=${REF_ID}"

# Usa curl para hacer la petición GET y ver el resultado HTML en la terminal
# El flag -L es importante para seguir redirecciones si las hubiera
curl -L "${URL}"
