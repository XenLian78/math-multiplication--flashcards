import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Math Tablet", page_icon="📱", layout="centered")

# 2. CSS για το Modern Tablet UI
st.markdown("""
<style>
    .stApp { background-color: #eef2f5; }
    
    /* Το σώμα του Tablet */
    .tablet-container {
        background: #2c2c2e;
        padding: 20px;
        border-radius: 40px;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.3);
        max-width: 500px;
        margin: auto;
        border: 4px solid #3a3a3c;
    }
    
    /* Η οθόνη του Tablet */
    .tablet-screen {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        min-height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .question-text {
        font-size: 60px;
        font-weight: 800;
        color: #1c1c1e;
        margin-top: 20px;
    }

    /* Το πλαίσιο της απάντησης */
    .answer-box {
        position: relative;
        background: #f2f2f7;
        border-radius:
