import streamlit as st
from Bio import Entrez
import openai
import urllib.parse

# Configurer l'API OpenAI
openai.api_key = "sk-5R_cChuz2kt1kbrEUxDw4s4mcdFbg8oY269CPslgnFT3BlbkFJuc-RtFfyIp-4h6zZ3mO1NG5SL0r_GYOsr7drXkqYkA"

# Configurer l'API NCBI (PubMed)
Entrez.email = "nesrinebenamor518@gmail.com"
Entrez.api_key = "e9b86dbdeea24408a2ff5f7ec86eedb24e09"

# Fonction pour rechercher des articles sur PubMed
def search_pubmed(query):
    try:
        # Échapper la requête pour éviter les problèmes de caractères spéciaux
        escaped_query = urllib.parse.quote(query)
        st.write(f"Requête PubMed : {escaped_query}")  # Afficher la requête pour débogage
        
        # Vérification de la longueur de la requête
        if len(escaped_query) < 1 or len(escaped_query) > 200:
            raise ValueError("La requête doit être entre 1 et 200 caractères.")

        handle = Entrez.esearch(db="pubmed", term=escaped_query, retmax=10)
        record = Entrez.read(handle)
        handle.close()
        return record["IdList"]
    except Exception as e:
        st.error(f"Erreur lors de la recherche dans PubMed : {e}")
        return []

# Fonction pour obtenir les détails des articles
def fetch_article_details(id_list):
    try:
        ids = ",".join(id_list)
        handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="text")
        records = handle.read()
        handle.close()
        return records
    except Exception as e:
        st.error(f"Erreur lors de la récupération des articles : {e}")
        return ""

# Fonction pour générer une réponse contextuelle avec GPT
def generate_contextual_answer(query, articles):
    prompt = f"Question : {query}\n\nVoici des extraits d'articles médicaux pertinents :\n{articles}\n\nÀ partir des informations ci-dessus, répondez à la question de manière concise :"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Vous pouvez aussi utiliser GPT-4 si disponible
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Erreur lors de la génération de la réponse : {e}")
        return ""

# Interface Streamlit
st.title("Moteur de Recherche Médicale")
st.write("Posez des questions spécifiques et obtenez des réponses à partir d'articles scientifiques.")

# Entrée de la question médicale
query = st.text_input("Entrez votre question médicale", key="question_input")

if query:
    st.write(f"Recherche en cours pour : {query}")
    
    # Rechercher des articles sur PubMed
    id_list = search_pubmed(query)
    
    if id_list:
        st.write("Articles trouvés :")
        # Récupérer les détails des articles
        articles = fetch_article_details(id_list)
        st.text(articles)  # Affichage des articles bruts
        
        # Générer une réponse contextuelle avec OpenAI
        generated_answer = generate_contextual_answer(query, articles)
        st.write(f"Réponse contextuelle : {generated_answer}")
    else:
        st.write("Aucun article trouvé.")
