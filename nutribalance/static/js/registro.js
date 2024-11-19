let contador = 0;
let objetivoLitros = 0; // Variable para el objetivo en litros

function actualizarContador() {
    if (contador >= 1000) {
        document.getElementById("contador").textContent = (contador / 1000).toFixed(2) + " L";
    } else {
        document.getElementById("contador").textContent = contador + " ml";
    }

    actualizarProgreso(); // Actualizar el progreso en cada modificación
}

function agregarVaso() {
    contador += 250;
    actualizarContador();
}

function restarVaso() {
    if (contador >= 250) {
        contador -= 250;
    } else {
        contador = 0;
    }
    actualizarContador();
}

function reiniciarContador() {
    contador = 0;
    actualizarContador();
}

function establecerObjetivo() {
    const inputObjetivo = document.getElementById("inputObjetivo").value;
    objetivoLitros = parseFloat(inputObjetivo); // Convertir el objetivo a número
    document.getElementById("objetivoDisplay").textContent = "Objetivo: " + objetivoLitros + " L";
    actualizarProgreso(); // Actualizar el progreso después de cambiar el objetivo
}

function actualizarProgreso() {
    if (objetivoLitros > 0) {
        let progreso = (contador / 1000) / objetivoLitros * 100; // Calcular el porcentaje de progreso
        if (progreso > 100) {
            progreso = 100; // Limitar el progreso al 100%
        }

        // Cambiar el color según el porcentaje de progreso
        const barraProgreso = document.getElementById("barraProgreso");
        if (progreso < 30) {
            barraProgreso.className = 'low'; // Menos del 30%
        } else if (progreso < 70) {
            barraProgreso.className = 'medium'; // Entre 30% y 70%
        } else {
            barraProgreso.className = 'high'; // Más del 70%
        }

        document.getElementById("progreso").textContent = "Progreso: " + progreso.toFixed(2) + "%";
        barraProgreso.value = progreso; // Actualizar la barra de progreso

        // Mostrar alerta cuando el progreso es del 100%
        if (progreso === 100) {
            alert("¡Felicidades! Has alcanzado tu objetivo de consumo de agua.");
        }
    } else {
        document.getElementById("progreso").textContent = "Progreso: 0%";
        document.getElementById("barraProgreso").value = 0; // Restablecer la barra si no hay objetivo
    }
}