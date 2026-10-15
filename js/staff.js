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
    cargarPedidosStaffGral();
});

function ingresarMenuStaff() {
    const select = document.getElementById('staff-select-mesero');
    const name = select.value;
    const pass = document.getElementById('staff-pass').value;
    const mesa = document.getElementById('staff-cliente').value;

    if (!name || !pass || !mesa) return alert('Por favor selecciona Mesero, Contraseña y Mesa/Cliente.');

    // Redirigir directamente al menú en Modo Staff sin forma de pago
    window.location.href = `index.html?origen=Staff&mesero=${encodeURIComponent(name)}&mesa=${encodeURIComponent(mesa)}`;
}

async function cargarPedidosStaffGral() {
    const list = document.getElementById('staff-pedidos-list');
    const todos = await obtenerPedidosSync();
    const staffPedidos = todos.filter(p => p.origen === 'Staff' && p.estado !== 'cobrado' && p.estado !== 'cancelado');

    if (staffPedidos.length === 0) {
        list.innerHTML = '<p style="color:#94a3b8; font-size:0.85rem;">Sin comandas activas de staff.</p>';
        return;
    }

    list.innerHTML = staffPedidos.map(p => `
        <div style="background:#0f172a; padding:10px; margin-bottom:8px; border-radius:6px;">
            <b>#${p.id} - ${p.cliente_mesa}</b> | Total: $${p.total.toFixed(2)} | Atiende: <b>${p.mesero_nombre}</b><br>
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
        cargarPedidosStaffGral();
    } else alert('Contraseña de administración incorrecta.');
}
