import re

# Update admin.js to include auto-logout logic
with open('js/admin.js', 'r') as f:
    code = f.read()

logout_func = '''
function cerrarAdmin() {
    const inputPass = document.getElementById('admin-pass-input');
    if (inputPass) inputPass.value = '';
    const panel = document.getElementById('admin-panel');
    const modal = document.getElementById('admin-login-modal');
    if (panel) panel.classList.add('hidden');
    if (modal) modal.classList.remove('hidden');
}
'''

if 'function cerrarAdmin()' not in code:
    code += '\n' + logout_func

# Modify ejecutarCorteConRespaldo to call cerrarAdmin at the end
if 'cerrarAdmin();' not in code:
    code = code.replace("renderCajaPrincipal();\n}", "renderCajaPrincipal();\n    cerrarAdmin();\n}")

with open('js/admin.js', 'w') as f:
    f.write(code)

# Update admin.html to add Logout Button
with open('admin.html', 'r') as f:
    html = f.read()

btn_logout = '<button onclick="cerrarAdmin()" class="btn btn-danger" style="grid-column: span 2; padding:10px;">🔒 Cerrar Sesión Admin</button>'

if 'Cerrar Sesión Admin' not in html:
    html = html.replace('<div class="admin-top-grid">', '<div class="admin-top-grid">\n            ' + btn_logout)

with open('admin.html', 'w') as f:
    f.write(html)

print("✅ Bloqueo y Cierre de Sesión Automático Configurado.")
