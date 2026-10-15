const SUPABASE_URL = 'https://qmctkrnwykbmlvypnctr.supabase.co';
const SUPABASE_KEY = 'Sb_publishable_m31I88aPiTIZWWANwueqSw_EMMgp6jM';
const db = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;
