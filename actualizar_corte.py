import re

with open('js/admin.js', 'r') as f:
    code = f.read()

nueva_funcion_corte = '''
function abrirModalCorte() {
    obtenerPedidosSync().then(todos => {
        const cobrados = todos.filter(p => p.estado === 'cobrado');
        const totEfectivo = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Efectivo')).reduce((sum, p) => sum + p.total, 0);
        const totTransf = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Transferencia')).reduce((sum, p) => sum + p.total, 0);
        const totalGen = totEfectivo + totTransf;

        const html = `
            <p>💵 <b>Efectivo:</b> $${totEfectivo.toFixed(2)}</p>
            <p>💳 <b>Transferencias:</b> $${totTransf.toFixed(2)}</p>
            <hr style="border-color:#334155;">
            <p style="font-size:1.2rem; color:#10b981;"><b>Total General: $${totalGen.toFixed(2)}</b></p>
            <button class="btn btn-warning" style="margin-top:12px; padding:12px; font-size:1rem;" onclick="ejecutarCorteConRespaldo()">🌅 Realizar Corte del Día y Archivar</button>
        `;

        showModalGen('💰 Corte de Caja Hoy', html);
    });
}

async function ejecutarCorteConRespaldo() {
    const pass = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para procesar el Corte del Día:');
    if (pass !== currentAdminPass && pass !== 'ROXANA') return alert('❌ Contraseña incorrecta.');

    const todos = await obtenerPedidosSync();
    const cobrados = todos.filter(p => p.estado === 'cobrado');

    if (cobrados.length === 0) return alert('⚠️ No hay cuentas cobradas registradas hoy para realizar el corte.');

    const totEfectivo = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Efectivo')).reduce((sum, p) => sum + p.total, 0);
    const totTransf = cobrados.filter(p => p.metodo_pago && p.metodo_pago.includes('Transferencia')).reduce((sum, p) => sum + p.total, 0);
    const totalGen = totEfectivo + totTransf;

    const comprobantes = cobrados.filter(p => p.comprobante_img).map(p => ({
        id: p.id,
        cliente: p.cliente_mesa,
        total: p.total,
        img: p.comprobante_img
    }));

    const hoyStr = new Date().toLocaleDateString('es-MX', { year: 'numeric', month: '2-digit', day: '2-digit' });

    const nuevoCorte = {
        fecha: hoyStr,
        timestamp: Date.now(),
        efectivo: totEfectivo,
        transferencia: totTransf,
        total: totalGen,
        comprobantes: comprobantes,
        pedidos: cobrados
    };

    let cortes = JSON.parse(localStorage.getItem('mar_y_sazon_cortes') || '[]');
    cortes.unshift(nuevoCorte);
    localStorage.setItem('mar_y_sazon_cortes', JSON.stringify(cortes));

    // Una vez respaldado en Historial de Días, limpiamos imágenes activas en pedidos
    let pedidos = getPedidosLocales();
    pedidos.forEach(p => { p.comprobante_img = null; });
    savePedidosLocales(pedidos);

    if (_supabase) {
        try {
            await _supabase.from('pedidos').update({ comprobante_img: null }).neq('id', 0);
        } catch(e){}
    }

    alert(`✅ Corte del día (${hoyStr}) guardado exitosamente en "Historial de Días". Los comprobantes activos se archivaron correctamente.`);
    cerrarModalGeneric();
    renderCajaPrincipal();
}
'''

if 'function abrirModalCorte()' in code:
    code = re.sub(r'function abrirModalCorte\(\)[\s\S]*?(?=function|\Z)', nueva_funcion_corte + '\n', code)
else:
    code += '\n' + nueva_funcion_corte

with open('js/admin.js', 'w') as f:
    f.write(code)

print("✅ Función de Corte del Día con respaldo automático configurada.")
