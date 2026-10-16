const SUPABASE_URL = 'https://qmctkrnwykbmlvypnctr.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_m31I88aPiTIZWWANwueqSw_EMMgp6jM';
const db = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;


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
