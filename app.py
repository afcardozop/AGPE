import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="APP AGPE EBSA", layout="wide")

# Leer archivo
df = pd.read_csv("AGPE_LIMPIO.csv")

# Limpiar tipos
df["DESCRIPCION"] = df["DESCRIPCION"].astype(str)
df["MUNICIPIO"] = df["MUNICIPIO"].astype(str)
df["LATITUD"] = pd.to_numeric(df["LATITUD"], errors="coerce")
df["LONGITUD"] = pd.to_numeric(df["LONGITUD"], errors="coerce")
df["URL_GOOGLE_MAPS"] = df["URL_GOOGLE_MAPS"].astype(str)

# Quitar filas sin coordenadas
df = df.dropna(subset=["LATITUD", "LONGITUD"]).copy()

st.title("APP AGPE EBSA")
st.write("Consulta de usuarios AGPE con mapa interactivo")

# Buscador
busqueda = st.text_input("Buscar usuario:")

if busqueda:
    df = df[df["DESCRIPCION"].str.contains(busqueda, case=False, na=False)]

# Filtro por municipio
municipios = sorted(df["MUNICIPIO"].dropna().unique())
municipio_sel = st.selectbox("Filtrar por municipio:", ["Todos"] + municipios)

if municipio_sel != "Todos":
    df = df[df["MUNICIPIO"] == municipio_sel]

st.write(f"Registros encontrados: {len(df)}")

if len(df) == 0:
    st.warning("No hay resultados para ese filtro.")
    st.stop()

# Centro del mapa
lat_centro = df["LATITUD"].mean()
lon_centro = df["LONGITUD"].mean()

m = folium.Map(location=[lat_centro, lon_centro], zoom_start=8)

# Marcadores con atributos + botón Ir
for _, fila in df.iterrows():
    popup_html = f"""
    <div style="width:260px;">
        <b>{fila['DESCRIPCION']}</b><br>
        <b>Municipio:</b> {fila['MUNICIPIO']}<br>
        <b>Latitud:</b> {fila['LATITUD']}<br>
        <b>Longitud:</b> {fila['LONGITUD']}<br><br>
        <a href="{fila['URL_GOOGLE_MAPS']}" target="_blank"
           style="display:inline-block;padding:8px 12px;background:#1f77b4;color:white;
                  text-decoration:none;border-radius:6px;">
           Ir
        </a>
    </div>
    """

    folium.Marker(
        location=[fila["LATITUD"], fila["LONGITUD"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=fila["DESCRIPCION"]
    ).add_to(m)

st.subheader("Mapa")
st_folium(m, width="100%", height=550)

st.subheader("Listado")
for _, fila in df.iterrows():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"{fila['DESCRIPCION']} - {fila['MUNICIPIO']}")
    with col2:
        st.link_button("Ir", fila["URL_GOOGLE_MAPS"])
