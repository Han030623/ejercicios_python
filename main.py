from nicegui import ui
from p1 import crear_interfaz as p1_interfaz #importar funcion 
from p2 import crear_interfaz as p2_interfaz
from p3 import crear_interfaz as p3_interfaz
from p4 import crear_interfaz as p4_interfaz
from p5 import crear_interfaz as p5_interfaz
from p6 import crear_interfaz as p6_interfaz
from p7 import crear_interfaz as p7_interfaz
from p8 import crear_interfaz as p8_interfaz
from p9 import crear_interfaz as p9_interfaz
from p10 import crear_interfaz as p10_interfaz
# --- PÁGINA PRINCIPAL (MENÚ) ---
@ui.page('/')
def menu_principal():
    with ui.card().classes('w-full max-w-4xl mx-auto p-6 shadow-xl'):
        ui.label('🎓 Menú Principal de Programas Python').classes('text-3xl font-bold mb-6 text-center text-primary')
        ui.label('Seleccione un programa para ejecutar:').classes('text-lg text-center mb-6 text-gray-600')
        
        # Crear grid de botones
        with ui.grid(columns='1 1 sm:2 md:3 lg:5').classes('w-full gap-4'):
            ui.link('P1 - Sistema de aumento de sueldos', '/p1').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P2 - Sistema de pago en parque de diversiones', '/p2').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P3 - Sistema de descuentos por mes en tienda', '/p3').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P4 - Validación de número menor que 10', '/p4').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P5 - Validación de número dentro de un rango', '/p5').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P6 - Registro de intentos de validación', '/p6').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P7 - Cálculo de suma de números enteros', '/p7').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P8 - Sistema de suma acumulativa', '/p8').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P9 - Suma de números hasta superar un límite', '/p9').classes('p-4 bg-blue-50 rounded-lg text-center')
            ui.link(' P10 - Sistema de pago de trabajadores', '/p10').classes('p-4 bg-blue-50 rounded-lg text-center')
    ui.separator().classes('my-6')
    ui.label('💡 Desarrollado con Python y NiceGUI').classes('text-center text-gray-500')

# --- RUTAS PARA CADA PROGRAMA ---

@ui.page('/p1')
def pagina_p1():
    ui.label('🔢 Sistema de aumento de sueldos').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p1_interfaz() #importación

@ui.page('/p2')
def pagina_p2():
    ui.label('📏 Sistema de pago en parque de diversiones').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p2_interfaz()

@ui.page('/p3')
def pagina_p3():
    ui.label('📝 Sistema de descuentos por mes en tienda').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p3_interfaz()

@ui.page('/p4')
def pagina_p4():
    ui.label('🧮 Validación de número menor que 10').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p4_interfaz()

@ui.page('/p5')
def pagina_p5():
    ui.label('🔄 Validación de número dentro de un rango').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p5_interfaz()


@ui.page('/p6')
def pagina_p6():
    ui.label('🎯 Registro de intentos de validación').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p6_interfaz()

@ui.page('/p7')
def pagina_p7():
    ui.label('💼 Cálculo de suma de números enteros').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p7_interfaz()

# Páginas genéricas
@ui.page('/p8')
def pagina_p8():
    ui.label('📊 Sistema de suma acumulativa').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p8_interfaz()

@ui.page('/p9')
def pagina_p9():
    ui.label('📈 Suma de números hasta superar un límite').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p9_interfaz()

@ui.page('/p10')
def pagina_p10():
    ui.label('📉 Sistema de pago de trabajadores').classes('text-2xl font-bold')
    ui.link('🔙 Volver al Menú', '/').classes('text-blue-500 mb-4')
    p10_interfaz()

# --- EJECUCIÓN ---
ui.run(title='Menú', port=8080)