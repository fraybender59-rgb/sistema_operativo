const MENU_DEFAULT = [
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
    let msg = `🌊 *NUEVO PEDIDO - MAR Y SAZÓN*

📌 *Cliente/Mesa:* ${cliente}
💳 *Pago:* ${metodo_pago}

*Detalles:*
`;
    carrito.forEach(c => { msg += `- ${c.cantidad}x ${c.nombre} ($${(c.precio * c.cantidad).toFixed(2)}) ${c.comentario ? '['+c.comentario+']' : ''}
`; });
    msg += `
💰 *Total:* $${total.toFixed(2)}`;

    alert('¡Pedido realizado con éxito!');
    if (waNum) window.open(`https://wa.me/52${waNum}?text=${encodeURIComponent(msg)}`, '_blank');

    carrito = [];
    actualizarTotal();
    document.getElementById('nombre-cliente').value = '';
}