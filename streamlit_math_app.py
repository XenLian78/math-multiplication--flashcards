import streamlit as st
import random

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. AMINATION CSS 
css_code = "<style>"
css_code += ".stApp { background-color: #f0f7ff; }"
css_code += "@keyframes fadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }"
css_code += "@keyframes slideInLeft { 0% { transform: translateX(-150%) rotate(-10deg); opacity: 0; } 100% { transform: translateX(0) rotate(0deg); opacity: 1; } }"
css_code += "@keyframes slideOutRight { 0% { transform: translateX(0); opacity: 1; } 100% { transform: translateX(150%) rotate(10deg); opacity: 0; } }"
css_code += ".main-card { background-color: transparent; width: 100%; height: 250px; perspective: 1000px; margin: 20px 0; }"
css_code += ".fade-anim { animation: fadeIn 2.5s ease-out forwards; }"
css_code += ".first-card-anim { animation: slideInLeft 2.5s ease-out forwards; }"
css_code += ".last-card-anim { animation: slideOutRight 2.5s ease-in forwards; }"
css_code += ".card-content { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; border-radius: 25px; font-size: 55px; font-weight: bold; box-shadow: 0px 8px 16px rgba(0,0,0,0.1); border: 4px solid; transition: background-color 0.5s ease; }"
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
            st.
