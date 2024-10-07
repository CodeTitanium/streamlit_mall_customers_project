# Streamlit imports
import pickle
import streamlit as st

# Load model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# CSS for transitions and button styles
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
    .fade-in {
        opacity: 0;
        transition: opacity 1.5s ease-in-out;
    }
    .fade-in.visible {
        opacity: 1;
    }
    .slide-in {
        transform: translateX(-100%);
        transition: transform 1.5s ease-in-out;
    }
    .slide-in.visible {
        transform: translateX(0);
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
    .start-btn, .next-btn {
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
    .start-btn:hover, .next-btn:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adding script for class toggling
st.markdown(
    """
    <script>
    function showContent() {
        document.querySelectorAll('.fade-in, .slide-in').forEach((el) => {
            el.classList.add('visible');
        });
    }
    document.addEventListener("DOMContentLoaded", function() {
        showContent();
    });
    </script>
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

# Use a container for the content and transitions
if st.session_state.step == 0:
    st.markdown(
        """
        <div class="container fade-in">
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
    st.markdown(
        """
        <div class="container slide-in">
            <h3>Step 1: Pick your gender</h3>
            <button class="next-btn">Next (Age)</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    gender = st.radio('Select Gender', ["Female", "Male"])
    if st.button("Next (Age)"):
        st.session_state.gender = 1 if gender == "Male" else 0
        st.session_state.step = 2
        st.experimental_rerun()  # Rerun to trigger transition

# Ensure you have animations or transitions on each necessitated step
