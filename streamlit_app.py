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
        background-color: #1a1a1a;
        color: #f0f0f0;
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #4CAF50;
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
        max-width: 600px;
        padding: 20px;
        border-radius: 10px;
        background-color: #2a2a2a;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
    }
    .start-btn, .refresh-btn, .clear-btn {
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
    .start-btn:hover, .refresh-btn:hover, .clear-btn:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .refresh-container img {
        cursor: pointer;
        background: none;
        border: none;
        width: 60px;
    }
    .segment-btn {
        background-color: #2a2a2a;
        color: #f0f0f0;
        padding: 15px;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        margin: 10px;
        width: 100%;
        font-size: 18px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
    }
    .segment-btn:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to reset the app
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# Function to clear all customer data
def clear_customer_data():
    st.session_state.customer_divisions = {i: [] for i in range(5)}
    st.success("All customer data has been cleared.")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'predicted' not in st.session_state:
    st.session_state.predicted = False
if 'customer_divisions' not in st.session_state:
    st.session_state.customer_divisions = {i: [] for i in range(5)}

# Collect user name and email
if st.session_state.step == 0:
    st.markdown("<div class='container'><h2>Enter Your Details</h2></div>", unsafe_allow_html=True)
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    
    if st.button("Submit"):
        if name and email:
            st.session_state.name = name
            st.session_state.email = email
            st.session_state.step = 1
        else:
            st.warning("Please enter both name and email.")

# Start Button
if st.session_state.step == 1:
    st.markdown(
        f"""
        <div class="container">
            <h2>Welcome, {st.session_state.name}</h2>
            <p style="color: #4CAF50;">Click the button below to begin the customer segmentation process.</p>
            <button class="start-btn" onclick="document.getElementById('content').classList.add('visible');">Let's Get Started</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Start"):
        st.session_state.step = 2

# Step 1: Pick gender
if st.session_state.step == 2:
    st.markdown("<div class='container'><h3>Step 1: Pick your gender</h3></div>", unsafe_allow_html=True)
    gender = st.radio('Select Gender', ["Female", "Male"])
    if st.button("Next (Age)"):
        st.session_state.gender = 1 if gender == "Male" else 0
        st.session_state.step = 3

# Step 2: Pick age
if st.session_state.step == 3:
    st.markdown("<div class='container'><h3>Step 2: Pick your age</h3></div>", unsafe_allow_html=True)
    age = st.slider('Select Age', 18, 70)
    if st.button("Next (Annual Salary)"):
        st.session_state.age = age
        st.session_state.step = 4

# Step 3: Pick annual income
if st.session_state.step == 4:
    st.markdown("<div class='container'><h3>Step 3: Pick your annual salary</h3></div>", unsafe_allow_html=True)
    annual_income = st.slider('Select Annual Salary in Thousands', 15, 137)
    if st.button("Next (Spending Score)"):
        st.session_state.annual_income = annual_income
        st.session_state.step = 5

# Step 4: Pick spending score
if st.session_state.step == 5:
    st.markdown("<div class='container'><h3>Step 4: Pick your spending score</h3></div>", unsafe_allow_html=True)
    spending_score = st.slider('Select Spending Score', 0, 100)
    if st.button("Predict Customer Segment"):
        st.session_state.spending_score = spending_score

        # Prepare user input for prediction
        user_input = np.array([[st.session_state.gender, st.session_state.age, st.session_state.annual_income, st.session_state.spending_score]])
        user_input_scaled = scaler.transform(user_input)

        # Prediction
        customer_group = model.predict(user_input_scaled)
        st.session_state.predicted = True
        st.session_state.prediction = customer_group[0]
        
        # Store customer name and email in the appropriate division using session state
        st.session_state.customer_divisions[st.session_state.prediction].append({
            "name": st.session_state.name,
            "email": st.session_state.email
        })
        
        st.session_state.step = 6

# Display only the predicted outcome
# The actual 5 customer groups (numbers) predicted by the model are:
# The range: [0, 4] = [0, 1, 2, 3, 4]
if st.session_state.step == 6:
    group_symbols = {
        1: "🥉",
        3: "🥈",
        2: "🥇",
        0: "🪙",
        4: "💎"
    }

    predicted_group = st.session_state.prediction
    st.markdown("<div class='container'><h3>Your Customer Segment</h3></div>", unsafe_allow_html=True)
    st.write(f"Congratulations, {st.session_state.name}, you belong to {group_symbols[predicted_group]}!")

    # Option to view divisions
    st.markdown("<div class='container'><h3>Select a Division to View Customers</h3></div>", unsafe_allow_html=True)
    
    division_labels = ["Division 1", "Division 2", "Division 3", "Division 4", "Division 5"]
    
    for i, label in enumerate(division_labels):
        if st.button(f"{label} ({group_symbols[i]})"):
            st.markdown(f"<div class='container'><h3>Customers in {label}</h3></div>", unsafe_allow_html=True)
            # Display customers in the selected division using session state
            if st.session_state.customer_divisions[i]:
                for customer in st.session_state.customer_divisions[i]:
                    st.write(f"Name: {customer['name']}, Email: {customer['email']}")
            else:
                st.write("No customers in this division yet.")

    # Clear customer data button
    if st.button("Clear All Customer Data", key="clear_data"):
        clear_customer_data()

    # Refresh button
    st.markdown(
        """
        <div class="refresh-container">
            <form action="" method="get">
                <button type="submit" style="background:none; border:none; padding:0;">
                    <img src="https://www.freeiconspng.com/uploads/green-refresh-icon-png-11.png" alt="Refresh" />
                </button>
            </form>
        </div>
        """,
        unsafe_allow_html=True
    )

# Reset app button (always visible)
if st.button("Reset App", key="reset_app"):
    reset_app()
    