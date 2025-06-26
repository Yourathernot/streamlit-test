import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("""Это моя вторая страница""")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet="Спринт 24")

st.dataframe(df)
