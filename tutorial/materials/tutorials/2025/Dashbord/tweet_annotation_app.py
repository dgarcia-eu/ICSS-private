import streamlit as st
import pandas as pd
import os


input_file = "data/tweet_sample_unclassified.json"
output_file = "data/output.json"

# Import Data
def load_input_data():
    return pd.read_json(input_file)

def load_progressed_data(): # import data if there exist some labeled data
    if os.path.exists(output_file):
        return pd.read_json(output_file)
    else:
        return pd.DataFrame(columns=["tweet", "tweet_id", "label"])

# Same funtion as in my TKinter app -> get the next uncategorized tweet
def get_next_uncategorized(data, progressed):
    uncategorized = data[data["id"].isin(progressed["tweet_id"]) == False]
    
    if not uncategorized.empty:
        random_row = uncategorized.sample(n=1).iloc[0]
        return random_row
    else:
        return None

# also same funtion as in my app -> what happens after pushing the button
def classify_callback(label):
    tweet = st.session_state.current_tweet
    st.session_state.progressed.loc[len(st.session_state.progressed)] = [
        tweet["text"],
        tweet["id"],
        label]
    st.session_state.current_tweet = get_next_uncategorized(
        st.session_state.data,
        st.session_state.progressed)
    st.success(f"Tweet labeled: **{label}**")


if "initialized" not in st.session_state:
    st.session_state.data = load_input_data()
    st.session_state.progressed = load_progressed_data()
    st.session_state.total = len(st.session_state.data)
    st.session_state.current_tweet = get_next_uncategorized(
        st.session_state.data,
        st.session_state.progressed)
    st.session_state.initialized = True


st.title("Tweet-Classification")
st.write(f"Progress: {len(st.session_state.progressed)} of {st.session_state.total} Tweets labeled")

# Save Button
if st.button("💾 Save progress"):
    st.session_state.progressed.to_json(output_file)
    st.success("Progress saved!")

# Labeling UI
if st.session_state.current_tweet is not None:
    tweet = st.session_state.current_tweet
    st.subheader("Tweet")
    st.write(tweet["text"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Positive 😊", on_click=classify_callback, args=("Positive",))
    with col2:
        st.button("Neutral 😐", on_click=classify_callback, args=("Neutral",))
    with col3:
        st.button("Negative 😠", on_click=classify_callback, args=("Negative",))
    with col4:
        st.button("Undecidable ❓", on_click=classify_callback, args=("Undecidable",))
else:
    st.info("✅ All tweets have been categorized!")
    if st.button("Save and exit"):
        st.session_state.progressed.to_json(output_file)
        st.success("Your data has been saved successfully. 🎉")