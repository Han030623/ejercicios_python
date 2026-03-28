from nicegui import ui

# --- VARIABLES GLOBALES ---
lista_trabajadores = []      # Almacena todos los trabajadores registrados
trabajador_actual = {}       # Datos del trabajador en proceso
proceso_finalizado = False

input_nombre=None
input_horas_normales=None
input_pago_hora=None
input_horas_extras=None
input_num_hijos=None
lbl_nombre=None
lbl_pago_normal=None
lbl_pago_extras=None
lbl_bonificacion=None
lbl_pago_total=None
lbl_reporte=None
lbl_total_general=None

# --- FUNCIONES DE VALIDACIÓN ---

def validar_texto(valor):
    """Valida que el valor sea texto no vacío"""
    return valor and valor.strip() != ''

def validar_numero_positivo(valor):
    """Valida que el valor sea un número positivo"""
    try:
        num = float(valor)
        return num >= 0
    except ValueError:
        return False

def validar_numero_entero_no_negativo(valor):
    """Valida que el valor sea un número entero no negativo"""
    try:
        num = int(valor)
        return num >= 0
    except ValueError:
        return False

# --- FUNCIONES DE CÁLCULO ---

def calcular_pago_horas_normales(horas, pago_hora):
    """Calcula el pago por horas normales"""
    return horas * pago_hora

def calcular_pago_horas_extras(horas, pago_hora):
    """Calcula el pago por horas extras (50% más que hora normal)"""
    return horas * (pago_hora * 1.5)

def calcular_bonificacion_hijos(num_hijos, pago_hora):
    """Calcula la bonificación por hijos (0.5 por cada hijo)"""
    return num_hijos * (pago_hora * 0.5)

def calcular_pago_total(pago_normal, pago_extras, bonificacion):
    """Calcula el pago total"""
    return pago_normal + pago_extras + bonificacion

# --- FUNCIONES DE PROCESO ---

def procesar_trabajador():
    """Procesa el cálculo de pago para un trabajador"""
    global lista_trabajadores, trabajador_actual, proceso_finalizado
    global input_nombre, input_horas_normales, input_pago_hora, input_num_hijos, input_horas_extras, lbl_bonificacion, lbl_nombre, lbl_pago_extras, lbl_pago_normal, lbl_pago_total, lbl_reporte, lbl_total_general

    # Obtener valores de los inputs
    nombre = input_nombre.value
    horas_normales = input_horas_normales.value
    pago_hora = input_pago_hora.value
    horas_extras = input_horas_extras.value
    num_hijos = input_num_hijos.value
    
    # Validaciones
    if not validar_texto(nombre):
        ui.notify('⚠️ Por favor, ingrese el nombre del trabajador.', type='warning')
        return
    
    if not validar_numero_positivo(horas_normales):
        ui.notify('⚠️ Las horas normales deben ser un número positivo.', type='warning')
        return
    
    if not validar_numero_positivo(pago_hora):
        ui.notify('⚠️ El pago por hora debe ser un número positivo.', type='warning')
        return
    
    if not validar_numero_entero_no_negativo(horas_extras):
        ui.notify('⚠️ Las horas extras deben ser un número entero no negativo.', type='warning')
        return
    
    if not validar_numero_entero_no_negativo(num_hijos):
        ui.notify('⚠️ El número de hijos debe ser un entero no negativo.', type='warning')
        return
    
    # Convertir valores
    horas_normales = float(horas_normales)
    pago_hora = float(pago_hora)
    horas_extras = int(horas_extras)
    num_hijos = int(num_hijos)
    
    # Calcular pagos
    pago_normal = calcular_pago_horas_normales(horas_normales, pago_hora)
    pago_extras = calcular_pago_horas_extras(horas_extras, pago_hora)
    bonificacion = calcular_bonificacion_hijos(num_hijos, pago_hora)
    pago_total = calcular_pago_total(pago_normal, pago_extras, bonificacion)
    
    # Guardar datos del trabajador
    trabajador_actual = {
        'nombre': nombre,
        'horas_normales': horas_normales,
        'pago_hora': pago_hora,
        'horas_extras': horas_extras,
        'num_hijos': num_hijos,
        'pago_normal': pago_normal,
        'pago_extras': pago_extras,
        'bonificacion': bonificacion,
        'pago_total': pago_total
    }
    
    # Agregar a la lista
    lista_trabajadores.append(trabajador_actual)
    
    # Mostrar resultados
    mostrar_resultados_trabajador(trabajador_actual)
    
    # Actualizar reporte
    actualizar_reporte()
    
    ui.notify(f'✅ Trabajador {nombre} registrado. Pago total: ${pago_total:.2f}', type='positive')

def mostrar_resultados_trabajador(trabajador):
    """Muestra los resultados del cálculo para un trabajador"""
    lbl_nombre.set_text(f'👤 Nombre: {trabajador["nombre"]}')
    lbl_pago_normal.set_text(f'💵 Pago horas normales: ${trabajador["pago_normal"]:.2f}')
    lbl_pago_extras.set_text(f'🌙 Pago horas extras: ${trabajador["pago_extras"]:.2f}')
    lbl_bonificacion.set_text(f'👶 Bonificación hijos: ${trabajador["bonificacion"]:.2f}')
    lbl_pago_total.set_text(f'💰 Pago total: ${trabajador["pago_total"]:.2f}')
    lbl_pago_total.style('color: green; font-weight: bold; font-size: 1.3em')

def actualizar_reporte():
    """Actualiza el reporte de todos los trabajadores"""
    if len(lista_trabajadores) == 0:
        lbl_reporte.set_text('📋 No hay trabajadores registrados')
        lbl_total_general.set_text('💰 Total general: $0.00')
        return
    
    # Crear tabla de reporte
    reporte = '📋 REPORTE DE PAGOS\n\n'
    reporte += f'{"Nombre":<20} {"Normal":<10} {"Extras":<10} {"Bonif.":<10} {"Total":<10}\n'
    reporte += '─' * 60 + '\n'
    
    suma_total = 0
    for i, trab in enumerate(lista_trabajadores, 1):
        reporte += f'{trab["nombre"]:<20} ${trab["pago_normal"]:<9.2f} ${trab["pago_extras"]:<9.2f} ${trab["bonificacion"]:<9.2f} ${trab["pago_total"]:<9.2f}\n'
        suma_total += trab['pago_total']
    
    reporte += '─' * 60 + '\n'
    lbl_reporte.set_text(reporte)
    lbl_total_general.set_text(f'💰 Total general: ${suma_total:.2f}')
    lbl_total_general.style('color: green; font-weight: bold; font-size: 1.2em')

def limpiar_formulario():
    """Limpia el formulario para ingresar un nuevo trabajador"""
    input_nombre.value = ''
    input_horas_normales.value = ''
    input_pago_hora.value = ''
    input_horas_extras.value = ''
    input_num_hijos.value = ''
    
    lbl_nombre.set_text('👤 Nombre: -')
    lbl_pago_normal.set_text('💵 Pago horas normales: -')
    lbl_pago_extras.set_text('🌙 Pago horas extras: -')
    lbl_bonificacion.set_text('👶 Bonificación hijos: -')
    lbl_pago_total.set_text('💰 Pago total: -')
    lbl_pago_total.style('color: black; font-weight: normal; font-size: 1em')
    
    input_nombre.focus()
    
    ui.notify('📝 Formulario limpio. Puede ingresar nuevo trabajador.', type='info')

def reiniciar_sistema():
    """Reinicia todo el sistema"""
    global lista_trabajadores, trabajador_actual
    global input_nombre, input_horas_normales, input_pago_hora, input_num_hijos, input_horas_extras, lbl_bonificacion, lbl_nombre, lbl_pago_extras, lbl_pago_normal, lbl_pago_total, lbl_reporte, lbl_total_general
    
    lista_trabajadores = []
    trabajador_actual = {}
    
    limpiar_formulario()
    
    lbl_reporte.set_text('📋 No hay trabajadores registrados')
    lbl_total_general.set_text('💰 Total general: $0.00')
    
    ui.notify('🔄 Sistema reiniciado', type='info')

def exportar_reporte():
    """Muestra mensaje de exportación (simulado)"""
    if len(lista_trabajadores) == 0:
        ui.notify('⚠️ No hay datos para exportar', type='warning')
        return
    
    ui.notify(f'📄 Reporte de {len(lista_trabajadores)} trabajadores listo para exportar', type='positive')

# --- INTERFAZ GRÁFICA ---

def crear_interfaz():

    global input_nombre, input_horas_normales, input_pago_hora, input_num_hijos, input_horas_extras, lbl_bonificacion, lbl_nombre, lbl_pago_extras, lbl_pago_normal, lbl_pago_total, lbl_reporte, lbl_total_general

    with ui.card().classes('w-full max-w-4xl mx-auto p-6 shadow-xl'):
        ui.label('💼 Sistema de Pago de Trabajadores').classes('text-3xl font-bold mb-2 text-center text-primary')
        ui.label('Calcule el pago incluyendo horas extras y bonificación por hijos').classes('text-gray-600 mb-6 text-center')
    
        # Sección de datos del trabajador
        with ui.row().classes('w-full gap-4'):
            with ui.column().classes('flex-1'):
                ui.label('📝 Datos del Trabajador').classes('text-xl font-bold mb-2')
            
                input_nombre = ui.input(label='👤 Nombre del trabajador', placeholder='Ej: Juan Pérez').classes('w-full')
                input_horas_normales = ui.input(label='⏰ Horas normales trabajadas', placeholder='Ej: 40').classes('w-full')
                input_pago_hora = ui.input(label='💲 Pago por hora normal', placeholder='Ej: 10.50').classes('w-full')
                input_horas_extras = ui.input(label='🌙 Horas extras trabajadas', placeholder='Ej: 5').classes('w-full')
                input_num_hijos = ui.input(label='👶 Número de hijos', placeholder='Ej: 2').classes('w-full')
        
            with ui.column().classes('flex-1'):
                ui.label('📊 Resultados del Cálculo').classes('text-xl font-bold mb-2')
            
                with ui.card().classes('w-full p-4 bg-blue-50'):
                    lbl_nombre = ui.label('👤 Nombre: -').classes('text-md font-semibold')
                    lbl_pago_normal = ui.label('💵 Pago horas normales: -').classes('text-md')
                    lbl_pago_extras = ui.label('🌙 Pago horas extras: -').classes('text-md')
                    lbl_bonificacion = ui.label('👶 Bonificación hijos: -').classes('text-md')
                    lbl_pago_total = ui.label('💰 Pago total: -').classes('text-xl font-bold my-2')
    
        # Botones de acción
        with ui.row().classes('w-full gap-2 mt-4 justify-center'):
            btn_calcular = ui.button('🧮 Calcular Pago', on_click=procesar_trabajador).classes('flex-1')
            btn_limpiar = ui.button('🧹 Limpiar', on_click=limpiar_formulario, color='orange').classes('w-32')
            btn_reiniciar = ui.button('🔄 Reiniciar', on_click=reiniciar_sistema, color='grey').classes('w-32')
    
        ui.separator().classes('my-6')
    
        # Sección de reporte
        ui.label('📋 Reporte de Pagos Realizados').classes('text-xl font-bold text-center mb-4')
    
        with ui.card().classes('w-full p-4 bg-gray-50'):
            lbl_reporte = ui.label('📋 No hay trabajadores registrados').classes('text-md font-mono whitespace-pre')
    
        with ui.card().classes('w-full p-4 bg-green-50 mt-2'):
            lbl_total_general = ui.label('💰 Total general: $0.00').classes('text-xl font-bold')
    
        # Información de reglas
        with ui.card().classes('w-full p-4 bg-yellow-50 mt-4'):
            ui.label('💡 Reglas de Cálculo:').classes('font-bold mb-2')
            ui.label('• Hora extra = 50% más que hora normal').classes('text-sm')
            ui.label('• Bonificación por hijo = 0.5 del pago por hora').classes('text-sm')

#se ejecuta en el menu
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)