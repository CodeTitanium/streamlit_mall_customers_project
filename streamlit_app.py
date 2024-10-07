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
    .fade-in {
        opacity: 0;
        transition: opacity 2s ease-in;
    }
    .fade-in.visible {
        opacity: 1;
    }
    .container {
        text-align: center;
        margin-top: 50px;
    }
    .start-btn, .refresh-btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        cursor: pointer;
        margin-bottom: 20px;
    }
    .start-btn:hover, .refresh-btn:hover {
        background-color: #45a049;
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
            <button class="start-btn" onclick="document.getElementById('content').classList.add('visible');">Let's Get Started</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Start"):
        st.session_state.step = 1

# Step 1: Pick gender
if st.session_state.step == 1:
    gender = st.radio('Step 1: Pick your gender', ["Female", "Male"])
    if st.button("Next (Age)"):
        st.session_state.gender = 1 if gender == "Male" else 0
        st.session_state.step = 2

# Step 2: Pick age
if st.session_state.step == 2:
    age = st.slider('Step 2: Pick your age', 18, 70)
    if st.button("Next (Annual Salary)"):
        st.session_state.age = age
        st.session_state.step = 3

# Step 3: Pick annual income
if st.session_state.step == 3:
    annual_income = st.slider('Step 3: Pick your annual salary in thousands of dollars', 15, 137)
    if st.button("Next (Spending Score)"):
        st.session_state.annual_income = annual_income
        st.session_state.step = 4

# Step 4: Pick spending score
if st.session_state.step == 4:
    spending_score = st.slider('Step 4: Pick your spending score', 0, 100)
    if st.button("Predict Customer Segment"):
        st.session_state.spending_score = spending_score

        # Prepare user input for prediction
        user_input = np.array([[st.session_state.gender, st.session_state.age, st.session_state.annual_income, st.session_state.spending_score]])
        user_input_scaled = scaler.transform(user_input)

        # Prediction
        customer_group = model.predict(user_input_scaled)
        st.session_state.predicted = True
        st.session_state.prediction = customer_group[0]
        st.session_state.step = 5

# Display prediction and refresh button
if st.session_state.step == 5:
    st.write('The 5 possible customer groups are: 0, 1, 2, 3, 4')
    st.write(f"Estimated group: {st.session_state.prediction}")
    
    # Display refresh button using the image
    st.image('/mnt/data/A_circular_green_button_with_a_white_refresh_icon_.png', width=100)
    if st.button("Refresh"):
        reset_app()
