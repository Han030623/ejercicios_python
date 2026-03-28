from nicegui import ui

# --- FUNCIONES DE LÓGICA ---
def calcular_aumento(sueldo: float) -> float:
    """Calcula el nuevo sueldo según las reglas de aumento."""
    if sueldo < 4000:
        return sueldo * 1.15
    elif 4000 <= sueldo <= 7000:
        return sueldo * 1.10
    else:
        return sueldo * 1.08

# --- Lista para almacenar historial ---
historial = []

# --- Referencias a elementos UI (se inicializarán en crear_interfaz) ---
tabla = None

def registrar_trabajador(nombre: str, sueldo: str, salida):
    """Valida datos, calcula aumento y guarda en historial."""
    global tabla
    
    if not nombre:
        salida.set_text("Error: El nombre no puede estar vacío.")
        return

    try:
        sueldo_valor = float(sueldo)
        nuevo_sueldo = calcular_aumento(sueldo_valor)

        historial.append({
            "nombre": nombre,
            "sueldo": f"${sueldo_valor:,.2f}",
            "nuevo": f"${nuevo_sueldo:,.2f}"
        })

        tabla.rows = historial 
        tabla.update()

        salida.set_text(
            f"✅ Trabajador registrado: {nombre}\n"
            f"Sueldo básico: ${sueldo_valor:,.2f}\n"
            f"Nuevo sueldo: ${nuevo_sueldo:,.2f}"
        )
        
    except ValueError:
        salida.set_text("❌ Error: El sueldo debe ser un número válido.")
        salida.classes('text-red-600')

def limpiar_campos(nombre_input, sueldo_input, salida):
    """Borra los datos ingresados en los campos y limpia resultados."""
    nombre_input.value = ""
    sueldo_input.value = ""
    salida.set_text("")
    salida.classes('text-black')

# --- FUNCIÓN QUE CREA LA INTERFAZ ---
def crear_interfaz():
    """todo el UI debe estar DENTRO de esta función"""
    global tabla  # Declarar como global para poder usarla en otras funciones
    
    with ui.column().classes('items-center justify-center h-screen gap-4'):
        ui.label("Sistema de Aumento de Sueldos").classes("text-2xl font-bold mb-2")

        nombre_input = ui.input("Nombre del trabajador").classes("w-80")
        sueldo_input = ui.input("Sueldo básico").classes("w-80")
        
        salida = ui.label("").classes("mt-2 font-medium")

        with ui.row().classes('gap-4'):
            ui.button("Registrar trabajador", 
                      on_click=lambda: registrar_trabajador(nombre_input.value, sueldo_input.value, salida),
                      color='primary').classes('w-40')
            
            ui.button("Limpiar campos", 
                      on_click=lambda: limpiar_campos(nombre_input, sueldo_input, salida),
                      color='negative').classes('w-40')

        # Tabla de historial
        tabla = ui.table(
            columns=[
                {"name": "nombre", "label": "Nombre", "field": "nombre"},
                {"name": "sueldo", "label": "Sueldo Básico", "field": "sueldo"},
                {"name": "nuevo", "label": "Nuevo Sueldo", "field": "nuevo"},
            ],
            rows=historial,
            row_key="nombre"
        ).classes("mt-6 w-3/4 bg-white shadow rounded-lg")

# --- SOLO ESTO AL FINAL ---
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='P1 - Aumento de Sueldos', port=8081)