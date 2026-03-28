from nicegui import ui

# --- VARIABLES GLOBALES DE ESTADO ---
lista_intentos = []          # Guarda TODOS los números ingresados
lista_intentos_incorrectos = []  # Guarda solo los incorrectos
numero_correcto = None
proceso_finalizado = False
entrada_numero=None
lbl_resultado=None
lbl_intentos_totales=None
lbl_intentos_incorrectos=None
lbl_numero_correcto=None
lbl_estadisticas=None
btn_validar=None
lbl_historial=None

# --- FUNCIONES DE LÓGICA Y PROCESO ---

def validar_numero_en_rango(numero, minimo=0, maximo=20):
    """
    Función reutilizable para validar si un número está dentro del rango.
    """
    return minimo <= numero <= maximo

def procesar_validacion():
    """
    Función principal que procesa la validación y registra todos los intentos.
    """
    global lista_intentos, lista_intentos_incorrectos, numero_correcto, proceso_finalizado
    global entrada_numero, lbl_resultado, lbl_intentos_totales, lbl_intentos_incorrectos,lbl_numero_correcto, lbl_estadisticas, btn_validar, lbl_historial
    # Evitar procesamiento si ya terminó
    if proceso_finalizado:
        ui.notify('⚠️ El proceso ya fue completado. Use Reiniciar para comenzar de nuevo.', type='warning')
        return
    
    valor_input = entrada_numero.value
    
    # 1. Validación de datos - Campo vacío
    if not valor_input or valor_input.strip() == '':
        ui.notify('⚠️ Por favor, escriba un número.', type='warning')
        return

    # 2. Validación de datos - Conversión a entero
    try:
        numero = int(valor_input)
    except ValueError:
        ui.notify('❌ Error: Debe ingresar un número entero válido.', type='negative')
        return

    # 3. Registrar el intento en la lista general
    lista_intentos.append(numero)
    
    # 4. Estructura de control condicional
    if validar_numero_en_rango(numero, 0, 20):
        # CASO ÉXITO - Número dentro del rango
        numero_correcto = numero
        proceso_finalizado = True
        
        # Actualizar interfaz
        actualizar_interfaz_exito(numero)
        
    else:
        # CASO ERROR - Número fuera del rango
        lista_intentos_incorrectos.append(numero)
        
        # Determinar tipo de error
        if numero < 0:
            mensaje = f'El número {numero} es MENOR que 0'
        else:
            mensaje = f'El número {numero} es MAYOR que 20'
        
        ui.notify(f'❌ Intento incorrecto: {mensaje}. Intente de nuevo.', type='negative')
        
        # Limpiar campo para nuevo intento
        entrada_numero.value = ''
        
        # Actualizar contadores y historial
        actualizar_contadores()
        mostrar_historial_completo()

def actualizar_interfaz_exito(numero):
    """Actualiza la interfaz cuando se ingresa un número válido"""
    global proceso_finalizado
    global entrada_numero, lbl_resultado, lbl_intentos_totales, lbl_intentos_incorrectos,lbl_numero_correcto, lbl_estadisticas, btn_validar, lbl_historial
    
    lbl_resultado.set_text(f'✅ NÚMERO VÁLIDO ENCONTRADO: {numero}')
    lbl_resultado.style('color: green; font-weight: bold; font-size: 1.3em')
    
    lbl_intentos_totales.set_text(f'Total de intentos: {len(lista_intentos)}')
    lbl_intentos_incorrectos.set_text(f'Intentos incorrectos: {len(lista_intentos_incorrectos)}')
    lbl_numero_correcto.set_text(f'Número correcto: {numero}')
    lbl_numero_correcto.style('color: green; font-weight: bold')
    
    # Mostrar estadísticas
    if len(lista_intentos) > 1:
        lbl_estadisticas.set_text(
            f'📊 Estadísticas: {len(lista_intentos_incorrectos)} errores antes del éxito'
        )
    else:
        lbl_estadisticas.set_text('📊 ¡Primer intento! Excelente.')
    
    # Mostrar historial completo
    mostrar_historial_completo()
    
    # Bloquear controles
    entrada_numero.disable()
    btn_validar.disable()
    btn_validar.label = '✓ Validación Completada'
    
    ui.notify(f'¡Éxito! El número {numero} está en el rango [0, 20].', type='positive')

def actualizar_contadores():
    """Actualiza las etiquetas de contadores"""
    lbl_intentos_totales.set_text(f'Total de intentos: {len(lista_intentos)}')
    lbl_intentos_incorrectos.set_text(f'Intentos incorrectos: {len(lista_intentos_incorrectos)}')
    lbl_numero_correcto.set_text('Número correcto: Pendiente...')
    lbl_numero_correcto.style('color: black; font-weight: normal')

def mostrar_historial_completo():
    """
    Muestra el historial completo de intentos en la interfaz.
    Usa la lista para almacenar y mostrar datos.
    """
    if len(lista_intentos) == 0:
        lbl_historial.set_text('📋 Historial: Sin intentos aún')
        return
    
    # Crear representación visual del historial
    historial_texto = ' → '.join(str(n) for n in lista_intentos)
    
    # Marcar el último como válido o inválido
    if len(lista_intentos_incorrectos) > 0 and lista_intentos[-1] == lista_intentos_incorrectos[-1]:
        estado = ' ❌'
    elif numero_correcto is not None and lista_intentos[-1] == numero_correcto:
        estado = ' ✅'
    else:
        estado = ''
    
    lbl_historial.set_text(f'📋 Historial: {historial_texto}{estado}')
    
    # Mostrar lista detallada en tooltip o label adicional
    if len(lista_intentos) > 1:
        detalle = f'\n   Detalle: {lista_intentos}'
        # lbl_detalle_historial.set_text(detalle)

def reiniciar_programa():
    """Reinicia todas las variables y la interfaz"""
    global lista_intentos, lista_intentos_incorrectos, numero_correcto, proceso_finalizado
    global entrada_numero, lbl_resultado, lbl_intentos_totales, lbl_intentos_incorrectos,lbl_numero_correcto, lbl_estadisticas, btn_validar, lbl_historial
    # Reiniciar variables
    lista_intentos = []
    lista_intentos_incorrectos = []
    numero_correcto = None
    proceso_finalizado = False
    
    # Reiniciar interfaz
    entrada_numero.value = ''
    entrada_numero.enable()
    
    btn_validar.enable()
    btn_validar.label = '🔍 Validar Número'
    
    lbl_resultado.set_text('Resultado: Esperando ingreso...')
    lbl_resultado.style('color: black; font-weight: normal; font-size: 1em')
    
    lbl_intentos_totales.set_text('Total de intentos: 0')
    lbl_intentos_incorrectos.set_text('Intentos incorrectos: 0')
    lbl_numero_correcto.set_text('Número correcto: Pendiente...')
    lbl_numero_correcto.style('color: black; font-weight: normal')
    lbl_estadisticas.set_text('📊 Estadísticas: Sin datos')
    lbl_historial.set_text('📋 Historial: Sin intentos aún')
    
    ui.notify('🔄 Programa reiniciado. Puede comenzar de nuevo.', type='info')

def mostrar_ayuda():
    """Muestra información sobre el rango válido"""
    ui.notify('📋 Instrucciones:\n• Ingrese un número entero entre 0 y 20 (inclusive)\n• El sistema registrará todos sus intentos\n• Continue intentando hasta acertar', 
              type='info', 
              multi_line=True)

# --- INTERFAZ GRÁFICA (UI) ---
def crear_interfaz():
    """Todo el UI debe estar DENTRO de esta función"""
    global entrada_numero, lbl_resultado, lbl_intentos_totales, lbl_intentos_incorrectos,lbl_numero_correcto, lbl_estadisticas, btn_validar, lbl_historial

    with ui.card().classes('w-full max-w-2xl mx-auto p-6 shadow-xl'):
        ui.label('📝 Registro de Intentos de Validación').classes('text-3xl font-bold mb-2 text-center text-primary')
        ui.label('Rango válido: [0 - 20]').classes('text-lg text-center text-gray-600 mb-6')
    
        # Sección de entrada
        with ui.row().classes('w-full gap-2'):
            entrada_numero = ui.input(
                label='Ingrese un número',
                placeholder='Ej: 15',
                validation={'Debe ser un número entero': lambda value: value == '' or value.lstrip('-').isdigit()}
            ).classes('flex-1')
        
            btn_validar = ui.button('🔍 Validar', on_click=procesar_validacion).classes('w-32')
    
        # Botones auxiliares
        with ui.row().classes('w-full justify-center gap-2 mt-2'):
            btn_ayuda = ui.button('ℹ️ Ayuda', on_click=mostrar_ayuda, color='info').classes('w-24')
            btn_reiniciar = ui.button('🔄 Reiniciar', on_click=reiniciar_programa, color='grey').classes('w-32')
    
        # Separador
        ui.separator().classes('my-6')
    
        # Sección de resultados principales
        ui.label('📊 RESULTADOS').classes('text-xl font-bold text-center mb-4')
    
        with ui.grid(columns=2).classes('w-full gap-4 mb-4'):
            with ui.card().classes('p-4 bg-blue-50'):
                lbl_intentos_totales = ui.label('Total de intentos: 0').classes('text-lg font-semibold')
        
            with ui.card().classes('p-4 bg-red-50'):
                lbl_intentos_incorrectos = ui.label('Intentos incorrectos: 0').classes('text-lg font-semibold')
        
            with ui.card().classes('p-4 bg-green-50'):
                lbl_numero_correcto = ui.label('Número correcto: Pendiente...').classes('text-lg font-semibold')
        
            with ui.card().classes('p-4 bg-purple-50'):
                lbl_estadisticas = ui.label('📊 Estadísticas: Sin datos').classes('text-sm')
    
        # Resultado principal
        lbl_resultado = ui.label('Resultado: Esperando ingreso...').classes('text-xl font-bold text-center my-4')
    
        # Separador
        ui.separator().classes('my-4')
    
        # Sección de historial
        ui.label('📋 HISTORIAL DE INTENTOS').classes('text-xl font-bold text-center mb-4')
        lbl_historial = ui.label('📋 Historial: Sin intentos aún').classes('text-lg text-gray-700 text-center p-4 bg-gray-50 rounded')
    
        # Espacio
        ui.label('').classes('h-4')

#mandar al menú principal
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)