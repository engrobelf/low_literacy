
# import streamlit as st
# from uuid import uuid4
# from streamlit_extras.switch_page_button import switch_page
# import random
# import pandas as pd
# import datetime
# import xgboost as xgb
# import copy
# from PIL import Image
# from datetime import datetime, timedelta
# import numpy as np
# import os
# from utils import doc_loader, summary_prompt_creator, doc_to_final_summary

# from my_prompts import file_map, file_combine, youtube_map, youtube_combine
# from streamlit_app_utils import (check_gpt_4, check_key_validity, create_temp_file,
# create_chat_model, token_limit, token_minimum, load_pdf_from_github, pdf_to_text)
# from utils import transcript_loader

import streamlit as st
from datetime import datetime
import os
from streamlit_extras.switch_page_button import switch_page
from utils import doc_loader, summary_prompt_creator, doc_to_final_summary, validate_doc_size
from my_prompts import file_map, file_combine
from streamlit_app_utils import check_gpt_4, check_key_validity, create_temp_file, create_chat_model, load_pdf_from_github
from pathlib import Path

header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

def record_page_start_time():
    st.session_state['page_start_time'] = datetime.now()

def record_page_duration_and_send():
    if 'page_start_time' in st.session_state:
        page_duration = datetime.now() - st.session_state['page_start_time']
        st.session_state.oocsi.send('Time_XAI', {
            "page_name": "Baseline - No tool",
            "duration_seconds": page_duration.total_seconds(),
            "participant_ID": st.session_state.name
        })

def validate_input(file_or_transcript, api_key, use_gpt_4):
    if file_or_transcript is None:
        st.warning("Please upload a file or enter a YouTube URL.")
        return False
    if not check_key_validity(api_key):
        st.warning('Key not valid or API is down.')
        return False
    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Key not valid for GPT-4.')
        return False
    return True

def process_summarize_button(url, api_key, use_gpt_4, find_clusters):
    if not check_key_validity(api_key):
        st.warning("Invalid API Key or GPT access denied.")
        return

    with st.spinner("Summarizing... please wait..."):
        temp_file_path = create_temp_file(url)
        try:
            # Load the document using doc_loader
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
                os.unlink(temp_file_path)  # Clean up the temporary text file



record_page_start_time()

with header2: 
    st.title("Summarization")

with body2:
    st.header(f"Explanation experiment - {st.session_state['topic']}")
    st.markdown('''To be modified: In this experiment we will show you four different profiles of passengers. 
    Using Machine Learning (ML) we will show a prediction whether they would have survived the disaster. 
    This prediction is accompanied by each time a different type of explanation.''')
    st.image('https://images.unsplash.com/photo-1566125882500-87e10f726cdc?q=80&w=2874&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', width=600,caption="Photo by Kate Macate on Unsplash")



    
    st.subheader('Model')

    use_gpt_4 = True
    find_clusters = False

## NO need for API key for now --> wizard of oz method
    # # Ask for the API key
    # api_key = st.text_input("Enter your API key:", type='password')

    # # Button to submit the API key
    # if st.button('Submit API Key'):
    #     if api_key:
    #         st.session_state['api_key'] = api_key  # Save API key in session state if needed
    #         st.success("API Key submitted successfully!")
    #     else:
    #         st.error("Please enter a valid API Key.")

    if st.button('Summarize (click once and wait)', key='summarize_button'):
        if st.session_state['topic'] == 'Financial': 
            st.markdown('''
                        📩 Afzender: 🏛️ Gemeente Eindhoven
                        
                        🎯 Doel: Belastingaanslag uitleggen
                        
                        🔑 Actiepunten:
                            💸 Betaal €269,72
                            📅 Voor 31-03-2024
                            🖥️ Betaal online
                            📆 10 termijnen mogelijk
                            📨 Maak bezwaar mogelijk
                        📞 Contactinformatie:
                            📞 14 040
                            📝 Online contactformulier
                        
                        📢 Voor vragen, bezoek eindhoven.nl.''')

        else: 
            st.markdown('''
                        📩 Afzender: RIVM

                        🎯 Doel: Coronaprik voor kinderen

                        💡 Highlights: 
                            💉 Informatie coronaprik
                            🧒 Kinderen vanaf 5 jaar
                            📄 Maak afspraak
                            📞 Bel 0800 7070
                            🆔 Neem ID en brief
                        
                        📞 Contactinformatie:
                        0800 7070 (gratis)
                        
                        📢 Call to Action:
                        Als je vragen hebt, bel 0800-7070 of bezoek www.coronavaccinatie.nl.''')
                                                

        # if st.session_state ['uploaded_file'] is not None:
        #     process_summarize_button(st.session_state['uploaded_file'], api_key, use_gpt_4, find_clusters)
        #     st.write('If you are not satisfied with the summary, you can summarize again')
        # else:
        #     st.warning('please uplaod your file')
    
st.sidebar.markdown('# Made by: [François and Sichen ](https://github.com/engrobelf)')
st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/engrobelf/low_literacy.git)') 
st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                    This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)

def validate_input(file_or_transcript, api_key, use_gpt_4):
    """
    Validates the user input, and displays warnings if the input is invalid

    :param file_or_transcript: The file uploaded by the user or the YouTube URL entered by the user

    :param api_key: The API key entered by the user

    :param use_gpt_4: Whether the user wants to use GPT-4

    :return: True if the input is valid, False otherwise
    """
    if file_or_transcript == None:
        st.warning("Please upload a file or enter a YouTube URL.")
        return False

    if not check_key_validity(api_key):
        st.warning('Key not valid or API is down.')
        return False

    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Key not valid for GPT-4.')
        return False

    return True



with body2:
    if st.session_state['topic'] == 'Health':
        with st.form("health_form2"):
            st.markdown('**AI literacy**')
            st.markdown("Please select the right answer to the multiple-choice questions below. \
                        A correct answer is awarded +1 point, an incorrect answer -1 point and the \"I don't know option\" 0 points.")

            question1 = st.radio(
                "Van welke organisatie is deze brief?",
                ["A) Gezondheidsraad",
                "B) RIVM",
                "C) Ministerie van Volksgezondheid",
                "D) Gemeentehuis",
                "E) I don't know"], index=4)
            
            question2 = st.radio(
                "Wat is het hoofddoel van deze brief?",
                ["A) Uitnodiging voor een feest",
                "B) Informatie over een coronaprik voor kinderen",
                "C) Advies over schoolbezoeken ",
                "D) Registratie voor een sportevenement",
                "E) I don't know"], index=4)
            
            question3 = st.radio(
                "Welke actie moet als eerste worden ondernomen om een afspraak te maken?",
                ["A) Bel de huisarts",
                "B) Zoek het BSN van je kind ",
                "C) Bezoek de lokale kliniek",
                "D) Schrijf je in op een website",
                "E) I don't know"], index=4)

            question4 = st.radio(
                "Op welk nummer moet je bellen om een vaccinatieafspraak te maken?",
                ["A) 0800 7070",
                "B) 112",
                "C) 0800 1234",
                "D) 0900 2020",
                "E) I don't know"], index=4)
            

            question5 = st.radio(
                "Wat is een vereiste om mee te nemen naar de vaccinatieafspraak?",
                ["A) Een waterfles",
                "B) Een pasfoto",
                "C) De uitnodigingsbrief en een ID",
                "D) Een medische geschiedenisrapport",
                "E) I don't know"], index=4)


            question6 = st.radio(
                "Waar kun je meer informatie vinden over de coronavaccinatie voor kinderen?",
                ["A) www.gezondheid.nl",
                "B) www.rivm.nl",
                "C) www.coronavaccinatie.nl",
                "D) www.kinderzorg.nl",
                "E) I don't know"], index=4)
            
            submitted = st.form_submit_button("Submit")
        if submitted:
            if 'page_start_time' in st.session_state:
                record_page_duration_and_send()    
            # st.write("question 1", q1)
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

# Financial Letter questions:
    elif st.session_state['topic'] == 'Financial':
            with st.form("financial_form2"):
                st.markdown('**Reading comprehension**')
                st.markdown("Please select the right answer to the multiple-choice questions below. \
                            A correct answer is awarded +1 point, an incorrect answer -1 point and the \"Ik weet het niet\" 0 points.")

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
                    ["A) belastingbalie.amsterdam.nl",
                    "B) belastingbalie.rotterdam.nl",
                    "C) belastingbalie.utrecht.nl",
                    "D) belastingbalie.eindhoven.nl",
                    "E) Ik weet het niet"], index=4)
                
                question6 = st.radio(
                    "Welke is de juiste contactinformatie?",
                    ["A) 14 020",
                    "B) 14 040",
                    "C) 14 030",
                    "D) 14 050",
                    "E) Ik weet het niet"], index=4)
                
                submitted = st.form_submit_button("Submit")
                if submitted:
                    if 'page_start_time' in st.session_state:
                        record_page_duration_and_send()    
                    st.session_state.oocsi.send('Baseline_text_question', {
                        'participant_ID': st.session_state.name,
                        'q1': question1,
                        'q2': question2,
                        'q3': question3,
                        'q4': question4,
                        'q5': question5,
                        'q6': question6,
                        })
                    switch_page("evaluation_tool")

# if st.button("Next page"):
    


