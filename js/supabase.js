cat << 'EOF' > js/supabase.js
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'

const supabaseUrl = 'https://atwtmuqkqypdodbhkrbe.supabase.co'
const supabaseKey = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy'
export const supabase = createClient(supabaseUrl, supabaseKey)

export async function getConfig(clave) {
    const { data } = await supabase.from('configuracion').select('valor').eq('clave', clave).single();
    return data ? data.valor : null;
}

export async function setConfig(clave, valor) {
    await supabase.from('configuracion').upsert({ clave, valor });
}
EOF
