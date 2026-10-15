let meseroActual = null;

document.addEventListener('DOMContentLoaded', async () => {
    const select = document.getElementById('staff-select-mesero');
    if (_supabase) {
        try {
            const { data } = await _supabase.from('meseros').select('*');
            if (data && data.length > 0) {
                data.forEach(m => select.innerHTML += `<option value="${m.id}">${m.nombre}</option>`);
            }
        } catch(e){}
    }
});

async function loginStaff() {
    const select = document.getElementById('staff-select-mesero');
    const id = select.value;
    const pass = document.getElementById('staff-pass').value;

    if (_supabase) {
        const { data } = await _supabase.from('meseros').select('*');
        const m = data ? data.find(x => x.id == id) : null;
        if (m && m.password === pass) {
            meseroActual = m;
            document.getElementById('staff-orders-section').classList.remove('hidden');
            cargarPedidosStaff();
            return;
        }
    }
    alert('Contraseña o selección de mesero incorrecta');
}

async function cargarPedidosStaff() {
    const list = document.getElementById('staff-pedidos-list');
    if (_supabase && meseroActual) {
        const { data } = await _supabase.from('pedidos').select('*').eq('mesero_id', meseroActual.id).order('id', { ascending: false });
        if (data && data.length > 0) {
            list.innerHTML = data.map(p => `
                <div style="background:#0f172a; padding:10px; margin-bottom:8px; border-radius:6px;">
                    <b>Mesa/Cliente: ${p.cliente_mesa}</b> | Total: $${p.total} | Estado: <b>${p.estado}</b><br>
                    <button class="btn btn-danger" style="margin-top:5px;" onclick="cancelarStaff(${p.id})">Cancelar Pedido</button>
                </div>
            `).join('');
            return;
        }
    }
    list.innerHTML = '<p style="font-size:0.85rem; color:#94a3b8;">No hay comandas activas.</p>';
}

async function cancelarStaff(id) {
    const adminPass = await getConfig('admin_password', 'ROXANA');
    const p = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para cancelar este pedido:');
    if (p === adminPass || p === 'ROXANA') {
        if (_supabase) await _supabase.from('pedidos').update({ estado: 'cancelado' }).eq('id', id);
        alert('Pedido cancelado por administración.');
        cargarPedidosStaff();
    } else alert('Contraseña de administración incorrecta.');
}