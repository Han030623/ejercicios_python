from nicegui import ui

# --- VARIABLES GLOBALES DE ESTADO ---
lista_intentos = []  # Lista para almacenar todos los números ingresados
intentos_fallidos = 0
numero_valido = None
proceso_finalizado = False
entrada_numero=None
lbl_resultado=None
lbl_intentos=None
lbl_rango=None
btn_validar=None
lbl_historial=None

# --- FUNCIONES DE LÓGICA Y PROCESO ---

def validar_numero_en_rango(numero, minimo=0, maximo=20):
    """
    Función reutilizable para validar si un número está dentro de un rango.
    Retorna True si está en rango, False si está fuera.
    """
    return minimo <= numero <= maximo

def procesar_validacion():
    """
    Función principal que contiene la lógica de validación,
    estructuras de control y actualización de la interfaz.
    """
    global lista_intentos, intentos_fallidos, numero_valido, proceso_finalizado
    global entrada_numero, lbl_resultado, lbl_intentos, lbl_rango, btn_validar, lbl_historial    
    # Evitar procesamiento si ya terminó
    if proceso_finalizado:
        return
    
    valor_input = entrada_numero.value
    
    # 1. Validación de datos (Evitar errores de entrada no numérica)
    if not valor_input:
        ui.notify('⚠️ Por favor, escribe un número.', type='warning')
        return

    try:
        numero = int(valor_input)
    except ValueError:
        ui.notify('❌ Error: Debes ingresar un número entero válido.', type='negative')
        return

    # 2. Almacenar el intento en la lista (Requisito de listas/arreglos)
    lista_intentos.append(numero)
    
    # 3. Estructura de control condicional usando función reutilizable
    if validar_numero_en_rango(numero, 0, 20):
        # CASO ÉXITO - Número dentro del rango
        numero_valido = numero
        proceso_finalizado = True
        
        # Actualizar interfaz con resultados
        lbl_resultado.set_text(f'✅ Número válido ingresado: {numero}')
        lbl_resultado.style('color: green; font-weight: bold; font-size: 1.2em')
        
        lbl_intentos.set_text(f'Cantidad total de intentos: {len(lista_intentos)}')
        lbl_rango.set_text(f'Rango válido: [0 - 20]')
        
        # Mostrar historial de intentos
        mostrar_historial()
        
        # Bloquear la entrada
        entrada_numero.disable()
        btn_validar.disable()
        btn_validar.label = '✓ Validación Completada'
        
        ui.notify(f'¡Éxito! El número {numero} está dentro del rango [0, 20].', type='positive')
        
    else:
        # CASO ERROR - Número fuera del rango
        intentos_fallidos += 1
        
        # Estructura condicional para mensaje de error específico
        if numero < 0:
            mensaje_error = f'El número {numero} es MENOR que 0.'
        else:
            mensaje_error = f'El número {numero} es MAYOR que 20.'
        
        ui.notify(f'❌ Error: {mensaje_error} Intente de nuevo.', type='negative')
        
        # Limpiar el campo para solicitar nuevamente el número
        entrada_numero.value = ''
        entrada_numero.focus()
        
        # Actualizar contador de intentos
        lbl_intentos.set_text(f'Intentos fallidos: {intentos_fallidos} | Total intentos: {len(lista_intentos)}')
        lbl_rango.set_text(f'Rango válido: [0 - 20] - ¡Sigue intentando!')

def mostrar_historial():
    """
    Función para mostrar la lista de todos los números intentados.
    """
    if len(lista_intentos) > 0:
        historial_texto = ', '.join(str(n) for n in lista_intentos)
        lbl_historial.set_text(f'Historial de intentos: [{historial_texto}]')
    else:
        lbl_historial.set_text('Historial de intentos: []')

def reiniciar_programa():
    """Función para limpiar el estado y volver a empezar"""
    global lista_intentos, intentos_fallidos, numero_valido, proceso_finalizado
    global entrada_numero, lbl_resultado, lbl_intentos, lbl_rango, btn_validar, lbl_historial
    lista_intentos = []
    intentos_fallidos = 0
    numero_valido = None
    proceso_finalizado = False
    
    entrada_numero.value = ''
    entrada_numero.enable()
    btn_validar.enable()
    btn_validar.label = 'Validar Número'
    
    lbl_resultado.set_text('Resultado: Esperando ingreso...')
    lbl_resultado.style('color: black; font-weight: normal; font-size: 1em')
    lbl_intentos.set_text('Cantidad de intentos: 0')
    lbl_rango.set_text('Rango válido: [0 - 20]')
    lbl_historial.set_text('Historial de intentos: []')
    
    ui.notify('Programa reiniciado. Puede ingresar un nuevo número.', type='info')

def mostrar_info_rango():
    """Función informativa sobre el rango válido"""
    ui.notify('📋 El número debe estar entre 0 y 20 (inclusive).', type='info')

# --- INTERFAZ GRÁFICA (UI) ---

def crear_interfaz():
    """Todo el UI debe estar DENTRO de esta función"""
    global entrada_numero, lbl_resultado, lbl_intentos, lbl_rango, btn_validar, lbl_historial
    
    with ui.card().classes('w-full max-w-lg mx-auto p-6 shadow-lg'):
        ui.label('Validación de Número en Rango [0, 20]').classes('text-2xl font-bold mb-4 text-center text-primary')
    
        ui.label('Ingrese un número entero dentro del rango:').classes('mb-2 font-medium')
    
        # Input numérico
        entrada_numero = ui.input(
            label='Número', 
            placeholder='Ej: 15',
        ).classes('w-full')
    
        # Botones de acción
        with ui.row().classes('w-full justify-center gap-2 mt-4'):
            btn_validar = ui.button('🔍 Validar Número', on_click=procesar_validacion).classes('flex-1')
            btn_info = ui.button('ℹ️ Info', on_click=mostrar_info_rango, color='info').classes('w-20')
    
        # Área de resultados (Etiquetas)
        ui.separator().classes('my-4')
    
        with ui.column().classes('w-full gap-2'):
            lbl_resultado = ui.label('Resultado: Esperando ingreso...').classes('text-lg font-bold')
            lbl_intentos = ui.label('Cantidad de intentos: 0').classes('text-gray-600')
            lbl_rango = ui.label('Rango válido: [0 - 20]').classes('text-gray-500 text-sm')
            lbl_historial = ui.label('Historial de intentos: []').classes('text-gray-500 text-sm italic')
    
        # Botón para reiniciar
        ui.button('🔄 Reiniciar', on_click=reiniciar_programa, color='grey').classes('mt-4 w-full')

#mandar al menú principal
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)