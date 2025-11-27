import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --------------------------
# Helper: save CSV results
# --------------------------
def save_csv(filename, participant_info, responses, questions):
    os.makedirs("results", exist_ok=True)
    path = f"results/{filename}_{participant_info['number']}.csv"

    rows = []
    for i, answer in responses.items():
        rows.append([
            participant_info["number"],
            participant_info["name"],
            i,
            answer,
            questions[i - 1]
        ])

    df = pd.DataFrame(rows, columns=["ID", "Name", "Q#", "Answer", "Question"])
    df.to_csv(path, index=False, sep=";")
    st.success(f"Saved: {path}")


# --------------------------
# Short questionnaire data
# --------------------------
instructions_lucid = (
    "Voici 7 questions concernant les rêves lucides.\n"
    "Un rêve lucide est un rêve pendant lequel tu sais que tu es en train de rêver."
)

lucid_questions = [
    "As-tu déjà fait un rêve lucide ?",
    "Combien au total ? (saisir un nombre)",
    "À quand remonte le dernier ?",
    "À quelle fréquence en fais-tu ?",
    "As-tu le contrôle dans ce rêve ?",
    "Contrôle général : comment le définirais-tu ?",
    "Contrôle des détails : comment le définirais-tu ?"
]

lucid_options = [
    ["Oui", "Non", "Je ne suis pas sûr(e)"],
    "text",
    ["La semaine passée", "Le mois passé", "Ces six derniers mois", "Cette dernière année", "Il y a plus d'un an", "Jamais"],
    ["Une fois par semaine", "Une fois par mois", "Toutes les deux semaines", "Tous les deux mois", "Tous les ans"],
    ["Parfois", "Toujours", "Jamais", "C'est arrivé une fois"],
    ["Très léger", "Léger", "Fort", "Très fort", "Pas de contrôle"],
    ["Très léger", "Léger", "Fort", "Très fort", "Pas de contrôle"]
]

lucid_final_message = "Merci pour votre participation !"

# --------------------------
# Long questionnaire data
# --------------------------
additional_questions = [
    "Q0 - A quand remonte le dernier rêve dont tu te souviens ?",
    "Q00 - Était-ce un rêve lucide ou normal ?"
]

additional_options = [
    ["Hier soir", "Cette semaine", "Ce mois-ci", "Cette année", "Je ne m'en souviens plus"],
    ["Rêve lucide", "Rêve normal"]
]

options_6 = [
    "Pas du tout d'accord",
    "Plutôt pas d'accord",
    "Légèrement pas d'accord",
    "Légèrement d'accord",
    "Plutôt d'accord",
    "Entièrement d'accord"
]

questions_28 = additional_questions + [
    "Q1 - Conscience que les choses du rêve n’étaient pas réelles.",
    "Q2 - Souvenir de mon intention.",
    "Q3 - Conscience du moi du rêve vs moi éveillé.",
    "Q4 - Manipuler des personnages impossible éveillé.",
    "Q5 - Penser aux personnages.",
    "Q6 - Actions surnaturelles.",
    "Q7 - Émotions identiques à éveillé.",
    "Q8 - Conscience du corps.",
    "Q9 - Certitude d'absence de conséquences.",
    "Q10 - Contrôle de l’environnement.",
    "Q11 - Me voir de l’extérieur.",
    "Q12 - Penser à mes actions.",
    "Q13 - Impression d’oubli.",
    "Q14 - Changer objets impossible éveillé.",
    "Q15 - Être une autre personne.",
    "Q16 - Se demander si je rêve.",
    "Q17 - Pensées identiques éveillé.",
    "Q18 - Souvenir de ma vie réelle.",
    "Q19 - Conscience que personnages irréels.",
    "Q20 - Les choses pourraient arriver réalité.",
    "Q21 - Voir le rêve comme un écran.",
    "Q22 - Penser aux choses du rêve.",
    "Q23 - Influencer l’histoire.",
    "Q24 - Établir des plans.",
    "Q25 - Euphorie.",
    "Q26 - Fortes émotions négatives.",
    "Q27 - Fortes émotions positives.",
    "Q28 - Forte anxiété."
]

# --------------------------
# STREAMLIT UI
# --------------------------

st.title("Questionnaire sur les rêves lucides")

# --------------------------
# Participant info
# --------------------------
st.header("Informations du participant")
participant_number = st.text_input("Numéro du participant")
participant_name = st.text_input("Nom")

if not participant_number or not participant_name:
    st.warning("Merci de remplir les informations pour commencer.")
    st.stop()

participant_info = {"number": participant_number, "name": participant_name}

st.divider()

# --------------------------
# SHORT questionnaire
# --------------------------
st.header("Questionnaire court (7 questions)")
st.write(instructions_lucid)

responses_short = {}
for i, question in enumerate(lucid_questions, 1):
    st.subheader(question)
    options = lucid_options[i - 1]

    if options == "text":
        answer = st.text_input(f"Réponse pour Q{i}", key=f"short_text_{i}")
    else:
        answer = st.radio("Choisissez :", options, key=f"short_radio_{i}")

    responses_short[i] = answer

    # If Q1 == "Non" → stop
    if i == 1 and answer == "Non":
        st.info("Vous n'avez jamais fait de rêve lucide : passage direct au questionnaire suivant.")
        break

if st.button("Enregistrer questionnaire court"):
    save_csv("lucid_frequency", participant_info, responses_short, lucid_questions)
    st.success("Questionnaire court enregistré !")

st.divider()

# --------------------------
# LONG questionnaire
# --------------------------
st.header("Questionnaire long (28 questions)")

responses_long = {}

for i, question in enumerate(questions_28, 1):
    st.subheader(question)

    if i <= len(additional_options):
        options = additional_options[i - 1]
        answer = st.radio("Choisissez :", options, key=f"long_add_{i}")
    else:
        answer = st.radio("Choisissez :", options_6, key=f"long_q{i}")

    responses_long[i] = answer

if st.button("Enregistrer questionnaire long"):
    save_csv("luciddreams", participant_info, responses_long, questions_28)
    st.success("Questionnaire long enregistré !")
