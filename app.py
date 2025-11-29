import time
import streamlit as st

# /workspaces/My/app.py

st.set_page_config(page_title="HelloWorld Streamlit", layout="centered")

st.title("Hello, World! (Streamlit)")
st.markdown("A tiny demo that streams greeting updates.")

name = st.text_input("Enter your name", "World")
count = st.slider("Number of updates", 1, 10, 5)

if st.button("Greet (stream)"):
    placeholder = st.empty()
    progress = st.progress(0)
    for i in range(1, count + 1):
        placeholder.markdown(f"**Hello, {name}!** (update {i}/{count})")
        progress.progress(i / count)
        time.sleep(0.4)
    placeholder.success(f"All done — Hello, {name}!")
    progress.empty()