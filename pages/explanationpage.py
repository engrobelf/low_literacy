import streamlit as st
from uuid import uuid4
from streamlit_extras.switch_page_button import switch_page
from streamlit_app_utils import download_pdf
import random
import pandas as pd
import datetime
import xgboost as xgb
import os
import copy
from PIL import Image
from datetime import datetime, timedelta
import numpy as np

header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])


def record_page_start_time():
    global page_start_time
    page_start_time = datetime.now()

# Function to record page duration and send to Data Foundry
def record_page_duration_and_send_explanation():
    current_page_title = st.session_state.current_page_title
    if page_start_time:
        page_end_time = datetime.now()
        page_duration = page_end_time - page_start_time

        st.write(f"Time spent on {current_page_title}: {page_duration}")
            # Send data to Data Foundry via OOCSI
        data = {
            "page_name": current_page_title,
            "duration_seconds": page_duration.total_seconds(), 
            'participant_ID': st.session_state.participantID
        }
        st.session_state.oocsi.send('Time_XAI', data)

# st.session_state.current_page_title = "Explanation Page"
page_start_time = None
record_page_start_time()

with header2:
    st.title("Low literacy issues?")

with body2:
    st.header("Overview")
    st.markdown("here it ould be nice to have some sort of explanaiton of the LL problem that is faced by a large number of people ")
    st.image('https://github.com/engrobelf/low_literacy/blob/francois/picture/LL_pic.png?raw=True')

    st.header('Explanation experiment')
    st.markdown('''You will have to select between 5 different letters from the dutch government which topic are realted to tax, health or even a typical check-up. 
                Then you will compare the summarization tool with a baseline (no summarization) and will need to answer some questions on the text to see how well (or bad) 
                you understood it. Do not worry about getting eerything correct! I you don't have the answer, an 'I don't know' will also be available. 
                Good luck and thanks again for participating!''')
    st.markdown("After answering the question, you will be asked to evaluate the method you have just seen.")
    
    st.subheader('Model')
    st.markdown(''' A GPT4 model was finetune and prompt engineer to provide the most tailored summary possible. Typical lexical metrics were also used to validate the quality of the 
                summary.''')
    
    st.subheader('Letters')

    # st.subheader('Demographic information')
    # st.markdown("Before you start with the study we would like to ask you to first answer these questions")


# with footer2:
#     if st.button("Start the experiment "):
#         if page_start_time:
#             record_page_duration_and_send_explanation()    
#         record_page_start_time()
#         st.session_state.oocsi.send('XAImethods_attentioncheck', {
#             'participant_ID': st.session_state.participantID,
#             'feature_explanation': feature_explanation,
#             })
#         switch_page(st.session_state.pages[st.session_state.nextPage])

# Assuming you have a directory containing PDF files for each topic
pdf_directory = r"https://github.com/engrobelf/low_literacy/tree/main/letters"

# Get the list of PDF files in the directory
# pdf_files = ['Health', 'Work', 'Digital_DataPrivacy', 'Relationship', 'Financial']
with footer2:
    input_method = st.radio("Select input prefered topic", ('Health', 'Work', 'Digital_DataPrivacy', 'Relationship', 'Financial' ))
    selected_pdf = None
    if input_method:
        st.write("You have selected:", input_method)
        selected_pdf = os.path.join(pdf_directory, input_method + '.pdf').replace('\\', '/').replace('tree', 'blob')
        # st.write("Selected PDF:", selected_pdf)
        # selected_pdf = download_pdf(selected_pdf, f'{input_method}.pdf')
        st.session_state['uploaded_file'] = selected_pdf
        st.write(selected_pdf)

    else:
        st.write("Please select a topic to proceed.")
          
    if st.button("Next page") and selected_pdf is not None:
                    # if page_start_time:
                        # record_page_duration_and_send()
                    # record_page_start_time()
                    # st.session_state.oocsi.send('XAI_consent', {
                    #     'participant_ID': st.session_state.participantID,
                    #     'expert': "yes",
                    #     'consent': 'yes',
                    #     'consentForOSF': consentforOSF
                    # })
        switch_page("Baseline")