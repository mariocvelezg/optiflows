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
    variables = ['st_archivo', 'st_opt', 'st_dwld', 'datos', 'requerimiento', 'costo_inicial', 'solucion_txt', 'solucion_list', 'costo_optimo', 'descarga']
    for var in variables:
        if var not in st.session_state:
            st.session_state[var] = False
        
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
    dat = st.session_state.datos
    fig = go.Figure(data=[go.Table(
            header=dict(values=['Shipper', 'Origen', 'Destino', 'Cantidad']),
            cells=dict(values=[
                [fila[0] for fila in dat],
                [fila[1] for fila in dat],
                [fila[2] for fila in dat],
                [fila[3] for fila in dat]]))])
    fig.update_layout(
        autosize=False,
        height=62*len(st.session_state.datos[0]),
        margin={'l':0, 'r':0, 'b':0, 't':0})
    st.session_state.tabla_datos=True
    st.write(fig)
    st.text('Costo inicial = $'+str(st.session_state.costo_inicial))

# Crea tabla con solución óptima en Plotly
def imprime_tabla_solucion():
    sol = st.session_state.solucion_list
    fig = go.Figure(data=[go.Table(
            header=dict(values=['Shipper', 'Origen', 'Destino', 'Cantidad']),
            cells=dict(values=[sol[0], sol[1], sol[2], sol[3]]))])
    fig.update_layout(autosize=False, height=25*len(sol[0]), margin={'l':0, 'r':0, 'b':0, 't':0})
    st.write(fig)
    st.text('Costo óptimo = $'+str(st.session_state.costo_optimo))

def imprime_todo():
    imprime_tabla_datos()
    imprime_tabla_solucion()
    st.session_state.descarga = True

inicializar_st()
st.title('Modelo de Simplicación de Flujos')

if st.session_state.st_archivo == False:
    archivo = st.file_uploader(label=":red[Subir archivo de requerimientos]", type='txt')
    st.session_state.st_archivo = True
    
    if st.session_state.datos == False:
        st.session_state.datos = [linea.decode('utf-8').split() for linea in archivo]
        st.session_state.costo_inicial = sum([float(linea[3])*float(linea[4]) for linea in st.session_state.datos])
        st.session_state.requerimiento = imprime_texto_datos(st.session_state.datos)
        imprime_tabla_datos()

    if st.session_state.solucion_txt == False:
        optimizar = st.button('Optimizar Flujos')
        if optimizar:
            st.session_state.costo_optimo, st.session_state.solucion_txt, st.session_state.solucion_list = lp.resuelve_modelo(st.session_state.datos)
            imprime_tabla_datos()
            imprime_tabla_solucion()
            if st.session_state.descarga == False:
                boton_descarga = st.download_button(label='Descargar Solucion', data=st.session_state.solucion_txt, file_name='flujos_optimos.txt')
