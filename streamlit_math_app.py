import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. CSS για τα Animations
st.markdown("""
    <style>
    .stApp { background-color: #f0f7ff; }
    
    /* Animation Εισόδου: Zoom In */
    @keyframes zoomIn {
      0% { transform: scale(0.5); opacity: 0; }
      100% { transform: scale(1); opacity: 1; }
    }

    /* Animation Εξόδου: Slide Out προς τα δεξιά */
    @keyframes slideOut {
      0% { transform: translateX(0); opacity: 1; }
      100% { transform: translateX(150%); opacity: 0; }
    }

    .flip-card {
      background-color: transparent;
      width: 100%;
      height: 250px;
      perspective: 1000px;
      margin: 20px 0;
    }

    .zoom-in-active {
      animation: zoomIn 0.6s ease-out forwards;
    }

    .slide-out-active {
      animation: slideOut 0.7s ease-in forwards;
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
      font-size:
