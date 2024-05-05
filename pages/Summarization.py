
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

with header2: 
    st.title("Summarization")

with body2:
    st.header('Explanation experiment')
    st.markdown('''To be modified: In this experiment we will show you four different profiles of passengers. 
    Using Machine Learning (ML) we will show a prediction whether they would have survived the disaster. 
    This prediction is accompanied by each time a different type of explanation.''')
    st.image('https://github.com/engrobelf/low_literacy/blob/francois/picture/LL_pic.png?raw=True', width=700, caption= 'Low literacy overview')



    
    st.subheader('Model')
    st.markdown(''' The same ML model is used to generate the predictions of who survived and who did not. 
                This model is used to generate all of the four types of explanations that you will see during the experiment. 
                ''')
    use_gpt_4 = st.checkbox("Use GPT-4 for the final prompt (STRONGLY recommended, requires GPT-4 API access - progress bar will appear to get stuck as GPT-4 is slow)", value=True)
    find_clusters = st.checkbox('Find optimal clusters (experimental, could save on token usage)', value=False)

    # Ask for the API key
    api_key = st.text_input("Enter your API key:", type='password')

    # Button to submit the API key
    if st.button('Submit API Key'):
        if api_key:
            st.session_state['api_key'] = api_key  # Save API key in session state if needed
            st.success("API Key submitted successfully!")
        else:
            st.error("Please enter a valid API Key.")

    if st.button('Summarize (click once and wait)'):
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
                    A correct answer is awarded +1 point, an incorrect answer -1 point and the \"I don't know option\" 0 points.")

        # socio1 = st.radio(
        # "AI was first mention in",
        # ["The 2000s",
        #  "The 1950s",
        #  "The 1880s",
        #  "The 1980s",
        #  "I don't know"], index =4)

        # socio2 = st.radio(
        # "How are human and artificial intelligence related?",
        # ["They are the same, concerning strengths and weaknesses",
        #  "They predict each other",
        #  "Their strengths and weaknesses converge",
        #  "They are different, each has its own strengths and weaknesses",
        #  "I don't know"], index =4)

        # socio3 = st.radio(
        # "AI research",
        # ["happens in an interdisciplinary field including multiple technologies ",
        #  "refers to one specific AI technology",
        #  "is only fiction at this point in time ",
        #  "revolves predominantly around optimization ",
        #  "I don't know"], index =4)

        # socio4 = st.radio(
        # "What is a possible risk for humans of AI technology",
        # ["Digital assistants take over self-driving cars",
        #  "Voice generators make people unlearn natural languages",
        #  "Image generator break the rule of art ",
        #  "Deep fakes render videos unattributable",
        #  "I don't know"], index =4)
        
        techCreator4 = st.radio(
            "What is not part of an ANN?",
            ["Input layer",
             "User layer",
             "Output layer",
             "Hidden layer",
             "I don't know"], index=4)
        
        techUser4 = st.radio(
            "Running the same request with the same data on the same AI",
            ["increase the computing speed",
             "never give different results",
             "double the computing time ",
             "could give different results",
             "I don't know"], index=4)
        
        techUser1 = st.radio(
            "What is the central distinction between supervised and unsupervised learning",
            ["Supervised learning uses labelled datasets",
             "Unsupervised learning may happen anytime ",
             "Supervised learning is performed by supervised personnel",
             "Supervised learning supersedes unsupervised learning ",
             "I don't know"], index=4)

        techCreator3 = st.radio(
            "What is not a strictly necessary part of a single AI system's development process?",
            ["Data preprocessing",
             "Model definition",
             "Benchmarking",
             "Training/Learning",
             "I don't know"], index=4)
        

        techUser3 = st.radio(
            "What is a typical application of an AI at which it is usually better than non-AI",
            ["Hardware space analysis",
             "Image recognition ",
             "Creating annual reports",
             "Undefined processes",
             "I don't know"], index=4)



        techCreator1 = st.radio(
            "What always distinguishes decision trees from support vector machine?",
            ["Decision trees are trained faster",
             "Decision trees generate more predictions ",
             "Decision trees are more implicit",
             "Decision trees are more interpretable ",
             "I don't know"], index=4)
        techUser2 = st.radio(
            "Which of the following statements is true?",
            ["Machine Learning is part of AI",
             "Machine Learning and AI are mutually exclusive",
             "AI and ML are the same ",
             "AI is a part of ML",
             "I don't know"], index=4)
        techCreator2 = st.radio(
            "What is a typical split of testing and training data for development purposes?",
            ["80% Training and 20% Testing",
             "40% Training, 40% Testing, 20% Train-Testing together",
             "95% Testing and 5% Training",
             "It does not matter",
             "I don't know"], index=4)
        submitted = st.form_submit_button("Submit")
        if submitted:
            pass
            # if page_start_time:
            #     record_page_duration_and_send()    
            # # st.write("question 1", q1)
            # st.session_state.oocsi.send('XAImethods_evaluation', {
            #     'participant_ID': st.session_state.participantID,
            #     'type of explanation': 'Decision tree',
            #     'cognitive load': c_load,
            #     'q1': q1,
            #     'q2': q2,
            #     'q3': q3,
            #     'q4': q4,
            #     'q5': q5,
            #     'q6': q6,
            #     'q7': q7,
            #     'q8': q8,
                
            #     })

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