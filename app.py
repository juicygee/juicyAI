import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
from PIL import Image

# --- GOOGLE SHEETS SETUP ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
client = gspread.authorize(creds)
sheet = client.open("streamlit_gsform").sheet1

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Club Membership Form", layout="centered", initial_sidebar_state="collapsed")

dark_style = """
    <style>
    body {background-color: #111;}
    .stApp {color: white; font-family: 'Segoe UI';}
    input, textarea, select {background-color: #333; color: white;}
    </style>
"""
st.markdown(dark_style, unsafe_allow_html=True)

st.title("📝 Club Membership Application Form")

# --- FORM START ---
with st.form("membership_form"):
    name = st.text_input("NAME (First Name Middle Initial Last Name)")
    member_id = st.text_input("MEMBER's CONTROL NO. (I.D. No.)")
    position = st.text_input("CLUB POSITION (if none, write 'MEMBER')")
    address = st.text_area("Complete Address")
    dob = st.date_input("Date of Birth")
    mobile = st.text_input("Mobile Number")
    email = st.text_input("Email")
    emergency_contact = st.text_input("Contact Person in Case of Emergency")
    emergency_number = st.text_input("Contact Person's Mobile Number")
    photo = st.file_uploader("Upload ID Photo", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Submit")

# --- ON SUBMIT ---
if submitted:
    photo_url = "Not uploaded"
    if photo:
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", photo.name)
        with open(file_path, "wb") as f:
            f.write(photo.getbuffer())
        photo_url = f"uploads/{photo.name}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [timestamp, name, member_id, position, address, str(dob), mobile, email,
            emergency_contact, emergency_number, photo_url]

    sheet.append_row(data)
    st.success("✅ Application submitted successfully!")
    if photo:
        st.image(Image.open(photo), caption="Uploaded ID Photo", width=200)
