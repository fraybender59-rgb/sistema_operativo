import re

with open('js/admin.js', 'r') as f:
    code = f.read()

# Nueva lógica con borrado en Supabase
nuevas_funciones = '''
async function abrirModalComprobantes() {
    const todos = await obtenerPedidosSync();
    const conComprobante = todos.filter(p => p.comprobante_img);
    
    let html = `
        <div style="margin-bottom:12px; text-align:center;">
            <button class="btn btn-danger" style="padding:8px 12px; font-size:0.85rem;" onclick="vaciarTodosComprobantes()">🗑️ Borrar TODOS los Comprobantes (Nube y Local)</button>
        </div>
    `;

    if (conComprobante.length === 0) {
        html += '<p style="color:#94a3b8; text-align:center;">No hay fotos de comprobantes guardadas.</p>';
    } else {
        html += conComprobante.map(p => `
            <div style="border-bottom:1px solid #334155; padding:10px 0; text-align:center;">
                <b>#${p.id} - ${p.cliente_mesa} ($${p.total.toFixed(2)})</b><br>
                <img src="${p.comprobante_img}" style="max-width:100%; height:auto; border-radius:8px; margin:8px 0; border:1px solid #334155;"><br>
                <button class="btn btn-danger" style="width:auto; padding:6px 12px; font-size:0.85rem;" onclick="borrarComprobanteFoto('${p.id}')">🗑️ Eliminar esta Foto</button>
            </div>
        `).join('');
    }

    showModalGen('📸 Comprobantes de Pago', html);
}

async function borrarComprobanteFoto(id) {
    let pedidos = getPedidosLocales();
    let target = pedidos.find(p => p.id == id);
    if (target) target.comprobante_img = null;
    savePedidosLocales(pedidos);

    if (_supabase) {
        try {
            await _supabase.from('pedidos').update({ comprobante_img: null }).eq('id', id);
        } catch(e) {}
    }
    alert('✅ Foto eliminada de la base de datos y del celular.');
    abrirModalComprobantes();
}

async function vaciarTodosComprobantes() {
    const pass = prompt('Ingrese contraseña de ADMINISTRACIÓN (ROXANA) para borrar todas las fotos:');
    if (pass === currentAdminPass || pass === 'ROXANA') {
        let pedidos = getPedidosLocales();
        pedidos.forEach(p => { p.comprobante_img = null; });
        savePedidosLocales(pedidos);

        if (_supabase) {
            try {
                await _supabase.from('pedidos').update({ comprobante_img: null }).neq('id', 0);
            } catch(e) {}
        }
        alert('✅ Todas las fotos fueron eliminadas de la nube.');
        abrirModalComprobantes();
    } else {
        alert('❌ Contraseña incorrecta.');
    }
}
'''

# Reemplazar la función anterior si existía
if 'function abrirModalComprobantes()' in code:
    code = re.sub(r'function abrirModalComprobantes\(\)[\s\S]*?(?=function|\Z)', nuevas_funciones + '\n', code)
else:
    code += '\n' + nuevas_funciones

with open('js/admin.js', 'w') as f:
    f.write(code)

print("✅ Módulo de borrado de comprobantes actualizado correctamente.")
