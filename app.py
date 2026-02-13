import streamlit as st
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText

st.set_page_config(page_title="AI Book Creation System", layout="centered")

st.title("📚 AI Book Creation Intake Form")

# -------------------------
# CLIENT INFORMATION
# -------------------------
st.header("Client Information")

client_name = st.text_input("Full Name")
client_email = st.text_input("Email Address")

# -------------------------
# IDEA SECTION
# -------------------------
st.header("Book Idea")

idea_option = st.radio(
    "Do you have a book idea?",
    ["Yes, I have an idea", "No, find me a profitable niche"]
)

idea_description = ""
if idea_option == "Yes, I have an idea":
    idea_description = st.text_area("Describe your idea (2-3 sentences)")

# -------------------------
# BOOK DETAILS
# -------------------------
st.header("Book Details")

book_type = st.selectbox(
    "Book Type",
    [
        "Fiction",
        "Non-Fiction",
        "Children",
        "Young Adult",
        "Self-Help",
        "Business",
        "Health & Fitness",
        "Cookbook",
        "Workbook",
        "Low Content"
    ]
)

genre = st.text_input("Genre")

length = st.selectbox(
    "Length",
    [
        "Short (10k-20k words)",
        "Medium (30k-60k words)",
        "Long (80k+ words)"
    ]
)

tone = st.selectbox(
    "Tone",
    [
        "Dark",
        "Inspirational",
        "Humorous",
        "Serious",
        "Emotional",
        "Academic"
    ]
)

atmosphere = st.selectbox(
    "Atmosphere",
    [
        "Cozy",
        "Suspenseful",
        "Epic",
        "Realistic",