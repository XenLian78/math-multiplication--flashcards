import streamlit as st
import random

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Math Tablet", page_icon="📱", layout="centered")

# 2. Ασφαλές CSS (χωρίς τριπλά εισαγωγικά για αποφυγή Syntax Errors)
css = "<style>"
css += "body { background-color: #eef2f5; }"
css += ".tablet-container { background: #2c2c2e; padding: 20px; border-radius: 40px; box-shadow: 0px 20px 40px rgba(0,0,0,0.3); max-width: 500px; margin: auto; border: 4px solid #3a3a3c; }"
css += ".tablet-screen { background: white; border-radius: 20px; padding: 30px; text-align: center; min-height: 350px; display: flex; flex-direction: column; justify-content: space-between; }"
css += ".question-text { font-size: 60px; font-weight: 800; color: #1c1c1e; margin-top: 20px; }"
css += ".answer-box { position: relative; background: #f2f2f7; border-radius: 15px; height: 120px; display: flex; align-items: center; justify-content: center; font-size: 50px; font-weight: bold; color: #007aff; overflow: hidden; }"
css += ".smart-cover { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #007aff; color: white; display: flex; align-items: center; justify-content: center; font-size: 40px; transition: transform 0.4s ease-in-out; z-index: 10; }"
css += ".cover-open { transform: translateY(-110%); }"
css += ".stButton>button { border-radius: 12px; height: 3em; font-weight: 600; }"
css += ".score-badge { background: #e5e5ea; padding: 5px 15px; border-radius: 20px; font-size: 14px; color: #8e8e93; }"
css += "</style>"
st.markdown(css, unsafe_allow_html=True)

# 3. Session State
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'correct_ones' not in st.session_state: st.session_state.correct_ones = set()
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'reveal' not in st.session_state: st.session_state.reveal = False
if 'nums' not in st.session_state: st.session_state.nums = []

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_active:
    st.title("📱 Math Tablet")
    st.subheader("Διάλεξε προπαίδεια:")
    cols = st.columns(5)
    selected = []
    for i in range(1, 11):
        if cols[(i-1)%5].checkbox(str(i), key=f"n{i}"):
            selected.append(i)
    
    if selected:
        if st.button("ΕΚΚΙΝΗΣΗ TABLET 🚀", type="primary", use_container_width=True):
            st.session_state.nums = selected
            st.session_state.game_active = True
            st.session_state.correct_ones = set()
            st.session_state.current_q = None
            st.rerun()
    else:
        st.info("Επίλεξε αριθμούς για να ξεκινήσεις!")

# --- ΟΘΟΝΗ ΠΑΙΧΝΙΔΙΟΥ ---
else:
    all_qs = [(n, i) for n in st.session_state.nums for i in range(1, 11)]
    todo = [q for q in all_qs if q not in st.session_state.correct_ones]

    if not todo:
        st.balloons()
        st.success("🎉 Μπράβο! Ολοκλήρωσες όλες τις ασκήσεις!")
        if st.button("Παίξε ξανά"):
            st.session_state.game_active = False
            st.rerun()
    else:
        if st.session_state.current_q is None:
            st.session_state.current_q = random.choice(todo)
            st.session_state.reveal = False

        n, i = st.session_state.current_q
        cover_class = "cover-open" if st.session_state.reveal else ""

        # Σχεδιασμός Tablet (Modern UX)
        tablet_html = f'<div class="tablet-container"><div class="tablet-screen">'
        tablet_html += f'<div class="score-badge">Πρόοδος: {len(st.session_state.correct_ones)} / {len(all_qs)}</div>'
        tablet_html += f'<div class="question-text">{n} × {i}</div>'
        tablet_html += f'<div class="answer-box"><div class="smart-cover {cover_class}">?</div>{n * i}</div>'
        tablet_html += '</div></div>'
        
        st.markdown(tablet_html, unsafe_allow_html=True)
        st.write("") 

        if not st.session_state.reveal:
            if st.button("ΔΕΣ ΤΗΝ ΑΠΑΝΤΗΣΗ 💡", type="primary", use_container_width=True):
                st.session_state.reveal = True
                st.rerun()
        else:
            c1, c2 = st.columns(2)
            if c1.button("✅ Το βρήκα!", use_container_width=True):
                st.session_state.correct_ones.add(st.session_state.current_q)
                st.session_state.current_q = None
                st.session_state.reveal = False
                st.rerun()
            if c2.button("❌ Λάθος", use_container_width=True):
                st.session_state.current_q = None
                st.session_state.reveal = False
                st.rerun()

        if st.button("⬅️ Πίσω στο Μενού", use_container_width=True):
            st.session_state.game_active = False
            st.rerun()
