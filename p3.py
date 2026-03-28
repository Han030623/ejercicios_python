from nicegui import ui

# --- ESTRUCTURA DE DATOS ---
lista_compras = []

# ← 🆕 AGREGAR: Declarar variables globales para los elementos UI
tabla_compras = None
input_nombre = None
input_mes = None
input_importe = None
lbl_resultado = None

# --- FUNCIONES DE LÓGICA ---

def validar_mes(mes_texto):
    meses_validos = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return mes_texto.lower().strip() in meses_validos

def calcular_descuento(mes_texto, importe):
    mes = mes_texto.lower().strip()
    porcentaje = 0.0

    if mes == "octubre":
        porcentaje = 0.15
    elif mes == "diciembre":
        porcentaje = 0.20
    elif mes == "julio":
        porcentaje = 0.10
    else:
        porcentaje = 0.0

    monto_descuento = importe * porcentaje
    total_final = importe - monto_descuento
    
    return monto_descuento, total_final, porcentaje

def obtener_total_vendido():
    total_acumulado = 0.0
    for compra in lista_compras:
        total_acumulado += compra['total']
    return total_acumulado

# --- FUNCIONES DE INTERFAZ ---

def registrar_compra():
    # Declarar como globales
    global input_nombre, input_mes, input_importe, lbl_resultado, tabla_compras
    
    nombre = input_nombre.value.strip()
    mes = input_mes.value.strip()
    importe_str = input_importe.value.strip()

    if not nombre or not mes or not importe_str:
        ui.notify('Todos los campos son obligatorios', type='negative')
        return

    try:
        importe = float(importe_str)
        if importe <= 0:
            raise ValueError
    except ValueError:
        ui.notify('El importe debe ser un número mayor a cero', type='negative')
        return

    if not validar_mes(mes):
        ui.notify(f'Mes "{mes}" no válido', type='warning')
        return

    descuento, total, porc = calcular_descuento(mes, importe)

    # Guardar como números puros (sin formato)
    nueva_compra = {
        "cliente": nombre,
        "mes": mes.capitalize(),
        "importe": importe,
        "descuento": descuento,
        "total": total
    }
    lista_compras.append(nueva_compra)

    # Mostrar resultado
    lbl_resultado.set_text(
        f"Cliente: {nombre} | Descuento: {porc*100:.0f}% | Total: S/ {total:.2f}"
    )
    
    actualizar_tabla()

    input_nombre.value = ""
    input_mes.value = ""
    input_importe.value = ""
    ui.notify('Compra registrada con éxito', type='positive')

def mostrar_total_dia():
    if not lista_compras:
        ui.notify('No hay compras registradas aún', type='info')
        return
    
    total = obtener_total_vendido()
    ui.notify(f'Total vendido en el día: S/ {total:.2f}', type='info', timeout=None)

def actualizar_tabla():
    #Declarar como global
    global tabla_compras
    tabla_compras.rows = lista_compras
    tabla_compras.update()  # ← Refrescar la tabla

# --- INTERFAZ GRÁFICA ---
def crear_interfaz():
    """Todo el UI debe estar DENTRO de esta función"""
    #Declarar como globales
    global tabla_compras, input_nombre, input_mes, input_importe, lbl_resultado

    with ui.column().classes('items-center justify-start min-h-screen p-6 gap-4'):
    
        ui.label("Sistema de Descuentos").classes("text-3xl font-bold mb-2 text-blue-600")
    
        with ui.card().classes('w-full max-w-2xl mx-auto p-6'):
            ui.label('Registro de Compras').classes('text-2xl font-bold mb-4 text-center')
        
            with ui.grid(columns=2).classes('w-full gap-4'):
                input_nombre = ui.input(label='Nombre del Cliente').classes('col-span-1')
                input_mes = ui.input(label='Mes (Ej: Octubre)').classes('col-span-1')
                input_importe = ui.input(label='Importe de Compra').classes('col-span-2')
        
            with ui.row().classes('w-full justify-center gap-4 mt-4'):
                ui.button('Registrar Compra', on_click=registrar_compra, color='green')
                ui.button('Ver Total Vendido', on_click=mostrar_total_dia, color='blue')

            lbl_resultado = ui.label('Esperando registro...').classes('text-lg font-bold mt-4 text-center')
            lbl_resultado.style('color: green')

            ui.separator().classes('my-6')
            ui.label('Historial de Compras del Día').classes('text-xl font-bold mb-2')
        
            # Columnas simples
            columns = [
                {'name': 'cliente', 'label': 'Cliente', 'field': 'cliente', 'align': 'left'},
                {'name': 'mes', 'label': 'Mes', 'field': 'mes', 'align': 'center'},
                {'name': 'importe', 'label': 'Importe', 'field': 'importe', 'align': 'right'},
                {'name': 'descuento', 'label': 'Descuento', 'field': 'descuento', 'align': 'right'},
                {'name': 'total', 'label': 'Total Final', 'field': 'total', 'align': 'right'},
            ]
        
            tabla_compras = ui.table(columns=columns, rows=[], row_key='cliente').classes('w-full')

#mandar al menú principal
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)