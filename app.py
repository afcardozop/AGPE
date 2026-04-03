# Título
st.title("APP AGPE EBSA ⚡")

st.write("Listado de usuarios:")

# Filtro por municipio
municipios = df["MUNICIPIO"].dropna().unique()
municipio_sel = st.selectbox("Filtrar por municipio:", ["Todos"] + list(municipios))

if municipio_sel != "Todos":
    df = df[df["MUNICIPIO"] == municipio_sel]

# Mostrar datos
for i in range(len(df)):
    col1, col2 = st.columns([3,1])

    with col1:
        st.write(f"{df.iloc[i]['DESCRIPCION']} - {df.iloc[i]['MUNICIPIO']}")

    with col2:
        st.link_button("Ir", df.iloc[i]["URL_GOOGLE_MAPS"])
