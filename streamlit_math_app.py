import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Μαθαίνω την Προπαίδεια", page_icon="🧮")

# 2. CSS για τα Animations
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
      animation: slideIn 0.7s ease-out forwards;
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
      font-size: 55px;
      font-weight: bold;
      box-shadow: 0px 8px 16px rgba(0,0,0,0.1
