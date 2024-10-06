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

# Initialize the session state for 'started'
if 'started' not in st.session_state:
    st.session_state.started = False

# Display the steps before clicking the "Let's Get Started" button
if not st.session_state.started:
    st.markdown("### Steps to Predict Customer Segment:")
    
    # Step 1: Pick your gender
    st.markdown("1. **Pick your gender**")
    st.markdown("2. **Pick your age**")
    st.markdown("3. **Pick your annual salary in thousands of dollars **")
    st.markdown("4. **Pick your spending score**")

    # Display the "Let's Get Started" button
    if st.button("Let's Get Started"):
        st.session_state.started = True  # Set to True when the button is clicked

# Content to display after clicking the button
if st.session_state.started:
    st.markdown("<div id='content' class='fade-in visible'>", unsafe_allow_html=True)

    # Layout of the app after clicking the button
    col0, col1, col2, col3, col4, col5 = st.columns(6)
    with col0:
        st.write('')
    with col1:
        st.write('')
    with col2:
        st.write('CUSTOMERS')    
    with col3:
        st.title('') 
    with col4:
        st.write('')
    with col5:
        st.write('')
    
    col6, col7 = st.columns(2)
        
    with col6:
        st.markdown("<h6 style='text-align: left;'>A simple web app to segment/group mall customers</h6>", unsafe_allow_html=True)
    with col7:
        st.write('')
    
    # Input selections for gender, age, annual salary, and spending score
    gen_list = ["Female", "Male"]
    
    gender = st.radio('', gen_list)  # Radio button without label
    gender = int(gender == "Male")  # Streamlined gender conversion

    age = st.slider('Pick your age', 18, 70)
    annual_income = st.slider('Pick your annual salary in thousands of dollars $', 15, 137)
    spending_score = st.slider('Pick your spending score', 0, 100, 0, 1)

    # Feature Scaling
    user_input = np.array([[gender, age, annual_income, spending_score]])

    # Apply scaling on the combined 2D array
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

