import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración "Modo Pro"
st.set_page_config(page_title="Sparrow Cloud Pro", page_icon="🦅", layout="wide")

# Estilo Neón para tus párpados
st.markdown("""<style>
    .stApp { background-color: #0a0a0a; color: #00FF00; }
    h1, h2, h3 { color: #00FF00 !important; font-family: 'Courier New'; }
    </style>""", unsafe_allow_html=True)

# Login de Seguridad
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🦅 SPARROW CLOUD LOGIN")
    user = st.text_input("ID de Ingeniero")
    pw = st.text_input("Contraseña", type="password")
    if st.button("ENTRAR"):
        if user == "admin" and pw == "1234":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Acceso Denegado")
else:
    # Conexión a Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()

    st.title("📊 DASHBOARD SPARROW CLOUD")
    
    # Formulario de Registro
    with st.expander("📝 REGISTRAR NUEVO EQUIPO"):
        with st.form("nuevo_registro"):
            col1, col2, col3 = st.columns(3)
            cliente = col1.text_input("Cliente")
            modelo = col2.text_input("Modelo")
            imei = col3.text_input("IMEI")
            costo = col1.number_input("Costo", min_value=0.0)
            venta = col2.number_input("Venta", min_value=0.0)
            
            if st.form_submit_button("GUARDAR EN LA NUBE"):
                nueva_fila = pd.DataFrame([{
                    "ID": len(df) + 1,
                    "FECHA": datetime.now().strftime("%d/%m/%Y"),
                    "CLIENTE": cliente.upper(),
                    "MODELO": modelo.upper(),
                    "IMEI": imei,
                    "COSTO": costo,
                    "VENTA": venta
                }])
                df_final = pd.concat([df, nueva_fila], ignore_index=True)
                conn.update(data=df_final)
                st.success("✅ Sincronizado con Google Sheets")
                st.rerun()

    # Tabla y Ganancias
    st.subheader("📂 INVENTARIO GLOBAL")
    if not df.empty:
        df['GANANCIA'] = df['VENTA'] - df['COSTO']
        st.dataframe(df, use_container_width=True)
        st.metric("📈 GANANCIA NETA TOTAL", f"${df['GANANCIA'].sum():,.2f}")
    
    if st.button("CERRAR SESIÓN"):
        st.session_state.auth = False
        st.rerun()
