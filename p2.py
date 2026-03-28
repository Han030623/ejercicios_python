from nicegui import ui

# Lista para almacenar todos los visitantes
visitantes = []

# Constantes
COSTO_POR_JUEGO = 50

# ← 🆕 AGREGAR: Declarar variable global para total_label
total_label = None

def calcular_descuento(edad: int) -> float:
    """Calcula el porcentaje de descuento según la edad."""
    if edad < 10:
        return 0.25  # 25% descuento
    elif 10 <= edad <= 17:
        return 0.10  # 10% descuento
    else:
        return 0.00  # Sin descuento

def calcular_precio_total(juegos: int, descuento: float) -> float:
    """Calcula el precio total aplicando el descuento."""
    precio_base = juegos * COSTO_POR_JUEGO
    precio_con_descuento = precio_base * (1 - descuento)
    return precio_con_descuento

def validar_datos(nombre: str, edad: str, juegos: str) -> tuple:
    """Valida que los datos ingresados sean correctos."""
    errores = []
    
    # Validar nombre
    if not nombre or nombre.strip() == "":
        errores.append("El nombre no puede estar vacío")
    
    # Validar edad
    try:
        edad_int = int(edad)
        if edad_int < 0 or edad_int > 120:
            errores.append("La edad debe estar entre 0 y 120 años")
    except ValueError:
        errores.append("La edad debe ser un número entero")
        edad_int = None
    
    # Validar cantidad de juegos
    try:
        juegos_int = int(juegos)
        if juegos_int < 0:
            errores.append("La cantidad de juegos no puede ser negativa")
        elif juegos_int == 0:
            errores.append("Debe ingresar al menos 1 juego")
    except ValueError:
        errores.append("La cantidad de juegos debe ser un número entero")
        juegos_int = None
    
    return errores, edad_int, juegos_int

def registrar_visitante(nombre: str, edad: str, juegos: str, salida, tabla):
    """Registra un visitante, calcula costos y actualiza la tabla."""
    
    # Validar datos
    errores, edad_int, juegos_int = validar_datos(nombre, edad, juegos)
    
    if errores:
        mensaje_error = "❌ Errores encontrados:\n" + "\n".join(f"• {e}" for e in errores)
        salida.set_text(mensaje_error)
        salida.classes('text-red-600 font-medium')
        return
    
    # Calcular descuento y precio
    descuento = calcular_descuento(edad_int)
    total_pagar = calcular_precio_total(juegos_int, descuento)
    
    # Determinar categoría
    if edad_int < 10:
        categoria = "Niño (25% desc)"
    elif edad_int <= 17:
        categoria = "Adolescente (10% desc)"
    else:
        categoria = "Adulto"
    
    # Guardar en la lista
    visitantes.append({
        "nombre": nombre.strip(),
        "edad": edad_int,
        "juegos": juegos_int,
        "categoria": categoria,
        "descuento": f"{descuento*100:.0f}%",
        "total": total_pagar
    })
    
    # Actualizar tabla
    tabla.rows = visitantes
    tabla.update()
    
    # Mostrar resultado
    precio_base = juegos_int * COSTO_POR_JUEGO
    ahorro = precio_base - total_pagar
    
    salida.set_text(
        f"✅ Visitante registrado exitosamente\n\n"
        f"📛 Nombre: {nombre.strip()}\n"
        f"🎂 Edad: {edad_int} años\n"
        f"🎮 Juegos: {juegos_int}\n"
        f"💰 Precio base: S/ {precio_base:,.2f}\n"
        f"🏷️ Descuento: {descuento*100:.0f}%\n"
        f"💵 Total a pagar: S/ {total_pagar:,.2f}"
    )
    salida.classes('text-green-700 font-medium')
    
    # Actualizar total recaudado
    actualizar_total_recaudado()

def actualizar_total_recaudado():
    """Calcula y muestra el total recaudado por el parque."""
    global total_label  # ← 🆕 AGREGAR: Declarar como global
    total = sum(v["total"] for v in visitantes)
    total_label.set_text(f"💰 Total Recaudado: S/ {total:,.2f}")

def limpiar_campos(nombre_input, edad_input, juegos_input, salida):
    """Limpia todos los campos de entrada."""
    nombre_input.value = ""
    edad_input.value = ""
    juegos_input.value = ""
    salida.set_text("")
    salida.classes('text-black')

def eliminar_ultimo_registro(tabla):
    """Elimina el último registro de la lista."""
    if visitantes:
        visitantes.pop()
        tabla.rows = visitantes
        tabla.update()
        actualizar_total_recaudado()
        ui.notify("Último registro eliminado", color='warning')
    else:
        ui.notify("No hay registros para eliminar", color='negative')

# ==================== INTERFAZ GRÁFICA ====================

def crear_interfaz():
    """Todo el UI debe estar DENTRO de esta función"""
    global total_label  # Declarar como global

    with ui.column().classes('items-center justify-start min-h-screen p-6 gap-4'):
    
        # Título
        ui.label("🎢 Sistema de Pago - Parque de Diversiones").classes("text-3xl font-bold mb-2 text-blue-600")
    
        # Campos de entrada
        with ui.card().classes('w-full max-w-md p-4'):
            ui.label("📝 Registro de Visitantes").classes("text-xl font-semibold mb-3")
        
            nombre_input = ui.input("Nombre del visitante").classes("w-full")
            edad_input = ui.input("Edad (años)").classes("w-full")
            juegos_input = ui.input("Cantidad de juegos").classes("w-full")
        
            # Mensaje de resultado
            salida = ui.label("").classes("mt-4 p-3 bg-gray-100 rounded w-full")
    
        # Botones de acción
        with ui.row().classes('gap-3'):
            ui.button("🎫 Registrar", 
                    on_click=lambda: registrar_visitante(
                        nombre_input.value, 
                        edad_input.value, 
                        juegos_input.value, 
                        salida, 
                        tabla
                    ),
                    color='primary').classes('w-32')
        
            ui.button("🧹 Limpiar", 
                    on_click=lambda: limpiar_campos(nombre_input, edad_input, juegos_input, salida),
                    color='secondary').classes('w-32')
        
            ui.button("🗑️ Eliminar Último", 
                    on_click=lambda: eliminar_ultimo_registro(tabla),
                    color='warning').classes('w-32')
    
        # Total recaudado
        total_label = ui.label("💰 Total Recaudado: S/ 0.00").classes("text-2xl font-bold text-green-600 mt-4")
    
        # Tabla de visitantes
        with ui.card().classes('w-full max-w-4xl mt-4'):
            ui.label("📋 Historial de Visitantes").classes("text-xl font-semibold mb-3")
        
            tabla = ui.table(
                columns=[
                    {"name": "nombre", "label": "Nombre", "field": "nombre"},
                    {"name": "edad", "label": "Edad", "field": "edad"},
                    {"name": "juegos", "label": "Juegos", "field": "juegos"},
                    {"name": "categoria", "label": "Categoría", "field": "categoria"},
                    {"name": "descuento", "label": "Descuento", "field": "descuento"},
                    {"name": "total", "label": "Total (S/)", "field": "total"},
                ],
                rows=visitantes,
                row_key="nombre"
            ).classes("w-full")

#mandar al menú principal
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)