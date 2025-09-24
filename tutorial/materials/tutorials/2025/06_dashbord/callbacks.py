import streamlit as st
import seaborn as sns
import pandas as pd

st.subheader("Callbacks")

penguins = sns.load_dataset("penguins")

if  "type" not in st.session_state: 
    st.session_state["type"] = "Categorical"

# reaction displaying content based on data type
types = {"Categorical":["species","island","sex"],
         "Numerical":["bill_length_mm","bill_depth_mm",
                      "flipper_length_mm","body_mass_g"]}

column = st.selectbox("Select a column", types[st.session_state["type"]])

def choose_reaction():
    if st.session_state.column_type:
        st.session_state.type = st.session_state.column_type

type_of_column = st.radio("What kind of analysis",["Categorical","Numerical"],
                          on_change=choose_reaction, key = "column_type")

if st.session_state["type"] == "Categorical":
    dist = pd.DataFrame(penguins[column].value_counts()).head(50)
    st.bar_chart(dist)
else: st.table(penguins[column].describe())
