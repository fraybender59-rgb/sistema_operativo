import os, re, glob

ROOT = os.getcwd()
SYNC_FILE = os.path.join(ROOT, 'js', 'realtime_sync.js')
os.makedirs(os.path.join(ROOT, 'js'), exist_ok=True)

# ============================================================
# 1. MOTOR DE SINCRONIZACIÓN EN TIEMPO REAL
# ============================================================
realtime_js = r'''
/* ============================================================
   MOTOR DE SINCRONIZACIÓN EN TIEMPO REAL - PWA SISTEMA
   - Toda lectura va PRIMERO a la nube (Supabase = fuente de verdad)
   - Los cambios se propagan por Realtime a TODOS los dispositivos
   - Al cerrar/ocultar la pestaña se hace flush automático
   - localStorage queda solo como caché pasivo (NO bloquea)
   ============================================================ */
(function () {
    'use strict';

    const TABLE = 'configuracion';
    const memCache = new Map();
    const broadcast = ('BroadcastChannel' in window)
        ? new BroadcastChannel('pwa-sistema-sync')
        : null;

    const lsGet = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
    const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };

    // ---------- GET: SIEMPRE DESDE LA NUBE ----------
    async function getConfigRealtime(clave, valorPorDefecto) {
        if (window._supabase) {
            try {
                const { data, error } = await window._supabase
                    .from(TABLE).select('valor').eq('clave', clave).maybeSingle();
                if (!error && data && data.valor !== undefined && data.valor !== null) {
                    memCache.set(clave, data.valor);
                    lsSet(clave, data.valor);
                    return data.valor;
                }
            } catch (e) {}
        }
        if (memCache.has(clave)) return memCache.get(clave);
        return lsGet(clave) || valorPorDefecto;   // último recurso
    }

    // ---------- SET: ESCRIBE EN LA NUBE INMEDIATAMENTE ----------
    async function setConfigRealtime(clave, valor) {
        memCache.set(clave, valor);
        lsSet(clave, valor);
        if (window._supabase) {
            try {
                await window._supabase.from(TABLE).upsert({
                    clave, valor, updated_at: new Date().toISOString()
                });
            } catch (e) { console.warn('[Sync] upsert:', e); }
        }
        if (broadcast) broadcast.postMessage({ type: 'config-update', clave, valor });
    }

    // ---------- REALTIME: ESCUCHA CAMBIOS DE OTROS DISPOSITIVOS ----------
    function initRealtime() {
        if (!window._supabase || window._supabase.__rtHooked) return;
        window._supabase.__rtHooked = true;
        try {
            window._supabase
                .channel('config-changes')
                .on('postgres_changes',
                    { event: '*', schema: 'public', table: TABLE },
                    payload => {
                        const row = payload.new || payload.old;
                        if (!row || !row.clave) return;
                        memCache.set(row.clave, row.valor);
                        lsSet(row.clave, row.valor);
                        window.dispatchEvent(new CustomEvent('config-updated', {
                            detail: { clave: row.clave, valor: row.valor, origen: 'realtime' }
                        }));
                        if (broadcast) broadcast.postMessage({
                            type: 'config-update', clave: row.clave, valor: row.valor
                        });
                    })
                .subscribe(status => console.log('[Sync] Realtime:', status));
        } catch (e) { console.warn('[Sync] Realtime no disponible:', e); }
    }

    // ---------- BROADCAST: MISMO NAVEGADOR, DISTINTAS PESTAÑAS ----------
    if (broadcast) {
        broadcast.onmessage = ev => {
            if (ev.data && ev.data.type === 'config-update') {
                memCache.set(ev.data.clave, ev.data.valor);
                lsSet(ev.data.clave, ev.data.valor);
                window.dispatchEvent(new CustomEvent('config-updated', {
                    detail: { clave: ev.data.clave, valor: ev.data.valor, origen: 'broadcast' }
                }));
            }
        };
    }

    // ---------- FLUSH: REENVIAR MEMORIA A LA NUBE ----------
    async function flushPendingToCloud() {
        if (!window._supabase) return;
        for (const [clave, valor] of memCache.entries()) {
            try {
                // keepalive permite que el fetch sobreviva al cierre de pestaña
                await fetch(
                    window._supabase.supabaseUrl + '/rest/v1/' + TABLE,
                    {
                        method: 'POST',
                        keepalive: true,
                        headers: {
                            'apikey': window._supabase.supabaseKey,
                            'Authorization': 'Bearer ' + window._supabase.supabaseKey,
                            'Content-Type': 'application/json',
                            'Prefer': 'resolution=merge-duplicates'
                        },
                        body: JSON.stringify({ clave, valor, updated_at: new Date().toISOString() })
                    }
                );
            } catch (e) {}
        }
    }

    // ---------- EVENTOS DE CICLO DE VIDA ----------
    window.addEventListener('pagehide',   () => { flushPendingToCloud(); });
    window.addEventListener('beforeunload', () => { flushPendingToCloud(); });

    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
            flushPendingToCloud();       // al salir/minimizar: empuja
        } else {
            // al volver: pide refresco desde la nube
            window.dispatchEvent(new CustomEvent('config-refresh-request'));
        }
    });

    window.addEventListener('focus', () => {
        window.dispatchEvent(new CustomEvent('config-refresh-request'));
    });

    // ---------- API GLOBAL ----------
    window.getConfigRealtime = getConfigRealtime;
    window.setConfigRealtime = setConfigRealtime;
    window.getConfig = getConfigRealtime;
    window.setConfig = setConfigRealtime;
    window.__syncFlush = flushPendingToCloud;

    // Iniciar Realtime en cuanto _supabase exista
    const t = setInterval(() => {
        if (window._supabase) {
            clearInterval(t);
            initRealtime();
            window.dispatchEvent(new CustomEvent('config-refresh-request'));
        }
    }, 200);
    setTimeout(() => clearInterval(t), 15000);

    console.log('✅ Motor de sincronización en tiempo real activo');
})();
'''

with open(SYNC_FILE, 'w', encoding='utf-8') as f:
    f.write(realtime_js)
print('✅ Creado:', SYNC_FILE)

# ============================================================
# 2. INYECTAR EL MOTOR EN TODOS LOS HTML
# ============================================================
TAG = '<script src="js/realtime_sync.js" defer></script>'
INYECTADOS = 0

for html in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    if 'node_modules' in html or '.vercel' in html:
        continue
    try:
        with open(html, 'r', encoding='utf-8') as f:
            c = f.read()
        if 'realtime_sync.js' in c:
            continue
        # Inyectar antes de </body> (o al final si no hay)
        if '</body>' in c:
            c = c.replace('</body>', f'  {TAG}\n</body>', 1)
        else:
            c += '\n' + TAG
        with open(html, 'w', encoding='utf-8') as f:
            f.write(c)
        INYECTADOS += 1
        print('  ↳ Inyectado en:', os.path.relpath(html, ROOT))
    except Exception as e:
        print('  ⚠️  Error en', html, ':', e)

print(f'✅ Motor inyectado en {INYECTADOS} archivos HTML')

# ============================================================
# 3. ASEGURAR QUE supabase_config.js DEFINE _supabase GLOBAL
# ============================================================
supa = os.path.join(ROOT, 'js', 'supabase_config.js')
if os.path.exists(supa):
    with open(supa, 'r', encoding='utf-8') as f:
        s = f.read()
    # Eliminar el puente viejo si existe (el nuevo motor lo reemplaza)
    s = re.sub(r'// --- PUENTE MAESTRO BACKEND.*?(?=\Z|// ---)', '', s, flags=re.DOTALL)
    with open(supa, 'w', encoding='utf-8') as f:
        f.write(s)
    print('✅ supabase_config.js limpiado (puente viejo eliminado)')

# ============================================================
# 4. SERVICE WORKER: NO CACHEAR CONFIGURACIÓN
# ============================================================
for sw_path in [os.path.join(ROOT, 'sw.js'),
                os.path.join(ROOT, 'service-worker.js')]:
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw = f.read()
        if 'NETWORK_ONLY_CONFIG' not in sw:
            patch = '''
// NETWORK_ONLY_CONFIG: la configuración siempre va a la red
self.addEventListener('fetch', event => {
    const url = event.request.url;
    if (url.includes('/rest/v1/configuracion') ||
        url.includes('realtime_sync.js') ||
        url.includes('supabase_config.js')) {
        event.respondWith(fetch(event.request, { cache: 'no-store' }));
    }
});
'''
            with open(sw_path, 'w', encoding='utf-8') as f:
                f.write(sw + '\n' + patch)
            print('✅ Service Worker actualizado:', os.path.basename(sw_path))

print('\n🎉 LISTO. Ahora ejecuta git + vercel.')
