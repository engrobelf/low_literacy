
import streamlit as st
from uuid import uuid4
from streamlit_extras.switch_page_button import switch_page
import random
import pandas as pd
import datetime
import xgboost as xgb
import copy
from PIL import Image
from datetime import datetime, timedelta
import numpy as np
import os
from utils import doc_loader, summary_prompt_creator, doc_to_final_summary

from my_prompts import file_map, file_combine, youtube_map, youtube_combine
from streamlit_app_utils import check_gpt_4, check_key_validity, create_temp_file, create_chat_model, token_limit, token_minimum
from utils import transcript_loader



header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

def record_page_start_time():
    st.session_state['page_start_time'] = datetime.now()

# Record page duration and send data via OOCSI
def record_page_duration_and_send():
    if 'page_start_time' in st.session_state:
        page_duration = datetime.now() - st.session_state['page_start_time']
        st.session_state.oocsi.send('Time_XAI', {
            "page_name": "Baseline - No tool",
            "duration_seconds": page_duration.total_seconds(),
            "participant_ID": st.session_state.name
        })

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


def process_summarize_button(file_or_transcript, api_key, use_gpt_4, find_clusters, file=True):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid

    :param file_or_transcript: The file uploaded by the user or the transcript from the YouTube URL

    :param api_key: The API key entered by the user

    :param use_gpt_4: Whether to use GPT-4 or not

    :param find_clusters: Whether to find optimal clusters or not, experimental

    :return: None
    """
    if not validate_input(file_or_transcript, api_key, use_gpt_4):
        return

    with st.spinner("Summarizing... please wait..."):
        if file:
            temp_file_path = create_temp_file(file_or_transcript)
            doc = doc_loader(temp_file_path)
            map_prompt = file_map
            combine_prompt = file_combine
        else:
            doc = file_or_transcript
            map_prompt = youtube_map
            combine_prompt = youtube_combine
        llm = create_chat_model(api_key, use_gpt_4)
        initial_prompt_list = summary_prompt_creator(map_prompt, 'text', llm)
        final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)

        if not validate_doc_size(doc):
            if file:
                os.unlink(temp_file_path)
            return

        if find_clusters:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key, use_gpt_4, find_clusters)

        else:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key, use_gpt_4)

        st.markdown(summary, unsafe_allow_html=True)
        if file:
            os.unlink(temp_file_path)

record_page_start_time()

with header2: 
    st.title("Summarization")

with body2:
    st.header('💡Scenrio')
    st.markdown('''Imagine it’s another quiet afternoon at home, and you got the same letter. However, this time you have access to a new tool designed to help you understand the contents more quickly and easily.

Your task is to select one of these letters and then use this new summarization tool. Compare it to the standard method without summarization. After using both methods, you will need to answer some questions about the text to see how well (or poorly) you understood it. Don’t worry about getting everything correct; if you don’t know the answer, an 'I don’t know' option will also be available. Good luck, and thanks again for participating!
''')
    st.image('https://images.unsplash.com/photo-1566125882500-87e10f726cdc?q=80&w=2874&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', width=800, caption= 'Photo by Kate Macate on Unsplash')

    use_gpt_4 = True
    find_clusters = False

    # Ask for the API key
    api_key = st.text_input("Enter your API key:", type='password')

    # Button to submit the API key
    if st.button('Submit API Key'):
        if api_key:
            st.session_state['api_key'] = api_key  # Save API key in session state if needed
            st.success("API Key submitted successfully!")
        else:
            st.error("Please enter a valid API Key.")

    if st.button('Summarize (click once and wait)', key='summarize_button'):
        if st.session_state ['uploaded_file'] is not None:
            process_summarize_button(st.session_state['uploaded_file'], api_key, use_gpt_4, find_clusters)
            st.write('If you are not satisfied with the summary, you can summarize again')
        else:
            st.warning('please uplaod your file')
    
st.sidebar.markdown('# Made by: [François and Sichen ](https://github.com/engrobelf)')
st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/engrobelf/low_literacy.git)') 
st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                    This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)


if st.button('Summarize (click once and wait)'):
    if st.session_state ['uploaded_file'] is not None:
        process_summarize_button(st.session_state['uploaded_file'], api_key, True, find_clusters)
        st.write('If you are not satisfied with the summary, you can summarize again')
    else:
        st.warning('please uplaod your file')




def validate_doc_size(doc):
    """
    Validates the size of the document

    :param doc: doc to validate

    :return: True if the doc is valid, False otherwise
    """
    if not token_limit(doc, 800000):
        st.warning('File or transcript too big!')
        return False

    if not token_minimum(doc, 50):
        st.warning('File or transcript too small!')
        return False
    return True


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
    with st.form("my_form"):

        gender = st.radio("How do you identify your gender", ('Female',
                          'Male', 'Non-binary', 'Other', 'Prefer not to say'))
        age = st.number_input("How old are you?", step=1)
        # educationlevel = st.radio("What is your highest level of education?",
        #                           ('elementary school', 'high school', 'MBO', 'HBO', 'University'))
        st.markdown('**AI literacy**')
        st.markdown("Please select the right answer to the multiple-choice questions below. \
                    A correct answer is awarded +1 point, an incorrect answer -1 point and the \"Ik weet het niet\" 0 points.")

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
            "E) I don't know"], index=4)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            if 'page_start_time' in st.session_state:
                record_page_duration_and_send()    
            # st.write("question 1", q1)
            st.session_state.oocsi.send('Baseline_text_question', {
                'participant_ID': st.session_state.name,
                'q1': question1,
                'q2': question2,
                'q3': question3,
                'q4': question4,
                'q5': question5,
                'q6': question6,
                })


if st.button("Next page"):
                # if page_start_time:
                    # record_page_duration_and_send()
                # record_page_start_time()
                # st.session_state.oocsi.send('Tool_answer', {
                #     'participant_ID': st.session_state.participantID,
                #     'expert': "yes",
                #     'consent': 'yes',
                #     'consentForOSF': consentforOSF
                # })
    switch_page("evaluation_tool")