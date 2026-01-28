import streamlit as st
import random

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. AMINATION CSS 
css_code = "<style>"
css_code += ".stApp { background-color: #f0f7ff; }"

# FADE IN
css_code += "@keyframes fadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }"

# Animations για αρχή και τέλος (λίγο πιο αργά - 1.0s)
css_code += "@keyframes slideInLeft { 0% { transform: translateX(-150%) rotate(-10deg); opacity: 0; } 100% { transform: translateX(0) rotate(0deg); opacity: 1; } }"
css_code += "@keyframes slideOutRight { 0% { transform: translateX(0); opacity: 1; } 100% { transform: translateX(150%) rotate(10deg); opacity: 0; } }"

# CARD STYLE
css_code += ".main-card { background-color: transparent; width: 100%; height: 250px; perspective: 1000px; margin: 20px 0; }"

# FADE IN TIME LAP
css_code += ".fade-anim { animation: fadeIn 1s ease-out forwards; }"
css_code += ".first-card-anim { animation: slideInLeft 1.0s ease-out forwards; }"
css_code += ".last-card-anim { animation: slideOutRight 1.0s ease-in forwards; }"

# CARD
css_code += ".card-content { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; border-radius: 25px; font-size: 55px; font-weight: bold; box-shadow: 0px 8px 16px rgba(0,0,0,0.1); border: 4px solid; transition: background-color 0.5s ease; }"

# CARD COLORS
css_code += ".front-style { background-color: white; color: #495057; border-color: #a2d2ff; }"
css_code += ".back-style { background-color: #f0f9ff; color: #0077b6; border-color: #00b4d8; }"

css_code += ".score-box { background-color: white; padding: 15px; border-radius: 12px; text-align: center; font-size: 18px; border: 2px solid #bde0fe; color: #0077b6; margin-bottom: 10px; }"
css_code += ".stButton>button { border-radius: 15px; font-weight: bold; }"
css_code += "div.stButton > button:first-child[kind='primary'] { background-color: #0077b6; color: white; width: 100%; height: 3.5em; font-size: 22px; }"
css_code += "</style>"

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
        st.info("💡 Επίλεξε αριθμούς για να ξεκινήσεις!")

# --- GAME PAGE ---
else:
    all_q = [(n, i) for n in st.session_state.selected_numbers for i in range(1, 11)]
    rem_q = [q for q in all_q if q not in st.session_state.correct_answers]

    if not rem_q and not st.session_state.is_finished:
        st.session_state.is_finished = True
        st.rerun()

    if st.session_state.is_finished:
        st.markdown('<div class="main-card last-card-anim"></div>', unsafe_allow_html=True)
        st.balloons()
        st.success("🎉 Συγχαρητήρια! Τα έμαθες όλα!")
        if st.button("🔄 Παίξε ξανά", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
    else:
        # PROGRESS BAR
        progress_val = len(st.session_state.correct_answers) / len(all_q)
        st.progress(progress_val)
        st.markdown(f'<div class="score-box">🟦 Σωστά: {len(st.session_state.correct_answers)} / {len(all_q)}</div>', unsafe_allow_html=True)
        
        if st.session_state.current_q is None:
            st.session_state.current_q = random.choice(rem_q)
            st.session_state.show_answer = False
            st.session_state.card_id += 1

        n, i = st.session_state.current_q
        
        # ANIMATION (SlideIn για την 1η, FadeIn για όλες τις άλλες)
        anim_class = "first-card-anim" if len(st.session_state.correct_answers) == 0 else "fade-anim"
            
        # Επιλογή Στυλ και Περιεχομένου
        if not st.session_state.show_answer:
            card_content = str(n) + " x " + str(i) + " = ?"
            card_style = "front-style"
        else:
            card_content = str(n * i)
            card_style = "back-style"

        # HTML με Double-ID για μηδενικό glitch
        card_html = '<div class="main-card ' + anim_class + '" id="card_' + str(st.session_state.card_id) + '_' + str(st.session_state.show_answer) + '">'
        card_html += '<div class="card-content ' + card_style + '">' + card_content + '</div>'
        card_html += '</div>'
        
        st.markdown(card_html, unsafe_allow_html=True)

        if not st.session_state.show_answer:
            if st.button("ΔΕΣ ΤΗΝ ΑΠΑΝΤΗΣΗ 💡", use_container_width=True, type="primary"):
                st.session_state.show_answer = True
                st.rerun()
        else:
            c1, c2 = st.columns(2)
            if c1.button("Το βρήκες! ✅", use_container_width=True):
                st.session_state.correct_answers.add(st.session_state.current_q)
                st.session_state.current_q = None
                st.rerun()
            if c2.button("Ξαναπροσπάθησε 😉", use_container_width=True):
                st.session_state.current_q = None
                st.rerun()

        st.write("")
        if st.button("⬅️ Αλλαγή Αριθμών", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
