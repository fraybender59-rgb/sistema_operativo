cat << 'EOF' > staff.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Punto Staff - Mar y Sazón</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header>
        <h1>👨‍🍳 Punto Staff - Meseros</h1>
    </header>

    <div class="admin-grid">
        <div class="admin-card">
            <h3>Identificación de Mesero</h3>
            <select id="staff-select-mesero"><option value="">Selecciona tu Nombre...</option></select>
            <input type="password" id="staff-pass" placeholder="Contraseña Mesero" style="margin-top:8px;">
            <button class="btn btn-success" id="btn-staff-login" style="margin-top:8px;">Ver Mis Comandas</button>
        </div>

        <div id="staff-orders-section" class="admin-card hidden">
            <h3>Comandas de Mis Mesas</h3>
            <div id="staff-pedidos-list"></div>
        </div>
    </div>

    <script type="module" src="js/staff.js"></script>
</body>
</html>
EOF

cat << 'EOF' > js/staff.js
import { supabase, getConfig } from './supabase.js';

let meseroActual = null;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const { data } = await supabase.from('meseros').select('*');
        const select = document.getElementById('staff-select-mesero');
        if (data && data.length > 0) {
            data.forEach(m => select.innerHTML += `<option value="${m.id}">${m.nombre}</option>`);
        }
    } catch(e){}

    document.getElementById('btn-staff-login').addEventListener('click', async () => {
        const id = document.getElementById('staff-select-mesero').value;
        const pass = document.getElementById('staff-pass').value;

        const { data } = await supabase.from('meseros').select('*');
        const m = data ? data.find(x => x.id == id) : null;

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
    if (!data || data.length === 0) {
        list.innerHTML = '<p style="font-size:0.85rem; color:#94a3b8;">No tienes comandas registradas.</p>';
        return;
    }
    list.innerHTML = data.map(p => `
        <div style="background:#0f172a; padding:10px; margin-bottom:8px; border-radius:6px;">
            <b>Mesa/Cliente: ${p.cliente_mesa}</b> | Total: $${p.total} | Estado: <b>${p.estado}</b><br>
            <button class="btn btn-danger" style="margin-top:5px;" onclick="window.cancelarStaff(${p.id})">Cancelar Pedido</button>
        </div>
    `).join('');
}

window.cancelarStaff = async (id) => {
    const adminPass = await getConfig('admin_password', 'ROXANA');
    const p = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para cancelar este pedido:');
    if (p === adminPass || p === 'ROXANA') {
        await supabase.from('pedidos').update({ estado: 'cancelado' }).eq('id', id);
        alert('Pedido cancelado por administración.');
        cargarPedidosStaff();
    } else alert('Contraseña de administración incorrecta.');
};
EOF
