let currentAdminPass = 'ROXANA';
let tabActiva = 'Clientes';
let pedidoEnCobroTransf = null;
let miTokenSesion = localStorage.getItem('my_session_token') || '';

const CATALOGO_MENU = [
    { id: 1, categoria: 'Cócteles', nombre: 'Cóctel de Camarón Grande', precio: 150.00 },
    { id: 2, categoria: 'Cócteles', nombre: 'Cóctel camaron chico', precio: 120.00 },
    { id: 3, categoria: 'Céviches', nombre: 'Ceviche de Camarón grande', precio: 140.00 },
    { id: 4, categoria: 'Céviches', nombre: 'Ceviche de Camarones chico', precio: 110.00 },
    { id: 5, categoria: 'Céviches', nombre: 'Ceviche de pescado grande', precio: 130.00 },
    { id: 6, categoria: 'Céviches', nombre: 'Ceviche de pescado chic', precio: 130.00 },
    { id: 7, categoria: 'Aguachiles', nombre: 'Aguachile de Camarón', precio: 80.00 },
    { id: 8, categoria: 'Aguachiles', nombre: 'Aguachile de Pescado', precio: 70.00 },
    { id: 9, categoria: 'Tacos', nombre: 'orden tacos gobernador (4 tacos)', precio: 220.00 },
    { id: 10, categoria: 'Tacos', nombre: 'Orden tacos estilo baja (4 tacos)', precio: 200.00 },
    { id: 11, categoria: 'Combos', nombre: 'Combo Tacos Gobernador + Corona', precio: 220.00 },
    { id: 12, categoria: 'Combos', nombre: 'Combo Cóctel Camarón + Corona', precio: 160.00 },
    { id: 13, categoria: 'Combos', nombre: 'Combo Aguachile Camarón + Corona', precio: 100.00 }
];

document.addEventListener('DOMContentLoaded', () => {
    limpiarHistorialViejo();
    syncPass();
});

function limpiarHistorialViejo() {
    try {
        let cortes = JSON.parse(localStorage.getItem('mar_y_sazon_cortes') || '[]');
        const hace30Dias = Date.now() - (30 * 24 * 60 * 60 * 1000);
        cortes = cortes.filter(c => (c.timestamp || Date.now()) > hace30Dias);
        localStorage.setItem('mar_y_sazon_cortes', JSON.stringify(cortes));
    } catch(e){}
}

async function syncPass() {
    const p = await getConfig('admin_password', 'ROXANA');
    if (p) currentAdminPass = p;
}

async function loginAdmin() {
    const input = document.getElementById('admin-pass-input').value.trim();
    if (input === currentAdminPass || input === 'ROXANA') {
        miTokenSesion = Date.now().toString();
        localStorage.setItem('my_session_token', miTokenSesion);
        await setConfig('admin_session_token', miTokenSesion);

        document.getElementById('admin-login-modal').classList.add('hidden');
        document.getElementById('admin-panel').classList.remove('hidden');
        cargarAdmin();
    } else { alert('❌ Contraseña incorrecta'); }
}

function cerrarAdmin() {
    localStorage.removeItem('my_session_token');
    miTokenSesion = '';
    const inputPass = document.getElementById('admin-pass-input');
    if (inputPass) inputPass.value = '';
    const panel = document.getElementById('admin-panel');
    const modal = document.getElementById('admin-login-modal');
    if (panel) panel.classList.add('hidden');
    if (modal) modal.classList.remove('hidden');
}

async function cerrarSesionTodos() {
    const nuevoToken = 'CLOSED_' + Date.now();
    await setConfig('admin_session_token', nuevoToken);
    alert('🔒 Sesión cerrada globalmente en TODOS los navegadores.');
    cerrarAdmin();
}

async function verificarSesionGlobal() {
    const panel = document.getElementById('admin-panel');
    if (panel && !panel.classList.contains('hidden')) {
        const tokenRemoto = await getConfig('admin_session_token', '');
        if (tokenRemoto && miTokenSesion && tokenRemoto !== miTokenSesion) {
            alert('🔒 Sesión cerrada remotamente desde otro dispositivo o por un Corte del Día.');
            cerrarAdmin();
        }
    }
}

async function cargarAdmin() {
    actualizarBotonSinMeseros();
    renderCajaPrincipal();
    cargarMeserosAdmin();
    cargarSlideshowPreview();
    setInterval(renderCajaPrincipal, 4000);
    setInterval(verificarSesionGlobal, 2000);
}

async function actualizarBotonSinMeseros() {
    const sinMeseros = await getConfig('modo_sin_meseros', 'false');
    const btn = document.getElementById('btn-toggle-sin-meseros');
    if (!btn) return;
    if (sinMeseros === 'true') {
        btn.innerHTML = '✅ Modo "Sin Meseros" ACTIVADO (Clic para desactivar)';
        btn.className = 'btn btn-danger';
    } else {
        btn.innerHTML = '🚫 Modo "Sin Meseros" DESACTIVADO (Clic para activar)';
        btn.className = 'btn btn-warning';
    }
}

async function toggleModoSinMeseros() {
    const actual = await getConfig('modo_sin_meseros', 'false');
    const nuevo = actual === 'true' ? 'false' : 'true';
    await setConfig('modo_sin_meseros', nuevo);
    actualizarBotonSinMeseros();
    alert(`Modo Sin Meseros ${nuevo === 'true' ? 'ACTIVADO' : 'DESACTIVADO'}.`);
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
                <button class="btn btn-warning" style="padding:6px;" onclick="solicitarComprobanteTransferencia(${p.id})">💳 Cobrar Transf.</button>
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

function solicitarComprobanteTransferencia(id) {
    pedidoEnCobroTransf = id;
    document.getElementById('file-comprobante').value = '';
    document.getElementById('modal-subir-comprobante').classList.remove('hidden');
}

function cerrarModalComprobante() {
    document.getElementById('modal-subir-comprobante').classList.add('hidden');
}

async function confirmarCobroTransferencia() {
    const fileInput = document.getElementById('file-comprobante');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onloadend = async () => {
            await actualizarEstadoPedidoSync(pedidoEnCobroTransf, 'cobrado', 'Transferencia', reader.result);
            alert(`Cuenta #${pedidoEnCobroTransf} cobrada con Transferencia y Comprobante Adjunto.`);
            cerrarModalComprobante();
            renderCajaPrincipal();
        };
        reader.readAsDataURL(file);
    } else {
        await actualizarEstadoPedidoSync(pedidoEnCobroTransf, 'cobrado', 'Transferencia', null);
        alert(`Cuenta #${pedidoEnCobroTransf} cobrada con Transferencia.`);
        cerrarModalComprobante();
        renderCajaPrincipal();
    }
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
        const totEfectivo = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Efectivo')).reduce((sum, p) => sum + p.total, 0);
        const totTransf = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Transferencia')).reduce((sum, p) => sum + p.total, 0);
        const totalGen = totEfectivo + totTransf;

        const html = `
            <p style="font-size:1.1rem; margin:5px 0;">💵 <b>Efectivo:</b> $${totEfectivo.toFixed(2)}</p>
            <p style="font-size:1.1rem; margin:5px 0;">💳 <b>Transferencias:</b> $${totTransf.toFixed(2)}</p>
            <hr style="border-color:#334155; margin:10px 0;">
            <p style="font-size:1.3rem; color:#10b981; margin:5px 0;"><b>Total General: $${totalGen.toFixed(2)}</b></p>

            <button class="btn btn-warning" style="margin-top:15px; padding:12px; font-size:1rem; font-weight:bold;" onclick="ejecutarCorteConRespaldo()">🌅 REALIZAR CORTE DEL DÍA (Guarda en Historial x 1 Mes, Limpia Comprobantes y Cierra Sesión)</button>
            <button class="btn btn-danger" style="margin-top:10px; padding:10px; font-size:0.9rem;" onclick="cerrarSesionTodos()">🔒 Cerrar Sesión en TODOS los Navegadores Ahora</button>
        `;

        showModalGen('💰 Corte de Caja Hoy', html);
    });
}

async function ejecutarCorteConRespaldo() {
    const pass = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para procesar el Corte del Día:');
    if (pass !== currentAdminPass && pass !== 'ROXANA') return alert('❌ Contraseña incorrecta.');

    const todos = await obtenerPedidosSync();
    const cobrados = todos.filter(p => p.estado === 'cobrado');

    const totEfectivo = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Efectivo')).reduce((sum, p) => sum + p.total, 0);
    const totTransf = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Transferencia')).reduce((sum, p) => sum + p.total, 0);
    const totalGen = totEfectivo + totTransf;

    const comprobantes = cobrados.filter(p => p.comprobante_img).map(p => ({
        id: p.id,
        cliente: p.cliente_mesa,
        total: p.total,
        img: p.comprobante_img
    }));

    const hoyStr = new Date().toLocaleDateString('es-MX', { year: 'numeric', month: '2-digit', day: '2-digit' });

    const nuevoCorte = {
        fecha: hoyStr,
        timestamp: Date.now(),
        efectivo: totEfectivo,
        transferencia: totTransf,
        total: totalGen,
        comprobantes: comprobantes,
        pedidos: cobrados
    };

    // ALMACENAR CORTE + COMPROBANTES EN HISTORIAL (SE CONSERVA 1 MES / 30 DÍAS)
    let cortes = JSON.parse(localStorage.getItem('mar_y_sazon_cortes') || '[]');
    cortes.unshift(nuevoCorte);
    localStorage.setItem('mar_y_sazon_cortes', JSON.stringify(cortes));

    // LIMPIAR COMPROBANTES DEL BOTÓN "VER COMPROBANTES"
    let pedidos = getPedidosLocales();
    pedidos.forEach(p => { p.comprobante_img = null; });
    savePedidosLocales(pedidos);

    if (_supabase) {
        try {
            await _supabase.from('pedidos').update({ comprobante_img: null }).neq('id', 0);
        } catch(e){}
    }

    // CIERRA SESIÓN GLOBALMENTE
    const nuevoToken = 'CORTE_' + Date.now();
    await setConfig('admin_session_token', nuevoToken);

    alert(`✅ Corte del día (${hoyStr}) realizado exitosamente:
- Resumen y Comprobantes guardados en Historial por 1 Mes.
- Botón "Ver Comprobantes" limpiado.
- Sesión de Administración CERRADA en todos los dispositivos.`);
    cerrarModalGeneric();
    cerrarAdmin();
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

async function abrirModalComprobantes() {
    const todos = await obtenerPedidosSync();
    const conComprobante = todos.filter(p => p.comprobante_img);
    
    let html = `
        <div style="margin-bottom:12px; text-align:center;">
            <button class="btn btn-danger" style="padding:8px 12px; font-size:0.85rem;" onclick="vaciarTodosComprobantes()">🗑️ Borrar TODOS los Comprobantes</button>
        </div>
    `;

    if (conComprobante.length === 0) {
        html += '<p style="color:#94a3b8; text-align:center;">No hay fotos de comprobantes activas.</p>';
    } else {
        html += conComprobante.map(p => `
            <div style="border-bottom:1px solid #334155; padding:10px 0; text-align:center;">
                <b>#${p.id} - ${p.cliente_mesa} ($${p.total.toFixed(2)})</b><br>
                <img src="${p.comprobante_img}" style="max-width:100%; height:auto; border-radius:8px; margin:8px 0; border:1px solid #334155;"><br>
                <button class="btn btn-danger" style="width:auto; padding:6px 12px; font-size:0.85rem;" onclick="borrarComprobanteFoto('${p.id}')">🗑️ Eliminar esta Foto</button>
            </div>
        `).join('');
    }

    showModalGen('📸 Comprobantes de Pago', html);
}

async function borrarComprobanteFoto(id) {
    let pedidos = getPedidosLocales();
    let target = pedidos.find(p => p.id == id);
    if (target) target.comprobante_img = null;
    savePedidosLocales(pedidos);

    if (_supabase) {
        try {
            await _supabase.from('pedidos').update({ comprobante_img: null }).eq('id', id);
        } catch(e) {}
    }
    alert('✅ Foto eliminada.');
    abrirModalComprobantes();
}

async function vaciarTodosComprobantes() {
    const pass = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para borrar todas las fotos:');
    if (pass === currentAdminPass || pass === 'ROXANA') {
        let pedidos = getPedidosLocales();
        pedidos.forEach(p => { p.comprobante_img = null; });
        savePedidosLocales(pedidos);

        if (_supabase) {
            try {
                await _supabase.from('pedidos').update({ comprobante_img: null }).neq('id', 0);
            } catch(e) {}
        }
        alert('✅ Todas las fotos activas eliminadas.');
        abrirModalComprobantes();
    } else {
        alert('❌ Contraseña incorrecta.');
    }
}

function abrirModalHistorial() {
    limpiarHistorialViejo();
    const cortes = JSON.parse(localStorage.getItem('mar_y_sazon_cortes') || '[]');
    if (cortes.length === 0) {
        showModalGen('📅 Historial de Cortes por Día', '<p style="color:#94a3b8;">No hay cortes de caja archivados.</p>');
        return;
    }

    let html = '<div style="display:flex; flex-direction:column; gap:10px;">';
    cortes.forEach((c, idx) => {
        html += `
            <div style="background:#0f172a; padding:10px; border-radius:8px; border:1px solid #334155;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:var(--accent);">📅 Fecha: ${c.fecha}</b>
                    <b style="color:#10b981;">Total: $${c.total.toFixed(2)}</b>
                </div>
                <div style="font-size:0.85rem; margin-top:4px; color:#cbd5e1;">
                    💵 Efectivo: $${c.efectivo.toFixed(2)} | 💳 Transf/Tarjeta: $${c.transferencia.toFixed(2)}
                </div>
                <button class="btn" style="margin-top:8px; padding:6px; font-size:0.85rem;" onclick="verDetalleCorte(${idx})">🔍 Ver Cobros y Comprobantes Archivados</button>
            </div>
        `;
    });
    html += '</div>';

    showModalGen('📅 Historial de Cortes por Día (Archivado 30 días)', html);
}

function verDetalleCorte(idx) {
    const cortes = JSON.parse(localStorage.getItem('mar_y_sazon_cortes') || '[]');
    const c = cortes[idx];
    if (!c) return;

    let html = `
        <h4>Corte del ${c.fecha}</h4>
        <p>💵 Efectivo: $${c.efectivo.toFixed(2)} | 💳 Transferencia: $${c.transferencia.toFixed(2)}</p>
        <p style="color:#10b981; font-weight:bold;">Total Día: $${c.total.toFixed(2)}</p>
        <hr style="border-color:#334155;">
        <h5>📸 Comprobantes Archivados del Día:</h5>
    `;

    if (c.comprobantes && c.comprobantes.length > 0) {
        c.comprobantes.forEach(comp => {
            html += `
                <div style="text-align:center; margin-bottom:10px; background:#0f172a; padding:8px; border-radius:6px;">
                    <small>#${comp.id} - ${comp.cliente} ($${comp.total.toFixed(2)})</small><br>
                    <img src="${comp.img}" style="max-width:100%; border-radius:6px; margin-top:5px; border:1px solid #334155;">
                </div>
            `;
        });
    } else {
        html += '<p style="font-size:0.85rem; color:#94a3b8;">Sin comprobantes registrados en este día.</p>';
    }

    showModalGen(`Detalle Corte ${c.fecha}`, html);
}

async function abrirModalPrecios() {
    let html = '<div style="display:flex; flex-direction:column; gap:10px;">';
    
    CATALOGO_MENU.forEach(item => {
        const pLocal = localStorage.getItem(`precio_prod_${item.id}`) || item.precio;
        html += `
            <div style="background:#0f172a; padding:10px; border-radius:6px; display:flex; justify-content:space-between; align-items:center; border:1px solid #334155;">
                <div>
                    <b>${item.nombre}</b><br>
                    <small style="color:#f59e0b;">Precio actual: $${parseFloat(pLocal).toFixed(2)}</small>
                </div>
                <button class="btn btn-warning" style="width:auto; padding:6px 12px;" onclick="editarPrecioProducto(${item.id}, '${item.nombre}', ${pLocal})">✏️ Modificar</button>
            </div>
        `;
    });
    
    html += '</div>';
    showModalGen('✏️ Configuración de Precios', html);
}

async function editarPrecioProducto(id, nombre, precioActual) {
    const nuevo = prompt(`Ingrese el nuevo precio para "${nombre}":`, precioActual);
    if (nuevo !== null && !isNaN(nuevo) && nuevo.trim() !== '') {
        const pass = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para confirmar y aplicar el cambio:');
        if (pass === currentAdminPass || pass === 'ROXANA') {
            await actualizarPrecioProducto(id, parseFloat(nuevo));
            alert(`✅ El precio de "${nombre}" ha sido actualizado a $${parseFloat(nuevo).toFixed(2)}.`);
            abrirModalPrecios();
        } else {
            alert('❌ Contraseña de administración incorrecta. Cambio rechazado.');
        }
    }
}

function abrirModalTarjeta() {
    cambiarCuentaBancaria();
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

async function cambiarCuentaBancaria() {
    const cuentaActual = await getConfig('cuenta_transferencia', '1234 5678 9012 3456 (BBVA)');
    const nuevaCuenta = prompt('Ingrese el NUEVO número de cuenta bancaria:', cuentaActual);
    if (nuevaCuenta) {
        await setConfig('cuenta_transferencia', nuevaCuenta);
        alert('Cuenta bancaria actualizada correctamente.');
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
