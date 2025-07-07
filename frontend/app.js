document.addEventListener('DOMContentLoaded', () => {
    cargarEventos();
});

// IMPORTANTE: Debes reemplazar este token con uno válido de tu API de login
const authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzUxODk4NDYyfQ.U8R6WR-_4vVmztLXB7F6pk-Q6O0ubgQI6xo0mbL6mlc';

function cargarEventos() {
    fetch("http://127.0.0.1:8080/internal/evento/", {
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401 || response.status === 403) {
               alert("Error de autenticación. Verifica tu token.");
            }
            throw new Error('Error al cargar los datos.');
        }
        return response.json();
    })
    .then(data => {
        const tbody = document.querySelector("#tabla-eventos tbody");
        tbody.innerHTML = ''; // Limpiar la tabla antes de cargar nuevos datos

        data.data.forEach(evento => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${evento.eventoId}</td>
                <td>${evento.nombre}</td>
                <td>${evento.categoriaEvento.nombre}</td>
                <td>${new Date(evento.fechaInicio).toLocaleDateString()}</td>
                <td>${new Date(evento.fechaFin).toLocaleDateString()}</td>
                <td>
                    <span class="status-${evento.estado.toLowerCase()}">
                        ${evento.estado === 'AC' ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
                <td>
                    <button onclick="editarEvento(${evento.eventoId})">Editar</button>
                    <button class="btn-delete" onclick="confirmarEliminar(${evento.eventoId})">Eliminar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    })
    .catch(err => console.error("Error cargando eventos:", err));
}

function editarEvento(id) {
    alert("Función para editar el evento ID: " + id + ". ¡La construiremos a continuación!");
}

function confirmarEliminar(id) {
    if (confirm(`¿Estás seguro de que quieres eliminar el evento ID: ${id}?`)) {
        eliminarEvento(id);
    }
}

function eliminarEvento(id) {
    fetch(`http://127.0.0.1:8000/internal/evento/${id}/eliminar`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    })
    .then(response => {
        if (response.ok) {
            alert("Evento eliminado correctamente.");
            cargarEventos(); // Recargar la tabla
        } else {
            throw new Error('Error al eliminar el evento.');
        }
    })
    .catch(err => console.error("Error eliminando evento:", err));
}