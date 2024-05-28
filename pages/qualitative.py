import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
from oocsi_source import OOCSI
import datetime
from datetime import datetime

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


def record_why(participant_id, why, question_id):
    st.session_state.oocsi.send('LL_qualitative', {
        'participant_ID': participant_id,
        f'why_{question_id}': why[:900],
    })
    if len(why) > 900:
        st.session_state.oocsi.send('LL_qualitative', {
            'participant_ID': participant_id,
            f'why_{question_id}_bis': why[900:1800],
        })

def check_input_length(text):
    words = text.split()
    word_count = len(words)
    return word_count


with header2:
    st.title("Comparing the different methods")
    st.markdown("In this section, we ask you to give you feedback regarding the summarization tool presented in the experiment.")


with body2:
    with st.form("my_form"):
        why = st.text_area('**In what situations and contexts do you foresee using this summarizing tool?**', "")
        why_2 = st.text_area('**How would you typically use the system to assist with reading and understanding text documents?**')
        why_3 = st.text_area('**What features would make the system particularly user-friendly for individuals with low literacy levels?**')
        why_4 = st.text_area('**What instruction or support might be necessary for new users to learn how to interact with this system effectively?**')
        why_5 = st.text_area('**What opportunities do you believe this tool could create for users with low literacy?**')
        why_6 = st.text_area('**What risks or challenges might arise from using this system?**')

        word_count_1 = check_input_length(why)
        word_count_2 = check_input_length(why_2)
        word_count_3 = check_input_length(why_3)
        word_count_4 = check_input_length(why_4)
        word_count_5 = check_input_length(why_5)
        word_count_6 = check_input_length(why_6)

        submitted = st.form_submit_button("Submit")

        if submitted:
            if word_count_1 < 7:
                st.warning('Please explain more extensively your answer (+7 words)')
            elif word_count_2 < 7:
                st.warning('Please explain more extensively your answer (+7 words)')
            elif word_count_3 < 7:
                st.warning('Please explain more extensively your answer (+7 words)')
            elif word_count_4 < 7:
                st.warning('Please explain more extensively your answer (+7 words)')
            elif word_count_5 < 7:
                st.warning('Please explain more extensively your answer (+7 words)')
            elif word_count_6 < 7:
                st.warning('Please explain more extensively your answer (+7 words)')
            else:
                st.success('Thank you!')

                participant_id = st.session_state.name

                record_why(participant_id, why, 1)
                record_why(participant_id, why_2, 2)
                record_why(participant_id, why_3, 3)
                record_why(participant_id, why_4, 4)
                record_why(participant_id, why_5, 5)
                record_why(participant_id, why_6, 6)

                switch_page('thankyou')