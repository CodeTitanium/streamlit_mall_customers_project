import pickle
import numpy as np
import streamlit as st

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

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

col6, col7 = st.columns(1)
    
with col6:
    st.markdown("<h6 style='text-align: center;'>A simple web app to segment(group) mall customers salary</h6>", unsafe_allow_html=True)
with col7:
    st.write('')

gen_list = ["Female", "Male"]

gender = st.radio('Pick your gender', gen_list)
if gender == "Male":
    gender = int(1)
else:
    gender = int(0)

age = st.slider('Pick your age', 18, 70)
annual_income = st.slider('Pick your annual_salary in thousands of dollars $', 15, 137)
spending_score = st.slider('Pick your spending score', 0, 100, 0, 1)

# Feature Scaling
user_input = np.array([[gender, age, annual_income, spending_score]])

# Apply scaling on the combined 2D array
user_input_scaled = scaler.transform(user_input)

col10, col11, col12 = st.columns(3)
with col10:
    st.write('')    
with col11:
    predict_btn = st.button('Predict Customer_Segment')
with col12:
    st.write('')

if(predict_btn):
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
        