import streamlit as st
import pandas as pd
import io
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --------------------------
# Google Sheets setup
# --------------------------
SHEET_NAME = "YOUR_SHEET_NAME"  # Replace with your Google Sheet name

def save_to_google_sheet(responses, questions, participant_info):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(SHEET_NAME).sheet1
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for i, answer in responses.items():
        rows.append([
            timestamp,
            participant_info["number"],
            participant_info["name"],
            i,
            questions[i - 1] if i - 1 < len(questions) else "",
            answer
        ])
    sheet.append_rows(rows)
    st.success(f"✅ Réponses sauvegardées dans Google Sheet: {SHEET_NAME}")

def generate_csv(responses, questions, participant_info, filename):
    rows = []
    for i, answer in responses.items():
        rows.append([
            participant_info["number"],
            participant_info["name"],
            i,
            questions[i - 1] if i - 1 < len(questions) else "",
            answer
        ])
    df = pd.DataFrame(rows, columns=["ID", "Name", "Q#", "Question", "Answer"])
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, sep=";")
    csv_bytes = csv_buffer.getvalue().encode('utf-8')

    st.download_button(
        label="Télécharger vos réponses CSV",
        data=csv_bytes,
        file_name=f"{filename}_{participant_info['number']}.csv",
        mime="text/csv"
    )

# --------------------------
# Questionnaire data
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
# Streamlit UI
# --------------------------
st.title("Questionnaire sur les rêves lucides")

# Participant info
st.header("Informations du participant")
participant_number = st.text_input("Numéro du participant")
participant_name = st.text_input("Nom")

if not participant_number or not participant_name:
    st.warning("Veuillez remplir les informations pour continuer.")
    st.stop()

participant_info = {"number": participant_number, "name": participant_name}

st.divider()

# Short questionnaire
st.header("Questionnaire court (7 questions)")
st.write(instructions_lucid)

responses_short = {}
stop_after_q1 = False

for i, question in enumerate(lucid_questions, 1):
    st.subheader(question)
    options = lucid_options[i - 1]

    if options == "text":
        answer = st.text_input(f"Réponse :", key=f"short_text_{i}")
    else:
        answer = st.radio("Choisissez :", options, key=f"short_radio_{i}")

    responses_short[i] = answer

    if i == 1 and answer == "Non":
        st.info("Vous n'avez jamais fait de rêve lucide : passage direct au questionnaire suivant.")
        stop_after_q1 = True
        break

if st.button("Enregistrer questionnaire court"):
    if stop_after_q1:
        responses_short = {1: responses_short[1]}
    save_to_google_sheet(responses_short, lucid_questions, participant_info)
    generate_csv(responses_short, lucid_questions, participant_info, "lucid_frequency")

st.divider()

# Long questionnaire
st.header("Questionnaire long (28 questions)")

responses_long = {}

for i, question in enumerate(questions_28, 1):
    st.subheader(question)

    if i <= len(additional_options):
        answer = st.radio("Choisissez :", additional_options[i - 1], key=f"long_add_{i}")
    else:
        answer = st.radio("Choisissez :", options_6, key=f"long_q{i}")

    responses_long[i] = answer

if st.button("Enregistrer questionnaire long"):
    save_to_google_sheet(responses_long, questions_28, participant_info)
    generate_csv(responses_long, questions_28, participant_info, "luciddreams")
