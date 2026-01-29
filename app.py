import streamlit as st
import pandas as pd
import numpy as np

# App title
st.title("Extended Streamlit App 🚀")

st.write("This app demonstrates inputs, calculations, tables, and charts.")

# -------- User Inputs --------
name = st.text_input("Enter your name")
age = st.slider("Select your age", 1, 100)
marks = st.number_input("Enter your marks", min_value=0, max_value=100)

# -------- Button Action --------
if st.button("Submit"):
    st.success(f"Hello {name}! 👋")
    st.write(f"Age: {age}")
    st.write(f"Marks: {marks}")

    if marks >= 50:
        st.write("✅ Status: Pass")
    else:
        st.write("❌ Status: Fail")

# -------- DataFrame Example --------
st.subheader("Sample Student Data")

data = {
    "Student": ["A", "B", "C", "D"],
    "Marks": [78, 65, 89, 45]
}

df = pd.DataFrame(data)
st.dataframe(df)

# -------- Chart Example --------
st.subheader("Marks Chart")

st.bar_chart(df.set_index("Student"))

# -------- Random Data --------
st.subheader("Random Numbers")

random_data = np.random.randint(1, 100, 10)
st.write(random_data)
