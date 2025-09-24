import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import time

penguins = sns.load_dataset("penguins") # build-in dataset

st.header("Penguin Dashbord")

col1, col2, col3 = st.columns([1,2,1])

# Left
with col1:
    desc_column = col1.selectbox("Select Column",
                             penguins.columns)
    st.table(penguins[desc_column].describe())

# Middle
with col2:
    fig, ax = plt.subplots()
    sns.scatterplot(data=penguins, x="bill_length_mm",
                    y="bill_depth_mm", hue="species", ax=ax)
    ax.set_title("Bill Dimensions by Species and Island")
    ax.set_xlabel("Bill Length in mm")
    ax.set_ylabel("Bill depth in mm")
    st.pyplot(fig)

# Right
with col3:
    uploaded_photo = st.file_uploader("Capture field notes or images")
    st.metric(label="Temperature", value="5 °C", delta="-2 °C")


# Expander
with st.expander("Click to do more"):
    st.write("Simulate data processing with a progress bar:")
    if st.button("Start Progress"):
        progress_bar = st.progress(0)
        for perc_completed in range(100):
            time.sleep(0.01)
            progress_bar.progress(perc_completed + 1)
        st.success("Done!")
