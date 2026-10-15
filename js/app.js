cat << 'EOF' > js/app.js
import { supabase, getConfig } from './supabase.js';

let menuData = [];
let carrito = [];
let itemSeleccionado = null;
let cantidadTemp = 1;

document.addEventListener('DOMContentLoaded', async () => {
    iniciarSlideshow();
    await cargarMenu();
    await cargarMeseros();
    await cargarCuentaTransferencia();

    document.getElementById('metodo-pago').addEventListener('change', (e) => {
        const divInfo = document.getElementById('info-transferencia');
        if (e.target.value === 'Transferencia') divInfo.classList.remove('hidden');
        else divInfo.classList.add('hidden');
    });

    document.getElementById('btn-plus').addEventListener('click', () => { cantidadTemp++; document.getElementById('modal-qty').innerText = cantidadTemp; });
    document.getElementById('btn-minus').addEventListener('click', () => { if (cantidadTemp > 1) cantidadTemp--; document.getElementById('modal-qty').innerText = cantidadTemp; });
    document.getElementById('btn-close-modal').addEventListener('click', () => document.getElementById('modal-item').classList.add('hidden'));
    document.getElementById('btn-add-modal').addEventListener('click', agregarAlCarritoDesdeModal);
    document.getElementById('btn-enviar-pedido').addEventListener('click', enviarPedido);
});

async function iniciarSlideshow() {
    const rawFondo = await getConfig('fondo_slideshow');
    let imagenes = rawFondo ? JSON.parse(rawFondo) : [];
    if (imagenes.length === 0) return;
    let idx = 0;
    const bgDiv = document.getElementById('bg-slideshow');
    bgDiv.style.backgroundImage = `url(${imagenes[0]})`;
    setInterval(() => {
        idx = (idx + 1) % imagenes.length;
        bgDiv.style.backgroundImage = `url(${imagenes[idx]})`;
    }, 5000);
}

async function cargarMenu() {
    const { data } = await supabase.from('menu').select('*');
    if (!data) return;
    menuData = data;
    const categorias = [...new Set(data.map(i => i.categoria))];
    
    const catContainer = document.getElementById('cat-container');
    catContainer.innerHTML = `<button class="cat-btn active" onclick="filtrarCat('Todas', this)">Todas</button>`;
    categorias.forEach(cat => {
        catContainer.innerHTML += `<button class="cat-btn" onclick="filtrarCat('${cat}', this)">${cat}</button>`;
    });

    renderMenu(menuData);
}

window.filtrarCat = (cat, btn) => {
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    if (cat === 'Todas') renderMenu(menuData);
    else renderMenu(menuData.filter(i => i.categoria === cat));
};

function renderMenu(items) {
    const grid = document.getElementById('menu-items');
    grid.innerHTML = items.map(item => `
        <div class="menu-card" onclick="abrirModal(${item.id})">
            <h3>${item.nombre}</h3>
            <p style="font-size:0.8rem; color:#94a3b8;">${item.descripcion || ''}</p>
            <p class="price">$${item.precio}</p>
        </div>
    `).join('');
}

window.abrirModal = (id) => {
    itemSeleccionado = menuData.find(i => i.id === id);
    cantidadTemp = 1;
    document.getElementById('modal-title').innerText = itemSeleccionado.nombre;
    document.getElementById('modal-desc').innerText = itemSeleccionado.descripcion || '';
    document.getElementById('modal-qty').innerText = 1;
    document.getElementById('modal-comment').value = '';
    document.getElementById('modal-item').classList.remove('hidden');
};

function agregarAlCarritoDesdeModal() {
    const comentario = document.getElementById('modal-comment').value;
    carrito.push({
        nombre: itemSeleccionado.nombre,
        precio: parseFloat(itemSeleccionado.precio),
        cantidad: cantidadTemp,
        comentario
    });
    actualizarTotal();
    document.getElementById('modal-item').classList.add('hidden');
}

function actualizarTotal() {
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    document.getElementById('total-price').innerText = total.toFixed(2);
}

async function cargarMeseros() {
    const { data } = await supabase.from('meseros').select('*');
    const select = document.getElementById('select-mesero');
    if (data) data.forEach(m => select.innerHTML += `<option value="${m.id}">${m.nombre}</option>`);
}

async function cargarCuentaTransferencia() {
    const cuenta = await getConfig('cuenta_transferencia');
    document.getElementById('info-transferencia').innerText = `Transferir a: ${cuenta || 'Consultar en caja'}`;
}

async function enviarPedido() {
    const cliente = document.getElementById('nombre-cliente').value;
    const mesero_id = document.getElementById('select-mesero').value;
    const metodo_pago = document.getElementById('metodo-pago').value;

    if (!cliente || !mesero_id || carrito.length === 0) return alert('Por favor ingresa Mesa/Cliente, selecciona Mesero y agrega platillos.');

    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    const { data: pedidoData, error } = await supabase.from('pedidos')
        .insert([{ cliente_mesa: cliente, mesero_id, total, metodo_pago, estado: 'pendiente' }]).select();

    if (error) return alert('Error al enviar pedido.');

    const pedidoId = pedidoData[0].id;
    const detalles = carrito.map(i => ({
        pedido_id: pedidoId,
        producto_nombre: i.nombre,
        precio: i.precio,
        cantidad: i.cantidad,
        comentario: i.comentario
    }));

    await supabase.from('detalles_pedido').insert(detalles);

    // Enviar a WhatsApp
    const waNum = await getConfig('whatsapp_num');
    let msg = `🌊 *NUEVO PEDIDO - MAR Y SAZÓN*\n\n📌 *Cliente/Mesa:* ${cliente}\n💳 *Pago:* ${metodo_pago}\n\n*Detalles:*\n`;
    carrito.forEach(c => { msg += `- ${c.cantidad}x ${c.nombre} ($${c.precio * c.cantidad}) ${c.comentario ? '['+c.comentario+']' : ''}\n`; });
    msg += `\n💰 *Total:* $${total.toFixed(2)}`;

    alert('¡Pedido enviado a Cocina exitosamente!');
    if (waNum) window.open(`https://wa.me/52${waNum}?text=${encodeURIComponent(msg)}`, '_blank');

    carrito = [];
    actualizarTotal();
    document.getElementById('nombre-cliente').value = '';
}
EOF
