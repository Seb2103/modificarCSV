import pandas as pd
import streamlit as st
import gdown
import os

st.set_page_config(page_title="Modificador Artículo desde Drive", layout="centered")
st.title("🌐 Modificador de Artículo (SKU) desde Google Drive")

st.write("""
1. Sube tu archivo CSV a Google Drive.  
2. Comparte el archivo como **'Cualquiera con el enlace' puede ver**.  
3. Pega aquí el enlace para modificar la columna **Artículo** (añadir un `0` al inicio).
""")

url = st.text_input("🔗 Pega el enlace de Google Drive aquí")

if url:
    try:
        # Obtener ID del enlace
        if "id=" in url:
            file_id = url.split("id=")[1]
        elif "/d/" in url:
            file_id = url.split("/d/")[1].split("/")[0]
        else:
            st.error("❌ Enlace inválido. Asegúrate de copiar bien el enlace.")
            st.stop()

        download_url = f"https://drive.google.com/uc?id={file_id}"
        output_file = "archivo_descargado.csv"

        # Descargar archivo desde Drive
        gdown.download(download_url, output_file, quiet=False)

        # Leer CSV descargado
        df = pd.read_csv(output_file, sep=';', encoding='utf-8', dtype=str)

        if 'Artículo' not in df.columns:
            st.error("❌ La columna 'Artículo' no fue encontrada en el archivo.")
        else:
            df['Artículo'] = '0' + df['Artículo'].str.strip()
            st.success("✅ Modificación completada.")

            st.subheader("Vista previa del archivo modificado")
            st.dataframe(df.head())

            csv_modificado = df.to_csv(index=False, sep=';', encoding='utf-8')
            st.download_button("📥 Descargar archivo modificado", data=csv_modificado, file_name="archivo_modificado.csv", mime="text/csv")

        # Borrar archivo descargado (opcional)
        os.remove(output_file)

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
