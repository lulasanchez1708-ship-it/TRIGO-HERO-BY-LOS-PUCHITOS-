import streamlit as st
import pandas as pd
import random
import os
import matplotlib.pyplot as plt

# =====================================
# CONFIGURACIÓN
# =====================================
st.set_page_config(
    page_title="TRIGO HERO by PUCHITOS",
    page_icon="🎮",
    layout="centered"
)

# DEBUG (puedes quitarlo luego)
st.write("ARCHIVOS QUE VE STREAMLIT:")
st.write(os.listdir())

# =====================================
# PREGUNTAS
# =====================================
preguntas = [
    {"pregunta":"¿Cuántos grados tiene un ángulo recto?","respuesta":"90"},
    {"pregunta":"¿Cuántos grados tiene un ángulo llano?","respuesta":"180"},
    {"pregunta":"¿Cuánto mide un ángulo completo?","respuesta":"360"},
    {"pregunta":"¿Seno de 30°?","respuesta":"0.5"},
    {"pregunta":"¿Coseno de 0°?","respuesta":"1"},
    {"pregunta":"¿Tangente de 45°?","respuesta":"1"},
    {"pregunta":"¿Seno de 90°?","respuesta":"1"},
    {"pregunta":"¿Coseno de 90°?","respuesta":"0"},
    {"pregunta":"¿Tangente de 0°?","respuesta":"0"},
    {"pregunta":"¿Pi radianes en grados?","respuesta":"180"},
    {"pregunta":"¿Pi/2 en grados?","respuesta":"90"},
    {"pregunta":"¿2π radianes en grados?","respuesta":"360"},
    {"pregunta":"¿Hipotenusa de 3 y 4?","respuesta":"5"},
    {"pregunta":"¿Hipotenusa de 5 y 12?","respuesta":"13"},
    {"pregunta":"¿Hipotenusa de 8 y 15?","respuesta":"17"},
    {"pregunta":"¿Hipotenusa de 7 y 24?","respuesta":"25"},
    {"pregunta":"¿Raíz de 25?","respuesta":"5"},
    {"pregunta":"¿Raíz de 81?","respuesta":"9"},
    {"pregunta":"¿Raíz de 144?","respuesta":"12"},
    {"pregunta":"¿Raíz de 169?","respuesta":"13"},
    {"pregunta":"¿5²?","respuesta":"25"},
    {"pregunta":"¿12²?","respuesta":"144"},
    {"pregunta":"¿13²?","respuesta":"169"},
    {"pregunta":"¿15²?","respuesta":"225"},
    {"pregunta":"¿20²?","respuesta":"400"},
    {"pregunta":"¿Cateto opuesto / hipotenusa?","respuesta":"seno"},
    {"pregunta":"¿Cateto adyacente / hipotenusa?","respuesta":"coseno"},
    {"pregunta":"¿Cateto opuesto / adyacente?","respuesta":"tangente"},
    {"pregunta":"¿Un triángulo tiene cuántos grados?","respuesta":"180"},
    {"pregunta":"¿Un minuto tiene cuántos segundos?","respuesta":"60"},
    {"pregunta":"¿Una hora tiene cuántos minutos?","respuesta":"60"},
    {"pregunta":"¿sin(0°)?","respuesta":"0"},
    {"pregunta":"¿cos(180°)?","respuesta":"-1"},
    {"pregunta":"¿sin(180°)?","respuesta":"0"},
    {"pregunta":"¿cos(360°)?","respuesta":"1"},
    {"pregunta":"¿tan(90°)?","respuesta":"undefined"},
    {"pregunta":"¿sin²x + cos²x?","respuesta":"1"},
    {"pregunta":"¿cos(-x)?","respuesta":"cos(x)"},
    {"pregunta":"¿sin(-x)?","respuesta":"-sin(x)"},
    {"pregunta":"¿tan(-x)?","respuesta":"-tan(x)"},
    {"pregunta":"¿ángulo de 45° en radianes aprox?","respuesta":"0.785"},
    {"pregunta":"¿π ≈ ?","respuesta":"3.14"},
    {"pregunta":"¿360° en radianes?","respuesta":"2π"},
    {"pregunta":"¿180° en radianes?","respuesta":"π"},
    {"pregunta":"¿90° en radianes?","respuesta":"π/2"},
    {"pregunta":"¿60° seno?","respuesta":"√3/2"},
    {"pregunta":"¿60° coseno?","respuesta":"0.5"},
    {"pregunta":"¿30° coseno?","respuesta":"√3/2"},
    {"pregunta":"¿30° seno?","respuesta":"0.5"},
    {"pregunta":"¿45° seno?","respuesta":"√2/2"},
    {"pregunta":"¿45° coseno?","respuesta":"√2/2"},
    {"pregunta":"¿tan(60°)?","respuesta":"√3"},
    {"pregunta":"¿tan(30°)?","respuesta":"√3/3"},
    {"pregunta":"¿identidad pitagórica?","respuesta":"1"}
]

# =====================================
# BASE DE DATOS
# =====================================
archivo = "resultados.csv"

if not os.path.exists(archivo):
    pd.DataFrame(columns=["Nombre", "Puntaje"]).to_csv(archivo, index=False)

df_global = pd.read_csv(archivo)

# =====================================
# SESSION STATE
# =====================================
if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "inicio" not in st.session_state:
    st.session_state.inicio = False

if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0

if "vidas" not in st.session_state:
    st.session_state.vidas = 3

if "orden_preguntas" not in st.session_state:
    st.session_state.orden_preguntas = random.sample(preguntas, len(preguntas))

if "indice" not in st.session_state:
    st.session_state.indice = 0
    if "pregunta" not in st.session_state:
     st.session_state.pregunta = random.choice(preguntas)
# =====================================
# PORTADA
# =====================================
if not st.session_state.inicio:

    st.title("🎮 TRIGO HERO by PUCHITOS")

    nombre = st.text_input("Ingresa tu nombre")

    if st.button("Comenzar"):
        if nombre.strip():
            st.session_state.nombre = nombre
            st.session_state.inicio = True
            st.rerun()

# =====================================
# JUEGO
# =====================================
elif st.session_state.vidas > 0:

    st.title("🎮 TRIGO HERO")

    st.write(f"Jugador: **{st.session_state.nombre}**")

    col1, col2 = st.columns(2)
    col1.metric("⭐ Puntos", st.session_state.puntaje)
    col2.metric("❤️ Vidas", st.session_state.vidas)

    p = st.session_state.orden_preguntas[st.session_state.indice]
    st.subheader(p["pregunta"])

    respuesta = st.text_input("Tu respuesta", key="input")

    if st.button("Responder"):

        if respuesta.lower().strip() == p["respuesta"].lower():
            st.success("✔ Correcto")
            st.session_state.puntaje += 10
        else:
            st.error(f"❌ Incorrecto. Era: {p['respuesta']}")
            st.session_state.vidas -= 1

        st.session_state.indice += 1

if st.session_state.indice >= len(preguntas):
    st.session_state.vidas = 0  # termina juego

st.rerun()

# =====================================
# GAME OVER
# =====================================
else:

    st.title("💀 Juego Terminado")

    st.write(f"Puntaje final: {st.session_state.puntaje}")

    # guardar resultado
    nuevo = pd.DataFrame({
        "Nombre": [st.session_state.nombre],
        "Puntaje": [st.session_state.puntaje]
    })

    nuevo.to_csv(archivo, mode="a", header=False, index=False)

    st.success("Resultado guardado")

    # =================================
    # HISTORIAL + GRÁFICA
    # =================================
    df_global = pd.read_csv(archivo)

    st.subheader("🏆 Historial")

    st.dataframe(df_global)

    fig, ax = plt.subplots()
    ax.bar(df_global["Nombre"], df_global["Puntaje"])

    st.subheader("📊 Ranking")
    st.pyplot(fig)

    # reinicio
    if st.button("Jugar otra vez"):
        st.session_state.inicio = False
        st.session_state.puntaje = 0
        st.session_state.vidas = 3
        st.session_state.pregunta = random.choice(preguntas)
        st.rerun()