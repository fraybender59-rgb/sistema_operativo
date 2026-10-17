import os, re

app_js_path = 'js/app.js'

try:
    with open(app_js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    nuevo_codigo = '''
// --- RENDERIZADOR ADAPTATIVO (INDEX OSCURO / STAFF CLARO) ---

// Función para ignorar acentos y mayúsculas al hacer clic
function normalizar(texto) {
    if(!texto) return '';
    return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
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
'''

    # Borrar lógicas previas de filtrado que causaban conflicto e inyectar la nueva
    if 'function renderizarMenu' in content:
        content = re.sub(r'function renderizarMenu[\s\S]*?(?=const|let|var|function|$)', nuevo_codigo, content, count=1)
    else:
        content += '\n' + nuevo_codigo

    # Limpiar document.addEventListener viejos para no duplicar
    content = re.sub(r'document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*renderizarMenu\(\'Todas\'\);\s*\}\);', '', content)

    with open(app_js_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Filtro visual inteligente instalado. Respetando diseños oscuro y claro.")
except Exception as e:
    print("Error:", e)
