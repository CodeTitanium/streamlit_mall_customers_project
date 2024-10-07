import pickle
import numpy as np
import streamlit as st

# Load model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #1a1a1a; 
        color: #f0f0f0;  
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #4CAF50; 
    }
    .container {
        text-align: center;
        margin: 50px auto;
        max-width: 600px;  
        padding: 20px;
        border-radius: 10px;
        background-color: #2a2a2a; 
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5); 
    }
    .button {
        background-color: #4CAF50; 
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 25px; 
        font-size: 18px;
        cursor: pointer;
        margin: 20px 0;
        transition: background-color 0.3s, transform 0.2s;
    }
    .button:hover {
        background-color: #45a049; 
        transform: scale(1.05); 
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Reset function
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'predicted' not in st.session_state:
    st.session_state.predicted = False

# Step navigation
def display_step():
    if st.session_state.step == 0:
        st.markdown(
            """
            <div class='container'>
                <h2>Welcome to the Customer Segmentation App</h2>
                <p>Click the button below to begin the process.</p>
                <button class="button" onclick="document.getElementById('start').click();">Let's Get Started</button>
                <form action="" method="get">
               
