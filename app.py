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
        "Futuristic",
        "Intense"
    ]
)

audience = st.selectbox(
    "Target Audience",
    [
        "Children (3-7)",
        "Middle Grade (8-12)",
        "Teens (13-17)",
        "Adults (18-40)",
        "40+",
        "Seniors"
    ]
)

extras = st.multiselect(
    "Extras (Optional)",
    [
        "Illustrations",
        "Workbook Exercises",
        "Case Studies",
        "Dialogue Heavy",
        "Fast Paced",
        "References",
        "SEO Optimization"
    ]
)

deadline = st.date_input("Deadline (Optional)")
budget = st.text_input("Budget (Optional)")

terms = st.checkbox("I agree to be contacted regarding this project")

# -------------------------
# SUBMIT BUTTON
# -------------------------
if st.button("Submit Order"):

    if not client_name or not client_email:
        st.error("Please enter your name and email.")
    elif not terms:
        st.error("You must accept the terms to continue.")
    else:
        try:
            order_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            prompt = f"""
NEW BOOK ORDER
=========================

Order ID: {order_id}
Submitted: {timestamp}

CLIENT DETAILS
--------------
Name: {client_name}
Email: {client_email}

BOOK SPECIFICATIONS
-------------------
Idea Option: {idea_option}
Idea Description: {idea_description}

Book Type: {book_type}
Genre: {genre}
Length: {length}
Tone: {tone}
Atmosphere: {atmosphere}
Target Audience: {audience}

Extras: {', '.join(extras)}

Deadline: {deadline}
Budget: {budget}

=========================

AI BOOK CREATION INSTRUCTIONS:

Create a professionally structured, commercially viable Amazon KDP book based on the specifications above.

Include:
- Structured chapter outline
- Strong hook
- Market positioning
- SEO optimized title ideas
- Amazon keywords
- Category suggestions
- Back cover description
"""

            sender = st.secrets["EMAIL"]
            password = st.secrets["PASSWORD"]
            receiver = st.secrets["EMAIL"]

            msg = MIMEText(prompt)
            msg["Subject"] = f"New Book Order - {order_id}"
            msg["From"] = sender
            msg["To"] = receiver
            msg["Reply-To"] = client_email

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()

            st.success("✅ Order submitted successfully!")
            st.info(f"Your Order ID is: {order_id}")

        except Exception as e:
            st.error("Something went wrong while sending the email.")