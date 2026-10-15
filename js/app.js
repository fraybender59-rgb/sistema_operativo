import { supabase, cargarFondo } from './supabase.js';

let carrito = [];
let total = 0;

document.addEventListener('DOMContentLoaded', async () => {
    await cargarFondo();
    await cargarMenu();
    await cargarMeserosSelect();

    document.getElementById('btn-enviar-pedido').addEventListener('click', enviarPedido);
});

async function cargarMenu() {
    const { data, error } = await supabase.from('almacen').select('*').gt('cantidad', 0);
    const grid = document.getElementById('menu-items');
    
    if(data) {
        grid.innerHTML = data.map(item => `
            <div class="menu-card" onclick="agregarAlCarrito(${item.id}, '${item.nombre_producto}', ${item.precio})">
                <h3>${item.nombre_producto}</h3>
                <p class="price">$${item.precio}</p>
            </div>
        `).join('');
    }
}

async function cargarMeserosSelect() {
    const { data } = await supabase.from('meseros').select('*');
    const select = document.getElementById('select-mesero');
    if(data) {
        data.forEach(m => {
            select.innerHTML += `<option value="${m.id}">${m.nombre}</option>`;
        });
    }
}

window.agregarAlCarrito = (id, nombre, precio) => {
    carrito.push({ id, nombre, precio });
    total += parseFloat(precio);
    document.getElementById('total-price').innerText = total.toFixed(2);
};

async function enviarPedido() {
    const cliente = document.getElementById('nombre-cliente').value;
    const mesero_id = document.getElementById('select-mesero').value;

    if (!cliente || carrito.length === 0 || !mesero_id) {
        return alert('Datos incompletos.');
    }

    const { data: pedidoData } = await supabase.from('pedidos')
        .insert([{ cliente_mesa: cliente, mesero_id, total }])
        .select();

    const pedidoId = pedidoData[0].id;

    const detalles = carrito.map(item => ({
        pedido_id: pedidoId,
        producto_id: item.id,
        cantidad: 1
    }));

    await supabase.from('detalles_pedido').insert(detalles);

    alert('¡Pedido enviado a cocina!');
    carrito = [];
    total = 0;
    document.getElementById('total-price').innerText = '0';
}
