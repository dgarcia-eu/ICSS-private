import streamlit as st
import seaborn as sns

st.subheader("✅ Session state: the app now remembers")

penguins = sns.load_dataset("penguins")

if "nrows" not in st.session_state: # Initialize first time
    st.session_state["nrows"] = 5 

if st.button("Show more rows ⬆️"):
    st.session_state.nrows += 1
if st.button("Show fewer rows ⬇️"):
    st.session_state.nrows -= 1

st.table(penguins.head(st.session_state["nrows"]))