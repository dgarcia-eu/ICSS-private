import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

penguins = sns.load_dataset("penguins") # build-in dataset
st.subheader("Data Overview")
st.dataframe(penguins.head(5))

fig, ax = plt.subplots()
sns.scatterplot(data=penguins, x="bill_length_mm",
                y="bill_depth_mm", hue="species", ax=ax)
ax.set_title("Bill Dimensions by Species and Island")
ax.set_xlabel("Bill Length in mm")
ax.set_ylabel("Bill depth in mm")
st.pyplot(fig)