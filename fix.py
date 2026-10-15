import os

# Crear directorios
os.makedirs('css', exist_ok=True)
os.makedirs('js', exist_ok=True)
os.makedirs('carrito', exist_ok=True)

# 1. Configuración de Supabase
supabase_config = """const SUPABASE_URL = 'https://qmctkrnwykbmlvypnctr.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_m31I88aPiTIZWWANwueqSw_EMMgp6jM';
const db = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;
"""

# 2. Estilos CSS completos (diseño idéntico a capturas)
styles_css = """* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
body { background-color: #0d141c; color: #ffffff; padding-bottom: 90px; background-size: cover; background-position: center; background-attachment: fixed; }

.header-title { text-align: center; padding: 20px 10px; background: rgba(13, 20, 28, 0.95); font-size: 1.6rem; font-weight: bold; border-bottom: 2px solid #ff9800; color: #fff; display: flex; align-items: center; justify-content: center; gap: 8px; }

/* Grid de Navegación Admin */
.admin-buttons-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 15px; }
.btn-nav-grid { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 14px 10px; border-radius: 10px; color: white; text-decoration: none; font-weight: bold; font-size: 0.95rem; border: none; cursor: pointer; text-align: center; }
.bg-publico { background: #2c3847; }
.bg-staff { background: #2c3847; }
.bg-almacen { background: #1b5e20; }
.bg-cocina { background: #e65100; }
.bg-corte { background: #f57c00; }
.bg-cobradas { background: #7b1fa2; }
.bg-historial { background: #00897b; }
.bg-comprobantes { background: #d81b60; }
.bg-precios { background: #f57c00; }
.bg-tarjeta { background: #1976d2; }

.seccion-titulo { padding: 10px 15px 5px 15px; font-size: 1.2rem; font-weight: bold; color: #fff; display: flex; align-items: center; gap: 8px; }
.cuentas-tabs { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px 15px; }
.btn-tab { padding: 10px; background: #2c3847; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
.btn-tab.active { background: #ff9800; color: #000; }

.box-ajustes { background: rgba(20, 28, 38, 0.8); margin: 10px 15px; padding: 15px; border-radius: 12px; border: 1px solid #233040; }
.btn-ajuste { width: 100%; padding: 12px; margin-bottom: 10px; border: none; border-radius: 8px; font-weight: bold; color: white; cursor: pointer; text-align: center; }
.btn-warning { background: #f57c00; }
.btn-blue { background: #0288d1; }
.btn-green { background: #00897b; }
.btn-red { background: #d32f2f; }

/* Categorías del Menú */
.categorias-bar { display: flex; overflow-x: auto; gap: 8px; padding: 12px 15px; background: rgba(13, 20, 28, 0.9); }
.categorias-bar button { padding: 8px 16px; border: none; background: #1e2936; color: white; border-radius: 20px; white-space: nowrap; font-weight: 600; cursor: pointer; }
.categorias-bar button.active { background: #2196f3; color: white; }

/* Tarjetas de Producto */
.grid-productos { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; padding: 15px; }
.card-producto { background: #1a232e; border: 1px solid #283545; border-radius: 12px; padding: 12px; text-align: center; display: flex; flex-direction: column; justify-content: space-between; }
.card-producto img { width: 100%; height: 110px; object-fit: cover; border-radius: 8px; }
.card-producto h3 { font-size: 1rem; margin: 8px 0 2px 0; color: #fff; }
.card-producto .precio { color: #ff9800; font-weight: bold; font-size: 1.1rem; margin-bottom: 8px; }
.card-producto button { width: 100%; padding: 10px; background: #ff9800; color: #000; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }

/* Modal de Selección y Cantidad */
.modal { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: #1a232e; padding: 20px; border-radius: 16px; width: 90%; max-width: 400px; border: 1px solid #2c3e50; }
.qty-control { display: flex; align-items: center; justify-content: center; gap: 20px; margin: 15px 0; }
.qty-btn { width: 45px; height: 45px; border-radius: 50%; font-size: 1.5rem; border: none; background: #2196f3; color: white; font-weight: bold; cursor: pointer; }
.qty-val { font-size: 1.5rem; font-weight: bold; }
.modal-content textarea { width: 100%; padding: 10px; background: #0d141c; border: 1px solid #2c3e50; border-radius: 8px; color: white; resize: none; margin-bottom: 12px; }

/* Barra Inferior Pedido */
.cart-footer { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(13, 20, 28, 0.98); padding: 12px 15px; border-top: 1px solid #283545; display: flex; flex-direction: column; gap: 8px; z-index: 100; }
.cart-footer input, .cart-footer select { padding: 10px; background: #1a232e; border: 1px solid #283545; border-radius: 8px; color: white; width: 100%; }
.cart-footer-row { display: flex; justify-content: space-between; align-items: center; margin-top: 4px; }
.btn-pedir { background: #00897b; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 1rem; }

.hidden { display: none !important; }
"""

# 3. Lógica JavaScript Principal (`app.js`)
app_js = """const MENU_ITEMS = [
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

function renderizarMenuClientes(categoria = 'todas') {
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
    let textoWA = `👑 *NUEVO PEDIDO - LA QUEEN*\\n\\n👤 *Cliente/Mesa:* ${clienteNombre}\\n💳 *Pago:* ${metodoPago.toUpperCase()}\\n\\n📋 *Detalle:*\\n`;
    carrito.forEach(i => {
        textoWA += `• ${i.cantidad}x ${i.nombre} ($${i.precio * i.cantidad}) ${i.notas ? '['+i.notas+']' : ''}\\n`;
    });
    textoWA += `\\n💰 *Total:* $${total}.00`;

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
"""

# 4. JS Admin (`admin.js`)
admin_js = """let modoSinMeseros = true;

function validarAccesoAdmin() {
    const pass = document.getElementById('pass-admin').value;
    if (pass === 'IBARRITA') {
        document.getElementById('login-modal').classList.add('hidden');
        document.getElementById('admin-content').classList.remove('hidden');
        cargarCuentasAdmin('clientes');
    } else {
        alert("Contraseña incorrecta.");
    }
}

function cambiarTabCuentas(tab) {
    document.querySelectorAll('.cuentas-tabs button').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    cargarCuentasAdmin(tab);
}

async function cargarCuentasAdmin(tab) {
    const cont = document.getElementById('contenedor-cuentas');
    if (!cont || !db) return;

    const { data: pedidos } = await db.from('pedidos').select('*').eq('estado', 'pendiente');
    cont.innerHTML = '';

    if (!pedidos || pedidos.length === 0) {
        cont.innerHTML = '<p style="color:#8b9bb0; padding:10px;">Sin cuentas abiertas en esta sección.</p>';
        return;
    }

    pedidos.forEach(p => {
        cont.innerHTML += `
            <div style="background:#1a232e; padding:12px; border-radius:10px; margin-bottom:10px; border:1px solid #2c3e50;">
                <h4 style="color:#ff9800;">Pedido #${p.id} - ${p.cliente_nombre || 'Cliente'}</h4>
                <p style="margin:4px 0;">Total: <b style="color:#4caf50;">$${p.total}.00</b> | Pago: ${p.metodo_pago}</p>
                <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:8px;">
                    <button onclick="cobrarCuenta(${p.id}, 'efectivo')" style="background:#4caf50; color:white; border:none; padding:6px 10px; border-radius:5px; font-weight:bold;">Efectivo</button>
                    <button onclick="cobrarCuenta(${p.id}, 'transferencia')" style="background:#2196f3; color:white; border:none; padding:6px 10px; border-radius:5px; font-weight:bold;">Transferencia</button>
                    <button onclick="cobrarCuenta(${p.id}, 'cancelacion')" style="background:#f44336; color:white; border:none; padding:6px 10px; border-radius:5px; font-weight:bold;">Cancelación 🔒</button>
                    <button onclick="cobrarCuenta(${p.id}, 'cortesia')" style="background:#ff9800; color:white; border:none; padding:6px 10px; border-radius:5px; font-weight:bold;">Cortesía 🔒</button>
                    <button onclick="cobrarCuenta(${p.id}, 'descuento')" style="background:#9c27b0; color:white; border:none; padding:6px 10px; border-radius:5px; font-weight:bold;">Descuento 🔒</button>
                </div>
            </div>
        `;
    });
}

async function cobrarCuenta(pedidoId, metodo) {
    const metodosProtegidos = ['cancelacion', 'cortesia', 'descuento'];
    if (metodosProtegidos.includes(metodo)) {
        const pass = prompt(`Autorización requerida para ${metodo.toUpperCase()}.\nIngrese clave admin:`);
        if (pass !== 'IBARRITA') return alert("Acceso denegado. Contraseña incorrecta.");
    }

    const nuevoEstado = metodo === 'cancelacion' ? 'cancelado' : 'cobrado';
    await db.from('pedidos').update({ estado: nuevoEstado, metodo_pago: metodo }).eq('id', pedidoId);
    alert(`Cuenta procesada: ${metodo.toUpperCase()}`);
    cargarCuentasAdmin('clientes');
}

function toggleSinMeseros() {
    modoSinMeseros = !modoSinMeseros;
    const btn = document.getElementById('btn-sin-meseros');
    if(modoSinMeseros) {
        btn.innerText = '✅ Modo "Sin Meseros" ACTIVADO (Clic para desactivar)';
        btn.style.background = '#d32f2f';
    } else {
        btn.innerText = '❌ Modo "Sin Meseros" DESACTIVADO (Clic para activar)';
        btn.style.background = '#388e3c';
    }
    if(db) db.from('configuracion').upsert([{ clave: 'modo_sin_meseros', valor: modoSinMeseros ? 'true' : 'false' }]);
}

async function agregarMeseroStaff() {
    const nombre = document.getElementById('mesero-nombre').value;
    if(!nombre || !db) return alert("Ingresa el nombre del mesero");

    const { data: meseros } = await db.from('meseros').select('*');
    if(meseros && meseros.length >= 10) return alert("Límite máximo de 10 meseros alcanzado.");

    await db.from('meseros').insert([{ nombre: nombre, activo: true }]);
    document.getElementById('mesero-nombre').value = '';
    alert("Mesero agregado con éxito.");
}

async function subirFondo(vista) {
    const fileInput = document.getElementById('file-fondo');
    const file = fileInput ? fileInput.files[0] : null;

    if (!file) return alert("Selecciona una imagen desde tu galería primero.");

    const reader = new FileReader();
    reader.onload = async function (e) {
        const base64Img = e.target.result;
        if (db) {
            await db.from('configuracion').upsert([{ clave: `fondo_${vista}`, valor: base64Img }]);
        }
        document.body.style.backgroundImage = `url('${base64Img}')`;
        alert(`Fondo de ${vista.toUpperCase()} actualizado.`);
    };
    reader.readAsDataURL(file);
}
"""

# 5. HTML Admin (`admin.html` - Réplica de Captura)
admin_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Caja Maestro - Administración</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body>
    <div id="login-modal" class="modal">
        <div class="modal-content" style="text-align:center;">
            <h3>🔒 Acceso Restringido</h3>
            <p style="color:#aaa; font-size:0.85rem; margin:10px 0;">Ingresa la clave de administrador</p>
            <input type="password" id="pass-admin" placeholder="Clave..." style="text-align:center; padding:10px; width:100%; margin-bottom:12px; background:#0d141c; border:1px solid #2c3e50; color:white; border-radius:6px;">
            <button onclick="validarAccesoAdmin()" style="width:100%; padding:10px; background:#ff9800; border:none; font-weight:bold; border-radius:6px; cursor:pointer;">Desbloquear Sistema</button>
        </div>
    </div>

    <div id="admin-content" class="hidden">
        <div class="header-title">⚙️ Caja Maestro - Administración</div>

        <!-- Botones Botonera Principal -->
        <div class="admin-buttons-grid">
            <a href="index.html" class="btn-nav-grid bg-publico">📱 Comandero Público</a>
            <a href="staff.html" class="btn-nav-grid bg-staff">📝 Comandero Staff</a>
            <a href="almacen.html" class="btn-nav-grid bg-almacen">📦 Almacén</a>
            <a href="#" class="btn-nav-grid bg-cocina">🧑‍🍳 Cocina</a>
            <button class="btn-nav-grid bg-corte">💰 Corte</button>
            <button class="btn-nav-grid bg-cobradas">📁 Cobradas Hoy</button>
            <button class="btn-nav-grid bg-historial">📅 Historial de Días</button>
            <button class="btn-nav-grid bg-comprobantes">📸 Ver Comprobantes</button>
            <button class="btn-nav-grid bg-precios">✏️ Precios</button>
            <button class="btn-nav-grid bg-tarjeta">💳 Config Tarjeta</button>
        </div>

        <!-- Caja Principal y Cuentas -->
        <div class="seccion-titulo">📝 Caja Principal</div>
        <div class="cuentas-tabs">
            <button class="btn-tab active" onclick="cambiarTabCuentas('clientes')">👤 Clientes</button>
            <button class="btn-tab" onclick="cambiarTabCuentas('staff')">👨‍🍳 Staff</button>
        </div>
        <div id="contenedor-cuentas" style="padding:0 15px;"></div>

        <!-- Ajustes del Sistema -->
        <div class="seccion-titulo">⚙️ Ajustes del Sistema</div>
        <div class="box-ajustes">
            <button class="btn-ajuste btn-warning">Cambiar Contraseña Admin</button>
            <button class="btn-ajuste btn-blue">Cambiar WhatsApp Recepción</button>
            <button class="btn-ajuste btn-green">Cambiar Número de Cuenta Bancaria</button>
        </div>

        <!-- Fondo de Pantalla -->
        <div class="seccion-titulo">🖼️ Fondo de Clientes (Galería)</div>
        <div class="box-ajustes">
            <input type="file" id="file-fondo" accept="image/*" style="width:100%; padding:8px; background:#0d141c; border:1px solid #233040; color:white; border-radius:6px; margin-bottom:10px;">
            <div style="display:flex; gap:8px;">
                <button onclick="subirFondo('admin')" style="flex:1; padding:8px; background:#2c3847; color:white; border:none; border-radius:6px; font-weight:bold;">Fondo Admin</button>
                <button onclick="subirFondo('staff')" style="flex:1; padding:8px; background:#2c3847; color:white; border:none; border-radius:6px; font-weight:bold;">Fondo Staff</button>
                <button onclick="subirFondo('cliente')" style="flex:1; padding:8px; background:#2c3847; color:white; border:none; border-radius:6px; font-weight:bold;">Fondo Clientes</button>
            </div>
        </div>

        <!-- Gestión de Meseros -->
        <div class="seccion-titulo">👥 Gestión de Meseros (Max 10)</div>
        <div class="box-ajustes">
            <button id="btn-sin-meseros" onclick="toggleSinMeseros()" class="btn-ajuste btn-red">✅ Modo "Sin Meseros" ACTIVADO (Clic para desactivar)</button>
            <input type="text" id="mesero-nombre" placeholder="Nombre Mesero" style="width:100%; padding:10px; margin-bottom:8px; background:#0d141c; border:1px solid #233040; color:white; border-radius:6px;">
            <button onclick="agregarMeseroStaff()" class="btn-ajuste btn-green" style="margin-bottom:0;">Agregar Mesero</button>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/app.js"></script>
    <script src="js/admin.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => cargarFondoPantalla('admin'));
    </script>
</body>
</html>
"""

# 6. HTML Clientes (`index.html`)
index_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menú Digital - La Queen</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body id="body-cliente">
    <div class="header-title">👑 Menú Digital - La Queen</div>

    <div class="categorias-bar">
        <button class="active" onclick="filtrarCategoria('todas')">Todas</button>
        <button onclick="filtrarCategoria('sencillas')">Sencillas</button>
        <button onclick="filtrarCategoria('clasicas')">Clásicas</button>
        <button onclick="filtrarCategoria('combinadas')">Combinadas</button>
        <button onclick="filtrarCategoria('especiales')">Especiales</button>
        <button onclick="filtrarCategoria('gigantes')">El Tamaño Sí Importa</button>
        <button onclick="filtrarCategoria('extras')">Extras y Bebidas</button>
    </div>

    <div id="contenedor-productos" class="grid-productos"></div>

    <!-- Modal Producto con Selección de Cantidad y Comentarios -->
    <div id="modal-producto" class="modal hidden">
        <div class="modal-content">
            <h3 id="modal-title" style="color:#ff9800;"></h3>
            <p id="modal-desc" style="font-size:0.85rem; color:#aaa; margin-bottom:10px;"></p>
            
            <div class="qty-control">
                <button class="qty-btn" onclick="cambiarCantidadModal(-1)">-</button>
                <span id="qty-count" class="qty-val">1</span>
                <button class="qty-btn" onclick="cambiarCantidadModal(1)">+</button>
            </div>

            <textarea id="modal-notas" rows="3" placeholder="Notas/Comentarios (Ej. Sin cebolla, picante aparte...)"></textarea>

            <button onclick="agregarModalAlPedido()" style="background:#388e3c; color:white; width:100%; padding:12px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; margin-bottom:8px;">Agregar al Pedido</button>
            <button onclick="cerrarModalProducto()" style="background:#d32f2f; color:white; width:100%; padding:10px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Cancelar</button>
        </div>
    </div>

    <!-- Barra Inferior de Pedido -->
    <div class="cart-footer">
        <input type="text" id="cliente-nombre" placeholder="Mesa / Nombre del Cliente">
        <select id="metodo-pago" onchange="cambiarMetodoPagoSelect()">
            <option value="efectivo">Efectivo al recibir</option>
            <option value="transferencia">Transferencia bancaria</option>
        </select>
        <div id="info-transferencia" class="hidden" style="font-size:0.8rem; color:#ff9800; text-align:center;">Transferir a: 1234 5678 9012 3456 (BBVA)</div>
        <div class="cart-footer-row">
            <span id="cart-total" style="font-size:1.2rem; font-weight:bold; color:#4caf50;">Total: $0.00</span>
            <button onclick="confirmarPedidoFinal('cliente')" class="btn-pedir">🚀 Pedir a Cocina</button>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/app.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            cargarFondoPantalla('cliente');
            renderizarMenuClientes();
        });
    </script>
</body>
</html>
"""

# 7. HTML Staff (`staff.html` - Sin Carrito Flotante Público)
staff_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Punto Staff - Meseros</title>
    <link rel="stylesheet" href="css/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<body id="body-staff">
    <div class="header-title">👨‍🍳 Punto Staff - Meseros</div>

    <div id="bloqueo-staff" class="hidden" style="margin:20px; padding:15px; background:#d32f2f; border-radius:10px; text-align:center;">
        <h3>🚫 Acceso Bloqueado</h3>
        <p style="margin-top:8px;">El Modo "Sin Meseros" se encuentra activado desde Administración.</p>
    </div>

    <div id="contenido-staff">
        <div class="categorias-bar">
            <button class="active" onclick="filtrarCategoria('todas')">Todas</button>
            <button onclick="filtrarCategoria('sencillas')">Sencillas</button>
            <button onclick="filtrarCategoria('clasicas')">Clásicas</button>
            <button onclick="filtrarCategoria('combinadas')">Combinadas</button>
            <button onclick="filtrarCategoria('especiales')">Especiales</button>
            <button onclick="filtrarCategoria('gigantes')">El Tamaño Sí Importa</button>
            <button onclick="filtrarCategoria('extras')">Extras y Bebidas</button>
        </div>

        <div id="contenedor-productos" class="grid-productos"></div>

        <div class="cart-footer">
            <input type="text" id="cliente-nombre" placeholder="Mesa / Nombre del Cliente">
            <select id="metodo-pago">
                <option value="efectivo">Efectivo al recibir</option>
                <option value="transferencia">Transferencia bancaria</option>
            </select>
            <div class="cart-footer-row">
                <span id="cart-total" style="font-size:1.2rem; font-weight:bold; color:#4caf50;">Total: $0.00</span>
                <button onclick="confirmarPedidoFinal('staff')" class="btn-pedir">🚀 Pedir a Cocina</button>
            </div>
        </div>
    </div>

    <!-- Modal Producto -->
    <div id="modal-producto" class="modal hidden">
        <div class="modal-content">
            <h3 id="modal-title" style="color:#ff9800;"></h3>
            <p id="modal-desc" style="font-size:0.85rem; color:#aaa; margin-bottom:10px;"></p>
            <div class="qty-control">
                <button class="qty-btn" onclick="cambiarCantidadModal(-1)">-</button>
                <span id="qty-count" class="qty-val">1</span>
                <button class="qty-btn" onclick="cambiarCantidadModal(1)">+</button>
            </div>
            <textarea id="modal-notas" rows="3" placeholder="Notas/Comentarios (Ej. Sin cebolla...)"></textarea>
            <button onclick="agregarModalAlPedido()" style="background:#388e3c; color:white; width:100%; padding:12px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; margin-bottom:8px;">Agregar al Pedido</button>
            <button onclick="cerrarModalProducto()" style="background:#d32f2f; color:white; width:100%; padding:10px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Cancelar</button>
        </div>
    </div>

    <script src="js/supabase_config.js"></script>
    <script src="js/app.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', async () => {
            cargarFondoPantalla('staff');
            if(db) {
                const { data } = await db.from('configuracion').select('valor').eq('clave', 'modo_sin_meseros').single();
                if(data && data.valor === 'true') {
                    document.getElementById('bloqueo-staff').classList.remove('hidden');
                    document.getElementById('contenido-staff').classList.add('hidden');
                    return;
                }
            }
            renderizarMenuClientes();
        });
    </script>
</body>
</html>
"""

# 8. Generar archivos físicamente
with open('js/supabase_config.js', 'w') as f: f.write(supabase_config)
with open('css/styles.css', 'w') as f: f.write(styles_css)
with open('js/app.js', 'w') as f: f.write(app_js)
with open('js/admin.js', 'w') as f: f.write(admin_js)
with open('index.html', 'w') as f: f.write(index_html)
with open('staff.html', 'w') as f: f.write(staff_html)
with open('admin.html', 'w') as f: f.write(admin_html)

print("ARCHIVOS_ACTUALIZADOS_OK")
