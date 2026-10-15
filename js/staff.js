cat << 'EOF' > js/staff.js
import { supabase, getConfig } from './supabase.js';

let meseroActual = null;

document.addEventListener('DOMContentLoaded', async () => {
    const { data } = await supabase.from('meseros').select('*');
    const select = document.getElementById('staff-select-mesero');
    if (data) data.forEach(m => select.innerHTML += `<option value="${m.id}">${m.nombre}</option>`);

    document.getElementById('btn-staff-login').addEventListener('click', async () => {
        const id = select.value;
        const pass = document.getElementById('staff-pass').value;
        const m = data.find(x => x.id == id);

        if (m && m.password === pass) {
            meseroActual = m;
            document.getElementById('staff-orders-section').classList.remove('hidden');
            cargarPedidosStaff();
        } else {
            alert('Contraseña de mesero incorrecta');
        }
    });
});

async function cargarPedidosStaff() {
    const { data } = await supabase.from('pedidos').select('*').eq('mesero_id', meseroActual.id).order('id', { ascending: false });
    const list = document.getElementById('staff-pedidos-list');
    list.innerHTML = data.map(p => `
        <div style="background:#0f172a; padding:10px; margin-bottom:8px; border-radius:6px;">
            <b>Mesa/Cliente: ${p.cliente_mesa}</b> | Total: $${p.total} | Estado: <b>${p.estado}</b><br>
            <button class="btn btn-danger" style="margin-top:5px;" onclick="cancelarStaff(${p.id})">Cancelar Pedido</button>
        </div>
    `).join('');
}

window.cancelarStaff = async (id) => {
    const adminPass = await getConfig('admin_password') || 'ROXANA';
    const p = prompt('Ingrese contraseña de ADMINISTRACIÓN para cancelar este pedido:');
    if (p === adminPass) {
        await supabase.from('pedidos').update({ estado: 'cancelado' }).eq('id', id);
        alert('Pedido cancelado por administración.');
        cargarPedidosStaff();
    } else alert('Contraseña de administración incorrecta.');
};
EOF
