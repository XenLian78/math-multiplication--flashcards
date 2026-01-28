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
.first-card-anim { animation: slide
