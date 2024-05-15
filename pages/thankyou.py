import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
from oocsi_source import OOCSI
# import datetime

header1, header2, header3 = st.columns([1,2,1])
body1, body2, body3 = st.columns([1,2,1])

with header2:
    st.balloons()
    st.title("Bedankt voor het invullen van deze enquête.\n We gaan nu een semi-gestructureerd interview over het experiment afnemen")
