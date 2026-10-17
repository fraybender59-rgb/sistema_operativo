const MENU_ITEMS = [
    { id: 1, nombre: 'Milanesa', precio: 75, cat: 'sencillas', desc: 'Torta sencilla de milanesa de res.', img: 'carrito/1.jpg' },
    { id: 2, nombre: 'Pierna', precio: 75, cat: 'sencillas', desc: 'Torta sencilla de pierna horneada.', img: 'carrito/2.jpg' },
    { id: 3, nombre: 'Salchicha', precio: 75, cat: 'sencillas', desc: 'Torta sencilla de salchicha.', img: 'carrito/3.jpg' },
    { id: 4, nombre: 'Jamón', precio: 75, cat: 'sencillas', desc: 'Torta sencilla de jamón de pierna.', img: 'carrito/4.jpg' },
    { id: 5, nombre: 'Huevo', precio: 75, cat: 'sencillas', desc: 'Torta sencilla de huevo al gusto.', img: 'carrito/5.jpg' },
    { id: 6, nombre: 'Chuleta', precio: 75, cat: 'sencillas', desc: 'Torta sencilla de chuleta ahumada.', img: 'carrito/6.jpg' },
    { id: 7, nombre: 'Q. Puerco', precio: 75, cat: 'sencillas', desc: 'Torta sencilla de queso de puerco.', img: 'carrito/7.jpg' },
    { id: 8, nombre: 'Verónica', precio: 80, cat: 'clasicas', desc: 'Milanesa, salchicha y queso Oaxaca.', img: 'carrito/8.jpg' },
    { id: 9, nombre: 'Tatiana', precio: 80, cat: 'clasicas', desc: 'Milanesa, pierna y queso Oaxaca.', img: 'carrito/9.jpg' },
    { id: 10, nombre: 'Mexiquense', precio: 80, cat: 'clasicas', desc: 'Milanesa, chorizo y queso Oaxaca.', img: 'carrito/10.jpg' },
    { id: 11, nombre: 'Alemana', precio: 80, cat: 'clasicas', desc: 'Milanesa, piña y queso Oaxaca.', img: 'carrito/11.jpg' },
    { id: 12, nombre: 'Texana', precio: 80, cat: 'clasicas', desc: 'Milanesa, chuleta y queso Oaxaca.', img: 'carrito/12.jpg' },
    { id: 13, nombre: 'Pachuqueña', precio: 80, cat: 'clasicas', desc: 'Milanesa, pierna y piña.', img: 'carrito/13.jpg' },
    { id: 14, nombre: 'Española', precio: 80, cat: 'clasicas', desc: 'Milanesa, pierna y huevo.', img: 'carrito/14.jpg' },
    { id: 15, nombre: 'Argentina', precio: 80, cat: 'clasicas', desc: 'Milanesa, queso amarillo y queso Oaxaca.', img: 'carrito/15.jpg' },
    { id: 16, nombre: 'Trailera', precio: 80, cat: 'combinadas', desc: 'Salchicha, pierna y queso Oaxaca.', img: 'carrito/16.jpg' },
    { id: 17, nombre: 'Toluqueña', precio: 80, cat: 'combinadas', desc: 'Salchicha, chorizo y queso Oaxaca.', img: 'carrito/17.jpg' },
    { id: 18, nombre: 'Italiana', precio: 80, cat: 'combinadas', desc: 'Jamón, queso amarillo y queso Oaxaca.', img: 'carrito/18.jpg' },
    { id: 19, nombre: 'Suiza', precio: 85, cat: 'combinadas', desc: 'Queso amarillo, queso Oaxaca y queso blanco.', img: 'carrito/19.jpg' },
    { id: 20, nombre: 'Especial', precio: 85, cat: 'especiales', desc: 'Milanesa, pierna, piña y queso Oaxaca.', img: 'carrito/20.jpg' },
    { id: 21, nombre: 'Diabla', precio: 85, cat: 'especiales', desc: 'Milanesa, chorizo, piña y queso Oaxaca.', img: 'carrito/21.jpg' },
    { id: 22, nombre: 'Mega Cubana Queen', precio: 150, cat: 'especiales', desc: 'Milanesa, salchicha, jamón, pierna, huevo, quesillo y tocino extra.', img: 'carrito/22.jpg' },
    { id: 23, nombre: 'Insaciable', precio: 90, cat: 'gigantes', desc: 'Milanesa, pierna, salchicha, chuleta y queso Oaxaca.', img: 'carrito/23.jpg' },
    { id: 24, nombre: 'Cubana', precio: 135, cat: 'gigantes', desc: 'Todos los ingredientes.', img: 'carrito/24.jpg' },
    { id: 25, nombre: 'Ingrediente Extra', precio: 5, cat: 'extras', desc: 'Porción o ingrediente extra.', img: 'carrito/25.jpg' },
    { id: 26, nombre: 'Coca Cola', precio: 30, cat: 'extras', desc: 'Refresco Coca Cola 600 ml.', img: 'carrito/26.jpg' },
    { id: 27, nombre: 'Agua Embotellada', precio: 20, cat: 'extras', desc: 'Agua embotellada 500 ml.', img: 'carrito/27.jpg' }
];

let carrito = [];
let productoSeleccionado = null;
let cantidadTemp = 1;


// --- RENDERIZADOR ADAPTATIVO (INDEX OSCURO / STAFF CLARO) ---

// Función para ignorar acentos y mayúsculas al hacer clic
function normalizar(texto) {
    if(!texto) return '';
    return texto.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
}

window.renderizarMenu = function(categoria = 'Todas') {
    // Detectar inteligentemente si estamos en el Comandero Staff
    const isStaff = window.location.href.includes('staff') || document.body.style.backgroundColor === 'white' || document.body.style.backgroundColor === '#ffffff' || document.querySelector('.bg-white') !== null;
    
    const contenedor = document.getElementById('menu-container') || document.getElementById('productos-container') || document.querySelector('.productos-grid');
    if (!contenedor) return;

    const catNorm = normalizar(categoria);
    const filtrados = (catNorm === 'todas') 
        ? CATALOGO_MENU 
        : CATALOGO_MENU.filter(p => normalizar(p.categoria) === catNorm);

    if (filtrados.length === 0) {
        contenedor.innerHTML = '<p style="text-align:center; padding:20px; color:#94a3b8;">Sin productos en esta categoría.</p>';
        return;
    }

    if (isStaff) {
        // --- ESTILO STAFF (CLARO / CUADRÍCULA) ---
        contenedor.style.display = 'grid';
        contenedor.style.gridTemplateColumns = 'repeat(2, 1fr)';
        contenedor.style.gap = '10px';
        
        contenedor.innerHTML = filtrados.map(prod => `
            <div onclick="if(typeof agregarAlCarrito === 'function') agregarAlCarrito(${prod.id})" style="background:#ffffff; border-radius:8px; padding:12px; border:1px solid #e2e8f0; text-align:center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); cursor:pointer;">
                <h3 style="margin:0 0 4px 0; color:#1e293b; font-size:1.1rem; font-weight:bold;">${prod.nombre}</h3>
                <div style="color:#16a34a; font-weight:bold; font-size:1.1rem; margin-bottom:6px;">$${prod.precio}</div>
                <p style="color:#64748b; font-size:0.8rem; margin:0; line-height:1.2;">${prod.descripcion}</p>
            </div>
        `).join('');
    } else {
        // --- ESTILO CLIENTES INDEX (OSCURO / LISTA) ---
        contenedor.style.display = 'block';
        contenedor.innerHTML = filtrados.map(prod => `
            <div class="card-producto" style="background:#1e293b; border-radius:12px; padding:15px; margin-bottom:15px; border:1px solid #334155;">
                <div style="background:#475569; height:120px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#94a3b8; font-weight:bold; font-size:1.2rem; margin-bottom:10px;">
                    150 x 150
                </div>
                <h3 style="margin:0 0 4px 0; color:#fff; text-align:center; font-size:1.1rem;">${prod.nombre}</h3>
                <div style="color:#f59e0b; font-weight:bold; text-align:center; font-size:1.2rem; margin-bottom:6px;">$${prod.precio.toFixed(2)}</div>
                <p style="color:#94a3b8; font-size:0.85rem; text-align:center; margin:0 0 12px 0;">${prod.descripcion}</p>
                <button class="btn btn-warning" style="width:100%; font-weight:bold; padding:10px; border-radius:8px; background:#f59e0b; color:#000; border:none; cursor:pointer;" onclick="if(typeof agregarAlCarrito === 'function') agregarAlCarrito(${prod.id})">Añadir al Carrito</button>
            </div>
        `).join('');
    }

    // Cambiar colores del botón presionado respetando tu diseño
    document.querySelectorAll('button, .btn-cat').forEach(btn => {
        const txt = normalizar(btn.innerText);
        const validCats = ['todas', 'sencillas', 'clasicas', 'combinadas', 'especiales', 'el tamano si importa', 'extras y bebidas'];
        if(validCats.includes(txt)) {
            if (txt === catNorm) {
                btn.style.backgroundColor = isStaff ? '#dc2626' : '#3b82f6'; // Rojo en Staff, Azul en Index
                btn.style.color = 'white';
            } else {
                btn.style.backgroundColor = isStaff ? '#e2e8f0' : '#1e293b'; // Gris claro o Gris oscuro
                btn.style.color = isStaff ? '#000' : '#fff';
            }
        }
    });
};

// Autoconectar los clics de los botones al filtro
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button, .btn-cat, .tab').forEach(btn => {
        const txt = normalizar(btn.innerText);
        const validCats = ['todas', 'sencillas', 'clasicas', 'combinadas', 'especiales', 'el tamano si importa', 'extras y bebidas'];
        if(validCats.includes(txt)) {
            // Reemplazar eventos viejos que chocaban
            btn.outerHTML = btn.outerHTML; 
        }
    });
    
    // Reasignar eventos limpios
    document.querySelectorAll('button, .btn-cat, .tab').forEach(btn => {
        const txt = normalizar(btn.innerText);
        const validCats = ['todas', 'sencillas', 'clasicas', 'combinadas', 'especiales', 'el tamano si importa', 'extras y bebidas'];
        if(validCats.includes(txt)) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                window.renderizarMenu(btn.innerText.trim());
            });
        }
    });

    setTimeout(() => window.renderizarMenu('Todas'), 300);
});
const contenedor = document.getElementById('contenedor-productos');
    if (!contenedor) return;
    contenedor.innerHTML = '';

    const filtrados = categoria === 'todas' ? MENU_ITEMS : MENU_ITEMS.filter(i => i.cat === categoria);
    filtrados.forEach(item => {
        contenedor.innerHTML += `
            <div class="card-producto">
                <img src="${item.img}" alt="${item.nombre}" onerror="this.src='https://via.placeholder.com/150'">
                <h3>${item.nombre}</h3>
                <p class="precio">$${item.precio}.00</p>
                <p style="font-size:0.75rem; color:#aaa; margin-bottom:8px;">${item.desc}</p>
                <button onclick="abrirModalProducto(${item.id})">Añadir al Carrito</button>
            </div>
        `;
    });
}

function abrirModalProducto(id) {
    productoSeleccionado = MENU_ITEMS.find(p => p.id === id);
    cantidadTemp = 1;
    document.getElementById('modal-title').innerText = productoSeleccionado.nombre;
    document.getElementById('modal-desc').innerText = productoSeleccionado.desc;
    document.getElementById('qty-count').innerText = cantidadTemp;
    document.getElementById('modal-notas').value = '';
    document.getElementById('modal-producto').classList.remove('hidden');
}

function cambiarCantidadModal(delta) {
    cantidadTemp = Math.max(1, cantidadTemp + delta);
    document.getElementById('qty-count').innerText = cantidadTemp;
}

function agregarModalAlPedido() {
    const notas = document.getElementById('modal-notas').value;
    carrito.push({ ...productoSeleccionado, cantidad: cantidadTemp, notas: notas });
    actualizarTotalCart();
    cerrarModalProducto();
}

function cerrarModalProducto() {
    document.getElementById('modal-producto').classList.add('hidden');
}

function actualizarTotalCart() {
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    if(document.getElementById('cart-total')) document.getElementById('cart-total').innerText = `Total: $${total}.00`;
}

function cambiarMetodoPagoSelect() {
    const metodo = document.getElementById('metodo-pago').value;
    const infoTransf = document.getElementById('info-transferencia');
    if(metodo === 'transferencia') {
        infoTransf.classList.remove('hidden');
    } else {
        infoTransf.classList.add('hidden');
    }
}

// Confirmar pedido -> Alert -> WhatsApp Redirección
async function confirmarPedidoFinal(origen = 'cliente') {
    const clienteNombre = document.getElementById('cliente-nombre').value.trim();
    if(!clienteNombre) return alert("Por favor ingresa Nombre / Mesa");
    if(carrito.length === 0) return alert("El carrito está vacío");

    const metodoPago = document.getElementById('metodo-pago').value;
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    // Guardar en Supabase
    if(db) {
        await db.from('pedidos').insert([{
            cliente_nombre: clienteNombre,
            detalle: carrito,
            total: total,
            estado: 'pendiente',
            metodo_pago: metodoPago
        }]);

        // Restar del Almacén
        for (let item of carrito) {
            let { data: prod } = await db.from('inventario').select('id, cantidad').eq('nombre', item.nombre).single();
            if (prod) {
                let nuevoStock = Math.max(0, prod.cantidad - item.cantidad);
                await db.from('inventario').update({ cantidad: nuevoStock }).eq('id', prod.id);
            }
        }
    }

    // Mensaje requerido al usuario
    alert("¡Gracias por su compra! Para empezar su pedido requerimos el comprobante de pago (transferencia).");

    // Construir resumen para WhatsApp
    let textoWA = `👑 *NUEVO PEDIDO - LA QUEEN*\n\n👤 *Cliente/Mesa:* ${clienteNombre}\n💳 *Pago:* ${metodoPago.toUpperCase()}\n\n📋 *Detalle:*\n`;
    carrito.forEach(i => {
        textoWA += `• ${i.cantidad}x ${i.nombre} ($${i.precio * i.cantidad}) ${i.notas ? '['+i.notas+']' : ''}\n`;
    });
    textoWA += `\n💰 *Total:* $${total}.00`;

    const urlWA = `https://wa.me/52795696184?text=${encodeURIComponent(textoWA)}`;
    carrito = [];
    actualizarTotalCart();
    
    window.location.href = urlWA;
}

async function cargarFondoPantalla(vista) {
    if (!db) return;
    const { data } = await db.from('configuracion').select('valor').eq('clave', `fondo_${vista}`).single();
    if (data && data.valor) {
        document.body.style.backgroundImage = `url('${data.valor}')`;
    }
}
