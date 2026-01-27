import streamlit as st
import random

# Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# CSS για την εμφάνιση
st.markdown("""
    <style>
    .stApp { background-color: #f0f7ff; }
    .card-box {
        background-color: white;
        padding: 40px;
        border-radius: 25px;
        border: 4px solid #a2d2ff;
        text-align: center;
        font-size: 55px;
        font-weight: bold;
        color: #495057;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.05);
        margin: 20px 0px;
    }
    .score-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-size: 18px;
        border: 2px solid #bde0fe;
        color: #0077b6;
        margin-bottom: 10px;
    }
    .stButton>button {
        border-radius: 15px;
        font-weight: bold;
    }
    /* Στυλ για το κουμπί Ξεκινάμε */
    div.stButton > button:first-child[kind="primary"] {
        background-color: #0077b6;
        color: white;
        width: 100%;
        height: 3em;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Αρχικοποίηση Session States
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = set()
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# ΟΘΟΝΗ ΕΠΙΛΟΓΗΣ (Αν το παιχνίδι ΔΕΝ έχει ξεκινήσει)
if not st.session_state.game_started:
    st.subheader("Ρυθμίσεις Παιχνιδιού")
    numbers = st.multiselect(
        "Με ποιους αριθμούς θα παίξουμε σήμερα;", 
        list(range(1, 11)), 
        key="numbers_select",
        placeholder="Επίλεξε αριθμό/ους"
    )
    
    if numbers:
        st.write(f"✅ Επιλέξατε την προπαίδεια του: {', '.join(map(str, numbers))}")
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary"):
            st.session_state.game_started = True
            st.rerun()
    else:
        st.info("👈 Διάλεξε τους αριθμούς για να εμφανιστεί το κουμπί έναρξης!")

# ΟΘΟΝΗ ΠΑΙΧΝΙΔΙΟΥ (Αν το παιχνίδι ΕΧΕΙ ξεκινήσει)
else:
    # Παίρνουμε τους αριθμούς από το widget (χρησιμοποιώντας το key)
    selected_numbers = st.session_state.numbers_select
    
    all_possible_questions = [(n, i) for n in selected_numbers for i in range(1, 11)]
    remaining_questions = [q for q in all_possible_questions if q not in st.session_state.correct_answers]

    if len(remaining_questions) == 0:
        st.balloons()
        st.success("🎉 Συγχαρητήρια! Έμαθες όλες τις κάρτες!")
        if st.button("Παίξε ξανά / Άλλαξε αριθμούς"):
            st.session_state.game_started = False
            st.session_state.correct_answers = set()
            st.session_state.current_q = None
            st.rerun()
    else:
        # Κουμπί επιστροφής στις ρυθμίσεις
        if st.button("⬅️ Αλλαγή Αριθμών"):
            st.session_state.game_started = False
            st.rerun()

        # Εμφάνιση Προόδου
        total_q = len(all_possible_questions)
        correct_q = len(st.session_state.correct_answers)
        st.markdown(f'<div class="score-box">🟦 Έμαθες: <b>{correct_q}</b> από <b>{total_q}</b> κάρτες</div>', unsafe_allow_html=True)
        st.progress(correct_q / total_q)

        # Επιλογή νέας ερώτησης
        if st.session_state.current_q is None or st.session_state.current_q not in remaining_questions:
            st.session_state.current_q = random.choice(remaining_questions)
            st.session_state.show_answer = False

        n, i = st.session_state.current_q
        
        # Εμφάνιση Κάρτας
        if not st.session_state.show_answer:
            st.markdown(f'<div class="card-box">{n} x {i} = ?</div>', unsafe_allow_html=True)
            if st.button("ΔΕΣ ΤΗΝ ΑΠΑΝΤΗΣΗ 💡"):
                st.session_state.show_answer = True
                st.rerun()
        else:
            st.markdown(f'<div class="card-box" style="color: #0077b6; background-color: #f0f9ff; border-color: #00b4d8;">{n * i}</div>', unsafe_allow_html=True)
            
            st.write("Πώς τα πήγες;")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Το βρήκες! ✅"):
                    st.session_state.correct_answers.add(st.session_state.current_q)
                    st.session_state.current_q = None
                    st.session_state.show_answer = False
                    st.rerun()
            with col2:
                if st.button("Ξαναπροσπάθησε 😉"):
                    st.session_state.current_q = random.choice(remaining_questions)
                    st.session_state.show_answer = False
                    st.rerun()
