import os

os.makedirs('css', exist_ok=True)
os.makedirs('js', exist_ok=True)

supabase_config = """const SUPABASE_URL = 'https://atwtmuqkqypdodbhkrbe.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy';

let _supabase = null;
if (window.supabase && window.supabase.createClient) {
    _supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
}

async function getConfig(clave, defaultValue = '') {
    if (!_supabase) return localStorage.getItem(clave) || defaultValue;
    try {
        const { data } = await _supabase.from('configuracion').select('valor').eq('clave', clave).single();
        return data ? data.valor : (localStorage.getItem(clave) || defaultValue);
    } catch(e) {
        return localStorage.getItem(clave) || defaultValue;
    }
}

async function setConfig(clave, valor) {
    localStorage.setItem(clave, valor);
    if (_supabase) {
        try { await _supabase.from('configuracion').upsert({ clave, valor }); } catch(e){}
    }
}"""

index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mar y Sazón - Menú</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <div id="bg-slideshow"></div>
    <div id="bg-overlay"></div>

    <header>
        <h1>🌊 Mar y Sazón</h1>
        <div class="categories" id="cat-container"></div>
    </header>

    <main class="menu-grid" id="menu-items"></main>

    <footer class="cart-footer">
        <input type="text" id="nombre-cliente" placeholder="Mesa / Nombre del Cliente">
        <select id="select-mesero"><option value="">Selecciona Mesero...</option></select>
        <select id="metodo-pago" onchange="togglePago(this.value)">
            <option value="Efectivo">Efectivo al recibir</option>
            <option value="Transferencia">Transferencia bancaria</option>
        </select>
        <div id="info-transferencia" class="hidden" style="font-size: 0.85rem; color: #f59e0b; text-align: center;"></div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span>Total: $<b id="total-price">0.00</b></span>
            <button class="btn btn-success" onclick="enviarPedido()" style="width: auto; padding: 10px 20px;">🚀 Pedir a Cocina</button>
        </div>
    </footer>

    <div id="modal-item" class="modal hidden">
        <div class="modal-content">
            <h3 id="modal-title">Platillo</h3>
            <p id="modal-desc" style="color: #94a3b8; font-size: 0.85rem; margin:0;"></p>
            <div class="qty-control">
                <button class="qty-btn" onclick="cambiarCantidad(-1)">-</button>
                <span id="modal-qty" style="font-size: 1.5rem; font-weight: bold;">1</span>
                <button class="qty-btn" onclick="cambiarCantidad(1)">+</button>
            </div>
            <textarea id="modal-comment" rows="2" placeholder="Notas/Comentarios (Ej. Sin cebolla, picante aparte...)"></textarea>
            <button class="btn btn-success" onclick="agregarAlCarritoDesdeModal()">Agregar al Pedido</button>
            <button class="btn btn-danger" onclick="cerrarModal()">Cancelar</button>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/app.js"></script>
</body>
</html>"""

app_js = """const MENU_DEFAULT = [
    { id: 1, categoria: 'Cócteles', nombre: 'Cóctel de Camarón Grande', descripcion: 'Cóctel grande preparado con camarón fresco', precio: 150.00 },
    { id: 2, categoria: 'Cócteles', nombre: 'Cóctel camaron chico', descripcion: 'Cóctel chico de camarón fresco', precio: 120.00 },
    { id: 3, categoria: 'Céviches', nombre: 'Ceviche de Camarón grande', descripcion: 'Ceviche fresco de camarón picado', precio: 140.00 },
    { id: 4, categoria: 'Céviches', nombre: 'Ceviche de Camarones chico', descripcion: 'Porción chica de ceviche de camarón', precio: 110.00 },
    { id: 5, categoria: 'Céviches', nombre: 'Ceviche de pescado grande', descripcion: 'Ceviche tradicional de pescado fresco', precio: 130.00 },
    { id: 6, categoria: 'Céviches', nombre: 'Ceviche de pescado chic', descripcion: 'Porción chica de ceviche de pescado', precio: 130.00 },
    { id: 7, categoria: 'Aguachiles', nombre: 'Aguachile de Camarón', descripcion: 'Camarones curtidos en limón y chile', precio: 80.00 },
    { id: 8, categoria: 'Aguachiles', nombre: 'Aguachile de Pescado', descripcion: 'Pescado fresco curtido en limón', precio: 70.00 },
    { id: 9, categoria: 'Tacos', nombre: 'orden tacos gobernador (4 tacos)', descripcion: '4 tacos gobernador con camarón y queso', precio: 220.00 },
    { id: 10, categoria: 'Tacos', nombre: 'Orden tacos estilo baja (4 tacos)', descripcion: '4 tacos de pescado capeado estilo Baja', precio: 200.00 },
    { id: 11, categoria: 'Combos', nombre: 'Combo Tacos Gobernador + Corona', descripcion: '4 Tacos Gobernador + 1 Cerveza Corona', precio: 220.00 },
    { id: 12, categoria: 'Combos', nombre: 'Combo Cóctel Camarón + Corona', descripcion: '1 Cóctel de Camarón + 1 Cerveza Corona', precio: 160.00 },
    { id: 13, categoria: 'Combos', nombre: 'Combo Aguachile Camarón + Corona', descripcion: '1 Aguachile de Camarón + 1 Cerveza Corona', precio: 100.00 }
];

let menuData = [...MENU_DEFAULT];
let carrito = [];
let itemSeleccionado = null;
let cantidadTemp = 1;

document.addEventListener('DOMContentLoaded', () => {
    renderCategorias();
    renderMenu(menuData);
    cargarMeseros();
    cargarCuentaTransferencia();
    iniciarSlideshow();
});

function renderCategorias() {
    const categorias = ['Todas', ...new Set(menuData.map(i => i.categoria))];
    const catContainer = document.getElementById('cat-container');
    if (!catContainer) return;
    catContainer.innerHTML = categorias.map((cat, idx) => `
        <button class="cat-btn ${idx === 0 ? 'active' : ''}" onclick="filtrarCat('${cat}', this)">${cat}</button>
    `).join('');
}

function filtrarCat(cat, btn) {
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    if (cat === 'Todas') renderMenu(menuData);
    else renderMenu(menuData.filter(i => i.categoria === cat));
}

function renderMenu(items) {
    const grid = document.getElementById('menu-items');
    if (!grid) return;
    grid.innerHTML = items.map(item => `
        <div class="menu-card" onclick="abrirModal(${item.id})">
            <div>
                <h3>${item.nombre}</h3>
                <p style="font-size:0.8rem; color:#94a3b8; margin: 4px 0;">${item.descripcion || ''}</p>
            </div>
            <p class="price">$${item.precio}</p>
        </div>
    `).join('');
}

function abrirModal(id) {
    itemSeleccionado = menuData.find(i => i.id === id);
    if (!itemSeleccionado) return;
    cantidadTemp = 1;
    document.getElementById('modal-title').innerText = itemSeleccionado.nombre;
    document.getElementById('modal-desc').innerText = itemSeleccionado.descripcion || '';
    document.getElementById('modal-qty').innerText = 1;
    document.getElementById('modal-comment').value = '';
    document.getElementById('modal-item').classList.remove('hidden');
}

function cambiarCantidad(delta) {
    if (cantidadTemp + delta >= 1) {
        cantidadTemp += delta;
        document.getElementById('modal-qty').innerText = cantidadTemp;
    }
}

function cerrarModal() {
    document.getElementById('modal-item').classList.add('hidden');
}

function agregarAlCarritoDesdeModal() {
    const comentario = document.getElementById('modal-comment').value;
    carrito.push({
        nombre: itemSeleccionado.nombre,
        precio: parseFloat(itemSeleccionado.precio),
        cantidad: cantidadTemp,
        comentario
    });
    actualizarTotal();
    cerrarModal();
}

function actualizarTotal() {
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    document.getElementById('total-price').innerText = total.toFixed(2);
}

function togglePago(val) {
    const divInfo = document.getElementById('info-transferencia');
    if (val === 'Transferencia') divInfo.classList.remove('hidden');
    else divInfo.classList.add('hidden');
}

async function cargarMeseros() {
    const select = document.getElementById('select-mesero');
    select.innerHTML = '<option value="">Selecciona Mesero...</option>';
    if (_supabase) {
        try {
            const { data } = await _supabase.from('meseros').select('*');
            if (data && data.length > 0) {
                data.forEach(m => select.innerHTML += `<option value="${m.id}">${m.nombre}</option>`);
                return;
            }
        } catch(e){}
    }
    select.innerHTML += '<option value="1">Mesero General</option>';
}

async function cargarCuentaTransferencia() {
    const cuenta = await getConfig('cuenta_transferencia', '1234 5678 9012 3456 (BBVA)');
    document.getElementById('info-transferencia').innerText = `Transferir a: ${cuenta}`;
}

async function iniciarSlideshow() {
    const rawFondo = await getConfig('fondo_slideshow', '[]');
    let imagenes = [];
    try { imagenes = JSON.parse(rawFondo); } catch(e){}
    if (!imagenes || imagenes.length === 0) return;
    let idx = 0;
    const bgDiv = document.getElementById('bg-slideshow');
    bgDiv.style.backgroundImage = `url(${imagenes[0]})`;
    setInterval(() => {
        idx = (idx + 1) % imagenes.length;
        bgDiv.style.backgroundImage = `url(${imagenes[idx]})`;
    }, 5000);
}

async function enviarPedido() {
    const cliente = document.getElementById('nombre-cliente').value;
    const mesero_id = document.getElementById('select-mesero').value;
    const metodo_pago = document.getElementById('metodo-pago').value;

    if (!cliente || carrito.length === 0) return alert('Ingresa Nombre/Mesa y agrega platillos al pedido.');

    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    if (_supabase) {
        try {
            const { data: pedidoData } = await _supabase.from('pedidos')
                .insert([{ cliente_mesa: cliente, mesero_id: mesero_id || null, total, metodo_pago, estado: 'pendiente' }]).select();

            if (pedidoData && pedidoData.length > 0) {
                const pedidoId = pedidoData[0].id;
                const detalles = carrito.map(i => ({
                    pedido_id: pedidoId,
                    producto_nombre: i.nombre,
                    precio: i.precio,
                    cantidad: i.cantidad,
                    comentario: i.comentario
                }));
                await _supabase.from('detalles_pedido').insert(detalles);
            }
        } catch (e) {}
    }

    const waNum = await getConfig('whatsapp_num', '5554746310');
    let msg = `🌊 *NUEVO PEDIDO - MAR Y SAZÓN*\n\n📌 *Cliente/Mesa:* ${cliente}\n💳 *Pago:* ${metodo_pago}\n\n*Detalles:*\n`;
    carrito.forEach(c => { msg += `- ${c.cantidad}x ${c.nombre} ($${(c.precio * c.cantidad).toFixed(2)}) ${c.comentario ? '['+c.comentario+']' : ''}\n`; });
    msg += `\n💰 *Total:* $${total.toFixed(2)}`;

    alert('¡Pedido realizado con éxito!');
    if (waNum) window.open(`https://wa.me/52${waNum}?text=${encodeURIComponent(msg)}`, '_blank');

    carrito = [];
    actualizarTotal();
    document.getElementById('nombre-cliente').value = '';
}"""

admin_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administración - Mar y Sazón</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <div id="admin-login-modal" class="modal">
        <div class="modal-content">
            <h3>🔒 Acceso Restringido</h3>
            <input type="password" id="admin-pass-input" placeholder="Contraseña Admin">
            <button class="btn btn-success" onclick="loginAdmin()">Ingresar</button>
        </div>
    </div>

    <div id="admin-panel" class="admin-grid hidden">
        <header style="background:none; border:none; padding:10px 0;">
            <h1>⚙️ Administración</h1>
        </header>

        <div class="admin-card">
            <h3>🔑 Configuración General</h3>
            <button class="btn btn-warning" onclick="cambiarPassAdmin()">Cambiar Contraseña Admin</button><br><br>
            <button class="btn" onclick="cambiarWhatsApp()">Cambiar WhatsApp Recepción</button><br><br>
            <button class="btn" onclick="cambiarCuentaBanco()">Cambiar Cuenta Transferencia</button>
        </div>

        <div class="admin-card">
            <h3>🖼️ Fondo de Clientes (Carrusel)</h3>
            <input type="file" id="slideshow-input" accept="image/*" onchange="subirImagenFondo(event)">
            <div id="slideshow-preview" style="display:flex; gap:8px; overflow-x:auto; margin-top:10px;"></div>
        </div>

        <div class="admin-card">
            <h3>👥 Gestión de Meseros (Max 10)</h3>
            <input type="text" id="mesero-nombre" placeholder="Nombre Mesero">
            <input type="password" id="mesero-pass" placeholder="Contraseña Mesero" style="margin-top:6px;">
            <input type="text" id="mesero-mesa" placeholder="Mesas Asignadas (Ej. Mesa 1)" style="margin-top:6px;">
            <button class="btn btn-success" onclick="agregarMesero()" style="margin-top:8px;">Agregar / Guardar Mesero</button>
            <ul id="lista-meseros" style="list-style:none; padding:0; margin-top:10px;"></ul>
        </div>

        <div class="admin-card">
            <h3>📋 Cuentas Activas y Cancelación</h3>
            <div id="lista-pedidos-admin"></div>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/admin.js"></script>
</body>
</html>"""

admin_js = """let currentAdminPass = 'ROXANA';

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
        cargarModuloAdmin();
    } else {
        alert('Contraseña incorrecta');
    }
}

async function cargarModuloAdmin() {
    cargarMeserosAdmin();
    cargarPedidosAdmin();
    cargarSlideshowPreview();
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

async function cambiarCuentaBanco() {
    const newBank = prompt('Ingrese la nueva cuenta bancaria para transferencias:');
    if (newBank) {
        await setConfig('cuenta_transferencia', newBank);
        alert('Cuenta bancaria actualizada.');
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
            document.getElementById('mesero-nombre').value = '';
            document.getElementById('mesero-pass').value = '';
            document.getElementById('mesero-mesa').value = '';
            cargarMeserosAdmin();
            return;
        } catch (e) {}
    }
    alert('Mesero guardado.');
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
    ul.innerHTML = '<li style="font-size:0.85rem; color:#94a3b8;">No hay meseros registrados.</li>';
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

async function cargarPedidosAdmin() {
    const div = document.getElementById('lista-pedidos-admin');
    if (_supabase) {
        try {
            const { data } = await _supabase.from('pedidos').select('*').order('id', { ascending: false });
            if (data && data.length > 0) {
                div.innerHTML = data.map(p => `
                    <div style="background:#0f172a; padding:10px; margin-bottom:8px; border-radius:6px;">
                        <b>#${p.id} - ${p.cliente_mesa}</b> | Total: $${p.total} | Estado: <span style="color:#f59e0b;">${p.estado}</span><br>
                        <button class="btn btn-danger" style="margin-top:5px;" onclick="cancelarPedidoAdmin(${p.id})">Cancelar Pedido</button>
                    </div>
                `).join('');
                return;
            }
        } catch(e){}
    }
    div.innerHTML = '<p style="font-size:0.85rem; color:#94a3b8;">No hay pedidos activos.</p>';
}

async function cancelarPedidoAdmin(id) {
    const p = prompt('Ingrese contraseña de administración (ROXANA) para cancelar pedido:');
    if (p === currentAdminPass || p === 'ROXANA') {
        if (_supabase) await _supabase.from('pedidos').update({ estado: 'cancelado' }).eq('id', id);
        alert('Pedido cancelado.');
        cargarPedidosAdmin();
    } else alert('Contraseña incorrecta.');
}"""

staff_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Punto Staff - Mar y Sazón</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
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
            <button class="btn btn-success" onclick="loginStaff()" style="margin-top:8px;">Ver Mis Comandas</button>
        </div>

        <div id="staff-orders-section" class="admin-card hidden">
            <h3>Comandas de Mis Mesas</h3>
            <div id="staff-pedidos-list"></div>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/staff.js"></script>
</body>
</html>"""

staff_js = """let meseroActual = null;

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
}"""

cocina_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cocina KDS - Mar y Sazón</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <header>
        <h1>🍳 Cocina KDS - Mar y Sazón</h1>
    </header>

    <main class="admin-grid" id="cocina-orders"></main>

    <script src="js/supabase_config.js"></script>
    <script src="js/cocina.js"></script>
</body>
</html>"""

cocina_js = """document.addEventListener('DOMContentLoaded', () => {
    cargarCocina();
    setInterval(cargarCocina, 5000);
});

async function cargarCocina() {
    const container = document.getElementById('cocina-orders');
    if (_supabase) {
        try {
            const { data: pedidos } = await _supabase.from('pedidos').select('*, detalles_pedido(*)').in('estado', ['pendiente', 'en_cocina']).order('id', { ascending: true });

            if (pedidos && pedidos.length > 0) {
                container.innerHTML = pedidos.map(p => `
                    <div class="admin-card" style="border-left: 5px solid var(--accent);">
                        <h3>Mesa/Cliente: ${p.cliente_mesa} (#${p.id})</h3>
                        <ul style="list-style:none; padding:0;">
                            ${(p.detalles_pedido || []).map(d => `
                                <li style="font-size:1.1rem; padding:4px 0;">
                                    <b>${d.cantidad}x ${d.producto_nombre}</b>${d.comentario ? `<br><small style="color:#f59e0b;">⚠️ Nota: ${d.comentario}</small>` : ''}
                                </li>
                            `).join('')}
                        </ul>
                        <button class="btn btn-success" onclick="marcarListo(${p.id})">Marcar como LISTO / ENTREGADO</button>
                    </div>
                `).join('');
                return;
            }
        } catch(e){}
    }
    container.innerHTML = '<p style="text-align:center; color:#94a3b8;">No hay comandas pendientes en cocina.</p>';
}

async function marcarListo(id) {
    if (_supabase) await _supabase.from('pedidos').update({ estado: 'listo' }).eq('id', id);
    cargarCocina();
}"""

styles_css = """:root { --primary: #0284c7; --dark: #0f172a; --card: #1e293b; --accent: #f59e0b; --danger: #ef4444; --success: #10b981; }
body { font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 0; background-color: var(--dark); color: #fff; min-height: 100vh; }
#bg-slideshow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2; background-size: cover; background-position: center; transition: background-image 1s; }
#bg-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background: rgba(15, 23, 42, 0.88); }
header { background: rgba(30, 41, 59, 0.95); padding: 15px; text-align: center; border-bottom: 2px solid var(--primary); position: sticky; top: 0; z-index: 10; }
.categories { display: flex; gap: 8px; overflow-x: auto; padding: 10px 5px; }
.cat-btn { background: #334155; color: #fff; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; white-space: nowrap; }
.cat-btn.active { background: var(--primary); font-weight: bold; }
.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; padding: 15px; margin-bottom: 160px; }
.menu-card { background: var(--card); padding: 12px; border-radius: 12px; text-align: center; border: 1px solid #334155; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between; }
.menu-card .price { color: var(--accent); font-weight: bold; font-size: 1.1rem; margin-top: 8px; }
.cart-footer { position: fixed; bottom: 0; width: 100%; background: rgba(15, 23, 42, 0.98); padding: 12px; box-sizing: border-box; border-top: 1px solid #334155; display: flex; flex-direction: column; gap: 8px; z-index: 20; }
input, select, textarea { padding: 10px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: white; width: 100%; box-sizing: border-box; }
.btn { background: var(--primary); color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; text-align: center; }
.btn-success { background: var(--success); }
.btn-danger { background: var(--danger); }
.btn-warning { background: var(--accent); color: #000; }
.modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal-content { background: var(--card); padding: 20px; border-radius: 12px; width: 90%; max-width: 400px; display: flex; flex-direction: column; gap: 12px; border: 1px solid #334155; }
.hidden { display: none !important; }
.qty-control { display: flex; align-items: center; justify-content: center; gap: 15px; margin: 10px 0; }
.qty-btn { width: 42px; height: 42px; border-radius: 50%; font-size: 1.4rem; background: var(--primary); color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.admin-grid { display: flex; flex-direction: column; gap: 15px; padding: 15px; max-width: 600px; margin: 0 auto; }
.admin-card { background: var(--card); padding: 15px; border-radius: 10px; border: 1px solid #334155; }"""

with open('index.html', 'w') as f: f.write(index_html)
with open('admin.html', 'w') as f: f.write(admin_html)
with open('staff.html', 'w') as f: f.write(staff_html)
with open('cocina.html', 'w') as f: f.write(cocina_html)
with open('css/styles.css', 'w') as f: f.write(styles_css)
with open('js/supabase_config.js', 'w') as f: f.write(supabase_config)
with open('js/app.js', 'w') as f: f.write(app_js)
with open('js/admin.js', 'w') as f: f.write(admin_js)
with open('js/staff.js', 'w') as f: f.write(staff_js)
with open('js/cocina.js', 'w') as f: f.write(cocina_js)

print("ARCHIVOS_LISTOS")
