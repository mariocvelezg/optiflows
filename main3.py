# -*- coding: utf-8 -*-
"""Mario C. Vélez G. -- marvelez@eafit.edu.co """

import streamlit as st
import modelo_lp as lp
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title='Optimización de Flujos', layout='centered')
ocultar_menu ='''
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden; }
    <\style>'''
st.markdown(ocultar_menu, unsafe_allow_html=True)

# Inicializar variables de estado
def inicializar_st():
    variables = ['datos', 'costo_inicial', 'solucion_txt', 'solucion_list', 'costo_optimo', 'descarga']
    for var in variables:
        if var not in st.session_state:
            st.session_state[var] = None
        
# Crea texto plano con los datos e entrada
def imprime_texto_datos(datos:list) -> str:
    req = 45*'='+'\n'
    req += "{:<10} {:<10} {:<12} {:^10} \n".format('Shipper', 'Origin', 'Destination', 'Quantity')
    req += 45*'='+'\n'
    for linea in datos:
        req +="{:<10} {:<10} {:<12} {:^10} \n".format(linea[0], linea[1], linea[2], linea[3])
    req += 45*'='+'\n'
    return(req)

# Crea tabla de datos de entrada en Plotly
def imprime_tabla_datos():
    col_names = ['Shipper', 'Origen', 'Destino', 'Cantidad'] 
    dat = st.session_state.datos
    fig = go.Figure(data=[go.Table(
            header=dict(values=[f"<b>{col}</b>" for col in col_names],
                        font=dict(color='black', family="Courier New", size=12)),
            cells=dict(values=[
                [fila[0] for fila in dat],
                [fila[1] for fila in dat],
                [fila[2] for fila in dat],
                [fila[3] for fila in dat]],
                        font=dict(color='black', family="Courier New", size=12),
                        height=25))])
    fig.update_layout(
        autosize=False,
        height=76*len(st.session_state.datos[0]),
        margin={'l':0, 'r':0, 'b':0, 't':0})
    st.session_state.tabla_datos=True
    st.write(fig)
    st.text('Costo inicial = $'+str(st.session_state.costo_inicial))
    st.text("") # Espacio en blanco

# Crea tabla con solución óptima en Plotly
def imprime_tabla_solucion():
    col_names = ['Shipper', 'Origen', 'Destino', 'Cantidad'] 
    sol = st.session_state.solucion_list
    fig = go.Figure(data=[go.Table(
            header=dict(values=[f"<b>{col}</b>" for col in col_names],
                        font=dict(color='black', family="Courier New", size=12)),
            cells=dict(values=[sol[0], sol[1], sol[2], sol[3]],
                       font=dict(color='black', family="Courier New", size=12), height=25))])
    fig.update_layout(autosize=False, height=31*len(sol[0]), margin={'l':0, 'r':0, 'b':0, 't':0})
    st.write(fig)
    st.text('Costo óptimo = $'+str(st.session_state.costo_optimo))
    st.text('') # Espacio en blanco

def optimizar_flujos():
    st.session_state.costo_optimo, st.session_state.solucion_txt, st.session_state.solucion_list = lp.resuelve_modelo(st.session_state.datos)

inicializar_st()
st.title('Modelo de Simplicación de Flujos')

archivo = st.file_uploader(label=":red[Subir archivo de requerimientos]", type='txt')

if archivo:
    
    if st.session_state.datos == None:
        st.session_state.datos = [linea.decode('utf-8').split() for linea in archivo]
        st.session_state.costo_inicial = sum([float(linea[3])*float(linea[4]) for linea in st.session_state.datos])
        st.session_state.requerimiento = imprime_texto_datos(st.session_state.datos)
    imprime_tabla_datos()
    optimizar = st.button('Optimizar Flujos', on_click=optimizar_flujos)

    if st.session_state.solucion_txt != None:
        imprime_tabla_solucion()
        st.download_button(label='Descargar Solucion', data=st.session_state.solucion_txt, file_name='flujos_optimos.txt')