import streamlit as st
from home import home_page
from settings import settings_page

st.set_page_config(page_title='Analizador de Riesgos', page_icon=':shield:')

# Sidebar with icons
st.sidebar.header("Navegación")
page = st.sidebar.radio(
    "Selecciona una página:",
    ["Home", "AI Settings"],
    index=0,
    format_func=lambda x: f"{'🏠 Home' if x == 'Home' else '⚙️ AI Settings'}"
)

if page == "Home":
    home_page()
elif page == "AI Settings":
    settings_page()
