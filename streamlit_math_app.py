import streamlit as st
import random

# Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# CSS για την εμφάνιση με Παλ Μπλε αποχρώσεις
st.markdown("""
    <style>
    .stApp { background-color: #f0f7ff; } /* Πολύ ανοιχτό γαλάζιο φόντο */
    .card-box {
        background-color: white;
        padding: 40px;
        border-radius: 25px;
        border: 4px solid #a2d2ff; /* Παλ μπλε περίγραμμα */
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
    /* Αλλαγή χρώματος στα κουμπιά */
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

# 2. Επιλογή Αριθμών
numbers = st.multiselect("Με ποιους αριθμούς θα παίξουμε σήμερα;", list(range(1, 11)), key="numbers_select")

all_possible_questions = [(n, i) for n in numbers for i in range(1, 11)]
remaining_questions = [q for q in all_possible_questions if q not in st.session_state.correct_answers]

if not numbers:
    st.info("👈 Διάλεξε από πάνω τους αριθμούς που θέλεις να μάθεις!")
    st.session_state.correct_answers = set()
    st.session_state.current_q = None
elif len(remaining_questions) == 0:
