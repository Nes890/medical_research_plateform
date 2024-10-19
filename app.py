import streamlit as st

st.title("Plateforme de Recherche Médicale")
question = st.text_input("Posez une question médicale")

if question:
    st.write(f"Vous avez posé la question : {question}")