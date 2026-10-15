cat << 'EOF' > js/supabase.js
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'

const supabaseUrl = 'https://atwtmuqkqypdodbhkrbe.supabase.co';
const supabaseKey = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy';

export const supabase = createClient(supabaseUrl, supabaseKey);

export async function getConfig(clave, defaultValue = null) {
    try {
        const { data, error } = await supabase.from('configuracion').select('valor').eq('clave', clave).maybeSingle();
        if (error || !data) return defaultValue;
        return data.valor || defaultValue;
    } catch (e) {
        return defaultValue;
    }
}

export async function setConfig(clave, valor) {
    try {
        await supabase.from('configuracion').upsert({ clave, valor });
    } catch (e) {
        console.warn('Error guardando config:', e);
    }
}
EOF
