import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. CSS για 3D Flip, Slide In και Slide Out
st.markdown("""
    <style>
    .stApp { background-color: #f0f7ff; }
    
    @keyframes slideIn {
      0% { transform: translateX(-150%) rotate(-10deg); opacity: 0; }
      100% { transform: translateX(0) rotate(0deg); opacity: 1; }
    }

    @keyframes slideOut {
      0% { transform: translateX(0) rotate(0deg); opacity: 1; }
      100% { transform: translateX(150%) rotate(10deg); opacity: 0; }
    }

    .flip-card {
      background-color: transparent;
      width: 100%;
      height: 250px;
      perspective: 1000px;
      margin-top: 20px;
      margin-bottom: 20px;
    }

    .slide-in-active {
      animation: slideIn 0.6s ease-out forwards;
    }

    .slide-out-active {
      animation: slideOut 0.6s ease-in forwards !important;
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
if 'is_exiting' not in st.session_state:
    st.session_state.is_exiting = False

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

    if not remaining_questions:
        st.balloons()
        st.success("🎉 Συγχαρητήρια! Τα έμαθες όλα!")
        if st.button("🔄 Παίξε ξανά"):
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

        # Επιλογή νέας ερώτησης αν δεν υπάρχει
        if st.session_state.current_q is None:
            st.session_state.current_q = random.choice(remaining_questions)
            st.session_state.show_answer = False
            st.session_state.is_exiting = False

        n, i = st.session_state.current_q
        
        # Καθορισμός κλάσεων animation
        flip_class = "do-flip" if st.session_state.show_answer else ""
        animation_class = "slide-out-active" if st.session_state.is_exiting else "slide-in-active"
        
        # HTML Κάρτας
        st.markdown(f"""
            <div class="flip-card {animation_class}">
              <div class="flip-card-inner {flip_class}">
                <div class="flip-card-front">{n} x {i} = ?</div>
                <div class="flip-card-back">{n * i}</div>
              </div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.show_answer and not st.session_state.is_exiting:
            if st.button("ΔΕΣ ΤΗΝ ΑΠΑΝΤΗΣΗ 💡"):
                st.session_state.show_answer = True
                st.rerun()
        elif st.session_state.show_answer and not st.session_state.is_exiting:
            st.write("Πώς τα πήγες;")
            col1, col2 = st.columns(2)
            
            if col1.button("Το βρήκες! ✅"):
                st.session_state.is_exiting = True
                # Πρώτα προσθέτουμε στα σωστά
                st.session_state.correct_answers.add(st.session_state.current_q)
                st.rerun()
            
            if col2.button("Ξαναπροσπάθησε 😉"):
                st.session_state.is_exiting = True
                st.rerun()

        # Η κρίσιμη διόρθωση: 
        # Όταν η κάρτα είναι σε φάση Slide Out, περιμένουμε και μετά ΜΗΔΕΝΙΖΟΥΜΕ τα πάντα
        if st.session_state.is_exiting:
            time.sleep(0.6)
            st.session_state.current_q = None # Αυτό θα προκαλέσει επιλογή νέας ερώτησης στο επόμενο rerun
            st.session_state.show_answer = False # Η νέα κάρτα θα ξεκινήσει από την "μπροστά" πλευρά
            st.session_state.is_exiting = False
            st.rerun()
