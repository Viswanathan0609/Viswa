import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os

# --------------------------
# USER CONFIGURATION
# --------------------------
USER_EMAIL = "youremail@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "your_app_password"  # Use Gmail App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# CSV file to store fridge items
INVENTORY_FILE = "fridge_inventory.csv"

# --------------------------
# HELPER FUNCTIONS
# --------------------------
def send_email_notification(item_name, expiry_status, user_email=USER_EMAIL):
    """Send email notification for expired/expiring item"""
    try:
        subject = f"Fridge Alert: {item_name} {expiry_status}"
        body = f"Your item '{item_name}' is {expiry_status}!"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = USER_EMAIL
        msg["To"] = user_email

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(USER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent for {item_name}")
    except Exception as e:
        print("Email not sent:", e)

def load_inventory():
    """Load inventory from CSV or create default"""
    if os.path.exists(INVENTORY_FILE):
        df = pd.read_csv(INVENTORY_FILE)
        df['Expiry Date'] = pd.to_datetime(df['Expiry Date']).dt.date
    else:
        data = {
            "Item Name": ["Milk", "Eggs", "Spinach"],
            "Quantity": ["1 litre", "12 pcs", "200 g"],
            "Expiry Date": ["2026-02-05", "2026-02-10", "2026-02-02"],
            "Notified": [False, False, False]  # Track if email sent
        }
        df = pd.DataFrame(data)
        df['Expiry Date'] = pd.to_datetime(df['Expiry Date']).dt.date
    return df

def save_inventory(df):
    """Save inventory to CSV"""
    df.to_csv(INVENTORY_FILE, index=False)

# --------------------------
# APP START
# --------------------------
st.title("🥗 FreshMate: Fridge Inventory & Expiry Tracker")
st.write("Add items, get expiry notifications, and track usage!")

# Load inventory
df = load_inventory()

# --------------------------
# ADD NEW ITEM
# --------------------------
st.subheader("➕ Add New Item")
with st.form("add_item_form"):
    item_name = st.text_input("Item Name")
    qty_number = st.number_input("Quantity", min_value=0.0, step=0.1)
    qty_unit = st.selectbox("Unit", ["pcs", "kg", "litre", "g", "ml"])
    quantity = f"{qty_number} {qty_unit}"
    expiry_date = st.date_input("Expiry Date")
    submitted = st.form_submit_button("Add Item")

    if submitted:
        new_row = {"Item Name": item_name, "Quantity": quantity, 
                   "Expiry Date": expiry_date, "Notified": False}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"✅ {item_name} added successfully!")
        save_inventory(df)

# --------------------------
# CHECK EXPIRY STATUS
# --------------------------
today = datetime.today().date()
df['Status'] = df['Expiry Date'].apply(
    lambda x: "Expired" if x < today else ("Expiring Soon" if x <= today + timedelta(days=3) else "Fresh")
)

# --------------------------
# SEND EMAIL NOTIFICATIONS (only once)
# --------------------------
for index, row in df.iterrows():
    if not row.get("Notified", False) and row['Status'] in ["Expired", "Expiring Soon"]:
        expiry_text = "expired" if row['Status']=="Expired" else "about to expire"
        send_email_notification(row['Item Name'], expiry_text)
        df.at[index, "Notified"] = True

# --------------------------
# MARK ITEM AS USED
# --------------------------
st.subheader("✅ Mark Items as Used")
used_items = st.multiselect("Select items you used:", df['Item Name'])
if st.button("Remove Used Items"):
    df = df[~df['Item Name'].isin(used_items)]
    st.success("Selected items removed from inventory!")

# Save updated inventory
save_inventory(df)

# --------------------------
# DISPLAY INVENTORY
# --------------------------
st.subheader("📋 Current Fridge Inventory")
def highlight_status(row):
    if row.Status == "Expired":
        return ["background-color: #ff9999"]*5
    elif row.Status == "Expiring Soon":
        return ["background-color: #fff799"]*5
    else:
        return [""]*5

st.dataframe(df.style.apply(highlight_status, axis=1))

# --------------------------
# RECIPE SUGGESTIONS
# --------------------------
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
