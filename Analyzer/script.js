document.getElementById('loadData').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("Por favor, selecciona un archivo JSON.");
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = function(event) {
        const data = JSON.parse(event.target.result);
        const victorias = calcularVictoriasPorEstrategia(data);
        const porcentajes = calcularPorcentajesVictorias(victorias);
        mostrarResultados(victorias, porcentajes);
    };
    
    reader.readAsText(file);
});

function calcularVictoriasPorEstrategia(data) {
    const resumeBots = data.resume.resume_bots;
    const estrategias = ["agresiva", "pasiva", "cartas", "aleatoria"];
    const totalVictorias = { agresiva: 0, pasiva: 0, cartas: 0, aleatoria: 0 };

    for (const botKey in resumeBots) {
        const botInfo = resumeBots[botKey];
        const matrizVictorias = JSON.parse(botInfo["Matriz de victorias en esta partida:"]);

        matrizVictorias.forEach((victorias, i) => {
            totalVictorias[estrategias[i]] += victorias;
        });
    }

    return totalVictorias;
}

function calcularPorcentajesVictorias(totalVictorias) {
    const totalVictoriasTotales = Object.values(totalVictorias).reduce((a, b) => a + b, 0);
    const porcentajes = {};

    for (const estrategia in totalVictorias) {
        porcentajes[estrategia] = ((totalVictorias[estrategia] / totalVictoriasTotales) * 100).toFixed(2);
    }

    return { porcentajes, totalVictoriasTotales };
}

function mostrarResultados(victorias, porcentajes) {
    const tbody = document.querySelector('#resultsTable tbody');
    tbody.innerHTML = ''; // Limpiar resultados anteriores

    for (const estrategia in victorias) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${estrategia}</td>
            <td>${victorias[estrategia]}</td>
            <td>${porcentajes.porcentajes[estrategia]}%</td>
        `;
        tbody.appendChild(row);
    }

    // Agregar fila para el total
    const totalRow = document.createElement('tr');
    totalRow.innerHTML = `
        <td>Total</td>
        <td>${porcentajes.totalVictoriasTotales}</td>
        <td>100.00%</td>
    `;
    tbody.appendChild(totalRow);
}
