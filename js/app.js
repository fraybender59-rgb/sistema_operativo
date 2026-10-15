
// Imágenes SVG garantizadas que cargan sin necesidad de conexión externa
const SVG_COCTEL = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200"><rect width="300" height="200" fill="%230f172a"/><path d="M100 60 L200 60 L150 130 Z" fill="%23f59e0b" opacity="0.8"/><rect x="145" y="130" width="10" height="40" fill="%23cbd5e1"/><rect x="120" y="170" width="60" height="10" fill="%23cbd5e1"/><circle cx="150" cy="50" r="15" fill="%23ef4444"/><text x="150" y="190" fill="%2338bdf8" font-size="14" font-family="sans-serif" text-anchor="middle">Cóctel de Camarón</text></svg>';
const SVG_CEVICHE = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200"><rect width="300" height="200" fill="%230f172a"/><circle cx="150" cy="110" r="60" fill="%231e293b" stroke="%23f59e0b" stroke-width="4"/><circle cx="130" cy="100" r="12" fill="%2310b981"/><circle cx="165" cy="115" r="14" fill="%23ef4444"/><circle cx="150" cy="125" r="10" fill="%23f59e0b"/><text x="150" y="190" fill="%2338bdf8" font-size="14" font-family="sans-serif" text-anchor="middle">Ceviche Fresco</text></svg>';
const SVG_AGUACHILE = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200"><rect width="300" height="200" fill="%230f172a"/><ellipse cx="150" cy="110" rx="70" ry="45" fill="%23064e3b" stroke="%2310b981" stroke-width="4"/><path d="M110 110 Q 150 80 190 110" stroke="%23ef4444" stroke-width="6" fill="none"/><text x="150" y="190" fill="%2338bdf8" font-size="14" font-family="sans-serif" text-anchor="middle">Aguachile Especial</text></svg>';
const SVG_TACOS = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200"><rect width="300" height="200" fill="%230f172a"/><path d="M80 130 A 70 50 0 0 1 220 130 Z" fill="%23d97706"/><path d="M90 125 A 60 40 0 0 1 210 125 Z" fill="%23ef4444"/><text x="150" y="190" fill="%2338bdf8" font-size="14" font-family="sans-serif" text-anchor="middle">Tacos Gobernador / Baja</text></svg>';
const SVG_COMBO = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200"><rect width="300" height="200" fill="%230f172a"/><rect x="80" y="60" width="50" height="90" rx="8" fill="%23f59e0b"/><rect x="170" y="50" width="35" height="100" rx="5" fill="%23d97706"/><text x="150" y="190" fill="%2338bdf8" font-size="14" font-family="sans-serif" text-anchor="middle">Combo + Cerveza</text></svg>';

const MENU_DEFAULT = [
    { id: 1, categoria: 'Cócteles', nombre: 'Cóctel de Camarón Grande', descripcion: 'Cóctel grande preparado con camarón fresco', precio: 150.00, img: SVG_COCTEL },
    { id: 2, categoria: 'Cócteles', nombre: 'Cóctel camaron chico', descripcion: 'Cóctel chico de camarón fresco', precio: 120.00, img: SVG_COCTEL },
    { id: 3, categoria: 'Céviches', nombre: 'Ceviche de Camarón grande', descripcion: 'Ceviche fresco de camarón picado', precio: 140.00, img: SVG_CEVICHE },
    { id: 4, categoria: 'Céviches', nombre: 'Ceviche de Camarones chico', descripcion: 'Porción chica de ceviche de camarón', precio: 110.00, img: SVG_CEVICHE },
    { id: 5, categoria: 'Céviches', nombre: 'Ceviche de pescado grande', descripcion: 'Ceviche tradicional de pescado fresco', precio: 130.00, img: SVG_CEVICHE },
    { id: 6, categoria: 'Céviches', nombre: 'Ceviche de pescado chic', descripcion: 'Porción chica de ceviche de pescado', precio: 130.00, img: SVG_CEVICHE },
    { id: 7, categoria: 'Aguachiles', nombre: 'Aguachile de Camarón', descripcion: 'Camarones curtidos en limón y chile', precio: 80.00, img: SVG_AGUACHILE },
    { id: 8, categoria: 'Aguachiles', nombre: 'Aguachile de Pescado', descripcion: 'Pescado fresco curtido en limón', precio: 70.00, img: SVG_AGUACHILE },
    { id: 9, categoria: 'Tacos', nombre: 'orden tacos gobernador (4 tacos)', descripcion: '4 tacos gobernador con camarón y queso', precio: 220.00, img: SVG_TACOS },
    { id: 10, categoria: 'Tacos', nombre: 'Orden tacos estilo baja (4 tacos)', descripcion: '4 tacos de pescado capeado estilo Baja', precio: 200.00, img: SVG_TACOS },
    { id: 11, categoria: 'Combos', nombre: 'Combo Tacos Gobernador + Corona', descripcion: '4 Tacos Gobernador + 1 Cerveza Corona', precio: 220.00, img: SVG_COMBO },
    { id: 12, categoria: 'Combos', nombre: 'Combo Cóctel Camarón + Corona', descripcion: '1 Cóctel de Camarón + 1 Cerveza Corona', precio: 160.00, img: SVG_COMBO },
    { id: 13, categoria: 'Combos', nombre: 'Combo Aguachile Camarón + Corona', descripcion: '1 Aguachile de Camarón + 1 Cerveza Corona', precio: 100.00, img: SVG_COMBO }
];

const PROMO_SLIDES = [SVG_COCTEL, SVG_CEVICHE, SVG_TACOS];

let currentPromoIdx = 0;
let menuData = [...MENU_DEFAULT];
let carrito = [];
let itemSeleccionado = null;
let cantidadTemp = 1;
let esModoStaff = false;

document.addEventListener('DOMContentLoaded', async () => {
    limpiarComprobantesAntiguos();
    await sincronizarMenu();
    await comprobarModoSinMeseros();
    detectarModoStaff();
    renderCategorias();
    renderMenu(menuData);
    cargarMeseros();
    cargarCuentaTransferencia();
    iniciarSlideshowPromos();
    
    // Cargar imagen inicial en modal bienvenida
    document.getElementById('promo-slide-img').src = PROMO_SLIDES[0];
});

async function sincronizarMenu() {
    menuData = MENU_DEFAULT.map(item => {
        const localP = localStorage.getItem(`precio_prod_${item.id}`);
        return {
            ...item,
            precio: localP ? parseFloat(localP) : item.precio
        };
    });
}

function iniciarSlideshowPromos() {
    const banner = document.getElementById('top-promo-banner');
    if (!banner) return;
    banner.style.backgroundImage = `url('${PROMO_SLIDES[0]}')`;
    setInterval(() => {
        currentPromoIdx = (currentPromoIdx + 1) % PROMO_SLIDES.length;
        banner.style.backgroundImage = `url('${PROMO_SLIDES[currentPromoIdx]}')`;
    }, 4000);
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
                <p class="price">$${parseFloat(item.precio).toFixed(2)}</p>
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
        let msg = `🌊 *NUEVO PEDIDO - MAR Y SAZÓN*

📌 *Cliente/Mesa:* ${cliente}
👨‍🍳 *Atiende:* ${mesero_nombre}
💳 *Pago:* ${metodo_pago}

*Detalles:*
`;
        carrito.forEach(c => { msg += `- ${c.cantidad}x ${c.nombre} ($${(c.precio * c.cantidad).toFixed(2)}) ${c.comentario ? '['+c.comentario+']' : ''}
`; });
        msg += `
💰 *Total:* $${total.toFixed(2)}`;
        if (waNum) window.open(`https://wa.me/52${waNum}?text=${encodeURIComponent(msg)}`, '_blank');
    }

    carrito = [];
    actualizarTotal();
    if (!esModoStaff) document.getElementById('nombre-cliente').value = '';
}
