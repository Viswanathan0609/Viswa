import streamlit as st

# App title
st.title("My First Streamlit App 🚀")

# Text
st.write("Welcome to Streamlit!")

# Input from user
name = st.text_input("Enter your name")

# Button
if st.button("Submit"):
    st.success(f"Hello, {name}! 👋")

# Slider
age = st.slider("Select your age", 1, 100)

st.write("Your age is:", age)
