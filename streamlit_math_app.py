import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. CSS (Συμπτυγμένο σε f-string για να αποφύγουμε Syntax Errors)
css = """<style>
.stApp { background-color: #f0f7ff; }
@keyframes zoomIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
@keyframes slideOut { 0% { transform: translateX(0); opacity: 1; } 100% { transform: translateX(150%); opacity: 0; } }
.flip-card { background-color: transparent; width: 100%; height: 250px; perspective: 1000px; margin: 20px 0; }
.zoom-in-active { animation: zoomIn 0.6s ease-out forwards; }
.slide-out-active { animation: slideOut 0.7s ease-in forwards; }
.flip-card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s; transform-style: preserve-3d; }
.do-flip { transform: rotateY(180deg); }
.flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; align-items: center; justify-content: center; border-radius: 25px; font-size: 55px; font-weight: bold; box-shadow: 0px 8px 16px rgba(0,0,0,0.1); }
.flip-card-front { background-color: white; color: #495057; border: 4px solid #a2d2ff; }
.flip-card-back { background-color: #f0f9ff; color: #0077b6; border: 4px solid #00b4d8; transform: rotateY(180deg); }
.score-box { background-color: white; padding: 15px; border-radius: 12px; text-align: center; font-size: 18px; border: 2px solid #bde0fe; color: #0077b6; }
.stButton>button { border-radius: 15px; font-weight: bold; }
div.stButton > button:first-child[kind="primary"] { background-color: #0077b6; color: white; width: 100%; height: 3.5em; font-size: 22px; }
</style>"""
st.markdown(css, unsafe_allow_html=True)

# 3. Session State
if 'game_started' not in st.session_state: st.session_state.game_started = False
if 'correct_answers' not in st.session_state: st.session_state.correct_answers = set()
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'show_answer' not in st.session_state: st.session_state.show_answer = False
if 'selected_numbers' not in st.session_state: st.session_state.selected_numbers = []
if 'is_exiting' not in st.session_state: st.session_state.is_exiting = False
if 'card_id' not in st.session_state: st.session_state.card_id = 0

st.title("🧮 Το παιχνίδι της Προπαίδειας")

# --- ΟΘΟΝΗ ΕΠΙΛΟΓΗΣ ---
if not st.session_state.game_started:
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    cols = st.columns(5)
    selected = []
    for i in range(1, 11):
        with cols[(i-1)%5]:
            if st.checkbox(str(i), key=f"s_{i}"): selected.append(i)
    st.session_state.selected_numbers = selected
    if selected:
        st.success(f"Επιλέξατε την προπαίδεια του: {selected}")
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary"):
            st.session_state.game_started = True
            st.rerun()
    else: st.info("💡 Επίλεξε αριθμούς!")

# --- ΟΘΟΝΗ ΠΑΙΧΝΙΔΙΟΥ ---
else:
    all_q = [(n, i) for n in st.session_state.selected_numbers for i in range(1, 11)]
    rem_q = [q for q in all_q if q not in st.session_state.correct_answers]

    if not rem_q and not st.session_state.is_exiting:
        st.balloons()
        st.success("🎉 Συγχαρητήρια!")
        if st.button("🔄 Ξανά"):
            st.session_state.game_started = False
            st.session_state.correct_answers = set()
            st.rerun()
    else:
        # Σκορ
        st.markdown(f'<div class="score-box">🟦 Σκορ: {len(st.session_state.correct_answers)} / {len(all_q)}</div>', unsafe_allow_html=True)
        
        if st.session_state.current_q is None:
            st.session_state.current_q = random.choice(rem_q)
            st.session_state.show_answer = False
            st.session_state.is_exiting = False
            st.session_state.card_id += 1

        n, i = st.session_state.current_q
        f_class = "do-flip" if st.session_state.show_answer else ""
        a_class = "slide-out-active" if st.session_state.is_exiting else "zoom-in-active"

        # HTML Κάρτας
        st.markdown(f'''
            <div class="flip-card {a_class}" id="card_{st.session_state.card_id}">
              <div class="flip-card-inner {f_class}">
                <div class="flip-card-front">{n} x {i} = ?</div>
                <div class="flip-card-back">{n * i}</div>
              </div>
            </div>
        ''', unsafe_allow_html=True)

        if not st.session_state.show_answer and not st.session_state.is_exiting:
            if st.button("ΔΕΣ ΤΗΝ ΑΠΑΝΤΗΣΗ 💡"):
                st.session_state.show_answer = True
                st.rerun()
        elif st.session_state.show_answer and not st.session_state.is_exiting:
            c1, c2 = st.columns(2)
            if c1.button("Το βρήκες! ✅"):
                st.session_state.correct_answers.add(st.session_state.current_q)
                st.session_state.is_exiting = True
                st.rerun()
            if c2.button("Ξαναπροσπάθησε 😉"):
                st.session_state.is_exiting = True
                st.rerun()

        if st.session_state.is_exiting:
            time.sleep(0.7)
            st.session_state.current_q = None
            st.session_state.show_answer = False
            st.rerun()

        if st.button("⬅️ Αλλαγή"):
            st.session_state.game_started = False
            st.rerun()
