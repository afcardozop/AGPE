import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="AGPE EBSA",
    page_icon="logo.png",
    layout="wide"
)

# GOOGLE SHEETS
sheet_id = "17Z_Yyx3m8AEVqE2Cdo8uUxhgDzGcH-Jjyiift4sKnYo"
gid = "1980430520"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# LEER DATOS
df = pd.read_csv(csv_url, dtype=str)
df.columns = df.columns.str.strip()

# LIMPIAR TEXTO
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# CONVERTIR COORDENADAS
df["LATITUD"] = df["LATITUD"].str.replace(",", ".", regex=False)
df["LONGITUD"] = df["LONGITUD"].str.replace(",", ".", regex=False)

df["LATITUD"] = pd.to_numeric(df["LATITUD"], errors="coerce")
df["LONGITUD"] = pd.to_numeric(df["LONGITUD"], errors="coerce")

# QUITAR FILAS SIN COORDENADAS
df = df.dropna(subset=["LATITUD", "LONGITUD"]).copy()

# ENCABEZADO
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo.png", width=100)

with col2:
    st.title("APP AGPE EBSA")
    st.write("Consulta de usuarios AGPE con mapa interactivo")

# BUSCADOR
busqueda = st.text_input("Buscar usuario:")

if busqueda:
    df = df[df["DESCRIPCION"].str.contains(busqueda, case=False, na=False)]

# FILTRO
municipios = sorted(df["MUNICIPIO"].dropna().unique())
municipio_sel = st.selectbox("Filtrar por municipio:", ["Todos"] + municipios)

if municipio_sel != "Todos":
    df = df[df["MUNICIPIO"] == municipio_sel]

st.write(f"Registros encontrados: {len(df)}")

if len(df) == 0:
    st.warning("No hay resultados para ese filtro.")
    st.stop()

# MAPA
lat_centro = df["LATITUD"].mean()
lon_centro = df["LONGITUD"].mean()

m = folium.Map(location=[lat_centro, lon_centro], zoom_start=8)

for _, fila in df.iterrows():
    popup_html = f"""
    <div style="width:300px; font-size:14px;">
        <h4>{fila.get('DESCRIPCION', '')}</h4>

        <b>Código AGPE:</b> {fila.get('CODIGO_AGPE', '')}<br>
        <b>Serial:</b> {fila.get('SERIAL', '')}<br>
        <b>Cuenta:</b> {fila.get('CUENTA', '')}<br>
        <b>Marca:</b> {fila.get('MARCA', '')}<br>
        <b>Municipio:</b> {fila.get('MUNICIPIO', '')}<br>
        <b>Latitud:</b> {fila.get('LATITUD', '')}<br>
        <b>Longitud:</b> {fila.get('LONGITUD', '')}<br>
        <b>Teléfono:</b> {fila.get('TELEFONO', '')}<br>
        <b>Email:</b> {fila.get('E_MAIL', fila.get('EMAIL', fila.get('E-MAIL', '')))}<br><br>

        <a href="{fila.get('URL_GOOGLE_MAPS', '')}" target="_blank"
           style="display:inline-block;
                  padding:8px 14px;
                  background:#0d6efd;
                  color:white;
                  text-decoration:none;
                  border-radius:8px;
                  font-weight:bold;">
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

st.subheader("Mapa")
st_folium(m, width=1200, height=600)

st.subheader("Listado")
for _, fila in df.iterrows():
    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(f"{fila.get('DESCRIPCION', '')} - {fila.get('MUNICIPIO', '')}")

    with col2:
        st.link_button("Ir", fila.get("URL_GOOGLE_MAPS", ""))
