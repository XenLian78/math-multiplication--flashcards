import streamlit as st
import random

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. CSS για 3D Flip και Slide Animation
st.markdown("""
    <style>
    .stApp { background-color: #f0f7ff; }
    
    @keyframes slideIn {
      0% { transform: translateX(-150%) rotate(-10deg); opacity: 0; }
      100% { transform: translateX(0) rotate(0deg); opacity: 1; }
    }

    .flip-card {
      background-color: transparent;
      width: 100%;
      height: 250px;
      perspective: 1000px;
      margin-top: 20px;
      margin-bottom: 20px;
      animation: slideIn 0.5s ease-out;
    }

    .flip-card-inner {
      position: relative;
      width: 100%;
      height: 100%;
      text-align: center;
      transition: transform 0.6s;
      transform-style: preserve-3d;
    }

    .do-flip { transform: rotateY(180deg); }

    .flip-card-front, .flip-card-back {
      position: absolute;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 25px;
      font-size: 55px;
      font-weight: bold;
      box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
    }

    .flip-card-front {
      background-color: white;
      color: #495057;
      border: 4px solid #a2d2ff;
    }

    .flip-card-back {
      background-color: #f0f9ff;
      color: #0077b6;
      border: 4px solid #00b4d8;
      transform: rotateY(180deg);
    }

    .score-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-size: 18px;
        border: 2px solid #bde0fe;
        color: #0077b6;
    }
    
    .stButton>button { border-radius: 15px; font-weight: bold; }
    div.stButton > button:first-child[kind="primary"] {
        background-color: #0077b6; color: white; width: 100%; height: 3.5em; font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Αρχικοποίηση Session States
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = set()
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'selected_numbers' not in st.session_state:
    st.session_state.selected_numbers = []

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# ΟΘΟΝΗ ΕΠΙΛΟΓΗΣ
if not st.session_state.game_started:
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = []
    for i in range(1, 11):
        with cols[(i-1)%5]:
            if st.checkbox(str(i), key=f"num_{i}"):
                selected.append(i)
    
    st.session_state.selected_numbers = selected

    if selected:
        st.success(f"Επιλέξατε την προπαίδεια του: **{', '.join(map(str, selected))}**")
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary"):
            st.session_state.game_started = True
            st.rerun()
    else:
        st.info("💡 Επίλεξε έναν ή περισσότερους αριθμούς από τους παραπάνω!")

# ΟΘΟΝΗ ΠΑΙΧΝΙΔΙΟΥ
else:
    selected_numbers = st.session_state.selected_numbers
    all_possible_questions = [(n, i) for n in selected_numbers for i in range(1, 11)]
    remaining_questions = [q for q in all_possible_questions if q not in st.session_state.correct_answers]

    if len(remaining_questions) == 0:
        st.balloons()
        st.success("🎉 Συγχαρητήρια! Τα έμαθες όλα!")
        if st.button("🔄 Παίξε ξανά / Άλλαξε αριθμούς"):
            st.session_state.game_started = False
            st.session_state.correct_answers = set()
            st.session_state.current_q = None
            st.rerun()
    else:
        if st.button("⬅️ Αλλαγή Αριθμών"):
            st.session_state.game_started = False
            st.rerun()

        total_q = len(all_possible_questions)
        correct_q = len(st.session_state.correct_answers)
        st.markdown(f'<div class="score-box">🟦 Έμαθες: <b>{correct_q}</b> από <b>{total_q}</b> κάρτες</div>', unsafe_allow_html=True)
        st.progress(correct_q / total_q)

        if st.session_state.current_q is None:
            st.session_state.current_q = random.choice(remaining_questions)
            st.session_state.show_answer = False

        n, i = st.session_state.current_q
        flip_class = "do-flip" if st.session_state.show_answer else ""
        
        # Το HTML της κάρτας
        st.markdown(f"""
            <div class="flip-card">
              <div class="flip-card-inner {flip_class}">
                <div class="flip-card-front">
                  {n} x {i} = ?
                </div>
                <div class="flip-card-back">
                  {n * i}
                </div>
              </div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.show_answer:
            if st.button("ΔΕΣ ΤΗΝ ΑΠΑΝΤΗΣΗ 💡"):
                st.session_state.show_answer = True
                st.rerun()
        else:
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
                    st.session_state.current_q = None
                    st.session_state.show_answer = False
                    st.rerun()
