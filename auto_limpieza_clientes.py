import os

try:
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    script_vacuna = '''
    <script>
        // Vacuna anti-caché: obliga al celular del cliente a recargar el menú invisiblemente
        const VERSION_ACTUAL = "3.5";
        if (localStorage.getItem("version_menu_cliente") !== VERSION_ACTUAL) {
            localStorage.setItem("version_menu_cliente", VERSION_ACTUAL);
            // Forzar limpieza de caché y recarga de la página original
            window.location.reload(true);
        }
    </script>
    '''

    if "version_menu_cliente" not in html:
        html = html.replace('<head>', '<head>\n' + script_vacuna)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✅ Auto-limpieza inyectada en el menú público (index.html).")
    else:
        print("La vacuna ya estaba inyectada.")
except Exception as e:
    print("Error:", e)
