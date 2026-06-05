import streamlit as st
import pandas as pd
import random
import os
import matplotlib.pyplot as plt
import time

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="TRIGO HERO",
    page_icon="🎮",
    layout="centered"
)

# =========================
# PREGUNTAS (60)
# =========================
preguntas = [
    {"pregunta":"¿Cuántos grados tiene un ángulo recto?","respuesta":"90"},
    {"pregunta":"¿Cuántos grados tiene un ángulo llano?","respuesta":"180"},
    {"pregunta":"¿Cuánto mide un ángulo completo?","respuesta":"360"},
    {"pregunta":"¿Seno de 30°?","respuesta":"0.5"},
    {"pregunta":"¿Coseno de 0°?","respuesta":"1"},
    {"pregunta":"¿Tangente de 45°?","respuesta":"1"},
    {"pregunta":"¿Seno de 90°?","respuesta":"1"},
    {"pregunta":"¿Coseno de 90°?","respuesta":"0"},
    {"pregunta":"¿π en grados?","respuesta":"180"},
    {"pregunta":"¿π/2 en grados?","respuesta":"90"},
    {"pregunta":"¿2π en grados?","respuesta":"360"},
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
    {"pregunta":"¿sin(0°)?","respuesta":"0"},
    {"pregunta":"¿cos(180°)?","respuesta":"-1"},
    {"pregunta":"¿sin(180°)?","respuesta":"0"},
    {"pregunta":"¿cos(360°)?","respuesta":"1"},
    {"pregunta":"¿sin²x + cos²x?","respuesta":"1"},
    {"pregunta":"¿cos(-x)?","respuesta":"cos(x)"},
    {"pregunta":"¿sin(-x)?","respuesta":"-sin(x)"},
    {"pregunta":"¿tan(-x)?","respuesta":"-tan(x)"},
    {"pregunta":"¿π ≈ ?","respuesta":"3.14"},
    {"pregunta":"¿180° en radianes?","respuesta":"π"},
    {"pregunta":"¿360° en radianes?","respuesta":"2π"},
    {"pregunta":"¿90° en radianes?","respuesta":"π/2"},
    {"pregunta":"¿60° seno?","respuesta":"√3/2"},
    {"pregunta":"¿30° seno?","respuesta":"0.5"},
    {"pregunta":"¿45° coseno?","respuesta":"√2/2"},
    {"pregunta":"¿tan(30°)?","respuesta":"√3/3"},
    {"pregunta":"¿identidad pitagórica?","respuesta":"1"},
    {"pregunta":"¿cateto opuesto/hipotenusa?","respuesta":"seno"},
    {"pregunta":"¿cateto adyacente/hipotenusa?","respuesta":"coseno"},
    {"pregunta":"¿cateto opuesto/adyacente?","respuesta":"tangente"},
    {"pregunta":"¿triángulo suma ángulos?","respuesta":"180"},
    {"pregunta":"¿1 hora cuántos minutos?","respuesta":"60"},
    {"pregunta":"¿1 minuto cuántos segundos?","respuesta":"60"},
    {"pregunta":"¿tan(90°)?","respuesta":"indefinido"},
    {"pregunta":"¿cos(0°)?","respuesta":"1"},
    {"pregunta":"¿sin(90°)?","respuesta":"1"},
    {"pregunta":"¿ángulo completo en radianes?","respuesta":"2π"},
]

# =========================
# CSV CONFIG
# =========================
archivo = "resultados.csv"

# =========================
# SESSION STATE
# =========================
if "inicio" not in st.session_state:
    st.session_state.inicio = False

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0

if "vidas" not in st.session_state:
    st.session_state.vidas = 3

if "indice" not in st.session_state:
    st.session_state.indice = 0

if "orden" not in st.session_state:
    st.session_state.orden = random.sample(preguntas, len(preguntas))

if "guardado" not in st.session_state:
    st.session_state.guardado = False

# =========================
# PORTADA
# =========================
if not st.session_state.inicio:
    st.title("🎮 TRIGO HERO")
    st.write("¡Bienvenido al juego de trivia de trigonometría!")
    
    nombre = st.text_input("Ingresa tu nombre", max_chars=20)

    if st.button("Comenzar", use_container_width=True):
        if nombre.strip():
            st.session_state.nombre = nombre.strip()
            st.session_state.inicio = True
            st.session_state.puntaje = 0
            st.session_state.vidas = 3
            st.session_state.indice = 0
            st.session_state.guardado = False
            st.session_state.orden = random.sample(preguntas, len(preguntas))
            st.rerun()
        else:
            st.warning("⚠️ Por favor, ingresa un nombre válido.")

# =========================
# JUEGO ACTIVO
# =========================
elif st.session_state.vidas > 0 and st.session_state.indice < len(preguntas):
    st.title("🎮 TRIGO HERO")
    st.write(f"Jugador: **{st.session_state.nombre}**")

    col1, col2 = st.columns(2)
    col1.metric("⭐ Puntaje", st.session_state.puntaje)
    col2.metric("❤️ Vidas", st.session_state.vidas)

    pregunta = st.session_state.orden[st.session_state.indice]
    st.subheader(f"Pregunta {st.session_state.indice + 1}: {pregunta['pregunta']}")

    # Formulario para evitar recargas raras al presionar Enter
    with st.form(key="formulario_pregunta"):
        respuesta = st.text_input("Tu respuesta:", key=f"resp_{st.session_state.indice}")
        enviado = st.form_submit_button("Responder", use_container_width=True)

    if enviado:
        if respuesta.lower().strip() == pregunta["respuesta"].lower().strip():
            st.success("✔ ¡Correcto! (+10 puntos)")
            st.session_state.puntaje += 10
        else:
            st.error(f"❌ Incorrecto. La respuesta era: {pregunta['respuesta']}")
            st.session_state.vidas -= 1

        st.session_state.indice += 1
        time.sleep(1.5)  # Breve pausa para que el jugador vea el resultado antes de avanzar
        st.rerun()

# =========================
# GAME OVER
# =========================
else:

    st.title("💀 Juego Terminado")
    st.write(f"Puntaje final de **{st.session_state.nombre}**: {st.session_state.puntaje} puntos")

    # 1. GUARDAR LIMPIO (Evita duplicados infinitos al recargar)
    if not st.session_state.get("guardado", False):
        nuevo = pd.DataFrame({
            "Nombre": [str(st.session_state.nombre).strip()],
            "Puntaje": [int(st.session_state.puntaje)]
        })

        if os.path.exists(archivo):
            try:
                df_old = pd.read_csv(archivo)
                df_final = pd.concat([df_old, nuevo], ignore_index=True)
            except:
                df_final = nuevo
        else:
            df_final = nuevo

        df_final.to_csv(archivo, index=False)
        st.session_state.guardado = True
        st.success("✔ Resultado guardado con éxito")

    # 2. LEER Y SANEAR DATOS (Aquí estaba el fallo de Matplotlib)
    if os.path.exists(archivo):
        try:
            df = pd.read_csv(archivo)
            
            # Forzar limpieza absoluta de datos corruptos
            df = df.dropna(subset=["Nombre", "Puntaje"]) # Elimina filas vacías
            df["Nombre"] = df["Nombre"].astype(str)      # Todo nombre DEBE ser texto puro
            df["Puntaje"] = pd.to_numeric(df["Puntaje"], errors='coerce').fillna(0).astype(int) # Todo puntaje DEBE ser entero
            
            # Ordenar para mostrar un Top 10 limpio
            df_ranking = df.sort_values(by="Puntaje", ascending=False).head(10)

            st.subheader("🏆 Tabla de Posiciones (Top 10)")
            st.dataframe(df_ranking, use_container_width=True, hide_index=True)

            # 3. GRÁFICO SEGURO (Formateado anti-errores)
            if not df_ranking.empty:
                st.subheader("📊 Historial de Puntajes")
                
                # Convertir explícitamente a listas nativas de Python para que Matplotlib no se confunda
                nombres_lista = df_ranking["Nombre"].tolist()
                puntajes_lista = df_ranking["Puntaje"].tolist()

                fig, ax = plt.subplots()
                ax.bar(nombres_lista, puntajes_lista, color="#FF4B4B")
                
                # Estética del gráfico
                ax.set_ylabel("Puntaje")
                ax.set_xlabel("Jugadores")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                st.pyplot(fig)
                plt.close(fig) # Liberar memoria en el servidor
        except Exception as e:
            st.error(f"Error al procesar el historial: {e}")
            st.warning("Si el problema persiste, borra el archivo 'resultados.csv' de tu repositorio para iniciar el historial desde cero.")

    st.write("---")

    # =========================
    # BOTÓN DE VOLVER A JUGAR (100% Funcional)
    # =========================
    if st.button("🔄 Jugar otra vez", use_container_width=True):
        st.session_state.inicio = False
        st.session_state.nombre = ""
        st.session_state.puntaje = 0
        st.session_state.vidas = 3
        st.session_state.indice = 0
        st.session_state.guardado = False
        st.session_state.orden = random.sample(preguntas, len(preguntas))
        st.rerun()