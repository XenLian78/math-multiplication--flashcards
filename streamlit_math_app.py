import streamlit as st
import random

# Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# CSS για την εμφάνιση
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .card-box {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        border: 3px solid #4CAF50;
        text-align: center;
        font-size: 55px;
        font-weight: bold;
        color: #333;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
        margin: 20px 0px;
    }
    .score-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# 1. Αρχικοποίηση Session States
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = set() # Αποθήκευση μοναδικών σωστών απαντήσεων
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# 2. Επιλογή Αριθμών
numbers = st.multiselect("Με ποιους αριθμούς θα παίξουμε σήμερα;", list(range(1, 11)), key="numbers_select")

# Δημιουργία όλων των πιθανών συνδυασμών για τους επιλεγμένους αριθμούς
all_possible_questions = [(n, i) for n in numbers for i in range(1, 11)]
remaining_questions = [q for q in all_possible_questions if q not in st.session_state.correct_answers]

if not numbers:
    st.info("👈 Διάλεξε από πάνω τους αριθμούς που θέλεις να μάθεις!")
    st.session_state.correct_answers = set()
    st.session_state.current_q = None
elif len(remaining_questions) == 0:
    st.balloons()
    st.success("🎉 Συγχαρητήρια! Έμαθες όλες τις κάρτες για τους αριθμούς που διάλεξες!")
    if st.button("Παίξε ξανά από την αρχή"):
        st.session_state.correct_answers = set()
        st.session_state.current_q = None
        st.rerun()
else:
    # Εμφάνιση Προόδου
    total_q = len(all_possible_questions)
    correct_q = len(st.session_state.correct_answers)
    st.markdown(f"""
        <div class="score-box">
            ✅ Έμαθες: <b>{correct_q}</b> από <b>{total_q}</b> κάρτες
        </div>
    """, unsafe_allow_html=True)
    st.progress(correct_q / total_q)

    # Επιλογή νέας ερώτησης αν δεν υπάρχει ήδη
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
        st.markdown(f'<div class="card-box" style="color: #2E7D32; background-color: #E8F5E9;">{n * i}</div>', unsafe_allow_html=True)
        
        st.write("Πώς τα πήγες;")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Το βρήκες! ✅"):
                st.session_state.correct_answers.add(st.session_state.current_q)
                st.session_state.current_q = None # Θα επιλεγεί νέα στο επόμενο run
                st.session_state.show_answer = False
                st.rerun()
        
        with col2:
            if st.button("Ξαναπροσπάθησε 😉"):
                # Απλά αλλάζουμε ερώτηση χωρίς να την προσθέσουμε στα σωστά
                st.session_state.current_q = random.choice(remaining_questions)
                st.session_state.show_answer = False
                st.rerun()

    if st.button("Μηδενισμός Προόδου 🔄"):
        st.session_state.correct_answers = set()
        st.session_state.current_q = None
        st.rerun()
