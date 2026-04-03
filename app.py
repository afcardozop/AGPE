import streamlit as st
import pandas as pd

st.set_page_config(page_title="APP AGPE EBSA", layout="wide")

# Leer archivo
df = pd.read_csv("AGPE_LIMPIO.csv")

# Asegurar nombres y tipos
df["DESCRIPCION"] = df["DESCRIPCION"].astype(str)
df["MUNICIPIO"] = df["MUNICIPIO"].astype(str)
df["LATITUD"] = pd.to_numeric(df["LATITUD"], errors="coerce")
df["LONGITUD"] = pd.to_numeric(df["LONGITUD"], errors="coerce")

# Quitar filas sin coordenadas válidas
df = df.dropna(subset=["LATITUD", "LONGITUD"])

st.title("APP AGPE EBSA")
st.write("Consulta de usuarios AGPE con ubicación en mapa")

# Buscador
busqueda = st.text_input("Buscar usuario:")

if busqueda:
    df = df[df["DESCRIPCION"].str.contains(busqueda, case=False, na=False)]

# Filtro por municipio
municipios = sorted(df["MUNICIPIO"].dropna().unique())
municipio_sel = st.selectbox("Filtrar por municipio:", ["Todos"] + municipios)

if municipio_sel != "Todos":
    df = df[df["MUNICIPIO"] == municipio_sel]

st.subheader("Mapa de ubicaciones")

# Dataframe para mapa
mapa_df = df[["LATITUD", "LONGITUD"]].rename(
    columns={"LATITUD": "lat", "LONGITUD": "lon"}
)

st.map(mapa_df)

st.subheader("Listado de usuarios")

for i in range(len(df)):
    col1, col2 = st.columns([4, 1])

    with col1:
        st.write(f"{df.iloc[i]['DESCRIPCION']} - {df.iloc[i]['MUNICIPIO']}")

    with col2:
        st.link_button("Ir", df.iloc[i]["URL_GOOGLE_MAPS"])
