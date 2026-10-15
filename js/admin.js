import { supabase, cargarFondo } from './supabase.js';

document.addEventListener('DOMContentLoaded', async () => {
    await cargarFondo();
    cargarMeseros();
    cargarAlmacen();
    cargarPedidos();

    // Fondo
    document.getElementById('bg-upload').addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onloadend = async () => {
            const base64String = reader.result;
            await supabase.from('configuracion').update({ valor: base64String }).eq('clave', 'fondo_app');
            alert('Fondo actualizado.');
            cargarFondo();
        };
        reader.readAsDataURL(file);
    });

    // Meseros
    document.getElementById('btn-agregar-mesero').addEventListener('click', async () => {
        const nombre = document.getElementById('nombre-mesero').value;
        if (!nombre) return;
        await supabase.from('meseros').insert([{ nombre }]);
        cargarMeseros();
    });

    async function cargarMeseros() {
        const { data } = await supabase.from('meseros').select('*');
        const lista = document.getElementById('lista-meseros');
        lista.innerHTML = data.map(m => `<li>${m.nombre}</li>`).join('');
    }

    // Almacén
    document.getElementById('btn-agregar-prod').addEventListener('click', async () => {
        const nombre = document.getElementById('prod-nombre').value;
        const cant = document.getElementById('prod-cant').value;
        const precio = document.getElementById('prod-precio').value;
        if (!nombre || !cant || !precio) return;
        await supabase.from('almacen').insert([{ nombre_producto: nombre, cantidad: cant, precio: precio }]);
        cargarAlmacen();
    });

    async function cargarAlmacen() {
        const { data } = await supabase.from('almacen').select('*');
        const lista = document.getElementById('lista-almacen');
        lista.innerHTML = data.map(p => `<li>${p.nombre_producto} - Quedan: ${p.cantidad} - $${p.precio}</li>`).join('');
    }

    // Pedidos y Cobro
    async function cargarPedidos() {
        const { data } = await supabase.from('pedidos').select('*').eq('estado', 'pendiente');
        const lista = document.getElementById('lista-pedidos');
        lista.innerHTML = data.map(p => `
            <div>
                Mesa: ${p.cliente_mesa} - Total: $${p.total}
                <button onclick="cobrar(${p.id}, 'efectivo')">Efectivo</button>
                <button onclick="cobrar(${p.id}, 'transferencia')">Transf.</button>
                <button onclick="cobrarEspecial(${p.id}, 'cancelacion')">Cancelar</button>
            </div>
        `).join('');
    }

    window.cobrar = async (id, metodo) => {
        await supabase.from('pedidos').update({estado: 'cobrado', metodo_pago: metodo}).eq('id', id);
        cargarPedidos();
    };

    window.cobrarEspecial = async (id, metodo) => {
        const pass = prompt(`Contraseña para ${metodo}:`);
        if(pass === 'IBARRITA'){
            await supabase.from('pedidos').update({estado: metodo, metodo_pago: metodo}).eq('id', id);
            cargarPedidos();
        } else {
            alert('Contraseña incorrecta');
        }
    };
});
