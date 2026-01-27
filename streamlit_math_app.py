import streamlit as st
import random

# Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# CSS για την εμφάνιση με Παλ Μπλε αποχρώσεις
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
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# 1. Αρχικοποίηση Session States
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = set()
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# 2. Επιλογή Αριθμών με Ελληνικό Placeholder
numbers = st.multiselect(
    "Με ποιους αριθμούς θα παίξουμε σήμερα;", 
    list(range(1, 11)), 
    key="numbers_select",
    placeholder="Επίλεξε έναν ή περισσότερους αριθμούς"
)

all_possible_questions = [(n, i) for n in numbers for i in range(1, 11)]
remaining_questions = [q for q in all_possible_questions if q not in st.session_state.correct_answers]

if not numbers:
    st.info("👈 Διάλεξε από πάνω τους αριθμούς που θέλεις να μάθεις!")
    st.session_state.correct_answers = set()
    st.session_state.current_q = None
elif len(remaining_questions) == 0:
    st.balloons()
    st.success("🎉 Συγχαρητήρια! Έμαθες όλες τις κάρτες!")
    if st.button("Παίξε ξανά από την αρχή"):
        st.session_state.correct_answers = set()
        st.session_state.current_q = None
        st.rerun()
else:
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
        st.markdown(f'<div class="card-box" style="border-color: #a2d2ff;">{n} x {i} = ?</div>', unsafe_allow_html=True)
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

    if st.button("Μηδενισμός Προόδου 🔄"):
        st.session_state.correct_answers = set()
        st.session_state.current_q = None
        st.rerun()
