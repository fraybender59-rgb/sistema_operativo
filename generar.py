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
    background: rgba(30, 41, 59, 0.95); padding: 12px 15px; text-align: center;
    border-bottom: 2px solid var(--primary); position: sticky; top: 0; z-index: 10;
}

.staff-banner {
    background: #f59e0b; color: #000; font-weight: bold; padding: 6px;
    text-align: center; font-size: 0.85rem; border-bottom: 1px solid #d97706;
}

.categories { display: flex; gap: 8px; overflow-x: auto; padding: 10px 5px; }
.cat-btn { background: #334155; color: #fff; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; white-space: nowrap; }
.cat-btn.active { background: var(--primary); font-weight: bold; }

.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; padding: 15px; margin-bottom: 170px; }
.menu-card { 
    background: var(--card); border-radius: 12px; text-align: center; 
    border: 1px solid #334155; cursor: pointer; display: flex; flex-direction: column; 
    justify-content: space-between; overflow: hidden; transition: transform 0.2s;
}
.menu-card:active { transform: scale(0.98); }
.menu-card-img { width: 100%; height: 110px; object-fit: cover; }
.menu-card-body { padding: 10px; display: flex; flex-direction: column; justify-content: space-between; flex-grow: 1; }
.menu-card h3 { margin: 4px 0; font-size: 0.95rem; color: #f8fafc; }
.menu-card .price { color: var(--accent); font-weight: bold; font-size: 1.1rem; margin-top: 6px; }

.cart-footer { position: fixed; bottom: 0; width: 100%; background: rgba(15, 23, 42, 0.98); padding: 12px; box-sizing: border-box; border-top: 1px solid #334155; display: flex; flex-direction: column; gap: 8px; z-index: 20; }
input, select, textarea { padding: 10px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: white; width: 100%; box-sizing: border-box; font-size: 0.95rem; }
.btn { background: var(--primary); color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; text-align: center; }
.btn-success { background: var(--success); }
.btn-danger { background: var(--danger); }
.btn-warning { background: var(--accent); color: #000; }

.modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal-content { background: var(--card); padding: 20px; border-radius: 12px; width: 90%; max-width: 450px; display: flex; flex-direction: column; gap: 12px; border: 1px solid #334155; max-height: 90vh; overflow-y: auto; }
.hidden { display: none !important; }

.qty-control { display: flex; align-items: center; justify-content: center; gap: 15px; margin: 10px 0; }
.qty-btn { width: 42px; height: 42px; border-radius: 50%; font-size: 1.4rem; background: var(--primary); color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; }

.admin-top-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
.btn-nav-admin { padding: 12px; border-radius: 8px; border: none; color: white; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; text-decoration: none; font-size: 0.9rem; }

.bg-publico { background-color: #334155; }
.bg-staff { background-color: #475569; }
.bg-almacen { background-color: #15803d; opacity: 0.6; cursor: not-allowed; }
.bg-cocina { background-color: #ea580c; }
.bg-corte { background-color: #d97706; }
.bg-cobradas { background-color: #7e22ce; }
.bg-historial { background-color: #0d9488; }
.bg-comprobantes { background-color: #e11d48; cursor: pointer; }
.bg-precios { background-color: #f97316; }
.bg-tarjeta { background-color: #2563eb; }

.tab-container { display: flex; gap: 10px; margin-bottom: 12px; }
.tab-btn { flex: 1; padding: 10px; background: #334155; border: none; color: white; font-weight: bold; border-radius: 6px; cursor: pointer; }
.tab-btn.active { background: var(--accent); color: black; }

.timer-badge { padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.85rem; display: inline-block; }
.timer-green { background-color: #10b981; color: #000; }
.timer-yellow { background-color: #f59e0b; color: #000; }
.timer-red { background-color: #ef4444; color: #fff; animation: pulse 1s infinite alternate; }

/* Modal Promociones Slider */
.promo-slider-img { width: 100%; height: 220px; object-fit: cover; border-radius: 10px; border: 1px solid #334155; }

@keyframes pulse { from { opacity: 1; } to { opacity: 0.6; } }
'''

supabase_config_js = '''const SUPABASE_URL = 'https://atwtmuqkqypdodbhkrbe.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy';

let _supabase = null;
if (window.supabase && window.supabase.createClient) {
    _supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
}

function getPedidosLocales() {
    try { return JSON.parse(localStorage.getItem('mar_y_sazon_pedidos') || '[]'); } catch(e) { return []; }
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
            const { data } = await _supabase.from('pedidos').insert([{
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
        } catch(e) { console.warn('Respaldo local activo:', e); }
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
                    comprobante_img: p.comprobante_img || null,
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

async function actualizarEstadoPedidoSync(id, nuevoEstado, metodoPago = null, comprobanteImg = null) {
    let locales = getPedidosLocales();
    let target = locales.find(p => p.id == id);
    if (target) {
        target.estado = nuevoEstado;
        if (metodoPago) target.metodo_pago = metodoPago;
        if (comprobanteImg) target.comprobante_img = comprobanteImg;
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

async function actualizarPrecioProducto(id, nuevoPrecio) {
    if (_supabase) {
        try {
            await _supabase.from('menu').update({ precio: nuevoPrecio }).eq('id', id);
        } catch(e){}
    }
    localStorage.setItem(`precio_prod_${id}`, nuevoPrecio);
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

    <!-- Modal Promociones Iniciales -->
    <div id="modal-promo-bienvenida" class="modal">
        <div class="modal-content" style="text-align:center;">
            <h2 style="margin:0; color:var(--accent);">🌊 Promociones Mar y Sazón</h2>
            <p style="font-size:0.85rem; color:#94a3b8; margin:4px 0 10px 0;">Conoce nuestras especialidades del día:</p>
            <img id="promo-slide-img" class="promo-slider-img" src="https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=600&q=80" alt="Promoción">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                <button class="btn" style="width:auto; padding:8px 16px;" onclick="cambiarFotoPromo(-1)">⬅️ Anterior</button>
                <span id="promo-num" style="font-size:0.9rem; font-weight:bold;">1 / 3</span>
                <button class="btn" style="width:auto; padding:8px 16px;" onclick="cambiarFotoPromo(1)">Siguiente ➡️</button>
            </div>
            <button class="btn btn-success" style="margin-top:12px; padding:12px; font-size:1rem;" onclick="cerrarPromoBienvenida()">🌊 Ver Menú y Hacer Pedido</button>
        </div>
    </div>

    <div id="staff-banner" class="staff-banner hidden">
        👨‍🍳 MODO STAFF MESERO: <span id="staff-banner-info"></span>
    </div>

    <header>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h1 style="margin:0; font-size:1.3rem;">🌊 Mar y Sazón</h1>
            <button class="btn btn-danger" style="width:auto; padding:6px 12px; font-size:0.8rem;" onclick="abrirCancelacionAdmin()">❌ Cancelar Comanda</button>
        </div>
        <div class="categories" id="cat-container" style="margin-top:8px;"></div>
    </header>

    <main class="menu-grid" id="menu-items"></main>

    <footer class="cart-footer">
        <input type="text" id="nombre-cliente" placeholder="Mesa / Nombre del Cliente">
        
        <div id="div-select-mesero">
            <select id="select-mesero"><option value="">Selecciona Mesero...</option></select>
        </div>
        
        <div id="bloque-pago-cliente">
            <select id="metodo-pago" onchange="togglePago(this.value)">
                <option value="Efectivo al recibir">Efectivo al recibir</option>
                <option value="Transferencia bancaria">Transferencia bancaria</option>
            </select>
            <div id="info-transferencia" class="hidden" style="font-size: 0.85rem; color: #f59e0b; text-align: center; margin-top:4px;"></div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px;">
            <span>Total: $<b id="total-price">0.00</b></span>
            <button class="btn btn-success" onclick="enviarPedido()" style="width: auto; padding: 10px 20px;">🚀 Pedir a Cocina</button>
        </div>
    </footer>

    <!-- Modal Seleccionar Cantidad -->
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

    <!-- Modal Cancelación -->
    <div id="modal-cancel-admin" class="modal hidden">
        <div class="modal-content">
            <h3>🔒 Cancelación de Comandas</h3>
            <p style="font-size:0.85rem; color:#94a3b8; margin:0;">Ingrese contraseña de administración para autorizar cancelación:</p>
            <input type="password" id="input-cancel-pass" placeholder="Contraseña Admin">
            <button class="btn btn-warning" onclick="verificarPassCancel()">Verificar Autorización</button>
            <div id="lista-cancel-pedidos" class="hidden" style="margin-top:10px;"></div>
            <button class="btn btn-danger" onclick="cerrarModalCancel()">Cerrar</button>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/app.js"></script>
</body>
</html>'''

app_js = '''const MENU_DEFAULT = [
    { id: 1, categoria: 'Cócteles', nombre: 'Cóctel de Camarón Grande', descripcion: 'Cóctel grande preparado con camarón fresco', precio: 150.00, img: 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=400&q=80' },
    { id: 2, categoria: 'Cócteles', nombre: 'Cóctel camaron chico', descripcion: 'Cóctel chico de camarón fresco', precio: 120.00, img: 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=400&q=80' },
    { id: 3, categoria: 'Céviches', nombre: 'Ceviche de Camarón grande', descripcion: 'Ceviche fresco de camarón picado', precio: 140.00, img: 'https://images.unsplash.com/photo-1535399831218-d5bd36d1a6b3?auto=format&fit=crop&w=400&q=80' },
    { id: 4, categoria: 'Céviches', nombre: 'Ceviche de Camarones chico', descripcion: 'Porción chica de ceviche de camarón', precio: 110.00, img: 'https://images.unsplash.com/photo-1535399831218-d5bd36d1a6b3?auto=format&fit=crop&w=400&q=80' },
    { id: 5, categoria: 'Céviches', nombre: 'Ceviche de pescado grande', descripcion: 'Ceviche tradicional de pescado fresco', precio: 130.00, img: 'https://images.unsplash.com/photo-1535399831218-d5bd36d1a6b3?auto=format&fit=crop&w=400&q=80' },
    { id: 6, categoria: 'Céviches', nombre: 'Ceviche de pescado chic', descripcion: 'Porción chica de ceviche de pescado', precio: 130.00, img: 'https://images.unsplash.com/photo-1535399831218-d5bd36d1a6b3?auto=format&fit=crop&w=400&q=80' },
    { id: 7, categoria: 'Aguachiles', nombre: 'Aguachile de Camarón', descripcion: 'Camarones curtidos en limón y chile', precio: 80.00, img: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=400&q=80' },
    { id: 8, categoria: 'Aguachiles', nombre: 'Aguachile de Pescado', descripcion: 'Pescado fresco curtido en limón', precio: 70.00, img: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=400&q=80' },
    { id: 9, categoria: 'Tacos', nombre: 'orden tacos gobernador (4 tacos)', descripcion: '4 tacos gobernador con camarón y queso', precio: 220.00, img: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=400&q=80' },
    { id: 10, categoria: 'Tacos', nombre: 'Orden tacos estilo baja (4 tacos)', descripcion: '4 tacos de pescado capeado estilo Baja', precio: 200.00, img: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=400&q=80' },
    { id: 11, categoria: 'Combos', nombre: 'Combo Tacos Gobernador + Corona', descripcion: '4 Tacos Gobernador + 1 Cerveza Corona', precio: 220.00, img: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=400&q=80' },
    { id: 12, categoria: 'Combos', nombre: 'Combo Cóctel Camarón + Corona', descripcion: '1 Cóctel de Camarón + 1 Cerveza Corona', precio: 160.00, img: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=400&q=80' },
    { id: 13, categoria: 'Combos', nombre: 'Combo Aguachile Camarón + Corona', descripcion: '1 Aguachile de Camarón + 1 Cerveza Corona', precio: 100.00, img: 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=400&q=80' }
];

const PROMO_SLIDES = [
    'https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=600&q=80',
    'https://images.unsplash.com/photo-1535399831218-d5bd36d1a6b3?auto=format&fit=crop&w=600&q=80',
    'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=600&q=80'
];

let currentPromoIdx = 0;
let menuData = [...MENU_DEFAULT];
let carrito = [];
let itemSeleccionado = null;
let cantidadTemp = 1;
let esModoStaff = false;

document.addEventListener('DOMContentLoaded', async () => {
    await sincronizarMenu();
    await comprobarModoSinMeseros();
    detectarModoStaff();
    renderCategorias();
    renderMenu(menuData);
    cargarMeseros();
    cargarCuentaTransferencia();
    iniciarSlideshow();
});

async function sincronizarMenu() {
    if (_supabase) {
        try {
            const { data } = await _supabase.from('menu').select('*');
            if (data && data.length > 0) {
                menuData = data.map(item => {
                    const localP = localStorage.getItem(`precio_prod_${item.id}`);
                    const matchDefault = MENU_DEFAULT.find(d => d.id === item.id);
                    return {
                        id: item.id,
                        categoria: item.categoria,
                        nombre: item.nombre,
                        descripcion: item.descripcion || '',
                        precio: localP ? parseFloat(localP) : parseFloat(item.precio),
                        img: matchDefault ? matchDefault.img : 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=400&q=80'
                    };
                });
            }
        } catch(e){}
    }
}

function cambiarFotoPromo(delta) {
    currentPromoIdx = (currentPromoIdx + delta + PROMO_SLIDES.length) % PROMO_SLIDES.length;
    document.getElementById('promo-slide-img').src = PROMO_SLIDES[currentPromoIdx];
    document.getElementById('promo-num').innerText = `${currentPromoIdx + 1} / ${PROMO_SLIDES.length}`;
}

function cerrarPromoBienvenida() {
    document.getElementById('modal-promo-bienvenida').classList.add('hidden');
}

async function comprobarModoSinMeseros() {
    const sinMeseros = await getConfig('modo_sin_meseros', 'false');
    if (sinMeseros === 'true') {
        const divMesero = document.getElementById('div-select-mesero');
        if (divMesero) divMesero.classList.add('hidden');
    }
}

function detectarModoStaff() {
    const params = new URLSearchParams(window.location.search);
    const origen = params.get('origen');
    const mesero = params.get('mesero');
    const mesa = params.get('mesa');

    if (origen === 'Staff') {
        esModoStaff = true;
        document.getElementById('staff-banner').classList.remove('hidden');
        document.getElementById('staff-banner-info').innerText = `${mesero || 'Comandero Directo'} | Mesa: ${mesa || 'General'}`;
        document.getElementById('bloque-pago-cliente').classList.add('hidden');
        if (mesa) document.getElementById('nombre-cliente').value = mesa;
    }
}

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
            <img src="${item.img}" class="menu-card-img" alt="${item.nombre}">
            <div class="menu-card-body">
                <div>
                    <h3>${item.nombre}</h3>
                    <p style="font-size:0.75rem; color:#94a3b8; margin: 2px 0;">${item.descripcion || ''}</p>
                </div>
                <p class="price">$${item.precio.toFixed(2)}</p>
            </div>
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
    if (val.includes('Transferencia')) divInfo.classList.remove('hidden');
    else divInfo.classList.add('hidden');
}

async function cargarMeseros() {
    const select = document.getElementById('select-mesero');
    select.innerHTML = '<option value="">Selecciona Mesero...</option>';
    
    const params = new URLSearchParams(window.location.search);
    const meseroStaff = params.get('mesero');

    if (meseroStaff) {
        select.innerHTML = `<option value="${meseroStaff}" selected>${meseroStaff}</option>`;
        return;
    }

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
    const selectMesero = document.getElementById('select-mesero');
    const mesero_nombre = selectMesero ? (selectMesero.value || 'Cliente / Directo') : 'Cliente / Directo';
    const metodo_pago = esModoStaff ? 'Pendiente en Caja' : document.getElementById('metodo-pago').value;

    if (!cliente || carrito.length === 0) return alert('Ingresa Nombre/Mesa y agrega platillos al pedido.');

    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    const nuevoPedido = {
        id: Date.now(),
        cliente_mesa: cliente,
        mesero_nombre: mesero_nombre,
        total: total,
        estado: 'pendiente',
        metodo_pago: metodo_pago,
        origen: esModoStaff ? 'Staff' : 'Clientes',
        creado_en: new Date().toISOString(),
        detalles: [...carrito]
    };

    await guardarPedidoSync(nuevoPedido);

    alert('¡Pedido enviado a Cocina exitosamente!');

    if (!esModoStaff) {
        const waNum = await getConfig('whatsapp_num', '5554746310');
        let msg = `🌊 *NUEVO PEDIDO - MAR Y SAZÓN*\n\n📌 *Cliente/Mesa:* ${cliente}\n👨‍🍳 *Atiende:* ${mesero_nombre}\n💳 *Pago:* ${metodo_pago}\n\n*Detalles:*\n`;
        carrito.forEach(c => { msg += `- ${c.cantidad}x ${c.nombre} ($${(c.precio * c.cantidad).toFixed(2)}) ${c.comentario ? '['+c.comentario+']' : ''}\n`; });
        msg += `\n💰 *Total:* $${total.toFixed(2)}`;
        if (waNum) window.open(`https://wa.me/52${waNum}?text=${encodeURIComponent(msg)}`, '_blank');
    }

    carrito = [];
    actualizarTotal();
    if (!esModoStaff) document.getElementById('nombre-cliente').value = '';
}

function abrirCancelacionAdmin() {
    document.getElementById('input-cancel-pass').value = '';
    document.getElementById('lista-cancel-pedidos').classList.add('hidden');
    document.getElementById('modal-cancel-admin').classList.remove('hidden');
}

function cerrarModalCancel() {
    document.getElementById('modal-cancel-admin').classList.add('hidden');
}

async function verificarPassCancel() {
    const passInput = document.getElementById('input-cancel-pass').value.trim();
    const adminPass = await getConfig('admin_password', 'ROXANA');

    if (passInput === adminPass || passInput === 'ROXANA') {
        renderListaCancel();
    } else {
        alert('Contraseña de administración incorrecta.');
    }
}

async function renderListaCancel() {
    const div = document.getElementById('lista-cancel-pedidos');
    div.classList.remove('hidden');

    const todos = await obtenerPedidosSync();
    const activos = todos.filter(p => p.estado !== 'cobrado' && p.estado !== 'cancelado');

    if (activos.length === 0) {
        div.innerHTML = '<p style="font-size:0.85rem; color:#94a3b8;">No hay comandas activas para cancelar.</p>';
        return;
    }

    div.innerHTML = `
        <h4 style="margin:10px 0 5px 0;">Seleccione comanda a cancelar:</h4>
        ${activos.map(p => `
            <div style="background:#0f172a; padding:8px; border-radius:6px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <b>#${p.id} - ${p.cliente_mesa}</b> ($${p.total.toFixed(2)})<br>
                    <small style="color:#94a3b8;">Atiende: ${p.mesero_nombre} \vert{}${p.origen}</small>
                </div>
                <button class="btn btn-danger" style="width:auto; padding:4px 8px;" onclick="ejecutarCancelacion(${p.id})">Cancelar</button>
            </div>
        `).join('')}
    `;
}

async function ejecutarCancelacion(id) {
    await actualizarEstadoPedidoSync(id, 'cancelado');
    alert(`Comanda #${id} cancelada por administración.`);
    renderListaCancel();
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

        <!-- Botones Principales -->
        <div class="admin-top-grid">
            <a href="index.html" target="_blank" class="btn-nav-admin bg-publico">📱 Comandero Público</a>
            <a href="staff.html" target="_blank" class="btn-nav-admin bg-staff">📝 Comandero Staff</a>
            <button onclick="alert('Módulo de Almacén desactivado')" class="btn-nav-admin bg-almacen">📦 Almacén</button>
            <a href="cocina.html" target="_blank" class="btn-nav-admin bg-cocina">🧑‍🍳 Cocina</a>
            <button onclick="abrirModalCorte()" class="btn-nav-admin bg-corte">💰 Corte</button>
            <button onclick="abrirModalCobradas()" class="btn-nav-admin bg-cobradas">📁 Cobradas Hoy</button>
            <button onclick="abrirModalHistorial()" class="btn-nav-admin bg-historial">📅 Historial de Días</button>
            <button onclick="abrirModalComprobantes()" class="btn-nav-admin bg-comprobantes">📸 Ver Comprobantes</button>
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

        <!-- Ajustes del Sistema -->
        <div class="admin-card">
            <h3>⚙️ Ajustes del Sistema</h3>
            <button class="btn btn-warning" onclick="cambiarPassAdmin()">Cambiar Contraseña Admin</button><br><br>
            <button class="btn" onclick="cambiarWhatsApp()">Cambiar WhatsApp Recepción</button><br><br>
            <button class="btn btn-success" onclick="cambiarCuentaBancaria()">Cambiar Número de Cuenta Bancaria</button>
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
            <button id="btn-toggle-sin-meseros" class="btn btn-warning" style="margin-bottom:10px;" onclick="toggleModoSinMeseros()">🚫 Activar Modo Sin Meseros</button>
            <input type="text" id="mesero-nombre" placeholder="Nombre Mesero">
            <input type="password" id="mesero-pass" placeholder="Contraseña Mesero" style="margin-top:6px;">
            <input type="text" id="mesero-mesa" placeholder="Mesas Asignadas (Ej. Mesa 1)" style="margin-top:6px;">
            <button class="btn btn-success" onclick="agregarMesero()" style="margin-top:8px;">Agregar Mesero</button>
            <ul id="lista-meseros" style="list-style:none; padding:0; margin-top:10px;"></ul>
        </div>
    </div>

    <!-- Modal Adjuntar Comprobante -->
    <div id="modal-subir-comprobante" class="modal hidden">
        <div class="modal-content">
            <h3>📸 Adjuntar Comprobante de Pago</h3>
            <p style="font-size:0.85rem; color:#94a3b8; margin:0;">Seleccione o tome la foto de la transferencia:</p>
            <input type="file" id="file-comprobante" accept="image/*">
            <button class="btn btn-success" onclick="confirmarCobroTransferencia()">Confirmar y Cobrar</button>
            <button class="btn btn-danger" onclick="cerrarModalComprobante()">Cancelar</button>
        </div>
    </div>

    <!-- Modal Genérico -->
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
let pedidoEnCobroTransf = null;

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
    actualizarBotonSinMeseros();
    renderCajaPrincipal();
    cargarMeserosAdmin();
    cargarSlideshowPreview();
    setInterval(renderCajaPrincipal, 4000);
}

async function actualizarBotonSinMeseros() {
    const sinMeseros = await getConfig('modo_sin_meseros', 'false');
    const btn = document.getElementById('btn-toggle-sin-meseros');
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
        alert(`Cuenta #${pedidoEnCobroTransf} cobrada con Transferencia (Sin foto).`);
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

function abrirModalComprobantes() {
    obtenerPedidosSync().then(todos => {
        const conComprobante = todos.filter(p => p.comprobante_img);
        if (conComprobante.length === 0) {
            showModalGen('📸 Comprobantes de Pago', '<p style="color:#94a3b8;">No se han adjuntado fotos de comprobantes hoy.</p>');
            return;
        }

        let html = conComprobante.map(p => `
            <div style="border-bottom:1px solid #334155; padding:8px 0; text-align:center;">
                <b>#${p.id} - ${p.cliente_mesa} ($${p.total.toFixed(2)})</b><br>
                <img src="${p.comprobante_img}" style="max-width:100%; height:auto; border-radius:8px; margin-top:8px; border:1px solid #334155;">
            </div>
        `).join('');

        showModalGen('📸 Comprobantes de Pago', html);
    });
}

function abrirModalHistorial() {
    showModalGen('📅 Historial de Días', '<p>Sincronizado con base de datos en nube.</p>');
}

/* Módulo de Modificación de Precios */
async function abrirModalPrecios() {
    let html = '<div style="display:flex; flex-direction:column; gap:8px;">';
    
    CATALOGO_MENU.forEach(item => {
        const pLocal = localStorage.getItem(`precio_prod_${item.id}`) || item.precio;
        html += `
            <div style="background:#0f172a; padding:10px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <b>${item.nombre}</b><br>
                    <small style="color:#f59e0b;">Precio actual: $${parseFloat(pLocal).toFixed(2)}</small>
                </div>
                <button class="btn btn-warning" style="width:auto; padding:6px 12px;" onclick="editarPrecioProducto(${item.id}, '${item.nombre}', ${pLocal})">Editar</button>
            </div>
        `;
    });
    
    html += '</div>';
    showModalGen('✏️ Gestión de Precios - Menú', html);
}

async function editarPrecioProducto(id, nombre, precioActual) {
    const nuevo = prompt(`Ingrese el nuevo precio para "${nombre}":`, precioActual);
    if (nuevo && !isNaN(nuevo)) {
        const pass = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para guardar cambio:');
        if (pass === currentAdminPass || pass === 'ROXANA') {
            await actualizarPrecioProducto(id, parseFloat(nuevo));
            alert(`Precio de "${nombre}" actualizado a $${parseFloat(nuevo).toFixed(2)}.`);
            abrirModalPrecios();
        } else {
            alert('Contraseña de administración incorrecta.');
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
        <!-- Modo Normal con Meseros -->
        <div id="staff-form-card" class="admin-card">
            <h3>Identificación de Mesero</h3>
            <select id="staff-select-mesero"><option value="">Selecciona tu Nombre...</option></select>
            <input type="password" id="staff-pass" placeholder="Contraseña Mesero" style="margin-top:8px;">
            <input type="text" id="staff-cliente" placeholder="Mesa / Nombre del Cliente" style="margin-top:8px;">
            <button class="btn btn-success" onclick="ingresarMenuStaff()" style="margin-top:12px;">Ingresar al Menú de Mesero</button>
        </div>

        <!-- Modo Directo cuando 'Sin Meseros' está activo -->
        <div id="staff-direct-card" class="admin-card hidden">
            <h3 style="color:var(--accent);">⚡ Comandero Directo (Sin Meseros)</h3>
            <p style="font-size:0.85rem; color:#94a3b8; margin:0 0 10px 0;">Modo rápido activo. Ingrese únicamente la mesa o cliente:</p>
            <input type="text" id="staff-direct-cliente" placeholder="Mesa / Nombre del Cliente">
            <button class="btn btn-success" onclick="ingresarMenuDirecto()" style="margin-top:12px;">🚀 Tomar Pedido Ahora</button>
        </div>

        <div id="staff-orders-section" class="admin-card">
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
    const sinMeseros = await getConfig('modo_sin_meseros', 'false');
    if (sinMeseros === 'true') {
        document.getElementById('staff-form-card').classList.add('hidden');
        document.getElementById('staff-direct-card').classList.remove('hidden');
    } else {
        const select = document.getElementById('staff-select-mesero');
        if (_supabase) {
            try {
                const { data } = await _supabase.from('meseros').select('*');
                if (data && data.length > 0) {
                    data.forEach(m => select.innerHTML += `<option value="${m.nombre}">${m.nombre}</option>`);
                }
            } catch(e){}
        }
        select.innerHTML += '<option value="Luis">Luis</option><option value="Ana">Ana</option>';
    }

    cargarPedidosStaffGral();
});

function ingresarMenuStaff() {
    const select = document.getElementById('staff-select-mesero');
    const name = select.value;
    const pass = document.getElementById('staff-pass').value;
    const mesa = document.getElementById('staff-cliente').value;

    if (!name || !pass || !mesa) return alert('Por favor selecciona Mesero, Contraseña y Mesa/Cliente.');

    window.location.href = `index.html?origen=Staff&mesero=${encodeURIComponent(name)}&mesa=${encodeURIComponent(mesa)}`;
}

function ingresarMenuDirecto() {
    const mesa = document.getElementById('staff-direct-cliente').value;
    if (!mesa) return alert('Por favor ingrese la Mesa o Nombre del Cliente.');

    window.location.href = `index.html?origen=Staff&mesero=${encodeURIComponent('Comandero Directo')}&mesa=${encodeURIComponent(mesa)}`;
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
    setInterval(cargarCocina, 1000);
});

async function cargarCocina() {
    const container = document.getElementById('cocina-orders');
    if (!container) return;

    const todos = await obtenerPedidosSync();
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

print("ACTUALIZACION_COMPLETA_EXITOSA")
