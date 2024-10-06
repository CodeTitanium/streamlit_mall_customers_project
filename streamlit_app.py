import pickle
import numpy as np
import streamlit as st

# Load the model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# CSS styling for transitions
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
    .start-btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        cursor: pointer;
        margin-bottom: 20px;
    }
    .start-btn:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session states for steps and started
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0  # Step 0 is the start
if 'started' not in st.session_state:
    st.session_state.started = False

# Function to handle step transitions
def next_step():
    if st.session_state.current_step < 4:  # There are 4 steps
        st.session_state.current_step += 1

# Step display logic
steps = [
    "Pick your gender",
    "Pick your age",
    "Pick your annual salary in thousands of dollars $",
    "Pick your spending score"
]

if not st.session_state.started:
    st.markdown("### Steps to Predict Customer Segment:")

    # Display current step
    st.markdown(f"**Step {st.session_state.current_step + 1}:** {steps[st.session_state.current_step]}")

    # Display button to start
    if st.button("Let's Get Started"):
        st.session_state.started = True  # Set to True when the button is clicked

# Content to display after clicking the button and during steps
if st.session_state.started:
    st.markdown("<div id='content' class='fade-in visible'>", unsafe_allow_html=True)

    # Step handling
    if st.session_state.current_step == 0:  # Gender selection
        gen_list = ["Female", "Male"]
        gender = st.radio('', gen_list)  # Radio button without label
        if st.button("Next"):
            if gender:
                st.session_state.gender = int(gender == "Male")  # Store gender value
                next_step()

    elif st.session_state.current_step == 1:  # Age selection
        age = st.slider('Pick your age', 18, 70)
        if st.button("Next"):
            st.session_state.age = age  # Store age value
            next_step()

    elif st.session_state.current_step == 2:  # Annual salary selection
        annual_income = st.slider('Pick your annual salary in thousands of dollars $', 15, 137)
        if st.button("Next"):
            st.session_state.annual_income = annual_income  # Store income value
            next_step()

    elif st.session_state.current_step == 3:  # Spending score selection
        spending_score = st.slider('Pick your spending score', 0, 100, 0, 1)
        if st.button("Next"):
            st.session_state.spending_score = spending_score  # Store spending score value
            
            # Feature Scaling
            user_input = np.array([[st.session_state.gender, st.session_state.age, st.session_state.annual_income, st.session_state.spending_score]])
            user_input_scaled = scaler.transform(user_input)

            # Prediction button layout
            col10, col11, col12 = st.columns(3)
            with col10:
                st.write('')    
            with col11:
                predict_btn = st.button('Predict Customer Segment')
            with col12:
                st.write('')

            if predict_btn:
                inp1 = float(user_input_scaled[0][0])
                inp2 = float(user_input_scaled[0][1])
                inp3 = float(user_input_scaled[0][2])
                inp4 = float(user_input_scaled[0][3])
                X = [inp1, inp2, inp3, inp4]
                customer_group = model.predict([X])
                col15, col16 = st.columns(2)
                with col15:
                    st.write('The 5 possible customer groups are: 0, 1, 2, 3, 4')    
                with col16:
                    st.text(f"Estimated group: {customer_group}")

    st.markdown("</div>", unsafe_allow_html=True)  # Closing the content div
