import os

# 1. Inyectar el receptor del Formateo en todos los dispositivos (supabase_config.js)
supa_path = 'js/supabase_config.js'
try:
    with open(supa_path, 'r', encoding='utf-8') as f:
        supa = f.read()
    
    reset_listener = '''
// --- RECEPTOR DE FORMATEO GLOBAL ---
async function verificarResetGlobal() {
    if (!_supabase) return;
    try {
        const { data } = await _supabase.from('configuracion').select('valor').eq('clave', 'reset_global').single();
        if (data && data.valor) {
            const resetBackend = data.valor;
            const resetLocal = localStorage.getItem('local_reset_version');
            
            if (resetBackend !== resetLocal) {
                console.log("⚠️ SEÑAL DE FORMATEO RECIBIDA. Borrando dispositivo...");
                localStorage.clear(); // Borra todo el caché y memoria del navegador
                localStorage.setItem('local_reset_version', resetBackend); // Guarda el sello de formateo
                window.location.reload(true); // Fuerza la recarga en limpio
            }
        }
    } catch(e) {}
}
// Escucha señales de formateo cada 7 segundos
setInterval(verificarResetGlobal, 7000);
'''
    if 'verificarResetGlobal' not in supa:
        with open(supa_path, 'w', encoding='utf-8') as f:
            f.write(supa + '\n' + reset_listener)
except Exception as e:
    print("Error en supabase:", e)

# 2. Agregar el botón de Formateo en el HTML de Administración
admin_html_path = 'admin.html'
try:
    with open(admin_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    btn_viejo = '<button class="btn btn-success" onclick="cambiarCuentaBancaria()">Cambiar Número de Cuenta Bancaria</button>'
    btn_nuevo = btn_viejo + '<br><br><button class="btn btn-danger" style="border:2px solid white; font-weight:bold; padding:15px; width:100%;" onclick="ejecutarResetGlobal()">💣 FORMATEAR Y BORRAR CACHÉ EN TODOS LOS DISPOSITIVOS</button>'
    
    if 'ejecutarResetGlobal' not in html:
        html = html.replace(btn_viejo, btn_nuevo)
        with open(admin_html_path, 'w', encoding='utf-8') as f:
            f.write(html)
except Exception as e:
    print("Error en admin.html:", e)

# 3. Agregar la función de disparo en la lógica de Administración
admin_js_path = 'js/admin.js'
try:
    with open(admin_js_path, 'r', encoding='utf-8') as f:
        admin_js = f.read()
        
    reset_trigger = '''
async function ejecutarResetGlobal() {
    const pass = prompt('⚠️ PELIGRO: Esto vaciará la memoria caché y cerrará sesión en TODOS los dispositivos de los meseros, clientes y cocina. Quedarán como nuevos.\\n\\nIngresa la contraseña de ADMIN (ROXANA) para confirmar:');
    
    if (pass === currentAdminPass || pass === 'ROXANA') {
        const nuevoReset = Date.now().toString();
        if (_supabase) {
            await _supabase.from('configuracion').upsert({ clave: 'reset_global', valor: nuevoReset });
        }
        alert("💣 SEÑAL ENVIADA.\\n\\nEn menos de 7 segundos, todos los dispositivos conectados borrarán su memoria internamente y se reiniciarán en blanco.");
    } else {
        alert('❌ Contraseña incorrecta. Formateo cancelado.');
    }
}
'''
    if 'ejecutarResetGlobal' not in admin_js:
        with open(admin_js_path, 'w', encoding='utf-8') as f:
            f.write(admin_js + '\n' + reset_trigger)
except Exception as e:
    print("Error en admin.js:", e)

print("✅ Botón de Formateo Remoto Global instalado correctamente.")
