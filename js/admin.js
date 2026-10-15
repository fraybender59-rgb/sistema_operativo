let modoSinMeseros = true;

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
        const pass = prompt(`Autorización requerida para ${metodo.toUpperCase()}.
Ingrese clave admin:`);
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
