import pandas as pd
import streamlit as st

st.set_page_config(page_title="Modificador DataBase NetSuite", layout="centered")

st.title("🛠️ Modificador de Artículo (SKU) en un CSV")

st.write("* Sube un archivo `.csv` con la columna SKU llamada **Artículo**.")
st.write("* Anadiré un `0` al inicio de cada valor en esa columna.")
         
archivo = st.file_uploader("📤 Sube tu archivo CSV aquí", type=["csv"])

if archivo:
    try:
        df = pd.read_csv(archivo, sep=';', encoding='utf-8', dtype=str)

        if 'Artículo' not in df.columns:
            st.error("❌ La columna 'Artículo' no fue encontrada en el archivo.")
        else:
            df['Artículo'] = '0' + df['Artículo'].str.strip()
            st.success("✅ Modificación completada.")

            st.subheader("Vista previa del archivo modificado")
            st.dataframe(df.head())

            csv_modificado = df.to_csv(index=False, sep=';', encoding='utf-8')
            st.download_button("📥 Descargar archivo modificado", data=csv_modificado, file_name="archivo_modificado.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
