import streamlit as st
from datetime import datetime
import os
from streamlit_extras.switch_page_button import switch_page
from utils import doc_loader, summary_prompt_creator, doc_to_final_summary, validate_doc_size
from my_prompts import file_map, file_combine
from streamlit_app_utils import check_gpt_4, check_key_validity, create_temp_file, create_chat_model, load_pdf_from_github
from pathlib import Path
from gtts import gTTS
import base64


header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

# Function to convert text to speech and save it as an mp3 file
def text_to_speech(text, lang='nl'):
    tts = gTTS(text=text, lang=lang)
    tts.save("text.mp3")

# Function to embed the audio in the Streamlit app
def audio_player(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f"""
            <audio controls autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            Your browser does not support the audio element.
            </audio>
            """, unsafe_allow_html=True)
def record_page_start_time():
    global page_start_time
    page_start_time = datetime.now()

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

        # Audios
    text = """Je ziet nu het hulpmiddel voor samenvatten. Klik op de knop "Samenvatten" en lees de tekst goed door.\
                 Probeer daarna alle vragen goed te beantwoorden.
        """
        # Add a button with a speaker icon
        
    if st.button("🔊",key="button6"):
            text_to_speech(text)
            audio_player("text.mp3")

        # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
            os.remove("text.mp3")
        # Text to be read aloud

        # Display the text
        #st.write(text)

    st.markdown('''Je ziet nu het hulpmiddel voor samenvatten. :orange-background[🖱 **Klik op de knop "Samenvatten"**] en lees de tekst goed door.\
                 Probeer daarna alle vragen goed te beantwoorden.''')
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image('https://i.pinimg.com/564x/1f/12/6d/1f126d5cf25d9a942f5af9debe1eab4a.jpg', width=200)


    use_gpt_4 = True
    find_clusters = False
    
    # api_key = st.text_input("Voer je API-sleutel in:", type='password')

    # if st.button('Dien API-sleutel in'):
    #     if api_key:
    #         st.session_state['api_key'] = api_key
    #         st.success("API-sleutel succesvol ingediend!")
    #     else:
    #         st.error("Voer een geldige API-sleutel in.")

    # if st.button('Samenvatten (klik eenmaal en wacht)', key='summarize_button'):
    #     if st.session_state['uploaded_file'] is not None:
    #         process_summarize_button(st.session_state['uploaded_file'], api_key, use_gpt_4, find_clusters)
    #         st.write('Als je niet tevreden bent met de samenvatting, kun je opnieuw samenvatten.')
    #     else:
    #         st.warning('Upload je bestand alstublieft.')
    if st.button('Samenvatten (klik eenmaal en wacht)', key='summarize_button'):
        if st.session_state['topic'] == 'Financial': 
            st.markdown('''
                        📩 Afzender: 
                        
                            🏛️ Gemeente Eindhoven
                        
                        🎯 Doel: 
                            
                            Belastingaanslag uitleggen
                        
                        🔑 Actiepunten:
                            
                            💸 Betaal €269,72
                        
                            📅 Voor 31-03-2024
                        
                            🖥️ Betaal online
                        
                            📆 10 termijnen mogelijk
                        
                            📨 Maak bezwaar mogelijk
                        
                        📞 Contactinformatie:
                            
                            📞 14 040
                            📝 Online contactformulier
                        
                        📢 Voor vragen, bezoek :blue[www.eindhoven.nl/contact-belastingen]''')

        else: 
            st.markdown('''
                        📩 Afzender: 
                        
                            RIVM

                        🎯 Doel: 
                        
                            Coronaprik voor kinderen

                        🔑 Actiepunten:
                            💉 Informatie coronaprik
                        
                            🧒 Kinderen vanaf 5 jaar
                        
                            📄 Maak afspraak
                        
                            📞 Bel 0800 7070
                        
                            🆔 Neem ID en brief
                        
                        📞 Contactinformatie:
                            0800 7070 (gratis)
                        
                        📢 Voor vragen, Als je vragen hebt, bezoek :blue[www.coronavaccinatie.nl.]''')
            
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
    if st.session_state['topic'] == 'Health':
        with st.form("health_form"):
            st.markdown('**Leesbegrip**')
            st.markdown("Selecteer het juiste antwoord op de onderstaande meerkeuzevragen. \
                        Een goed antwoord krijgt +1 punt, een fout antwoord -1 punt en de \"Ik weet het niet\" 0 punten")

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
                "C) Advies over schoolbezoeken ",
                "D) Registratie voor een sportevenement",
                "E) Ik weet het niet"], index=4)
            
            question3 = st.radio(
                "Welke actie moet als eerste worden ondernomen om een afspraak te maken?",
                ["A) Bel de huisarts",
                "B) Zoek het BSN van je kind ",
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
            # st.write("question 1", q1)
            st.session_state.oocsi.send('Tool_answer', {
                'participant_ID': st.session_state.name,
                'topic': st.session_state['topic'],
                'q1': question1,
                'q2': question2,
                'q3': question3,
                'q4': question4,
                'q5': question5,
                'q6': question6,
                })
            switch_page("evaluation_tool")

# Financial Letter questions:
    elif st.session_state['topic'] == 'Financial':
        with st.form("financial_form"):
            st.markdown('**Leesbegrip**')
            st.markdown("Selecteer het juiste antwoord op de onderstaande meerkeuzevragen. \
                        Een goed antwoord krijgt +1 punt, een fout antwoord -1 punt en de \"Ik weet het niet\" 0 punten")

            question1 = st.radio(
                "Van welke organisatie is deze brief?",
                ["A) Gemeente Amsterdam",
                "B) Gemeente Rotterdam",
                "C) Gemeente Utrecht",
                "D) Gemeente Eindhoven",
                "E) Ik weet het niet"], index=4)
            
            question2 = st.radio(
                "Wat is het totaalbedrag van de aanslag?",
                ["A) €150,50",
                "B) €200,20",
                "C) €269,72 ",
                "D) €300,30",
                "E) Ik weet het niet"], index=4)
            
            question3 = st.radio(
                "Wat is de vervaldatum voor de betaling?",
                ["A) 15-02-2024",
                "B) 22-02-2024",
                "C) 31-03-2024",
                "D) 01-04-2024",
                "E) Ik weet het niet"], index=4)

            question4 = st.radio(
                "Hoeveel termijnen kun je kiezen om in te betalen via automatische afschrijving?",
                ["A) 5 termijnen",
                "B) 8 termijnen",
                "C) 10 termijnen",
                "D) 12 termijnen",
                "E) Ik weet het niet"], index=4)
            
            question5 = st.radio(
                "Waar kun je contact opnemen voor meer informatie of bezwaar maken?",
                ["A) www.amsterdam.nl/contact-belastingen",
                "B) www.rotterdam.nl/contact-belastingen",
                "C) www.utrecht.nl/contact-belastingen",
                "D) www.eindhoven.nl/contact-belastingen",
                "E) Ik weet het niet"], index=4)
            
            question6 = st.radio(
                "Welke is de juiste contactinformatie?",
                ["A) 14 020",
                "B) 14 040",
                "C) 14 030",
                "D) 14 050",
                "E) Ik weet het niet"], index=4)
            
            submitted = st.form_submit_button("Indienen")
            if submitted:
                if 'page_start_time' in st.session_state:
                    record_page_duration_and_send()    
                st.session_state.oocsi.send('Baseline_text_question', {
                    'participant_ID': st.session_state.name,
                    'topic': st.session_state['topic'],
                    'q1': question1,
                    'q2': question2,
                    'q3': question3,
                    'q4': question4,
                    'q5': question5,
                    'q6': question6,
                    })
                url_directory = "https://raw.githubusercontent.com/engrobelf/low_literacy/main/letters"
                input_method = 'Health'
                selected_pdf = os.path.join(url_directory, input_method + '.pdf')
                selected_pdf = selected_pdf.replace('\\', '/')
                st.session_state['uploaded_file'] = selected_pdf
                st.session_state['topic'] = 'Health'
                switch_page("Baseline")
