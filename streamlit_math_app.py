import streamlit as st
import random

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮", layout="centered")

# 2. CSS για Animations και Responsive Layout
css_code = """
<style>
.stApp { background-color: #f0f7ff; }

/* Animations */
@keyframes textFadeIn {
    0% { opacity: 0; filter: blur(5px); }
    100% { opacity: 1; filter: blur(0px); }
}
@keyframes slideInLeft {
    0% { transform: translateX(-150%) rotate(-10deg); opacity: 0; }
    100% { transform: translateX(0) rotate(0deg); opacity: 1; }
}
@keyframes boxFade {
    0% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* Responsive Κάρτα */
.main-card {
    background-color: transparent;
    width: 100%;
    max-width: 500px;
    margin: 20px auto;
    perspective: 1000px;
}

.card-content {
    width: 100%;
    aspect-ratio: 16 / 9;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 25px;
    font-weight: bold;
    box-shadow: 0px 8px 16px rgba(0,0,0,0.1);
    border: 4px solid;
    font-size: clamp(40px, 10vw, 70px); 
}

.slow-text-fade { animation: textFadeIn 1s ease-out forwards; }
.box-anim { animation: boxFade 1.5s ease-in-out; }
.first-card-anim { animation: slideInLeft 2s ease-out forwards; }

.front-style { background-color: white; color: #495057; border-color: #a2d2ff; }
.back-style { background-color: #f0f9ff; color: #0077b6; border-color: #00b4d8; }

/* Τελικό Πλαίσιο - Responsive & Τετράγωνο */
.final-success-box {
    background-color: #f0f9ff;
    color: #0077b6;
    border: 8px solid #00b4d8;
    border-radius: 30px;
    width: 100%;
    max-width: 500px;
    margin: 10px auto;
    aspect-ratio: 1 / 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: clamp(30px, 8vw, 55px);
    font-weight: bold;
    box-shadow: 0px 15px 30px rgba(0,0,0,0.2);
    animation: textFadeIn 1.5s ease-out;
}

.score-box {
    background-color: white;
    padding: 10px;
    border-radius: 12px;
    text-align: center;
    font-size: 16px;
    border: 2px solid #bde0fe;
    color: #0077b6;
    margin-bottom: 10px;
}

/* Διόρθωση Χρώματος Κουμπιών */
div.stButton > button {
    border-radius: 15px;
