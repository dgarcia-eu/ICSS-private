import streamlit as st
from datetime import date

name = st.text_input("Enter your name")
age = st.number_input("Your age", min_value=0, max_value=100, step=1)
birthday = st.date_input("Your birthday", value=date(2000, 1, 1))

show_more = st.checkbox("Show more options")
mood = st.radio("How are you feeling today?", ["😊 Happy", "😐 Okay", "😔 Sad"])
topics = st.multiselect("What are your favorite subjects?",
    ["Data Mining", "ICSS", "Maths for Social Science", "Database Systems", "Research Design"],
    default=["ICSS"])

if name and show_more:
    st.subheader("📋 Your Summary:")
    st.write(f"**Name:** {name}")
    st.write(f"**Age:** {age} years")
    st.write(f"**Birthday:** {birthday.strftime('%B %d, %Y')}")
    st.write(f"**Mood:** {mood}")
    st.write("**Favorite Topics:**")
    if topics:
        st.write(", ".join(topics))
    else:
        st.write("No topics selected.")
