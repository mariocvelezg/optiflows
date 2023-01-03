# -*- coding: utf-8 -*-
"""Mario C. Vélez G. -- marvelez@eafit.edu.co """

import streamlit as st
import modelo_lp as lp

# Inicializar variables de estado
variables = ['datos', 'requerimiento', 'costo_inicial', 'solucion', 'costo_optimo', 'descarga']
for var in variables:
    if var not in st.session_state:
        st.session_state[var] = None
  
def imprime_todo():
    st.session_state.descarga = True


st.title('Modelo de Simplicación de Flujos')

archivo = st.file_uploader('Subir archivo de requerimientos', type='txt', label_visibility='visible')

if archivo:
    if st.session_state.datos == None:
        st.session_state.datos = [linea.decode('utf-8').split() for linea in archivo]
        costo_antes = 0
        req = 45*'='+'\n'
        req += "{:<10} {:<10} {:<12} {:^10} \n".format('Shipper', 'Origin', 'Destination', 'Quantity')
        req += 45*'='+'\n'
        for linea in st.session_state.datos:
            costo_antes += float(linea[3])*float(linea[4])
            req +="{:<10} {:<10} {:<12} {:^10} \n".format(linea[0], linea[1], linea[2], linea[3])
        req += 45*'='+'\n'
        st.session_state.requerimiento = req
        st.session_state.costo_inicial = costo_antes
        st.text(st.session_state.requerimiento)
        st.text('Costo inicial = $'+str(st.session_state.costo_inicial))
    else:
        st.text(st.session_state.requerimiento)
        st.text('Costo inicial = $'+str(st.session_state.costo_inicial))
        if st.session_state.descarga:
            st.text(st.session_state.solucion)
            st.text('Costo óptimo = $'+str(st.session_state.costo_optimo))
    
    if st.session_state.solucion == None:
        optimizar = st.button('Optimizar Flujos')
        if optimizar:
            st.session_state.costo_optimo, st.session_state.solucion = lp.resuelve_modelo(st.session_state.datos)
            st.text(st.session_state.solucion)
            st.text('Costo óptimo = $'+str(st.session_state.costo_optimo))
            st.download_button(
                'Descargar Solucion',
                st.session_state.solucion,
                file_name='flujos_optimos.txt',
                on_click=imprime_todo)