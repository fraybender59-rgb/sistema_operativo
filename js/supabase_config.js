const SUPABASE_URL = 'https://atwtmuqkqypdodbhkrbe.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy';

let _supabase = null;
if (window.supabase && window.supabase.createClient) {
    _supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
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