import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# CONFIGURACIÓN (ICONO Y NOMBRE)
st.set_page_config(
    page_title="AGPE EBSA",
    page_icon="logo.png",
    layout="wide"
)

# Leer archivo
df = pd.read_csv("AGPE_LIMPIO.csv")

# Limpiar tipos
for col in df.columns:
    df[col] = df[col].astype(str)

df["LATITUD"] = pd.to_numeric(df["LATITUD"], errors="coerce")
df["LONGITUD"] = pd.to_numeric(df["LONGITUD"], errors="coerce")

# Quitar filas sin coordenadas
df = df.dropna(subset=["LATITUD", "LONGITUD"]).copy()

# Título
st.title("APP AGPE EBSA ⚡")
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

# Marcadores
for _, fila in df.iterrows():
    popup_html = f"""
    <div style="width:300px; font-size:14px;">
        <h4>{fila.get('DESCRIPCION','')}</h4>

        <b>Código AGPE:</b> {fila.get('CODIGO_AGPE','')}<br>
        <b>Serial:</b> {fila.get('SERIAL','')}<br>
        <b>Cuenta:</b> {fila.get('CUENTA','')}<br>
        <b>Marca:</b> {fila.get('MARCA','')}<br>
        <b>Municipio:</b> {fila.get('MUNICIPIO','')}<br>
        <b>Latitud:</b> {fila.get('LATITUD','')}<br>
        <b>Longitud:</b> {fila.get('LONGITUD','')}<br>
        <b>Teléfono:</b> {fila.get('TELEFONO','')}<br>
        <b>Email:</b> {fila.get('E_MAIL', fila.get('EMAIL',''))}<br><br>

        <a href="{fila.get('URL_GOOGLE_MAPS','')}" target="_blank"
           style="padding:8px 14px;background:#0d6efd;color:white;
           text-decoration:none;border-radius:8px;font-weight:bold;">
           Ir
        </a>
    </div>
    """

    folium.Marker(
        location=[fila["LATITUD"], fila["LONGITUD"]],
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=fila.get("DESCRIPCION", ""),
        icon=folium.Icon(color="green", icon="flash", prefix="glyphicon")
    ).add_to(m)

# Mostrar mapa
st.subheader("Mapa")
st_folium(m, width="100%", height=600)

# Listado
st.subheader("Listado")
for _, fila in df.iterrows():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"{fila.get('DESCRIPCION','')} - {fila.get('MUNICIPIO','')}")
    with col2:
        st.link_button("Ir", fila.get("URL_GOOGLE_MAPS",""))
