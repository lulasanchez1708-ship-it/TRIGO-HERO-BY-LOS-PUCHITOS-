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
    {"pregunta":"¿Pi radianes equivalen a cuántos grados?","respuesta":"180"},
    {"pregunta":"¿Pi/2 radianes equivalen a cuántos grados?","respuesta":"90"},
    {"pregunta":"¿360 grados equivalen a cuántos radianes?","respuesta":"2pi"},
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
    {"pregunta":"¿Cateto opuesto sobre hipotenusa?","respuesta":"seno"},
    {"pregunta":"¿Cateto adyacente sobre hipotenusa?","respuesta":"coseno"},
    {"pregunta":"¿Cateto opuesto sobre adyacente?","respuesta":"tangente"},
    {"pregunta":"¿Un triángulo tiene cuántos grados?","respuesta":"180"},
    {"pregunta":"¿Un minuto tiene cuántos segundos?","respuesta":"60"},
    {"pregunta":"¿Una hora tiene cuántos minutos?","respuesta":"60"}
]

# =====================================
# BASE DE DATOS
# =====================================

archivo = "resultados.csv"

if not os.path.exists(archivo):
    pd.DataFrame(columns=["Nombre", "Puntaje"]).to_csv(
        archivo,
        index=False
    )

# =====================================
# VARIABLES
# =====================================

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "inicio" not in st.session_state:
    st.session_state.inicio = False

if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0

if "vidas" not in st.session_state:
    st.session_state.vidas = 3

if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = random.choice(preguntas)

# =====================================
# PORTADA
# =====================================

if not st.session_state.inicio:

    st.title("🎮 TRIGO HERO by PUCHITOS")

    st.markdown("""
### Sistema Interactivo de Evaluación Trigonométrica

👥 Grupo Puchitos

❤️ 3 vidas

⭐ 10 puntos por respuesta correcta
""")

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

    st.title("🎮 TRIGO HERO by PUCHITOS")

    st.write(f"Jugador: **{st.session_state.nombre}**")

    col1, col2 = st.columns(2)

    col1.metric("⭐ Puntos", st.session_state.puntaje)
    col2.metric("❤️ Vidas", st.session_state.vidas)

    pregunta = st.session_state.pregunta_actual

    st.subheader(pregunta["pregunta"])

    respuesta = st.text_input("Tu respuesta")

    if st.button("Responder"):

        if respuesta.lower().strip() == pregunta["respuesta"].lower():

            st.success("✅ Correcto")
            st.session_state.puntaje += 10

        else:

            st.error(
                f"❌ Incorrecto. Era: {pregunta['respuesta']}"
            )

            st.session_state.vidas -= 1

        st.session_state.pregunta_actual = random.choice(
            preguntas
        )

        st.rerun()

# =====================================
# GAME OVER
# =====================================

else:

    st.title("💀 Juego Terminado")

    st.write(
        f"Puntaje final: {st.session_state.puntaje}"
    )

    archivo = st.file_uploader("Sube tu Excel", type=["xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)

    df = df.dropna(subset=["Nombre", "Puntaje"])
    df["Puntaje"] = pd.to_numeric(df["Puntaje"], errors="coerce")
    df = df.dropna(subset=["Puntaje"])

    fig, ax = plt.subplots()
    ax.bar(df["Nombre"], df["Puntaje"])

    st.pyplot(fig)

    nuevo = pd.DataFrame({
        "Nombre":[st.session_state.nombre],
        "Puntaje":[st.session_state.puntaje]
    })

    df = pd.concat([df, nuevo], ignore_index=True)

    df.to_csv(archivo, index=False)

    st.success("Resultado guardado")

    st.subheader("🏆 Historial")

    st.dataframe(df)

    # gráfico

    fig, ax = plt.subplots()

ax.bar(
    df["Nombre"],
    df["Puntaje"]
)

ax.set_title(
        "Puntajes de jugadores"
    )

st.pyplot(fig)

if st.button("Jugar otra vez"):

        st.session_state.inicio = False
        st.session_state.puntaje = 0
        st.session_state.vidas = 3
        st.session_state.pregunta_actual = random.choice(
            preguntas
        )

        st.rerun()