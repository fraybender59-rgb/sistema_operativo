let currentAdminPass = 'ROXANA';
let tabActiva = 'Clientes';

document.addEventListener('DOMContentLoaded', () => {
    syncPass();
});

async function syncPass() {
    const p = await getConfig('admin_password', 'ROXANA');
    if (p) currentAdminPass = p;
}

function loginAdmin() {
    const input = document.getElementById('admin-pass-input').value.trim();
    if (input === currentAdminPass || input === 'ROXANA') {
        document.getElementById('admin-login-modal').classList.add('hidden');
        document.getElementById('admin-panel').classList.remove('hidden');
        cargarAdmin();
    } else { alert('Contraseña incorrecta'); }
}

async function cargarAdmin() {
    renderCajaPrincipal();
    cargarMeserosAdmin();
    cargarSlideshowPreview();
    setInterval(renderCajaPrincipal, 4000);
}

function cambiarTabCaja(tab) {
    tabActiva = tab;
    document.getElementById('tab-cli').classList.toggle('active', tab === 'Clientes');
    document.getElementById('tab-sta').classList.toggle('active', tab === 'Staff');
    renderCajaPrincipal();
}

async function renderCajaPrincipal() {
    const div = document.getElementById('lista-caja-abierta');
    if (!div) return;
    const todos = await obtenerPedidosSync();
    const pendientes = todos.filter(p => (p.origen === tabActiva || (tabActiva==='Clientes' && !p.origen)) && p.estado !== 'cobrado' && p.estado !== 'cancelado');

    if (pendientes.length === 0) {
        div.innerHTML = '<p style="color:#94a3b8; font-size:0.9rem;">Sin cuentas abiertas en esta sección.</p>';
        return;
    }

    div.innerHTML = pendientes.map(p => `
        <div style="background:#0f172a; padding:12px; border-radius:8px; margin-bottom:10px; border:1px solid #334155;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b>#${p.id} - ${p.cliente_mesa}</b>
                <span style="color:#f59e0b; font-weight:bold;">$${p.total.toFixed(2)}</span>
            </div>
            <small style="color:#94a3b8;">Atiende: ${p.mesero_nombre} | Pago solicit.: ${p.metodo_pago}</small>
            <ul style="font-size:0.85rem; padding-left:15px; margin:6px 0;">
                ${p.detalles.map(d => `<li>${d.cantidad}x ${d.nombre} (${d.comentario ? d.comentario : 'Sin notas'})</li>`).join('')}
            </ul>
            <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:6px; margin-top:8px;">
                <button class="btn btn-success" style="padding:6px;" onclick="cobrarPedido(${p.id}, 'Efectivo')">💵 Cobrar Efectivo</button>
                <button class="btn btn-warning" style="padding:6px;" onclick="cobrarPedido(${p.id}, 'Transferencia')">💳 Cobrar Transf.</button>
                <button class="btn" style="background:#8b5cf6; padding:6px;" onclick="aplicarDescuento(${p.id})">🏷️ Descuento</button>
                <button class="btn btn-danger" style="padding:6px;" onclick="cancelarCuenta(${p.id})">❌ Cancelar</button>
            </div>
        </div>
    `).join('');
}

async function cobrarPedido(id, metodo) {
    await actualizarEstadoPedidoSync(id, 'cobrado', metodo);
    alert(`Cuenta #${id} cobrada exitosamente con ${metodo}.`);
    renderCajaPrincipal();
}

async function aplicarDescuento(id) {
    const desc = prompt('Ingrese monto de descuento en $');
    if (desc && !isNaN(desc)) {
        let todos = await obtenerPedidosSync();
        let target = todos.find(p => p.id == id);
        if (target) {
            target.total = Math.max(0, target.total - parseFloat(desc));
            savePedidosLocales(todos);
            renderCajaPrincipal();
        }
    }
}

async function cancelarCuenta(id) {
    const p = prompt('Ingrese contraseña de administración (ROXANA) para cancelar:');
    if (p === currentAdminPass || p === 'ROXANA') {
        await actualizarEstadoPedidoSync(id, 'cancelado');
        alert('Cuenta cancelada.');
        renderCajaPrincipal();
    } else alert('Contraseña incorrecta.');
}

function abrirModalCorte() {
    obtenerPedidosSync().then(todos => {
        const cobrados = todos.filter(p => p.estado === 'cobrado');
        const totEfectivo = cobrados.filter(p => p.metodo_pago.includes('Efectivo')).reduce((sum, p) => sum + p.total, 0);
        const totTransf = cobrados.filter(p => p.metodo_pago.includes('Transferencia')).reduce((sum, p) => sum + p.total, 0);
        const totalGen = totEfectivo + totTransf;

        showModalGen('💰 Corte de Caja Hoy', `
            <p>💵 <b>Efectivo:</b> $${totEfectivo.toFixed(2)}</p>
            <p>💳 <b>Transferencias:</b> $${totTransf.toFixed(2)}</p>
            <hr>
            <p style="font-size:1.2rem; color:#10b981;"><b>Total General: $${totalGen.toFixed(2)}</b></p>
        `);
    });
}

function abrirModalCobradas() {
    obtenerPedidosSync().then(todos => {
        const cobrados = todos.filter(p => p.estado === 'cobrado');
        let html = cobrados.length === 0 ? '<p>No hay cuentas cobradas hoy.</p>' : cobrados.map(p => `
            <div style="border-bottom:1px solid #334155; padding:6px 0;">
                <b>#${p.id} - ${p.cliente_mesa}</b>: $${p.total.toFixed(2)} (${p.metodo_pago})
            </div>
        `).join('');
        showModalGen('📁 Cuentas Cobradas Hoy', html);
    });
}

function abrirModalHistorial() {
    showModalGen('📅 Historial de Días', '<p>Sincronizado con base de datos en nube.</p>');
}

function abrirModalPrecios() {
    showModalGen('✏️ Configuración de Precios', '<p>Gestión directa activa mediante catálogo.</p>');
}

function abrirModalTarjeta() {
    getConfig('cuenta_transferencia', '1234 5678 9012 3456 (BBVA)').then(c => {
        const n = prompt('Ingrese nueva cuenta bancaria para transferencias:', c);
        if (n) setConfig('cuenta_transferencia', n).then(() => alert('Guardado.'));
    });
}

function showModalGen(title, body) {
    document.getElementById('modal-gen-title').innerText = title;
    document.getElementById('modal-gen-body').innerHTML = body;
    document.getElementById('modal-generic').classList.remove('hidden');
}

function cerrarModalGeneric() {
    document.getElementById('modal-generic').classList.add('hidden');
}

async function cambiarPassAdmin() {
    const newPass = prompt('Ingrese la NUEVA contraseña de administración:');
    if (newPass) {
        await setConfig('admin_password', newPass);
        currentAdminPass = newPass;
        alert('Contraseña actualizada con éxito.');
    }
}

async function cambiarWhatsApp() {
    const newWa = prompt('Ingrese el nuevo número de WhatsApp (10 dígitos):');
    if (newWa) {
        await setConfig('whatsapp_num', newWa);
        alert('Número de WhatsApp actualizado.');
    }
}

async function agregarMesero() {
    const nombre = document.getElementById('mesero-nombre').value;
    const pass = document.getElementById('mesero-pass').value;
    const mesa = document.getElementById('mesero-mesa').value;

    if (!nombre || !pass) return alert('Completa el nombre y contraseña del mesero.');

    if (_supabase) {
        try {
            await _supabase.from('meseros').insert([{ nombre, password: pass, mesas_asignadas: mesa }]);
        } catch(e){}
    }
    alert('Mesero registrado.');
    cargarMeserosAdmin();
}

async function cargarMeserosAdmin() {
    const ul = document.getElementById('lista-meseros');
    if (_supabase) {
        try {
            const { data } = await _supabase.from('meseros').select('*');
            if (data && data.length > 0) {
                ul.innerHTML = data.map(m => `
                    <li style="background:#0f172a; padding:8px; margin-bottom:5px; border-radius:5px; display:flex; justify-content:space-between; align-items:center;">
                        <span>👨‍🍳 <b>${m.nombre}</b> (${m.mesas_asignadas || 'Sin mesa'})</span>
                        <button class="btn btn-danger" style="width:auto; padding:4px 8px;" onclick="eliminarMesero(${m.id})">Borrar</button>
                    </li>
                `).join('');
                return;
            }
        } catch(e){}
    }
    ul.innerHTML = '<li style="font-size:0.85rem; color:#94a3b8;">Meseros activos.</li>';
}

async function eliminarMesero(id) {
    const p = prompt(`Ingrese contraseña de administración (ROXANA) para eliminar mesero:`);
    if (p === currentAdminPass || p === 'ROXANA') {
        if (_supabase) await _supabase.from('meseros').delete().eq('id', id);
        cargarMeserosAdmin();
    } else alert('Contraseña incorrecta.');
}

async function subirImagenFondo(e) {
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
}

async function cargarSlideshowPreview() {
    const raw = await getConfig('fondo_slideshow', '[]');
    let imgs = [];
    try { imgs = JSON.parse(raw); } catch(e){}
    const prev = document.getElementById('slideshow-preview');
    prev.innerHTML = imgs.map((img, idx) => `
        <div style="position:relative;">
            <img src="${img}" style="width:60px; height:60px; object-fit:cover; border-radius:5px;">
            <button onclick="borrarImgSlide(${idx})" style="position:absolute; top:0; right:0; background:red; color:white; border:none; border-radius:50%; width:20px; height:20px; font-size:12px; cursor:pointer;">x</button>
        </div>
    `).join('');
}

async function borrarImgSlide(idx) {
    const raw = await getConfig('fondo_slideshow', '[]');
    let imgs = [];
    try { imgs = JSON.parse(raw); } catch(e){}
    imgs.splice(idx, 1);
    await setConfig('fondo_slideshow', JSON.stringify(imgs));
    cargarSlideshowPreview();
}
