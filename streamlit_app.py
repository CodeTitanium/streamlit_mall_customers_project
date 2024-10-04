import pickle
import numpy as np
import streamlit as st

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

col0, col1, col2, col3, col4, col5, col6 = st.columns(7)
with col0:
    st.write('')
with col1:
    st.write('')
with col2:
    st.write('')    
with col3:
    st.title("Customers") 
with col4:
    st.write('')
with col5:
    st.write('')
with col6:
    st.write('')

col7, col8, col9 = st.columns(3)
with col7:
    st.write('')    
with col8:
    st.markdown("<h6 style='text-align: center;'>A simple web app to segment(group) mall customers salary</h6>", unsafe_allow_html=True)
with col9:
    st.write('')

gen_list = ["Female", "Male"]

gender = st.radio('Pick your gender', gen_list)
age = st.slider('Pick your age', 18, 70)
annual_income = st.slider('Pick your annual_salary in thousands of dollars', 15, 137)
spending_score = st.slider('Pick your speding score', 0, 100, 0, 1)

# Feature Scaling
user_input = [age, annual_income, spending_score, gender]
user_input_scaled = scaler.transform(user_input)

col10, col11, col12, col13, col14 = st.columns(5)
with col10:
    st.write('')
with col11:
    st.write('')    
with col12:
    predict_btn = st.button('Predict Customer_Segment')
with col13:
    st.write('')
with col14:
    st.write('')

if(predict_btn):
    inp1 = float(user_input_scaled[0])
    inp2 = float(user_input_scaled[1])
    inp3 = float(user_input_scaled[2])
    inp4 = float(user_input_scaled[3])
    X = [inp1, inp2, inp3, inp4]
    customer_group = model.predict([X])
    col15, col16, col17 = st.columns(3)
    with col15:
        st.write('')    
    with col16:
        st.text(f"Estimated group: ${customer_group}")
    with col17:
        st.write('')
        