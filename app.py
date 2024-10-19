import streamlit as st

st.title("Plateforme de Recherche Médicale")
question = st.text_input("Posez une question médicale")

if question:
    answer = generate_answer(question)
    st.write(f"Réponse : {answer}")

import requests

def search_pubmed(query):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json"
    response = requests.get(url)
    data = response.json()
    return data["esearchresult"]["idlist"]

if question:
    pubmed_ids = search_pubmed(question)
    st.write(f"Articles PubMed trouvés : {pubmed_ids}")
