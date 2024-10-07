import pickle
import numpy as np
import streamlit as st

# Load model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# CSS for transitions and button styles
st.markdown(
    """
    <style>
    body {
        background-color: #1a1a1a;  /* Dark background */
        color: #f0f0f0;  /* Light text color */
        font-family: 'Arial', sans-serif; /* Modern font */
    }
    h1, h2, h3, h4 {
        color: #4CAF50; /* Bright green for headings */
    }
    .container {
        text-align: center;
        margin: 50px auto;
        max-width: 600px;  /* Centered container */
        padding: 20px;
        border-radius: 10px;
        background-color: #2a2a2a; /* Slightly lighter background for the container */
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5); /* Shadow for depth */
    }
    .start-btn, .next-btn, .back-btn, .refresh-btn {
        background-color: #4CAF50; /* Button color */
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 25px; /* Rounded edges */
        font-size: 18px;
        cursor: pointer;
        margin: 20px 10px; /* Adjusted margins for side-by-side buttons */
        transition: background-color 0.3s, transform 0.2s; /* Smooth transitions */
    }
    .start-btn:hover, .next-btn:hover, .back-btn:hover, .refresh-btn:hover {
        background-color: #45a049; /* Darker on hover */
        transform: scale(1.05); /* Slightly grow */
    }
    .refresh-container img {
        cursor: pointer;
        background: none;
        border: none;
        width: 60px; /* Set refresh icon size */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initial setup for session state to control the steps
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'gender' not in st.session_state:
    st.session_state.gender = None
if 'age' not in st.session_state:
    st.session_state.age = None
if 'annual_income' not in st.session_state:
    st.session_state.annual_income = None
if 'spending_score' not in st.session_state:
    st.session_state.spending_score = None
if 'predicted' not in st.session_state:
    st.session_state.predicted = False
if 'prediction' not in st.session_state:
    st.session_state.prediction = None

# Start Button
if st.session_state.step == 0:
    st.markdown(
        """
        <div class="container">
            <h2>Welcome to the Customer Segmentation App</h2>
            <p>Click the button below to begin the process.</p>
            <button class="start-btn">Let's Get Started</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Start"):
        st.session_state.step = 1

# Step 1: Pick gender
if st.session_state.step == 1:
    st.markdown("<div class='container'><h3>Step 1: Pick your gender</h3></div>", unsafe_allow_html=True)
    gender = st.radio('Select Gender', ["Female", "Male"], index=0 if st.session_state.gender is None else st.session_state.gender)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next (Age)", key='next1'):
            st.session_state.gender = 1 if gender == "Male" else 0
            st.session_state.step = 2
    with col2:
        if st.button("Back"):
            st.session_state.step = 0

# Step 2: Pick age
if st.session_state.step == 2:
    st.markdown("<div class='container'><h3>Step 2: Pick your age</h3></div>", unsafe_allow_html=True)
    age = st.slider('Select Age', 18, 70, value=st.session_state.age if st.session_state.age is not None else 25)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next (Annual Salary)", key='next2'):
            st.session_state.age = age
            st.session_state.step = 3
    with col2:
  
