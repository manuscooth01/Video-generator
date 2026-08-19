import streamlit as st
import replicate
import os

# Configurar el token (se leerá de los secretos de Streamlit)
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

st.set_page_config(page_title="Generador de Video IA", layout="centered")
st.title("🎬 Generador de Video con IA")
st.write("Escribe un prompt y genera un video usando HunyuanVideo.")

prompt = st.text_input("Prompt", "Un astronauta montando un caballo en Marte, estilo cinematográfico")
video_length = st.selectbox("Longitud de video", [49, 73, 97, 129])
width = st.selectbox("Ancho", [512, 640, 720, 768, 832, 896, 960, 1024], index=2)
height = st.selectbox("Alto", [320, 384, 480, 512, 576, 640, 704, 768], index=2)
infer_steps = st.slider("Pasos de inferencia", min_value=1, max_value=50, value=20)
fps = st.slider("FPS", min_value=1, max_value=30, value=8)

if st.button("Generar video"):
    with st.spinner("Generando video... (puede tardar 1-5 minutos)"):
        try:
            output = replicate.run(
                "tencent/hunyuan-video:6c9132aee14409cd6568d030453f1ba50f5f3412b844fe67f78a9eb62d55664f",
                input={
                    "prompt": prompt,
                    "video_length": video_length,
                    "width": width,
                    "height": height,
                    "infer_steps": infer_steps,
                    "fps": fps,
                }
            )
            if isinstance(output, list):
                video_url = output[0]
            else:
                video_url = output
            st.video(video_url)
            st.success("¡Video generado!")
            st.markdown(f"[Descargar video]({video_url})")
        except Exception as e:
            st.error(f"Error: {e}")