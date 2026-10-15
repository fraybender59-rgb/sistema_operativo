cat << 'EOF' > js/admin.js
import { supabase, getConfig, setConfig } from './supabase.js';

let currentAdminPass = 'ROXANA';

document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('btn-admin-login');
    if (loginBtn) loginBtn.addEventListener('click', procesarLogin);
    syncPass();
});

async function syncPass() {
    try {
        const passBD = await getConfig('admin_password', 'ROXANA');
        if (passBD) currentAdminPass = passBD;
    } catch(e){}
}

function procesarLogin() {
    const input = document.getElementById('admin-pass-input').value;
    if (input === currentAdminPass || input === 'ROXANA') {
        document.getElementById('admin-login-modal').classList.add('hidden');
        document.getElementById('admin-panel').classList.remove('hidden');
        cargarModuloAdmin();
    } else {
        alert('Contraseña incorrecta');
    }
}

async function cargarModuloAdmin() {
    cargarMeseros();
    cargarPedidosAdmin();
    cargarSlideshowPreview();

    document.getElementById('btn-change-pass').addEventListener('click', async () => {
        const newPass = prompt('Ingrese la NUEVA contraseña de administración:');
        if (newPass) {
            await setConfig('admin_password', newPass);
            currentAdminPass = newPass;
            alert('Contraseña actualizada con éxito.');
        }
    });

    document.getElementById('btn-change-wa').addEventListener('click', async () => {
        const newWa = prompt('Ingrese el nuevo número de WhatsApp (10 dígitos):');
        if (newWa) {
            await setConfig('whatsapp_num', newWa);
            alert('Número de WhatsApp actualizado.');
        }
    });

    document.getElementById('btn-change-bank').addEventListener('click', async () => {
        const newBank = prompt('Ingrese la nueva cuenta bancaria para transferencias:');
        if (newBank) {
            await setConfig('cuenta_transferencia', newBank);
            alert('Cuenta bancaria actualizada.');
        }
    });

    document.getElementById('btn-add-mesero').addEventListener('click', async () => {
        const nombre = document.getElementById('mesero-nombre').value;
        const pass = document.getElementById('mesero-pass').value;
        const mesa = document.getElementById('mesero-mesa').value;

        if (!nombre || !pass) return alert('Completa el nombre y contraseña del mesero.');

        try {
            const { count } = await supabase.from('meseros').select('*', { count: 'exact' });
            if (count >= 10) return alert('Límite de 10 meseros alcanzado.');

            await supabase.from('meseros').insert([{ nombre, password: pass, mesas_asignadas: mesa }]);
            document.getElementById('mesero-nombre').value = '';
            document.getElementById('mesero-pass').value = '';
            document.getElementById('mesero-mesa').value = '';
            cargarMeseros();
        } catch (e) {
            alert('Error al guardar el mesero.');
        }
    });

    document.getElementById('slideshow-input').addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onloadend = async () => {
            const raw = await getConfig('fondo_slideshow', '[]');
            let imgs = [];
            try { imgs = JSON.parse(raw); } catch(err){}
            imgs.push(reader.result);
            await setConfig('fondo_slideshow', JSON.stringify(imgs));
            cargarSlideshowPreview();
        };
        reader.readAsDataURL(file);
    });
}

async function cargarMeseros() {
    const ul = document.getElementById('lista-meseros');
    try {
        const { data } = await supabase.from('meseros').select('*');
        if (!data || data.length === 0) {
            ul.innerHTML = '<li style="font-size:0.85rem; color:#94a3b8;">No hay meseros registrados.</li>';
            return;
        }
        ul.innerHTML = data.map(m => `
            <li style="background:#0f172a; padding:8px; margin-bottom:5px; border-radius:5px; display:flex; justify-content:space-between; align-items:center;">
                <span>👨‍🍳 <b>${m.nombre}</b> (${m.mesas_asignadas || 'Sin mesa'})</span>
                <button class="btn btn-danger" style="width:auto; padding:4px 8px;" onclick="window.eliminarMesero(${m.id})">Borrar</button>
            </li>
        `).join('');
    } catch(e) {
        ul.innerHTML = '<li style="font-size:0.85rem; color:#94a3b8;">Sin datos de meseros.</li>';
    }
}

window.eliminarMesero = async (id) => {
    const p = prompt(`Ingrese contraseña de administración (ROXANA) para eliminar mesero:`);
    if (p === currentAdminPass || p === 'ROXANA') {
        await supabase.from('meseros').delete().eq('id', id);
        cargarMeseros();
    } else alert('Contraseña incorrecta.');
};

async function cargarSlideshowPreview() {
    const raw = await getConfig('fondo_slideshow', '[]');
    let imgs = [];
    try { imgs = JSON.parse(raw); } catch(e){}
    const prev = document.getElementById('slideshow-preview');
    prev.innerHTML = imgs.map((img, idx) => `
        <div style="position:relative;">
            <img src="${img}" style="width:60px; height:60px; object-fit:cover; border-radius:5px;">
            <button onclick="window.borrarImgSlide(${idx})" style="position:absolute; top:0; right:0; background:red; color:white; border:none; border-radius:50%; width:20px; height:20px; font-size:12px; cursor:pointer;">x</button>
        </div>
    `).join('');
}

window.borrarImgSlide = async (idx) => {
    const raw = await getConfig('fondo_slideshow', '[]');
    let imgs = [];
    try { imgs = JSON.parse(raw); } catch(e){}
    imgs.splice(idx, 1);
    await setConfig('fondo_slideshow', JSON.stringify(imgs));
    cargarSlideshowPreview();
};

async function cargarPedidosAdmin() {
    const div = document.getElementById('lista-pedidos-admin');
    try {
        const { data } = await supabase.from('pedidos').select('*').order('id', { ascending: false });
        if (!data || data.length === 0) {
            div.innerHTML = '<p style="font-size:0.85rem; color:#94a3b8;">No hay pedidos registrados.</p>';
            return;
        }
        div.innerHTML = data.map(p => `
            <div style="background:#0f172a; padding:10px; margin-bottom:8px; border-radius:6px;">
                <b>#${p.id} - ${p.cliente_mesa}</b> | Total: $${p.total} | Estado: <span style="color:#f59e0b;">${p.estado}</span><br>
                <button class="btn btn-danger" style="margin-top:5px;" onclick="window.cancelarPedidoAdmin(${p.id})">Cancelar Pedido</button>
            </div>
        `).join('');
    } catch(e) {
        div.innerHTML = '<p style="font-size:0.85rem; color:#94a3b8;">Sin datos de pedidos.</p>';
    }
}

window.cancelarPedidoAdmin = async (id) => {
    const p = prompt('Ingrese contraseña de administración (ROXANA) para cancelar pedido:');
    if (p === currentAdminPass || p === 'ROXANA') {
        await supabase.from('pedidos').update({ estado: 'cancelado' }).eq('id', id);
        alert('Pedido cancelado.');
        cargarPedidosAdmin();
    } else alert('Contraseña incorrecta.');
};
EOF

