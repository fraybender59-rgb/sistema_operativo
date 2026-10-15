document.addEventListener('DOMContentLoaded', () => {
    cargarCocina();
    setInterval(cargarCocina, 5000);
});

async function cargarCocina() {
    const container = document.getElementById('cocina-orders');
    if (_supabase) {
        try {
            const { data: pedidos } = await _supabase.from('pedidos').select('*, detalles_pedido(*)').in('estado', ['pendiente', 'en_cocina']).order('id', { ascending: true });

            if (pedidos && pedidos.length > 0) {
                container.innerHTML = pedidos.map(p => `
                    <div class="admin-card" style="border-left: 5px solid var(--accent);">
                        <h3>Mesa/Cliente: ${p.cliente_mesa} (#${p.id})</h3>
                        <ul style="list-style:none; padding:0;">
                            ${(p.detalles_pedido || []).map(d => `
                                <li style="font-size:1.1rem; padding:4px 0;">
                                    <b>${d.cantidad}x ${d.producto_nombre}</b>${d.comentario ? `<br><small style="color:#f59e0b;">⚠️ Nota: ${d.comentario}</small>` : ''}
                                </li>
                            `).join('')}
                        </ul>
                        <button class="btn btn-success" onclick="marcarListo(${p.id})">Marcar como LISTO / ENTREGADO</button>
                    </div>
                `).join('');
                return;
            }
        } catch(e){}
    }
    container.innerHTML = '<p style="text-align:center; color:#94a3b8;">No hay comandas pendientes en cocina.</p>';
}

async function marcarListo(id) {
    if (_supabase) await _supabase.from('pedidos').update({ estado: 'listo' }).eq('id', id);
    cargarCocina();
}