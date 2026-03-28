from nicegui import ui

# --- VARIABLES GLOBALES ---
lista_numeros = []
suma_acumulada = 0
proceso_finalizado = False
entrada_numero=None
lbl_lista=None
lbl_cantidad=None
lbl_suma=None
lbl_estado=None
btn_agregar=None

# --- FUNCIONES ---

def validar_numero(valor):
    """Valida que el valor sea un número entero"""
    try:
        int(valor)
        return True
    except ValueError:
        return False

def agregar_numero():
    """Agrega un número a la lista y actualiza la suma acumulada"""
    global lista_numeros, suma_acumulada, proceso_finalizado
    global entrada_numero, lbl_lista, lbl_cantidad, lbl_suma, lbl_estado, btn_agregar

    if proceso_finalizado:
        ui.notify('⚠️ El proceso ya finalizó. Use Reiniciar para comenzar de nuevo.', type='warning')
        return
    
    valor_input = entrada_numero.value
    
    # Validación de campo vacío
    if not valor_input or valor_input.strip() == '':
        ui.notify('⚠️ Por favor, ingrese un número.', type='warning')
        return
    
    # Validación de número entero
    if not validar_numero(valor_input):
        ui.notify('❌ Error: Debe ingresar un número entero válido.', type='negative')
        return
    
    numero = int(valor_input)
    
    # Verificar si es 0 (condición de parada)
    if numero == 0:
        finalizar_proceso()
        return
    
    # Guardar número en la lista
    lista_numeros.append(numero)
    
    # Actualizar suma acumulada
    suma_acumulada += numero
    
    # Mostrar resultados parciales
    actualizar_interfaz()
    
    # Limpiar campo para siguiente número
    entrada_numero.value = ''
    entrada_numero.focus()
    
    ui.notify(f'➕ Número {numero} agregado. Suma acumulada: {suma_acumulada}', type='info')

def actualizar_interfaz():
    """Actualiza la interfaz con los datos actuales"""
    lbl_lista.set_text(f'📋 Lista de números: {lista_numeros}')
    lbl_cantidad.set_text(f'🔢 Cantidad de números: {len(lista_numeros)}')
    lbl_suma.set_text(f'💰 Suma acumulada: {suma_acumulada}')

def finalizar_proceso():
    """Finaliza el proceso cuando se ingresa 0"""
    global proceso_finalizado
    global entrada_numero, lbl_lista, lbl_cantidad, lbl_suma, lbl_estado, btn_agregar
    proceso_finalizado = True
    
    # Mostrar resultados finales
    lbl_lista.set_text(f'📋 Lista de números: {lista_numeros}')
    lbl_cantidad.set_text(f'🔢 Cantidad de números: {len(lista_numeros)}')
    lbl_suma.set_text(f'💰 Suma total: {suma_acumulada}')
    
    lbl_estado.set_text('✅ Proceso finalizado (se ingresó 0)')
    lbl_estado.style('color: green; font-weight: bold')
    
    # Bloquear controles
    entrada_numero.disable()
    btn_agregar.disable()
    
    ui.notify('🏁 Proceso finalizado. Se ingresó el número 0.', type='positive')

def reiniciar():
    """Reinicia el programa"""
    global lista_numeros, suma_acumulada, proceso_finalizado
    global entrada_numero, lbl_lista, lbl_cantidad, lbl_suma, lbl_estado, btn_agregar
    
    lista_numeros = []
    suma_acumulada = 0
    proceso_finalizado = False
    
    entrada_numero.value = ''
    entrada_numero.enable()
    btn_agregar.enable()
    
    lbl_lista.set_text('📋 Lista de números: []')
    lbl_cantidad.set_text('🔢 Cantidad de números: 0')
    lbl_suma.set_text('💰 Suma acumulada: 0')
    lbl_estado.set_text('⏳ Estado: Esperando números...')
    lbl_estado.style('color: black; font-weight: normal')
    
    ui.notify('🔄 Programa reiniciado', type='info')

# --- INTERFAZ ---

def crear_interfaz():

    global entrada_numero, lbl_lista, lbl_cantidad, lbl_suma, lbl_estado, btn_agregar

    with ui.card().classes('w-full max-w-2xl mx-auto p-6 shadow-lg'):
        ui.label('🔄 Sistema de Suma Acumulativa').classes('text-2xl font-bold mb-2 text-center')
        ui.label('Ingrese números continuos. Ingrese 0 para finalizar.').classes('text-gray-600 mb-4 text-center')
    
        # Entrada de números
        ui.label('📝 Ingrese un número:').classes('mb-2 font-semibold')
        entrada_numero = ui.input(label='Número', placeholder='Ej: 5').classes('w-full')
    
        # Botones
        with ui.row().classes('w-full gap-2 mt-4'):
            btn_agregar = ui.button('➕ Agregar Número', on_click=agregar_numero).classes('flex-1')
            btn_reiniciar = ui.button('🔄 Reiniciar', on_click=reiniciar, color='grey').classes('w-32')
    
        ui.separator().classes('my-4')
    
        # Estado del proceso
        lbl_estado = ui.label('⏳ Estado: Esperando números...').classes('text-lg font-semibold mb-4')
    
        # Resultados
        with ui.card().classes('w-full p-4 bg-blue-50'):
            lbl_lista = ui.label('📋 Lista de números: []').classes('text-md font-mono')
            lbl_cantidad = ui.label('🔢 Cantidad de números: 0').classes('text-lg font-bold my-2')
            lbl_suma = ui.label('💰 Suma acumulada: 0').classes('text-xl font-bold text-green-600 my-2')
    
        ui.label('💡 Tip: Ingrese 0 para terminar y ver resultados finales.').classes('text-sm text-gray-500 text-center mt-2')

#se ejecuta en el menu
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)