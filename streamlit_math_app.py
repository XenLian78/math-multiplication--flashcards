import streamlit as st
import random

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. CSS για Animations και Fixes
css_code = """
<style>
.stApp { background-color: #f0f7ff; }

/* Slide In μόνο για την πρώτη κάρτα */
@keyframes slideInLeft {
    0% { transform: translateX(-150%) rotate(-10deg); opacity: 0; }
    100% { transform: translateX(0) rotate(0deg); opacity: 1; }
}

/* Slide Out μόνο για την τελευταία κάρτα */
@keyframes slideOutRight {
    0% { transform: translateX(0); opacity: 1; }
    100% { transform: translateX(150%) rotate(10deg); opacity: 0; }
}

.flip-card { background-color: transparent; width: 100%; height: 250px; perspective: 1000px; margin: 20px 0; }

.first-card-anim { animation: slideInLeft 0.8s ease-out forwards; }
.last-card-anim { animation: slideOutRight 0.8s ease-in forwards; }

.flip-card-inner { 
    position: relative; width: 100%; height: 100%; text-align: center; 
    transition: transform 0.6s; transform-style: preserve-3d; 
}

.do-flip { transform: rotateY(180deg); }

.flip-card-front, .flip-card-back { 
    position: absolute; width: 100%; height: 100%; backface-visibility: hidden; 
    display: flex; align-items: center; justify-content: center; border-radius: 25px; 
    font-size: 55px; font-weight: bold; box-shadow: 0px 8px 16px rgba(0,0,0,0.1); 
}

.flip-card-front { background-color: white; color: #495057; border: 4px solid #a2d2ff; }
.flip-card-back { 
    background-color: #f0f9ff; color: #0077b6; border: 4px solid #00b4d8; 
    transform: rotateY(180deg); 
}

/* Opacity Masking για το "τυφλό" Reset */
.hiding-content { opacity: 0; transition: opacity 0.1s; }

.score-box { 
    background-color: white; padding: 15px; border-radius: 12px; text-align: center; 
    font-size: 18px; border: 2px solid #bde0fe; color: #0077b6; margin-bottom: 10px; 
}
.stButton>button { border-radius: 15px; font-weight: bold; }
div.stButton > button:first-child[kind="primary"] { 
    background-color: #0077b6; color: white; width: 100%; height: 3.5em; font-size: 22px; 
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
if 'is_transitioning' not in st.session_state: st.session_state.is_transitioning = False

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# --- ΟΘΟΝΗ ΕΠΙΛΟΓΗΣ ---
if not st.session_state.game_started:
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    cols = st.columns(5)
    selected = []
    for i in range(1, 11):
        if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}"):
            selected.append(i)
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
        st.info("💡 Επίλεξε αριθμούς για να ξεκινήσεις!")

# --- ΟΘΟΝΗ ΠΑΙΧΝΙΔΙΟΥ ---
else:
    all_q = [(n, i) for n in st.session_state.selected_numbers for i in range(1, 11)]
    rem_q = [q for q in all_q if q not in st.session_state.correct_answers]

    if not rem_q and not st.session_state.is_finished:
        st.session_state.is_finished = True
        st.rerun()

    if st.session_state.is_finished:
        st.markdown('<div class="flip-card last-card-anim"></div>', unsafe_allow_html=True)
        st.balloons()
        st.success("🎉 Συγχαρητήρια! Τα έμαθες όλα!")
        if st.button("🔄 Παίξε ξανά", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
    else:
        # Μπάρα Εξέλιξης
        progress_val = len(st.session_state.correct_answers) / len(all_q)
        st.progress(progress_val)
        st.markdown(f'<div class="score-box">🟦 Σωστά: {len(st.session_state.correct_answers)} / {len(all_q)}</div>', unsafe_allow_html=True)
        
        if st.session_state.current_q is None:
            st.session_state.current_q = random.choice(rem_q)
            st.session_state.show_answer = False
            st.session_state.card_id += 1
            st.session_state.is_transitioning = False # Reset το masking

        n, i = st.session_state.current_q
        
        anim_class = "first-card-anim" if len(st.session_state.correct_answers) == 0 else ""
        f_class = "do-flip" if st.session_state.show_answer else ""
        
        # Εφαρμογή του Masking αν αλλάζουμε ερώτηση
        hide_class = "hiding-content" if st.session_state.is_transitioning else ""

        st.markdown(f'''
            <div class="flip-card {anim_class}" id="card_container_{st.session_state.card_id}">
              <div class="flip-card-inner {f_class}">
                <div class="flip-card-front {hide_class}">{n} x {i} = ?</div>
                <div class="flip-card-back {hide_class}">{n * i}</div>
              </div>
            </div>
