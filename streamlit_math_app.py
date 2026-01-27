import streamlit as st
import random

st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# CSS για να μοιάζει με κάρτα (Flip effect προσομοίωση)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-size: 20px; }
    .card-box {
        background-color: white;
        padding: 50px;
        border-radius: 15px;
        border: 2px solid #4CAF50;
        text-align: center;
        font-size: 60px;
        font-weight: bold;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_status_code=True)

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# 1. Επιλογή Αριθμών
numbers = st.multiselect("Με ποιους αριθμούς θα παίξουμε σήμερα;", list(range(1, 11)))

if not numbers:
    st.warning("Παρακαλώ διάλεξε τουλάχιστον έναν αριθμό για να ξεκινήσουμε!")
else:
    if 'current_q' not in st.session_state:
        st.session_state.current_q = (random.choice(numbers), random.randint(1, 10))
        st.session_state.show_answer = False

    n, i = st.session_state.current_q

    st.write(f"### Έχεις επιλέξει την προπαίδεια του: {', '.join(map(str, numbers))}")
    
    # Εμφάνιση Κάρτας
    if not st.session_state.show_answer:
        st.markdown(f'<div class="card-box">{n} x {i} = ?</div>', unsafe_allow_status_code=True)
        if st.button("Δες την Απάντηση 👈"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.markdown(f'<div class="card-box" style="color: #4CAF50;">{n * i}</div>', unsafe_allow_status_code=True)
        if st.button("Επόμενη Κάρτα ➡️"):
            st.session_state.current_q = (random.choice(numbers), random.randint(1, 10))
            st.session_state.show_answer = False
            st.rerun()
