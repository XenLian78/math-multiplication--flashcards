import streamlit as st
import random

# Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# CSS για την εμφάνιση της κάρτας
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .card-box {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        border: 3px solid #4CAF50;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #333;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
        margin: 20px 0px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# 1. Επιλογή Αριθμών
st.subheader("Ρυθμίσεις")
numbers = st.multiselect("Με ποιους αριθμούς θα παίξουμε σήμερα;", list(range(1, 11)))

if not numbers:
    st.info("👈 Διάλεξε από πάνω τους αριθμούς που θέλεις να μάθεις!")
else:
    # Αρχικοποίηση μεταβλητών στην πρώτη εκτέλεση
    if 'current_q' not in st.session_state:
        st.session_state.current_q = (random.choice(numbers), random.randint(1, 10))
        st.session_state.show_answer = False

    n, i = st.session_state.current_q
    
    st.success(f"Παίζουμε με την προπαίδεια του: {', '.join(map(str, numbers))}")

    # Εμφάνιση Κάρτας
    if not st.session_state.show_answer:
        st.markdown(f'<div class="card-box">{n} x {i} = ?</div>', unsafe_allow_html=True)
        if st.button("ΔΕΣ ΤΗΝ ΑΠΑΝΤΗΣΗ"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.markdown(f'<div class="card-box" style="color: #2E7D32; background-color: #E8F5E9;">{n * i}</div>', unsafe_allow_html=True)
        if st.button("ΕΠΟΜΕΝΗ ΕΡΩΤΗΣΗ ➡️"):
            # Επιλογή νέας τυχαίας ερώτησης
            st.session_state.current_q = (random.choice(numbers), random.randint(1, 10))
            st.session_state.show_answer = False
            st.rerun()
