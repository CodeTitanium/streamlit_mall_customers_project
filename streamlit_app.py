import pickle
import numpy as np
import streamlit as st

# Load model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# CSS for transitions, button styles, and background image
st.markdown(
    """
    <style>
    body {
        background-image: url('background_image.jpg');  /* Set background image */
        background-size: cover;  /* Cover the entire screen */
        background-position: center;  /* Center the background */
        color: #f0f0f0;  /* Light text color */
        font-family: 'Arial', sans-serif; /* Modern font */
    }
    h1, h2, h3, h4 {
        color: #4CAF50; /* Bright green for headings */
    }
    .fade-in {
        opacity: 0;
        transition: opacity 2s ease-in;
    }
    .fade-in.visible {
        opacity: 1;
    }
    .container {
        text-align: center;
        margin: 50px auto;
        max-width: 600px;  /* Centered container */
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(42, 42, 42, 0.8); /* Slightly lighter, semi-transparent background for the container */
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5); /* Shadow for depth */
    }
    .start-btn, .refresh-btn {
        background-color: #4CAF50; /* Button color */
        color: white;
        padding: 12px 30px;
        border: none;
        border-radius: 25px; /* Rounded edges */
        font-size: 18px;
        cursor: pointer;
        margin: 20px 0;
        transition: background-color 0.3s, transform 0.2s; /* Smooth transitions */
    }
    .start-btn:hover, .refresh-btn:hover {
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

# Function to reset the app
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# Initial setup for session state to control the steps
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'predicted' not in st.session_state:
    st.session_state.predicted = False

# Start Button
if st.session_state.step == 0:
    st.markdown(
        """
        <div class="container">
            <h2>Welcome to the Customer Segmentation App</h2>
            <p>Click the button below to begin the process.</p>
            <button class="start-btn" onclick="document.getElementById('content').classList.add('visible');">Let's Get Started</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Start"):
        st.session_state.step = 1

# Step 1: Pick gender
if st.session_state.step == 1:
    st.markdown("<div class='container'><h3>Step 1: Pick your gender</h3></div>", unsafe_allow_html=True)
    gender = st.radio('Select Gender', ["Female", "Male"])
    if st.button("Next (Age)"):
        st.session_state.gender = 1 if gender == "Male" else 0
        st.session_state.step = 2

# Step 2: Pick age
if st.session_state.step == 2:
    st.markdown("<div class='container'><h3>Step 2: Pick your age</h3></div>", unsafe_allow_html=True)
    age = st.slider('Select Age', 18, 70)
    if st.button("Next (Annual Salary)"):
        st.session_state.age = age
        st.session_state.step = 3

# Step 3: Pick annual income
if st.session_state.step == 3:
    st.markdown("<div class='container'><h3>Step 3: Pick your annual salary</

