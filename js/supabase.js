import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'

const supabaseUrl = 'https://atwtmuqkqypdodbhkrbe.supabase.co'
const supabaseKey = 'Sb_publishable_MEy55fYU0IPdivDrbnWgsA_75__Y_Uoy'
export const supabase = createClient(supabaseUrl, supabaseKey)

// Función para cambiar la imagen de fondo desde la base de datos
export async function cargarFondo() {
    const { data } = await supabase.from('configuracion').select('valor').eq('clave', 'fondo_app').single();
    if (data && data.valor) {
        document.body.style.backgroundImage = `url(${data.valor})`;
        document.body.style.backgroundSize = 'cover';
        document.body.style.backgroundPosition = 'center';
        document.body.style.backgroundAttachment = 'fixed';
    }
}
