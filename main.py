"""
These are the meta data and instructions
Author: François Leborgne & Guoze

Instructions:
1. Pip install streamlit, oocsi, streamlit_extras in your python environment
2. Save this file somewhere on your computer
3. In the command line, cd to where your file is: "cd/...../folder

4. To run it: streamlit run app.py 
5. Click on the link it provides you
6. You need to click sometimes rerun in the website

To hide menu: copy paste this in config.toml
[ui]
hideSidebarNav = true
"""
#  #OPEN_AI_KEI = sk-proj-TrjEp8HF1XMceDrHHtcMT3BlbkFJ0nPa9Jep1HvtiBilzRd0

import os
from datetime import datetime
import streamlit as st
from oocsi_source import OOCSI
from streamlit_extras.switch_page_button import switch_page
from utils import (
    doc_loader,
    summary_prompt_creator,
    doc_to_final_summary,
    transcript_loader
)
from my_prompts import file_map, file_combine, youtube_map, youtube_combine
from streamlit_app_utils import (
    check_gpt_4,
    check_key_validity,
    create_temp_file,
    create_chat_model,
    token_limit,
    token_minimum
)

# Constants
find_clusters = False

st.set_page_config(page_title="Low literacy research", layout="wide")


# Initialize OOCSI
if 'oocsi' not in st.session_state:
    st.session_state.oocsi = OOCSI('', 'oocsi.id.tue.nl')

# Record start time for each page
def record_page_start_time():
    global page_start_time
    page_start_time = datetime.now()

# Record page duration and send data via OOCSI
def record_page_duration_and_send():
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

# Set up page configuration
st.sidebar.markdown('# Made by: [François and Sichen ](https://github.com/engrobelf?tab=repositories)')
st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/engrobelf/low_literacy.git)')
st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key.
                    This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)

page_start_time = None
record_page_start_time()

with st.container():
    st.title("Low literacy research - Document Summarizer")

with st.container():
    st.header(' 📄 Information form for participants')
    st.write('''Hello and thank you for considering participation in our research project at Eindhoven University of Techonology. This study involves an innovative GPT-4 summarization tool, and your involvement would be invaluable, especially given your interest or expertise in this field.

Participation is entirely voluntary, with no associated physical, legal, or economic risks. You have full freedom to choose which questions to answer and the option to withdraw at any time, without any adverse consequences. If you have questions or need more information after reading about the study, please reach out to Sichen Guo or feel free to consult with trusted individuals.''')

    st.subheader('🎯 Aim and benefit of the study')
    st.write('''The aim of this research project is to invite the participants to engage with our designed tool, experience
            real-time interaction, and receive immediate outcomes. We will evaluate the effectiveness of these
            interactions by measuring both the duration of validated engagement and the overall user experience via
            questionnaires, and interviews.  ''')
    st.write('''This study is performed by François Leborgne and Sichen Guo, all EngD trainees of the Designing Human-System Interaction program and for this study under the supervision of Jun Hu of the Industrial Design Department.''')

    st.subheader('🧗 Procedure')
    st.markdown('''During this project we ask you to: 
    -	Choose one letter to upload
    -	wirite down the action points or high light points you know from this letter
    -	put the chosen letter in the new designed summrized system 
    -	wirite down the action points or high light points you know from this letter
    -   fill in a survey with 12 questions 
    -   In the end, you will be invited to do a semi-structure interview 
   
''')

    st.subheader('⚠️ Risks')
    st.markdown(
        "The study does not involve any risks, detrimental side effects, or cause discomfort.")

    st.subheader("🕙 Duration")
    st.markdown(
        "The instructions, measurements and debriefing will take approximately 30 minutes.")

    st.subheader("🧑‍💼 Voluntary")
    st.markdown('''Your participation is completely voluntary. You can refuse to participate without giving any reasons and you can stop your participation at any time during the study. You can also withdraw your permission to use your data immediately after completing the study. None of this will have any negative consequences for you whatsoever.''')

    st.subheader("📊 Confidentiality and use, storage, and sharing of data")
    st.markdown('''
                    The collected data will be stored on TU/e supported storage facilities.
                    
                    We will make sure that any published research results will not include confidential or identifiable
                    information about you unless you explicitly agree to it, for example, if you want your name to be
                    mentioned in publications.
                    
                    Your personal data might be used for future research, but only if your data is truly necessary if the
                    recognized ethical standards for scientific research are followed, and if the new research objectives align
                    with the current research objectives. If your personal data is used in future research, we will take all
                    reasonable steps to inform you about this. You can object to the use of your data for new research.
                    
                    We might use anonymized data for new purposes such as research or education. We will ensure the data
                    cannot be linked to you and we will not disclose anything that makes you identifiable.
                    This research has been assessed and approved by the ethical committee of Eindhoven University of
                    Technology.
                                
                    The screen and time will be recorded during the interacting process, and the interview script will be recorded by audio recording.
    
    ''')

    st.subheader("📰 Further information")
    st.markdown('''If you want more information about this study, the study design, or the results, you can contact François Leborgne (contact email: f.m.g.leborgne@tue.nl ) or Sichen Guo (contact email: s.guo3@tue.nl). 
    If you have any complaints about this study, please contact the supervisor, Jun Hu (j.hu@tue.nl)  You can report irregularities related to scientific integrity to confidential advisors of the TU/e.
    ''')

    st.subheader("📝 Informed consent form")
    st.markdown('''
        1. I have enough information about the research project from the separate information sheet. I
        have read it, and I have had the chance to ask questions, which have been answered to my
        satisfaction.
        2. I take part in this research project voluntarily. There is no explicit or implicit pressure for me to
        take part in this research project, and I understand I can stop my participation at any moment
        without explaining why. I do not have to answer any question I do not want to answer.
        3. I know my personal data will be collected and used for the research, as explained to me in the
        information sheet.
    ''')

    # Consent form
    OSF = st.radio

    st.subheader("✍️ Consent")
    agree = st.radio(
        'I consent to my answers being used for quotes in the research publications – without including my name.',
        ('do', 'do not'), index=1)

    consent_for_osf = "yes" if OSF == 'do' else 'no'
    agree = st.radio(
            'I consent to my real name being mentioned in the quotes as described under 4',
            ('do', 'do not'), index=1)

    consent_for_osf = "yes" if OSF == 'do' else 'no'

    nameID = st.text_input(
        "Please enter/paste here your name")
    st.session_state.name = nameID

    if agree == "do":
        st.write('Thank you! Please continue to the next page to start the experiment')
        if st.button("Next page"):
            st.session_state.oocsi.send('Lowl_consent', {
                'participant_ID': st.session_state.name,
                'expert': "yes",
                'consent': 'no',
                'consentForOSF': consent_for_osf
            })
            switch_page("explanationpage")
    else:
        if st.button("Next page"):
            st.session_state.oocsi.send('Lowl_consent', {
                'participant_ID': st.session_state.name,
                'expert': "yes",
                'consent': 'no',
                'consentForOSF': consent_for_osf
            })
            switch_page('noconsent')
