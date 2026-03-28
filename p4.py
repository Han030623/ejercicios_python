from nicegui import ui

# --- VARIABLES GLOBALES DE ESTADO ---
# Usamos estas variables para recordar la información entre clics
intentos = 0
validado = False
entrada_numero= None
lbl_resultado= None
lbl_intentos=None
btn_validar=None


# --- FUNCIONES DE LÓGICA Y PROCESO ---

def validar_numero():
    """
    Función principal que contiene la lógica de validación,
    estructuras de control y actualización de la interfaz.
    """
    global intentos, validado
    global entrada_numero, lbl_resultado, lbl_intentos, btn_validar
    
    # Obtener el valor del input
    valor_input = entrada_numero.value
    
    # 1. Validación de datos (Evitar errores de entrada no numérica)
    if not valor_input:
        ui.notify('Por favor, escribe un número.', type='warning')
        return

    try:
        numero = int(valor_input)
    except ValueError:
        ui.notify('Error: Debes ingresar un número entero válido.', type='negative')
        return

    # 2. Estructura de control condicional (Verificar si es menor que 10)
    if numero < 10:
        # CASO ÉXITO
        validado = True
        intentos += 1 # Contamos el intento exitoso también
        
        # Actualizar interfaz con resultados
        lbl_resultado.set_text(f'¡Número correcto ingresado: {numero}!')
        lbl_intentos.set_text(f'Cantidad de intentos realizados: {intentos}')
        lbl_intentos.style('color: green; font-weight: bold')
        
        # Bloquear la entrada para que no siga intentando
        entrada_numero.disable()
        btn_validar.disable()
        btn_validar.label = 'Proceso Finalizado'
        
        ui.notify(f'¡Éxito! El número {numero} es menor que 10.', type='positive')
        
    else:
        # CASO ERROR (El número es 10 o mayor)
        intentos += 1
        
        # Mostrar mensaje de error
        ui.notify(f'Error: El número {numero} NO es menor que 10. Intente de nuevo.', type='negative')
        
        # Limpiar el campo para solicitar nuevamente el número
        entrada_numero.value = ''
        entrada_numero.focus() # Poner el cursor de nuevo en la caja
        
        # Actualizar contador de intentos en tiempo real (opcional, para feedback)
        lbl_intentos.set_text(f'Intentos fallidos hasta ahora: {intentos}')

def reiniciar_programa():
    """Función auxiliar para limpiar el estado y volver a empezar"""
    global intentos, validado
    global entrada_numero, lbl_resultado, lbl_intentos, btn_validar
    intentos = 0
    validado = False
    
    entrada_numero.value = ''
    entrada_numero.enable()
    btn_validar.enable()
    btn_validar.label = 'Validar Número'
    
    lbl_resultado.set_text('Resultado: Esperando ingreso...')
    lbl_intentos.set_text('Cantidad de intentos: 0')
    lbl_intentos.style('color: black')

# --- INTERFAZ GRÁFICA (UI) ---

def crear_interfaz():
    """Todo el UI debe estar DENTRO de esta función"""
    global entrada_numero, lbl_resultado, lbl_intentos, btn_validar

    with ui.card().classes('w-full max-w-md mx-auto p-6'):
        ui.label('Validación de Número < 10').classes('text-2xl font-bold mb-4 text-center')
    
        ui.label('Ingrese un número entero menor que 10:').classes('mb-2')
    
        # Input numérico
        entrada_numero = ui.input(label='Número', placeholder='Ej: 5').classes('w-full')
    
        # Botón de acción
        with ui.row().classes('w-full justify-center mt-4'):
            btn_validar = ui.button('Validar Número', on_click=validar_numero).classes('w-full')
    
        # Área de resultados (Etiquetas)
        ui.separator().classes('my-4')
    
        lbl_resultado = ui.label('Resultado: Esperando ingreso...').classes('text-lg font-bold')
        lbl_intentos = ui.label('Cantidad de intentos: 0').classes('text-gray-600')
    
        # Botón extra para reiniciar (cumple requisito de estructuras de control si se usa)
        ui.button('Reiniciar', on_click=reiniciar_programa, color='grey').classes('mt-4 w-full')

#mandar al menú principal
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)