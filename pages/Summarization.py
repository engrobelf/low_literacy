import streamlit as st
from uuid import uuid4
from streamlit_extras.switch_page_button import switch_page
import random
import pandas as pd
import datetime
import xgboost as xgb
import copy
import os
from PIL import Image
from datetime import datetime
import numpy as np
from utils import doc_loader, summary_prompt_creator, doc_to_final_summary, validate_doc_size
from streamlit_app_utils import check_gpt_4, check_key_validity, create_temp_file, create_chat_model, load_pdf_from_github


header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

def record_page_start_time():
    st.session_state['page_start_time'] = datetime.now()

def record_page_duration_and_send():
    if 'page_start_time' in st.session_state:
        page_duration = datetime.now() - st.session_state['page_start_time']
        st.session_state.oocsi.send('Time_XAI', {
            "page_name": "Baseline - Geen tool",
            "duration_seconds": page_duration.total_seconds(),
            "participant_ID": st.session_state.name
        })

def validate_input(file_or_transcript, api_key, use_gpt_4):
    if file_or_transcript is None:
        st.warning("Upload een bestand of voer een YouTube-URL in.")
        return False
    if not check_key_validity(api_key):
        st.warning('Sleutel niet geldig of API is niet bereikbaar.')
        return False
    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Sleutel niet geldig voor GPT-4.')
        return False
    return True

def process_summarize_button(url, api_key, use_gpt_4, find_clusters):
    if not check_key_validity(api_key):
        st.warning("Ongeldige API-sleutel of GPT-toegang geweigerd.")
        return

    with st.spinner("Samenvatten... even geduld..."):
        temp_file_path = create_temp_file(url)
        try:
            doc = doc_loader(temp_file_path)
            map_prompt = file_map
            combine_prompt = file_combine
            llm = create_chat_model(api_key, use_gpt_4)
            initial_prompt_list = summary_prompt_creator(map_prompt, 'text', llm)
            final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key, use_gpt_4)
            st.markdown(summary, unsafe_allow_html=True)
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

record_page_start_time()

with header2:
    st.title("Samenvatting")

with body2:
    st.header('Uitleg experiment')
    st.markdown('''Om te worden aangepast: In dit experiment laten we je vier verschillende profielen van passagiers zien.
    Met behulp van Machine Learning (ML) laten we een voorspelling zien of ze de ramp zouden hebben overleefd.
    Deze voorspelling gaat telkens vergezeld van een ander type uitleg.''')
    st.image('https://github.com/engrobelf/low_literacy/blob/francois/picture/LL_pic.png?raw=True', width=700, caption='Overzicht laaggeletterdheid')

    st.subheader('Model')
    st.markdown('''Hetzelfde ML-model wordt gebruikt om de voorspellingen te genereren van wie heeft overleefd en wie niet.
                Dit model wordt gebruikt om alle vier de typen uitleg te genereren die je tijdens het experiment zult zien.''')
    use_gpt_4 = True
    find_clusters = False

    api_key = st.text_input("Voer je API-sleutel in:", type='password')

    if st.button('Dien API-sleutel in'):
        if api_key:
            st.session_state['api_key'] = api_key
            st.success("API-sleutel succesvol ingediend!")
        else:
            st.error("Voer een geldige API-sleutel in.")

    if st.button('Samenvatten (klik eenmaal en wacht)', key='summarize_button'):
        if st.session_state['uploaded_file'] is not None:
            process_summarize_button(st.session_state['uploaded_file'], api_key, use_gpt_4, find_clusters)
            st.write('Als je niet tevreden bent met de samenvatting, kun je opnieuw samenvatten.')
        else:
            st.warning('Upload je bestand alstublieft.')

st.sidebar.markdown('# Gemaakt door: [François en Sichen](https://github.com/engrobelf)')
st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/engrobelf/low_literacy.git)')
st.sidebar.markdown("""<small>Het is altijd goed om te controleren of een website veilig is voordat je je API-sleutel invoert.
                    Deze site is open source, dus je kunt de code zelf controleren of de streamlit-app lokaal draaien.</small>""", unsafe_allow_html=True)

def validate_input(file_or_transcript, api_key, use_gpt_4):
    if file_or_transcript == None:
        st.warning("Upload een bestand of voer een YouTube-URL in.")
        return False

    if not check_key_validity(api_key):
        st.warning('Sleutel niet geldig of API is niet bereikbaar.')
        return False

    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Sleutel niet geldig voor GPT-4.')
        return False

    return True

with body2:
    with st.form("my_form"):
        st.markdown('**AI-geletterdheid**')
        st.markdown("Selecteer de juiste antwoorden op de meerkeuzevragen hieronder. \
                    Een correct antwoord levert +1 punt op, een incorrect antwoord -1 punt en de optie 'Ik weet het niet' 0 punten.")

        question1 = st.radio(
            "Van welke organisatie is deze brief?",
            ["A) Gezondheidsraad",
            "B) RIVM",
            "C) Ministerie van Volksgezondheid",
            "D) Gemeentehuis",
            "E) Ik weet het niet"], index=4)

        question2 = st.radio(
            "Wat is het hoofddoel van deze brief?",
            ["A) Uitnodiging voor een feest",
            "B) Informatie over een coronaprik voor kinderen",
            "C) Advies over schoolbezoeken",
            "D) Registratie voor een sportevenement",
            "E) Ik weet het niet"], index=4)

        question3 = st.radio(
            "Welke actie moet als eerste worden ondernomen om een afspraak te maken?",
            ["A) Bel de huisarts",
            "B) Zoek het BSN van je kind",
            "C) Bezoek de lokale kliniek",
            "D) Schrijf je in op een website",
            "E) Ik weet het niet"], index=4)

        question4 = st.radio(
            "Op welk nummer moet je bellen om een vaccinatieafspraak te maken?",
            ["A) 0800 7070",
            "B) 112",
            "C) 0800 1234",
            "D) 0900 2020",
            "E) Ik weet het niet"], index=4)

        question5 = st.radio(
            "Wat is een vereiste om mee te nemen naar de vaccinatieafspraak?",
            ["A) Een waterfles",
            "B) Een pasfoto",
            "C) De uitnodigingsbrief en een ID",
            "D) Een medische geschiedenisrapport",
            "E) Ik weet het niet"], index=4)

        question6 = st.radio(
            "Waar kun je meer informatie vinden over de coronavaccinatie voor kinderen?",
            ["A) www.gezondheid.nl",
            "B) www.rivm.nl",
            "C) www.coronavaccinatie.nl",
            "D) www.kinderzorg.nl",
            "E) Ik weet het niet"], index=4)

        submitted = st.form_submit_button("Indienen")
    if submitted:
        if 'page_start_time' in st.session_state:
            record_page_duration_and_send()
        st.session_state.oocsi.send('Tool_answer', {
            'participant_ID': st.session_state.name,
            'q1': question1,
            'q2': question2,
            'q3': question3,
            'q4': question4,
            'q5': question5,
            'q6': question6,
        })
        switch_page("evaluation_tool")

# if st.button("Volgende pagina"):
