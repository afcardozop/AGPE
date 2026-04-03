import streamlit as st
import pandas as pd

# Leer archivo CSV
df = pd.read_csv("AGPE_LIMPIO.csv")

# Título
st.title("APP AGPE EBSA")

st.write("Listado de usuarios:")

# Buscador
busqueda = st.text_input("Buscar usuario:")

if busqueda:
    df = df[df["DESCRIPCION"].astype(str).str.contains(busqueda, case=False, na=False)]

# Filtro por municipio
municipios = sorted(df["MUNICIPIO"].dropna().astype(str).unique())
municipio_sel = st.selectbox("Filtrar por municipio:", ["Todos"] + municipios)

if municipio_sel != "Todos":
    df = df[df["MUNICIPIO"].astype(str) == municipio_sel]

# Mostrar datos
for i in range(len(df)):
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"{df.iloc[i]['DESCRIPCION']} - {df.iloc[i]['MUNICIPIO']}")

    with col2:
        st.link_button("Ir", df.iloc[i]["URL_GOOGLE_MAPS"])
