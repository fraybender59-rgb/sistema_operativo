const SUPABASE_URL = 'https://atwtmuqkqypdodbhkrbe.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy';

let _supabase = null;
if (window.supabase && window.supabase.createClient) {
    _supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
}

function getPedidosLocales() {
    try { return JSON.parse(localStorage.getItem('mar_y_sazon_pedidos') || '[]'); } catch(e) { return []; }
}

function savePedidosLocales(pedidos) {
    localStorage.setItem('mar_y_sazon_pedidos', JSON.stringify(pedidos));
}

function limpiarComprobantesAntiguos() {
    try {
        let pedidos = getPedidosLocales();
        const hace7Dias = Date.now() - (7 * 24 * 60 * 60 * 1000);
        let modificado = false;
        
        pedidos.forEach(p => {
            const fechaP = new Date(p.creado_en || Date.now()).getTime();
            if (fechaP < hace7Dias && p.comprobante_img) {
                p.comprobante_img = null;
                modificado = true;
            }
        });
        
        if (modificado) savePedidosLocales(pedidos);

        let cortes = JSON.parse(localStorage.getItem('mar_y_sazon_cortes') || '[]');
        let modCortes = false;
        cortes.forEach(c => {
            const fechaC = new Date(c.fecha || Date.now()).getTime();
            if (fechaC < hace7Dias && c.comprobantes && c.comprobantes.length > 0) {
                c.comprobantes = [];
                modCortes = true;
            }
        });
        if (modCortes) localStorage.setItem('mar_y_sazon_cortes', JSON.stringify(cortes));
    } catch(e){}
}

async function guardarPedidoSync(pedido) {
    let pedidos = getPedidosLocales();
    pedidos.unshift(pedido);
    savePedidosLocales(pedidos);

    if (_supabase) {
        try {
            const { data } = await _supabase.from('pedidos').insert([{
                cliente_mesa: pedido.cliente_mesa,
                mesero_nombre: pedido.mesero_nombre,
                total: pedido.total,
                estado: pedido.estado,
                metodo_pago: pedido.metodo_pago,
                origen: pedido.origen,
                creado_en: pedido.creado_en
            }]).select();

            if (data && data.length > 0) {
                const pId = data[0].id;
                pedido.id = pId;
                const detalles = pedido.detalles.map(d => ({
                    pedido_id: pId,
                    producto_nombre: d.nombre,
                    precio: d.precio,
                    cantidad: d.cantidad,
                    comentario: d.comentario
                }));
                await _supabase.from('detalles_pedido').insert(detalles);
                savePedidosLocales(pedidos);
            }
        } catch(e) { console.warn('Respaldo local activo:', e); }
    }
}

async function obtenerPedidosSync() {
    limpiarComprobantesAntiguos();
    let locales = getPedidosLocales();
    if (_supabase) {
        try {
            const { data } = await _supabase.from('pedidos').select('*, detalles_pedido(*)').order('id', { ascending: false });
            if (data && data.length > 0) {
                const remotos = data.map(p => ({
                    id: p.id,
                    cliente_mesa: p.cliente_mesa,
                    mesero_nombre: p.mesero_nombre || 'General',
                    total: parseFloat(p.total),
                    estado: p.estado,
                    metodo_pago: p.metodo_pago,
                    origen: p.origen || 'Clientes',
                    comprobante_img: p.comprobante_img || null,
                    creado_en: p.creado_en,
                    detalles: (p.detalles_pedido || []).map(d => ({
                        nombre: d.producto_nombre,
                        precio: parseFloat(d.precio),
                        cantidad: d.cantidad,
                        comentario: d.comentario
                    }))
                }));
                savePedidosLocales(remotos);
                return remotos;
            }
        } catch(e){}
    }
    return locales;
}

async function actualizarEstadoPedidoSync(id, nuevoEstado, metodoPago = null, comprobanteImg = null) {
    let locales = getPedidosLocales();
    let target = locales.find(p => p.id == id);
    if (target) {
        target.estado = nuevoEstado;
        if (metodoPago) target.metodo_pago = metodoPago;
        if (comprobanteImg) target.comprobante_img = comprobanteImg;
        savePedidosLocales(locales);
    }
    if (_supabase) {
        try {
            let updatePayload = { estado: nuevoEstado };
            if (metodoPago) updatePayload.metodo_pago = metodoPago;
            await _supabase.from('pedidos').update(updatePayload).eq('id', id);
        } catch(e){}
    }
}

async function getConfig(clave, defaultValue = '') {
    if (!_supabase) return localStorage.getItem(clave) || defaultValue;
    try {
        const { data } = await _supabase.from('configuracion').select('valor').eq('clave', clave).single();
        return data ? data.valor : (localStorage.getItem(clave) || defaultValue);
    } catch(e) {
        return localStorage.getItem(clave) || defaultValue;
    }
}

async function setConfig(clave, valor) {
    localStorage.setItem(clave, valor);
    if (_supabase) {
        try { await _supabase.from('configuracion').upsert({ clave, valor }); } catch(e){}
    }
}

async function actualizarPrecioProducto(id, nuevoPrecio) {
    localStorage.setItem(`precio_prod_${id}`, nuevoPrecio);
    if (_supabase) {
        try {
            await _supabase.from('menu').update({ precio: nuevoPrecio }).eq('id', id);
        } catch(e){}
    }
}
