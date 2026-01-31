import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("🥗 Fridge Inventory & Expiry Tracker")

# Preloaded fridge items
data = {
    "Item Name": ["Milk", "Eggs", "Spinach"],
    "Quantity": ["1 liter", "12 pcs", "200 g"],
    "Expiry Date": ["2026-02-05", "2026-02-10", "2026-02-02"]
}

# Create DataFrame
df = pd.DataFrame(data)
df['Expiry Date'] = pd.to_datetime(df['Expiry Date']).dt.date

# User input form
st.subheader("➕ Add New Item")
with st.form("add_item_form"):
    item_name = st.text_input("Item Name")
    quantity = st.text_input("Quantity (e.g., 1 liter, 5 pcs)")
    expiry_date = st.date_input("Expiry Date")
    submitted = st.form_submit_button("Add Item")

    if submitted:
        # Append new item to DataFrame
        new_row = {"Item Name": item_name, "Quantity": quantity, "Expiry Date": expiry_date}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"✅ {item_name} added successfully!")

# Check expiry status
today = datetime.today().date()
df['Status'] = df['Expiry Date'].apply(
    lambda x: "Expired" if x < today else ("Expiring Soon" if x <= today + timedelta(days=3) else "Fresh")
)

# Display full fridge inventory
st.subheader("📋 Current Fridge Inventory")
def highlight_status(row):
    if row.Status == "Expired":
        return ["background-color: #ff9999"]*4  # red
    elif row.Status == "Expiring Soon":
        return ["background-color: #fff799"]*4  # yellow
    else:
        return [""]*4

st.dataframe(df.style.apply(highlight_status, axis=1))

# Recipe suggestions
st.subheader("🍳 Recipe Suggestions for Expiring Items")
recipes = {
    "Milk": ["Pancakes", "Smoothie"],
    "Spinach": ["Spinach Soup", "Omelette"],
    "Eggs": ["Omelette", "Egg Curry"]
}

expiring_items = df[df['Status'] != "Fresh"]['Item Name'].tolist()

if expiring_items:
    for item in expiring_items:
        if item in recipes:
            st.write(f"{item}: {', '.join(recipes[item])}")
else:
    st.write("No items are expiring soon! ✅")
