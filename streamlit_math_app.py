import streamlit as st
import random

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. CSS για Animations και Τελική Οθόνη
css_code = """
<style>
.stApp { background-color: #f0f7ff; }

/* Animations */
@keyframes textFadeIn {
    0% { opacity: 0; filter: blur(5px); }
    100% { opacity: 1; filter: blur(0px); }
}

@keyframes slideInLeft {
    0% { transform: translateX(-150%) rotate(-10deg); opacity: 0; }
    100% { transform: translateX(0) rotate(0deg); opacity: 1; }
}

@keyframes boxFade {
    0% { opacity: 0.5; }
    100% { opacity: 1; }
}

.main-card {
    background-color: transparent;
    width: 100%;
    height: 250px;
    perspective: 1000px;
    margin: 20px 0;
}

.slow-text-fade { animation: textFadeIn 1s ease-out forwards; }
.box-anim { animation: boxFade 1.5s ease-in-out; }
.first-card-anim { animation: slideInLeft 2.5s ease-out forwards; }

.card-content {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 25px;
    font-size: 65px;
    font-weight: bold;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
    border: 4px solid;
}

.front-style { background-color: white; color: #495057; border-color: #a2d2ff; }
.back-style { background-color: #f0f9ff; color: #0077b6; border-color: #00b4d8; }

/* Το Τελικό Γαλάζιο Τετράγωνο Πλαίσιο - Μεγαλύτερο & Πιο Ψηλά */
.final-success-box {
    background-color: #f0f9ff;
    color: #0077b6;
    border: 8px solid #00b4d8;
    border-radius: 30px;
    padding: 80px 40px; 
    text-align: center;
    font-size: 55px; /* Μεγάλη γραμματοσειρά */
    font-weight: bold;
    box-shadow: 0px 15px 30px rgba(0,0,0,0.15);
    margin-top: -60px; /* Ανέβασμα πιο ψηλά */
    margin-bottom: 40px;
    line-height: 1.3;
    animation: textFadeIn 1.5s ease-out;
    width: 100%;
    display: block;
}

.score-box {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    font-size: 18px;
    border: 2px solid #bde0fe;
    color: #0077b6;
    margin-bottom: 10px;
}

.stButton>button { border-radius: 15px; font-weight: bold; }
div.stButton > button:first-child[kind='primary'] {
    background-color: #0077b6;
    color: white;
    width: 100%;
    height: 3.5em;
    font-size: 22px;
}
</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

# 3. Session State
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'correct_answers' not in st.session_state: st.session_state.correct_answers = set()
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'show_answer' not in st.session_state: st.session_state.show_answer = False
if 'selected_numbers' not in st.session_state: st.session_state.selected_numbers = []
if 'is_finished' not in st.session_state: st.session_state.is_finished = False
if 'card_id' not in st.session_state: st.session_state.card_id = 0

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# --- HOME PAGE ---
if not st.session_state.game_started:
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    st.session_state.selected_numbers = selected
    
    if selected:
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.session_state.correct_answers = set()
            st.session_state.current_q = None
            st.session_state.is_finished = False
            st.session_state.card_id = 0
            st.rerun()
    else:
        st.info("✅ Επίλεξε αριθμούς για να ξεκινήσεις!")

# --- GAME PAGE ---
else:
    all_q = [(n, i) for n in st.session_state.selected_numbers for i in range(1, 11)]
    rem_q = [q for q in all_q if q not in st.session_state.correct_answers]

    if not rem_q and not st.session_state.is_finished:
        st.session_state.is_finished = True
        st.rerun()

    if st.session_state.is_finished:
        st.balloons()
        st.markdown('<div class="final-success-box">🎈👏🏻 Συγχαρητήρια!<br>Τα έμαθες όλα!</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Παίξε ξανά", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.is_finished = False
            st.rerun()
    else:
        progress_val = len(st.session_state.correct_answers) / len(all_q)
        st.progress(progress_val)
        st.markdown(f'<div class="score-box">🟦 Σωστά: {len(st.session_state
