function filtrar_comunas () {
    // Obtener cod de la región
    const cod_region = $(this).val() 
    // Iteramos sobre todas las comunas y mostramos solo aquellas cuyo prefijo tenga el cod_region
    $('#comuna_cod option').each(function() {
        const comuna = $(this)
        const cod_comuna = comuna.val()
        if (cod_region == cod_comuna.substring(0,2)) {
            comuna.show()
        } else {
            comuna.hide()
        }
    })
}

// Ejecuta la función filtrar_comuna al detectar cambios
$('#region_cod').on('change', filtrar_comunas)

// Función para mostrar un mensaje antes de eliminar
function eliminar(event) {
    event.preventDefault() // 1. Evitamos que el enlace me dirija a otro lado
    const id = event.target.id // 2. Recuperamos el hred del enlace clickeado
    const url = '/propiedad/delete-propiedad/' + id // 3. Confirmamos si el usuario desea eliminar
    console.log("Eliminando inmueble " + id) 
    const confirmacion = confirm('¿Deseas eliminar la propiedad?')
    if (confirmacion == true) {
        window.location.href = url // 4. Redirijo a la URL Construída
    }
}