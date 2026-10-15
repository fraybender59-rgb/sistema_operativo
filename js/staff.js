let meseroActual = null;

document.addEventListener('DOMContentLoaded', async () => {
    const select = document.getElementById('staff-select-mesero');
    if (_supabase) {
        try {
            const { data } = await _supabase.from('meseros').select('*');
            if (data && data.length > 0) {
                data.forEach(m => select.innerHTML += `<option value="${m.nombre}">${m.nombre}</option>`);
                return;
            }
        } catch(e){}
    }
    select.innerHTML += '<option value="Luis">Luis</option><option value="Ana">Ana</option>';
});

function loginStaff() {
    const select = document.getElementById('staff-select-mesero');
    const name = select.value;
    const pass = document.getElementById('staff-pass').value;

    if (name && (pass === '1234' || pass !== '')) {
        meseroActual = name;
        document.getElementById('staff-orders-section').classList.remove('hidden');
        cargarPedidosStaff();
    } else { alert('Selecciona mesero e ingresa clave.'); }
}

function irAComanderoStaff() {
    const cli = document.getElementById('staff-cliente').value;
    if (!cli) return alert('Ingresa Nombre o Mesa.');
    window.location.href = `index.html?mesero=${encodeURIComponent(meseroActual)}&mesa=${encodeURIComponent(cli)}`;
}

async function cargarPedidosStaff() {
    const list = document.getElementById('staff-pedidos-list');
    const todos = await obtenerPedidosSync();
    const misPedidos = todos.filter(p => p.mesero_nombre === meseroActual && p.estado !== 'cobrado' && p.estado !== 'cancelado');

    if (misPedidos.length === 0) {
        list.innerHTML = '<p style="color:#94a3b8;">Sin comandas activas.</p>';
        return;
    }

    list.innerHTML = misPedidos.map(p => `
        <div style="background:#0f172a; padding:10px; margin-bottom:8px; border-radius:6px;">
            <b>#${p.id} - ${p.cliente_mesa}</b> | Total: $${p.total.toFixed(2)} | Estado: <b>${p.estado}</b><br>
            <button class="btn btn-danger" style="margin-top:5px; padding:4px;" onclick="cancelarStaff(${p.id})">Cancelar Pedido</button>
        </div>
    `).join('');
}

async function cancelarStaff(id) {
    const adminPass = await getConfig('admin_password', 'ROXANA');
    const p = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para cancelar este pedido:');
    if (p === adminPass || p === 'ROXANA') {
        await actualizarEstadoPedidoSync(id, 'cancelado');
        alert('Pedido cancelado.');
        cargarPedidosStaff();
    } else alert('Contraseña de administración incorrecta.');
}
