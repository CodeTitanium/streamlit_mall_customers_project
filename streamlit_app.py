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

# Start the app flow
if st.session_state.step == 0:
    st.markdown(
        """
        <div class='container'>
            <h2>Welcome to the Customer Segmentation App</h2>
            <p>Click the button below to begin the process.</p>
            <button class="button" id="start-button" onclick="document.getElementById('start').click();">Let's Get Started</button>
            <form action="" method="get">
                <button id="start" style="display:none;" type="submit">Start</button>
            </form>
        </div>
        """,
        unsafe_allow_html=True
    )

# Handling the Start button action
if st.button("Start", key='start', help="Click to begin"):
    st.session_state.step = 1

# Step navigation
if st.session_state.step == 1:
    st.markdown("<div class='container'><h3>Step 1: Pick your gender</h3></div>", unsafe_allow_html=True)
    gender = st.radio('Select Gender', ["Female", "Male"])
    if st.button("Next (Age)"):
        st.session_state.gender = 1 if gender == "Male" else 0
        st.session_state.step = 2

elif st.session_state.step == 2:
    st.markdown("<div class='container'><h3>Step 2: Pick your age</h3></div>", unsafe_allow_html=True)
    age = st.slider('Select Age', 18, 70)
    if st.button("Next (Annual Salary)"):
        st.session_state.age = age
        st.session_state.step = 3

elif st.session_state.step == 3:
    st.markdown("<div class='container'><h3>Step 3: Pick your annual salary</h3></div>", unsafe_allow_html=True)
    annual_income = st.slider('Select Annual Salary in Thousands', 15, 137)
    if st.button("Next (Spending Score)"):
        st.session_state.annual_income = annual_income
        st.session_state.step = 4

elif st.session_state.step == 4:
    st.markdown("<div class='container'><h3>Step 4: Pick your spending score</h3></div>", unsafe_allow_html=True)
    spending_score = st.slider('Select Spending Score', 0, 100)
    if st.button("Predict Customer Segment"):
        st.session_state.spending_score = spending_score
        user_input = np.array([[st.session_state.gender, st.session_state.age, st.session_state.annual_income, st.session_state.spending_score]])
        user_input_scaled = scaler.transform(user_input)
        customer_group = model.predict(user_input_scaled)
        st.session_state.predicted = True
        st.session_state.prediction = customer_group[0]
        st.session_state.step = 5

elif st.session_state.step == 5:
    st.markdown("<div class='container'><h3>Prediction Result</h3></div>", unsafe_allow_html=True)
    st.write('The 5 possible customer groups are: 0, 1, 2, 3, 4')
    st.write(f"Estimated group: {st.session_state.prediction}")
    if st.button("Start Over"):
        reset_app()
