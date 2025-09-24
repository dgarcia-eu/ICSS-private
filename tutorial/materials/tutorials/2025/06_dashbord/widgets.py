import streamlit as st

st.button("Button")
st.checkbox("I got it!")
st.radio("Pick your favorite lecture",
         ["Data Mining","ICSS","Math for Social Scientists"])
st.selectbox("Pick your favorite lecture",
             ["Data Mining","ICSS","Math for Social Scientists"])
st.select_slider("How confident do you feel about this?",
                 ["not at all","time will tell","pro"])
st.slider("How confident do you feel about this (scale 1-10)?",0,10)