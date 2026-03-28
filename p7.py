from nicegui import ui

# --- VARIABLES GLOBALES ---
lista_numeros = []
suma_total = 0
proceso_completado = False
entrada_numero=None
lbl_n=None
lbl_secuencia=None
lbl_resultado=None
btn_calcular=None

# --- FUNCIONES ---

def validar_numero_positivo(numero):
    """Valida si el número es positivo"""
    return numero > 0

def calcular_suma(n):
    """Calcula la suma de los primeros n números enteros"""
    lista = []
    suma = 0
    for i in range(1, n + 1):
        lista.append(i)
        suma += i
    return suma, lista

def procesar_calculo():
    """Función principal que valida y calcula"""
    global lista_numeros, suma_total, proceso_completado
    global entrada_numero, lbl_n, lbl_secuencia, lbl_resultado, btn_calcular
    
    if proceso_completado:
        return
    
    valor_input = entrada_numero.value
    
    # Validación de campo vacío
    if not valor_input or valor_input.strip() == '':
        ui.notify('⚠️ Por favor, ingrese un número.', type='warning')
        return
    
    # Validación de número entero
    try:
        n = int(valor_input)
    except ValueError:
        ui.notify('❌ Error: Debe ingresar un número entero válido.', type='negative')
        return
    
    # Validación de número positivo
    if not validar_numero_positivo(n):
        ui.notify('❌ Error: El número debe ser positivo (mayor que 0).', type='negative')
        return
    
    # Calcular
    suma_total, lista_numeros = calcular_suma(n)
    proceso_completado = True
    
    # Mostrar resultados
    lbl_n.set_text(f'📥 Valor de n: {n}')
    
    # Mostrar secuencia completa
    secuencia = ' + '.join(str(num) for num in lista_numeros)
    lbl_secuencia.set_text(f'🔢 Secuencia: {secuencia}')
    
    lbl_resultado.set_text(f'✅ Resultado final: {suma_total}')
    
    # Bloquear
    entrada_numero.disable()
    btn_calcular.disable()
    
    ui.notify(f'🎉 Cálculo exitoso! Suma = {suma_total}', type='positive')

def reiniciar():
    """Reinicia el programa"""
    global lista_numeros, suma_total, proceso_completado
    global entrada_numero, lbl_n, lbl_secuencia, lbl_resultado, btn_calcular
    
    lista_numeros = []
    suma_total = 0
    proceso_completado = False
    
    entrada_numero.value = ''
    entrada_numero.enable()
    btn_calcular.enable()
    
    lbl_n.set_text('📥 Valor de n: -')
    lbl_secuencia.set_text('🔢 Secuencia: -')
    lbl_resultado.set_text('✅ Resultado final: -')
    
    ui.notify('🔄 Programa reiniciado', type='info')

# --- INTERFAZ ---

def crear_interfaz():

    global entrada_numero, lbl_n, lbl_secuencia, lbl_resultado, btn_calcular

    with ui.card().classes('w-full max-w-2xl mx-auto p-6 shadow-lg'):
        ui.label('🧮 Cálculo de Suma de Números Enteros').classes('text-2xl font-bold mb-4 text-center')
    
        ui.label('📝 Ingrese un número n:').classes('mb-2 font-semibold')
        entrada_numero = ui.input(label='n', placeholder='Ej: 10').classes('w-full')
    
        with ui.row().classes('w-full gap-2 mt-4'):
            btn_calcular = ui.button('🔢 Calcular Suma', on_click=procesar_calculo).classes('flex-1')
            btn_reiniciar = ui.button('🔄 Reiniciar', on_click=reiniciar, color='grey').classes('w-32')
    
        ui.separator().classes('my-4')
    
        # Resultados
        with ui.card().classes('w-full p-4 bg-blue-50'):
            lbl_n = ui.label('📥 Valor de n: -').classes('text-lg font-bold')
            lbl_secuencia = ui.label('🔢 Secuencia: -').classes('text-md my-2 font-mono')
            lbl_resultado = ui.label('✅ Resultado final: -').classes('text-xl font-bold text-green-600 my-4')
    
        ui.label('💡 Tip: La fórmula es n(n+1)/2').classes('text-sm text-gray-500 text-center mt-2')

#mandar al menú principal
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title='Programa Individual', port=8081)