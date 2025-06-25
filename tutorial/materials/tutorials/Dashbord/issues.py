import streamlit as st
import seaborn as sns

st.subheader("⚠️ Without state: the app forgets your changes")

penguins = sns.load_dataset("penguins")

nrows = 5

if st.button("Show more rows ⬆️"):
    nrows += 1
if st.button("Show fewer rows ⬇️"):
    nrows -= 1

st.subheader(f"Trying to show {nrows} rows")
st.table(penguins.head(nrows))