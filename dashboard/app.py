import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="GetAround - Delay Analysis", layout="wide")

st.title("🚗 GetAround : Optimisation des délais entre locations")

# Chargement des données
@st.cache_data
def load_data():
    # On précise le séparateur ';' pour correspondre à ton fichier
    df = pd.read_csv("rental_data.csv", sep=";")
    return df

try:
    df = load_data()

    # --- SIDEBAR ---
    st.sidebar.header("Paramètres de simulation")
    threshold = st.sidebar.slider("Seuil de sécurité (minutes)", 0, 120, 60, step=15)
    
    # --- ANALYSE DES RETARDS ---
    st.header("1. Analyse globale des retards")
    
    # Calcul du taux de retard
    late_count = len(df[df['delay_at_checkout_in_minutes'] > 0])
    late_rate = late_count / len(df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Taux de retard global", f"{late_rate:.1%}")
    with col2:
        st.metric("Retard moyen (minutes)", f"{df['delay_at_checkout_in_minutes'].mean():.1f}")

    # Graphique de distribution
    fig_dist = px.histogram(df, x="delay_at_checkout_in_minutes", 
                            title="Distribution des retards au checkout",
                            nbins=100, range_x=[-60, 300])
    st.plotly_chart(fig_dist, use_container_width=True)

    # --- SIMULATION D'IMPACT ---
    st.header(f"2. Simulation avec un seuil de {threshold} min")
    
    # On identifie les locations consécutives (dos-à-dos)
    consecutive = df[df['previous_ended_rental_id'].notna()].copy()
    
    # Une collision arrive si le retard précédent > temps entre les deux locations
    collisions_initial = consecutive[consecutive['delay_at_checkout_in_minutes'] > consecutive['time_delta_with_previous_rental_in_minutes']]
    
    # Avec le seuil, on regarde combien de ces collisions disparaitraient
    # (Si le retard est inférieur ou égal au nouveau seuil)
    solved = collisions_initial[collisions_initial['delay_at_checkout_in_minutes'] <= threshold]
    
    c1, c2 = st.columns(2)
    with c1:
        st.error(f"Collisions identifiées : {len(collisions_initial)}")
    with c2:
        st.success(f"Collisions résolues par le seuil : {len(solved)}")

    st.info(f"En tant que mentor, je note qu'un seuil de {threshold} min résoudrait {(len(solved)/len(collisions_initial)*100):.1%}" if len(collisions_initial) > 0 else "Aucune collision détectée.")

except FileNotFoundError:
    st.error("Erreur : Le fichier 'rentals_data.csv' est introuvable dans le dossier dashboard.")