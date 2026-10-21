<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dashboard Docente - AVIA SIALU</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gradient-to-b from-indigo-900 to-purple-900 text-white font-sans p-6">
  <div class="max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold text-yellow-400 mb-4">📊 Dashboard Cognitivo-Emocional AVIA (Modo Docente)</h1>

    <div class="grid md:grid-cols-4 gap-4 mb-6">
      <label class="flex flex-col">
        <span class="text-sm mb-1">👤 Usuario:</span>
        <input id="usuarioFiltro" type="text" placeholder="juanita@escuela.edu" class="rounded px-3 py-2 text-black" />
      </label>
      <label class="flex flex-col">
        <span class="text-sm mb-1">📅 Fecha desde:</span>
        <input id="desdeFiltro" type="date" class="rounded px-2 py-1 text-black" />
      </label>
      <label class="flex flex-col">
        <span class="text-sm mb-1">📅 Fecha hasta:</span>
        <input id="hastaFiltro" type="date" class="rounded px-2 py-1 text-black" />
      </label>
      <label class="flex flex-col">
        <span class="text-sm mb-1">📘 Capítulo:</span>
        <select id="capituloFiltro" class="rounded px-2 py-1 text-black">
          <option value="">Todos</option>
          <option value="Lía y el Árbol - Capítulo 1">Lía y el Árbol - Capítulo 1</option>
          <option value="El Bosque Mágico">El Bosque Mágico</option>
        </select>
      </label>
    </div>

    <div class="mb-6">
      <button onclick="filtrarResumen()" class="bg-yellow-400 hover:bg-yellow-300 text-black px-5 py-2 rounded">🔍 Filtrar Datos</button>
      <button onclick="exportarCSV()" class="ml-4 bg-green-400 hover:bg-green-300 text-black px-5 py-2 rounded">📤 Exportar CSV</button>
    </div>

    <div id="alertaContainer" class="mb-6"></div>
    <canvas id="graficoResumen" class="bg-white rounded shadow-lg"></canvas>
  </div>

  <script>
    async function filtrarResumen() {
      const usuario = document.getElementById('usuarioFiltro').value;
      const desde = document.getElementById('desdeFiltro').value;
      const hasta = document.getElementById('hastaFiltro').value;
      const capitulo = document.getElementById('capituloFiltro').value;

      const params = new URLSearchParams();
      if (usuario) params.append('usuario', usuario);
      if (desde) params.append('desde', new Date(desde).getTime());
      if (hasta) params.append('hasta', new Date(hasta).getTime());
      if (capitulo) params.append('capitulo', capitulo);

      const res = await fetch('/modulos/sialu/resumen?' + params.toString());
      const resumen = await res.json();
      renderChart(resumen);
      window.resumenRaw = resumen;
      verificarAlertas(resumen);
    }

    function renderChart(data) {
      const ctx = document.getElementById('graficoResumen').getContext('2d');
      if (window.chart) window.chart.destroy();

      window.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(data),
          datasets: [{
            label: 'Eventos SIALU por tipo',
            data: Object.values(data),
            backgroundColor: 'rgba(255, 206, 86, 0.7)',
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: { mode: 'index', intersect: false }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }

    function exportarCSV() {
      const data = window.resumenRaw || {};
      const filas = Object.entries(data).map(([clave, valor]) => `${clave},${valor}`);
      const contenido = 'Evento,Conteo\n' + filas.join('\n');
      const blob = new Blob([contenido], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "resumen_sialu.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    function verificarAlertas(resumen) {
      const alertaDiv = document.getElementById('alertaContainer');
      alertaDiv.innerHTML = '';
      let mensajes = [];

      for (let clave in resumen) {
        if (clave.includes('emocion::triste') && resumen[clave] >= 3) {
          mensajes.push('⚠️ Alerta: se detectaron más de 3 registros de tristeza.');
        }
        if (clave.includes('emocion::ansioso') && resumen[clave] >= 2) {
          mensajes.push('🚨 Atención: signos de ansiedad en el grupo.');
        }
      }

      if (mensajes.length > 0) {
        alertaDiv.innerHTML = mensajes.map(m => `<div class='bg-red-500 text-white px-4 py-2 rounded mb-2'>${m}</div>`).join('');
      }
    }

    // Carga inicial
    filtrarResumen();
  </script>
</body>
</html>
