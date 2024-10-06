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
    .fade-out {
        opacity: 1;
        transition: opacity 1s ease-out;
    }
    .fade-out.invisible {
        opacity: 0;
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

# Initialize session state
if 'started' not in st.session_state:
    st.session_state.started = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Display the initial instructions
if not st.session_state.started:
    st.markdown(
        """
        <div class="container">
            <h2>Welcome!</h2>
            <h4>Follow these steps:</h4>
            <ol>
                <li>Pick your gender</li>
                <li>Pick your age</li>
                <li>Pick your annual salary in thousands of dollars</li>
                <li>Pick your spending score</li>
            </ol>
            <button class="start-btn" onclick="document.getElementById('content').classList.add('visible');">Let's Get Started</button>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
# If the user clicks the "Let's Get Started" button
if st.button("Start"):
    st.session_state.started = True
    st.session_state.current_step = 0  # Reset steps

# Content display logic after clicking the start button
if st.session_state.started:
    if st.session_state.current_step > 0:
        st.markdown("<div class='fade-out invisible' id='fade'></div>", unsafe_allow_html=True)

    st.markdown("<div id='content' class='fade-in visible'>", unsafe_allow_html=True)

    if st.session_state.current_step == 0:
        st.markdown("<h6>Step 1: Pick your gender</h6>", unsafe_allow_html=True)
        gen_list = ["Female", "Male"]
        st.session_state.gender = st.radio('Select your gender', gen_list)
        if st.button('Next'):
            st.session_state.current_step += 1

    elif st.session_state.current_step == 1:
        st.markdown("<h6>Step 2: Pick your age</h6>", unsafe_allow_html=True)
        st.session_state.age = st.slider('Select your age', 18, 70)
        if st.button('Next'):
            st.session_state.current_step += 1

    elif st.session_state.current_step == 2:
        st.markdown("<h6>Step 3: Pick your annual salary in thousands of dollars</h6>", unsafe_allow_html=True)
        st.session_state.annual_income = st.slider('Select your annual salary ($ thousands)', 15, 137)
        if st.button('Next'):
            st.session_state.current_step += 1

    elif st.session_state.current_step == 3:
        st.markdown("<h6>Step 4: Pick your spending score</h6>", unsafe_allow_html=True)
        st.session_state.spending_score = st.slider('Select your spending score', 0, 100)
        if st.button('Predict Customer Segment'):
            # Feature Scaling
            user_input = np.array([[1 if st.session_state.gender == "Male" else 0, st.session_state.age, st.session_state.annual_income, st.session_state.spending_score]])
            user_input_scaled = scaler.transform(user_input)
            customer_group = model.predict(user_input_scaled)

            st.write('The 5 possible customer groups are: 0, 1, 2, 3, 4')    
            st.text(f"Estimated group: {customer_group[0]}")
    
    st.markdown("</div>", unsafe_allow_html=True)  # Closing the content div

    # Adding a script to trigger fade-in/out effects
    if st.session_state.current_step > 0:
        st.markdown(
            """
            <script>
            setTimeout(function() {
                document.getElementById('fade').classList.remove('invisible');
                document.getElementById('fade').classList.add('fade-out');
            }, 100);  // Short delay before fading out
            </script>
            """,
            unsafe_allow_html=True
        )
