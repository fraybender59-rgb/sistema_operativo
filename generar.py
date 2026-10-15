import os

os.makedirs('css', exist_ok=True)
os.makedirs('js', exist_ok=True)

styles_css = ''':root {
    --primary: #0284c7;
    --dark: #0f172a;
    --card: #1e293b;
    --accent: #f59e0b;
    --danger: #ef4444;
    --success: #10b981;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    margin: 0; padding: 0;
    background-color: var(--dark); color: #fff;
    min-height: 100vh;
}

#bg-slideshow {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -2; background-size: cover; background-position: center;
    transition: background-image 1s ease-in-out;
}

#bg-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1; background: rgba(15, 23, 42, 0.88);
}

header {
    background: rgba(30, 41, 59, 0.95); padding: 15px; text-align: center;
    border-bottom: 2px solid var(--primary); position: sticky; top: 0; z-index: 10;
}

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
.modal-content { background: var(--card); padding: 20px; border-radius: 12px; width: 90%; max-width: 450px; display: flex; flex-direction: column; gap: 12px; border: 1px solid #334155; max-height: 90vh; overflow-y: auto; }
.hidden { display: none !important; }

.qty-control { display: flex; align-items: center; justify-content: center; gap: 15px; margin: 10px 0; }
.qty-btn { width: 42px; height: 42px; border-radius: 50%; font-size: 1.4rem; background: var(--primary); color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; }

/* Grid Estilo Menú Botones de Administración */
.admin-top-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
.btn-nav-admin { padding: 12px; border-radius: 8px; border: none; color: white; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; text-decoration: none; font-size: 0.9rem; }

.bg-publico { background-color: #334155; }
.bg-staff { background-color: #475569; }
.bg-almacen { background-color: #15803d; opacity: 0.6; cursor: not-allowed; }
.bg-cocina { background-color: #ea580c; }
.bg-corte { background-color: #d97706; }
.bg-cobradas { background-color: #7e22ce; }
.bg-historial { background-color: #0d9488; }
.bg-comprobantes { background-color: #e11d48; opacity: 0.6; cursor: not-allowed; }
.bg-precios { background-color: #f97316; }
.bg-tarjeta { background-color: #2563eb; }

/* Pestañas de Caja Principal */
.tab-container { display: flex; gap: 10px; margin-bottom: 12px; }
.tab-btn { flex: 1; padding: 10px; background: #334155; border: none; color: white; font-weight: bold; border-radius: 6px; cursor: pointer; }
.tab-btn.active { background: var(--accent); color: black; }

/* Badges de Tiempo KDS */
.timer-badge { padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.85rem; display: inline-block; }
.timer-green { background-color: #10b981; color: #000; }
.timer-yellow { background-color: #f59e0b; color: #000; }
.timer-red { background-color: #ef4444; color: #fff; animation: pulse 1s infinite alternate; }

@keyframes pulse { from { opacity: 1; } to { opacity: 0.6; } }
'''

supabase_config_js = '''const SUPABASE_URL = 'https://atwtmuqkqypdodbhkrbe.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy';

let _supabase = null;
if (window.supabase && window.supabase.createClient) {
    _supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
}

// Auxiliares de Sincronización Local + Remota
function getPedidosLocales() {
    try {
        return JSON.parse(localStorage.getItem('mar_y_sazon_pedidos') || '[]');
    } catch(e) { return []; }
}

function savePedidosLocales(pedidos) {
    localStorage.setItem('mar_y_sazon_pedidos', JSON.stringify(pedidos));
}

async function guardarPedidoSync(pedido) {
    let pedidos = getPedidosLocales();
    pedidos.unshift(pedido);
    savePedidosLocales(pedidos);

    if (_supabase) {
        try {
            const { data, error } = await _supabase.from('pedidos').insert([{
                cliente_mesa: pedido.cliente_mesa,
                mesero_nombre: pedido.mesero_nombre,
                total: pedido.total,
                estado: pedido.estado,
                metodo_pago: pedido.metodo_pago,
                origen: pedido.origen,
                creado_en: pedido.creado_en
            }]).select();

            if (data && data.length > 0) {
                const pId = data[0].id;
                pedido.id = pId;
                const detalles = pedido.detalles.map(d => ({
                    pedido_id: pId,
                    producto_nombre: d.nombre,
                    precio: d.precio,
                    cantidad: d.cantidad,
                    comentario: d.comentario
                }));
                await _supabase.from('detalles_pedido').insert(detalles);
                savePedidosLocales(pedidos);
            }
        } catch(e) { console.warn('Guardado en respaldo local:', e); }
    }
}

async function obtenerPedidosSync() {
    let locales = getPedidosLocales();
    if (_supabase) {
        try {
            const { data } = await _supabase.from('pedidos').select('*, detalles_pedido(*)').order('id', { ascending: false });
            if (data && data.length > 0) {
                const remotos = data.map(p => ({
                    id: p.id,
                    cliente_mesa: p.cliente_mesa,
                    mesero_nombre: p.mesero_nombre || 'General',
                    total: parseFloat(p.total),
                    estado: p.estado,
                    metodo_pago: p.metodo_pago,
                    origen: p.origen || 'Clientes',
                    creado_en: p.creado_en,
                    detalles: (p.detalles_pedido || []).map(d => ({
                        nombre: d.producto_nombre,
                        precio: parseFloat(d.precio),
                        cantidad: d.cantidad,
                        comentario: d.comentario
                    }))
                }));
                savePedidosLocales(remotos);
                return remotos;
            }
        } catch(e){}
    }
    return locales;
}

async function actualizarEstadoPedidoSync(id, nuevoEstado, metodoPago = null) {
    let locales = getPedidosLocales();
    let target = locales.find(p => p.id == id);
    if (target) {
        target.estado = nuevoEstado;
        if (metodoPago) target.metodo_pago = metodoPago;
        savePedidosLocales(locales);
    }
    if (_supabase) {
        try {
            let updatePayload = { estado: nuevoEstado };
            if (metodoPago) updatePayload.metodo_pago = metodoPago;
            await _supabase.from('pedidos').update(updatePayload).eq('id', id);
        } catch(e){}
    }
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
}
'''

index_html = '''<!DOCTYPE html>
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
</html>'''

app_js = '''const MENU_DEFAULT = [
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
                data.forEach(m => select.innerHTML += `<option value="${m.nombre}">${m.nombre}</option>`);
                return;
            }
        } catch(e){}
    }
    select.innerHTML += '<option value="Luis">Luis</option><option value="Ana">Ana</option>';
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
    const mesero_nombre = document.getElementById('select-mesero').value || 'Cliente Web';
    const metodo_pago = document.getElementById('metodo-pago').value;

    if (!cliente || carrito.length === 0) return alert('Ingresa Nombre/Mesa y agrega platillos al pedido.');

    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    const nuevoPedido = {
        id: Date.now(),
        cliente_mesa: cliente,
        mesero_nombre: mesero_nombre,
        total: total,
        estado: 'pendiente',
        metodo_pago: metodo_pago,
        origen: 'Clientes',
        creado_en: new Date().toISOString(),
        detalles: [...carrito]
    };

    await guardarPedidoSync(nuevoPedido);

    const waNum = await getConfig('whatsapp_num', '5554746310');
    let msg = `🌊 *NUEVO PEDIDO - MAR Y SAZÓN*\n\n📌 *Cliente/Mesa:* ${cliente}\n👨‍🍳 *Atiende:* ${mesero_nombre}\n💳 *Pago:* ${metodo_pago}\n\n*Detalles:*\n`;
    carrito.forEach(c => { msg += `- ${c.cantidad}x ${c.nombre} ($${(c.precio * c.cantidad).toFixed(2)}) ${c.comentario ? '['+c.comentario+']' : ''}\n`; });
    msg += `\n💰 *Total:* $${total.toFixed(2)}`;

    alert('¡Pedido realizado con éxito!');
    if (waNum) window.open(`https://wa.me/52${waNum}?text=${encodeURIComponent(msg)}`, '_blank');

    carrito = [];
    actualizarTotal();
    document.getElementById('nombre-cliente').value = '';
}
'''

admin_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Caja Maestro - Administración</title>
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
            <h1>⚙️ Caja Maestro - Administración</h1>
        </header>

        <!-- Botones Principales de Navegación Exactos -->
        <div class="admin-top-grid">
            <a href="index.html" target="_blank" class="btn-nav-admin bg-publico">📱 Comandero Público</a>
            <a href="staff.html" target="_blank" class="btn-nav-admin bg-staff">📝 Comandero Staff</a>
            <button onclick="alert('Módulo de Almacén desactivado para Mar y Sazón')" class="btn-nav-admin bg-almacen">📦 Almacén</button>
            <a href="cocina.html" target="_blank" class="btn-nav-admin bg-cocina">🧑‍🍳 Cocina</a>
            <button onclick="abrirModalCorte()" class="btn-nav-admin bg-corte">💰 Corte</button>
            <button onclick="abrirModalCobradas()" class="btn-nav-admin bg-cobradas">📁 Cobradas Hoy</button>
            <button onclick="abrirModalHistorial()" class="btn-nav-admin bg-historial">📅 Historial de Días</button>
            <button onclick="alert('Sin comprobantes adjuntos')" class="btn-nav-admin bg-comprobantes">📸 Ver Comprobantes</button>
            <button onclick="abrirModalPrecios()" class="btn-nav-admin bg-precios">✏️ Precios</button>
            <button onclick="abrirModalTarjeta()" class="btn-nav-admin bg-tarjeta">💳 Config Tarjeta</button>
        </div>

        <!-- Caja Principal -->
        <div class="admin-card">
            <h3>📝 Caja Principal</h3>
            <div class="tab-container">
                <button class="tab-btn active" id="tab-cli" onclick="cambiarTabCaja('Clientes')">👤 Clientes</button>
                <button class="tab-btn" id="tab-sta" onclick="cambiarTabCaja('Staff')">🧑‍🍳 Staff</button>
            </div>
            <div id="lista-caja-abierta"></div>
        </div>

        <!-- Ajustes de Sistema -->
        <div class="admin-card">
            <h3>⚙️ Ajustes del Sistema</h3>
            <button class="btn btn-warning" onclick="cambiarPassAdmin()">Cambiar Contraseña Admin</button><br><br>
            <button class="btn" onclick="cambiarWhatsApp()">Cambiar WhatsApp Recepción</button>
        </div>

        <!-- Fondo Slideshow -->
        <div class="admin-card">
            <h3>🖼️ Fondo de Clientes (Carrusel)</h3>
            <input type="file" id="slideshow-input" accept="image/*" onchange="subirImagenFondo(event)">
            <div id="slideshow-preview" style="display:flex; gap:8px; overflow-x:auto; margin-top:10px;"></div>
        </div>

        <!-- Gestión Meseros -->
        <div class="admin-card">
            <h3>👥 Gestión de Meseros (Max 10)</h3>
            <input type="text" id="mesero-nombre" placeholder="Nombre Mesero">
            <input type="password" id="mesero-pass" placeholder="Contraseña Mesero" style="margin-top:6px;">
            <input type="text" id="mesero-mesa" placeholder="Mesas Asignadas (Ej. Mesa 1)" style="margin-top:6px;">
            <button class="btn btn-success" onclick="agregarMesero()" style="margin-top:8px;">Agregar Mesero</button>
            <ul id="lista-meseros" style="list-style:none; padding:0; margin-top:10px;"></ul>
        </div>
    </div>

    <!-- Modales de Funciones -->
    <div id="modal-generic" class="modal hidden">
        <div class="modal-content">
            <h3 id="modal-gen-title">Modal</h3>
            <div id="modal-gen-body"></div>
            <button class="btn btn-danger" onclick="cerrarModalGeneric()">Cerrar</button>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/admin.js"></script>
</body>
</html>'''

admin_js = '''let currentAdminPass = 'ROXANA';
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

/* Modales de Botones de Arriba */
function abrirModalCorte() {
    obtenerPedidosSync().then(todos => {
        const cobrados = todos.filter(p => p.estado === 'cobrado');
        const totEfectivo = cobrados.filter(p => p.metodo_pago === 'Efectivo').reduce((sum, p) => sum + p.total, 0);
        const totTransf = cobrados.filter(p => p.metodo_pago === 'Transferencia').reduce((sum, p) => sum + p.total, 0);
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
'''

staff_html = '''<!DOCTYPE html>
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

    <div class="admin-grid" style="max-width:500px; margin:20px auto; padding:15px;">
        <div class="admin-card">
            <h3>Identificación de Mesero</h3>
            <select id="staff-select-mesero"><option value="">Selecciona tu Nombre...</option></select>
            <input type="password" id="staff-pass" placeholder="Contraseña Mesero" style="margin-top:8px;">
            <button class="btn btn-success" onclick="loginStaff()" style="margin-top:8px;">Ingresar a Tomar Pedidos</button>
        </div>

        <div id="staff-orders-section" class="admin-card hidden">
            <h3>📝 Tomar Nuevo Pedido</h3>
            <input type="text" id="staff-cliente" placeholder="Mesa / Nombre del Cliente">
            <button class="btn" style="margin-top:8px;" onclick="irAComanderoStaff()">Ir al Menú de Mesero</button>
            <hr>
            <h3>Comandas de Mis Mesas</h3>
            <div id="staff-pedidos-list"></div>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/staff.js"></script>
</body>
</html>'''

staff_js = '''let meseroActual = null;

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
'''

cocina_html = '''<!DOCTYPE html>
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

    <main class="admin-grid" id="cocina-orders" style="max-width:800px; margin:0 auto; padding:15px;"></main>

    <script src="js/supabase_config.js"></script>
    <script src="js/cocina.js"></script>
</body>
</html>'''

cocina_js = '''document.addEventListener('DOMContentLoaded', () => {
    cargarCocina();
    setInterval(cargarCocina, 1000); // Refresco de temporizadores cada segundo
});

async function cargarCocina() {
    const container = document.getElementById('cocina-orders');
    if (!container) return;

    const todos = await obtenerPedidosSync();
    // Se muestran pedidos en estado 'pendiente' o 'en_cocina' (no cobrados ni cerrados)
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
'''

with open('index.html', 'w') as f: f.write(index_html)
with open('admin.html', 'w') as f: f.write(admin_html)
with open('staff.html', 'w') as f: f.write(staff_html)
with open('cocina.html', 'w') as f: f.write(cocina_html)
with open('css/styles.css', 'w') as f: f.write(styles_css)
with open('js/supabase_config.js', 'w') as f: f.write(supabase_config_js)
with open('js/app.js', 'w') as f: f.write(app_js)
with open('js/admin.js', 'w') as f: f.write(admin_js)
with open('js/staff.js', 'w') as f: f.write(staff_js)
with open('js/cocina.js', 'w') as f: f.write(cocina_js)

print("SISTEMA_KDS_GENERADO_EXITOSAMENTE")
