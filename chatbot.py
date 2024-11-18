import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv  # 1. Importar la librería para cargar variables de entorno

# Cargar las variables de entorno desde el archivo .env
load_dotenv()  # 2. Llamar a load_dotenv() para cargar las variables desde el .env

# Verificar que la clave de API se haya cargado correctamente
api_key = os.getenv('GROQ_API_KEY')  # 3. Obtener la clave de API desde las variables de entorno
print(f"Clave de API cargada: {api_key}")  # 4. Imprimir la clave para verificar que se cargó

# Configuración de modelos de Groq
MODELOS = [
    'mixtral-8x7b-32768',
    'llama2-70b-4096',
    'gemma-7b-it'
]

# Inicializar el cliente de Groq usando la clave cargada
client = Groq(api_key=api_key)  # 5. Usar la clave cargada para configurar el cliente

# Inicializar el historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

def configurar_pagina():
    """Configura la página principal y la barra lateral"""
    st.set_page_config(
        page_title="Chat con Groq",
        page_icon="🤖",
        layout="centered"
    )
    
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: 2rem;'>
            🤖 Chat con Groq
        </h1>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
        <h2 style='text-align: center;'>
            ⚙️ Configuración de la IA
        </h2>
    """, unsafe_allow_html=True)
    
    modelo_elegido = st.sidebar.selectbox(
        'Modelo disponible:',
        options=MODELOS,
        index=0
    )
    
    # Agregar información sobre el modelo
    st.sidebar.markdown(f"""
        ### Información del modelo
        - **Modelo seleccionado:** {modelo_elegido}
        - **Contexto máximo:** 32,768 tokens
        - **Capacidades:** Procesamiento de lenguaje natural, respuestas coherentes
    """)
    
    return modelo_elegido

def obtener_respuesta_ia(mensaje, modelo):
    """Obtiene la respuesta de la IA usando Groq"""
    try:
        completion = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un asistente amable y servicial que proporciona respuestas claras y precisas."},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error al procesar la solicitud: {str(e)}"

def mostrar_historial():
    """Muestra el historial de mensajes"""
    for mensaje in st.session_state.messages:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def main():
    modelo = configurar_pagina()
    
    # Mostrar historial de chat
    mostrar_historial()
    
    # Campo de entrada para el chat
    mensaje = st.chat_input("Escribe tu mensaje aquí... 💬")
    
    if mensaje:
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": mensaje})
        with st.chat_message("user"):
            st.markdown(mensaje)
        
        # Obtener y mostrar respuesta de la IA
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                respuesta = obtener_respuesta_ia(mensaje, modelo)
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})

if __name__ == "__main__":
    main()
