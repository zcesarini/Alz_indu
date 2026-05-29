import streamlit as st
import requests
import os


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")




st.title("Prédiction précoce de la maladie d'Alzheimer")
st.write("Veuillez renseigner les caractéristiques du patient pour obtenir une estimation du risque.")


with st.expander("Scores cognitifs"):
    col1, col2 = st.columns(2)

    with col1:
        cdglobal = st.slider(
            "Stade globale des capacités cognitives (CDGLOBAL)",
            0, 3, 0,
            help="Mesure générale du fonctionnement cognitif. Un score élevé indique plus de difficultés."
        )

        cdrsb = st.slider(
            "Score de déclin cognitif sur 6 domaines(CDR-SB) ",
            0, 18, 0,
            help="Mesure la sévérité du déclin cognitif. Plus le score est élevé, plus le déclin est important."
        )

        cdmemory = st.slider(
            "Mémoire – capacité à se souvenir (CDMEMORY)",
            0, 3, 0,
            help="Évalue la mémoire immédiate et à court terme."
        )

        cdjudge = st.slider(
            "Capacité de jugement (CDJUDGE)",
            0, 3, 0,
            help="Évalue la capacité à prendre des décisions et résoudre des problèmes."
        )

        cdhome = st.slider(
            "Autonomie à domicile (CDHOME)",
            0, 3, 0,
            help="Évalue la capacité à gérer les activités quotidiennes à la maison."
        )

        cdcommun = st.slider(
            "Capacité de communication (CDCOMMUN)",
            0, 3, 0,
            help="Mesure la capacité à comprendre et à s’exprimer."
        )



    with col2:
        mmscore = st.slider(
            "Score MMSE (test cognitif standard)",
            0, 30, 29,
            help="Test de référence pour évaluer la mémoire, l’orientation et le raisonnement."
        )

        word2dl = st.slider(
            "Test de rappel de mots (WORD2DL)",
            0, 3, 0,
            help="Nombre de mots correctement rappelés après un délai."
        )
                
        totscore = st.slider(
            "Score cognitif total (TOTSCORE-ADAS11)",
            0, 70, 12,
            help="Score global regroupant plusieurs tests cognitifs : mémoire, langage, attention, capacités d’apprentissage, reconnaissance d’objets."
        )

        total13 = st.slider(
            "Score cognitif étendu (TOTAL13-ADAS13)",
            0, 85, 20,
            help="Version plus détaillée du score cognitif total : mémoire, langage, attention, apprentissage verbal, reconnaissance d’objets, orientation, compréhension, praxies."
        )



with st.expander("Signes vitaux et mesures"):
    col1, col2 = st.columns(2)

    with col1:
        vsweight = st.slider(
            "Poids (kg)",
            0, 200, 94,
            help="Poids du patient en kilogrammes."
        )

        vsheight = st.slider(
            "Taille (cm)",
            0, 250, 170,
            help="Taille du patient en centimètres."
        )

        
        vspulse = st.slider(
            "Fréquence cardiaque (battements/min)",
            0, 200, 64,
            help="Nombre de battements du cœur par minute."
        )

    with col2:
        vsbpsys = st.slider(
            "Tension artérielle systolique",
            50, 250, 150,
            help="Pression du sang lors de la contraction du cœur."
        )

        vsbpdia = st.slider(
            "Tension artérielle diastolique",
            30, 150, 64,
            help="Pression du sang entre deux battements."
        )


with st.expander("Mesures biologiques"):
    col1, col2 = st.columns(2)

    with col1:
        st112sv = st.slider(
            "Volume du putamen gauche ST112SV",
            0.0, 10000.0, 4184.10, step=0.1,
            help="Motricité, coordination, apprentissage procédural, habitudes, vitesse motrice."
        )

    with col2:
        st120sv = st.slider(
            "Mesure anatomique de l’hippocampe ST120SV",
            0, 10000, 6224,
            help="Mémoire épisodique, encodage des souvenirs, rappel différé."
        )

        st101sv = st.slider(
            "Volume de l’amygdale gauche ST101SV",
            0.0, 5000.0, 1819.45, step=0.1,
            help="Mémoire émotionnelle, reconnaissance des émotions, régulation affective, aspects du comportement social."
        )

        st125sv = st.slider(
            "Volume du thalamus gauche ST125SV",
            0.0, 100.0, 24.50, step=0.1,
            help="Attention, mémoire, perception, vitesse de traitement, coordination."
        )


st.markdown("---")

if st.button("Calculer la prédiction", type="primary"):
    payload = {
        "CDGLOBAL": cdglobal,
        "CDMEMORY": cdmemory,
        "CDRSB": cdrsb,
        "TOTSCORE": totscore,
        "TOTAL13": total13,
        "CDJUDGE": cdjudge,
        "MMSCORE": mmscore,
        "VSWEIGHT": vsweight,
        "VSPULSE": vspulse,
        "CDHOME": cdhome,
        "VSBPSYS": vsbpsys,
        "CDCOMMUN": cdcommun,
        "VSBPDIA": vsbpdia,
        "ST112SV": st112sv,
        "ST120SV": st120sv,
        "ST101SV": st101sv,
        "ST125SV": st125sv,
        "WORD2DL": word2dl,
        "VSHEIGHT":vsheight,
    }


    try:
        response = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=5)
        response.raise_for_status()
        prediction = response.json()["prediction"]
        proba = response.json()["probabilite"]

        # Interprétation du résultat
        if prediction == 0:
            st.success("🟢 Le patient est **sain**.")
            
        else:
            st.error("🔴 Le patient est **à risque**.")
        
        st.metric("Probabilité de risque", f"{proba:.2f} %")

    except requests.exceptions.ConnectionError:
        st.error("Impossible de contacter le serveur backend.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")


