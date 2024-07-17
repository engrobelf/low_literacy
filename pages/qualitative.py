import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
from oocsi_source import OOCSI
import datetime
from datetime import datetime
import time


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
    st.markdown("In this section, we ask you to give feedback regarding the summarization tool presented in the experiment.")


with body2:
    with st.form("mijn formulier"):
        why = st.text_area('**In welke situaties en contexten denk je dit samenvattingshulpmiddel te gebruiken?**', "")
        why_2 = st.text_area('**Hoe zou je het systeem gebruiken om te helpen met het lezen en begrijpen van teksten?**')
        why_3 = st.text_area('**Welke functies zouden het systeem gemakkelijk maken voor mensen met lage leesvaardigheid?**')
        why_4 = st.text_area('**Welke instructie of hulp is nodig om nieuwe gebruikers het systeem goed te laten gebruiken?**')
        why_5 = st.text_area('**Welke kansen kan dit hulpmiddel bieden voor mensen met lage leesvaardigheid?**')
        why_6 = st.text_area('**Welke risicos of problemen kunnen ontstaan door het gebruik van dit systeem?**')
        why_7 = st.text_area('**Heb je feedback voor het hulpmiddel en de evaluatie in het algemeen?**')

        word_count_1 = check_input_length(why)
        word_count_2 = check_input_length(why_2)
        word_count_3 = check_input_length(why_3)
        word_count_4 = check_input_length(why_4)
        word_count_5 = check_input_length(why_5)
        word_count_6 = check_input_length(why_6)
        word_count_7 = check_input_length(why_7)

        submitted = st.form_submit_button("Verstuur")

        if submitted:
            if word_count_1 < 5:
                st.warning('Geef alsjeblieft een uitgebreidere uitleg (meer dan 5 woorden)')
            elif word_count_2 < 5:
                st.warning('Geef alsjeblieft een uitgebreidere uitleg (meer dan 5 woorden)')
            elif word_count_3 < 5:
                st.warning('Geef alsjeblieft een uitgebreidere uitleg (meer dan 5 woorden)')
            elif word_count_4 < 5:
                st.warning('Geef alsjeblieft een uitgebreidere uitleg (meer dan 5 woorden)')
            elif word_count_5 < 5:
                st.warning('Geef alsjeblieft een uitgebreidere uitleg (meer dan 5 woorden)')
            elif word_count_6 < 5:
                st.warning('Geef alsjeblieft een uitgebreidere uitleg (meer dan 5 woorden)')
            elif word_count_7 < 5:
                st.warning('Geef alsjeblieft een uitgebreidere uitleg (meer dan 5 woorden)')
            else:
                st.success('Dank je wel!')

                participant_id = st.session_state.name
                
                record_why(participant_id, why_2, 2)
                time.sleep(1)  # Add delay between calls

                record_why(participant_id, why, 1)
                time.sleep(1)  # Add delay between calls

                record_why(participant_id, why_3, 3)
                time.sleep(1)  # Add delay between calls

                record_why(participant_id, why_4, 4)
                time.sleep(1)  # Add delay between calls

                record_why(participant_id, why_5, 5)
                time.sleep(1)  # Add delay between calls

                record_why(participant_id, why_6, 6)
                time.sleep(1)  # Add delay between calls

                record_why(participant_id, why_7, 7)
                


                switch_page('thankyou')