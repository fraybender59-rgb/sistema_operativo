document.addEventListener('DOMContentLoaded', () => {
    cargarCocina();
    setInterval(cargarCocina, 1000);
});

async function cargarCocina() {
    const container = document.getElementById('cocina-orders');
    if (!container) return;

    const todos = await obtenerPedidosSync();
    const enCocina = todos.filter(p => p.estado === 'pendiente' || p.estado === 'en_cocina');

    if (enCocina.length === 0) {
        container.innerHTML = '<p style="text-align:center; color:#94a3b8; font-size:1.1rem; margin-top:40px;">No hay comandas pendientes en cocina.</p>';
        return;
    }

    const ahora = new Date();

    container.innerHTML = enCocina.map(p => {
        const fechaIngreso = new Date(p.creado_en || Date.now());
        const diffMs = ahora - fechaIngreso;
        const diffMin = Math.floor(diffMs / 60000);
        const diffSeg = Math.floor((diffMs % 60000) / 1000);

        let badgeClass = 'timer-green';
        if (diffMin >= 7 && diffMin < 21) badgeClass = 'timer-yellow';
        else if (diffMin >= 21) badgeClass = 'timer-red';

        const horaTexto = fechaIngreso.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

        return `
            <div class="admin-card" style="border-left: 6px solid #0284c7; background:#1e293b; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155; padding-bottom:8px;">
                    <div>
                        <h2 style="margin:0; font-size:1.2rem; color:#f8fafc;">📍 ${p.cliente_mesa}</h2>
                        <small style="color:#94a3b8;">Hora: ${horaTexto} | Atiende: <b>${p.mesero_nombre}</b> (${p.origen})</small>
                    </div>
                    <div class="timer-badge ${badgeClass}">
                        ⏱️ ${diffMin}m ${diffSeg < 10 ? '0' : ''}${diffSeg}s
                    </div>
                </div>
                <ul style="list-style:none; padding:0; margin:12px 0;">
                    ${p.detalles.map(d => `
                        <li style="font-size:1.1rem; padding:6px 0; border-bottom:1px dashed #334155;">
                            <b>${d.cantidad}x ${d.nombre}</b>${d.comentario ? `<br><small style="color:#f59e0b; font-size:0.9rem;">⚠️ Nota: ${d.comentario}</small>` : ''}
                        </li>
                    `).join('')}
                </ul>
                <button class="btn btn-success" style="padding:12px; font-size:1rem;" onclick="cerrarEnCocina(${p.id})">✅ Marcar como LISTO / ENTREGADO</button>
            </div>
        `;
    }).join('');
}

async function cerrarEnCocina(id) {
    await actualizarEstadoPedidoSync(id, 'listo');
    cargarCocina();
}
