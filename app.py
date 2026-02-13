import streamlit as st
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText

st.set_page_config(page_title="AI Book Creation Service", layout="wide")

st.title("📚 AI Book Creation Service")

# -------------------------
# CLIENT INFORMATION
# -------------------------
st.header("Client Information")

client_name = st.text_input("Full Name")
client_email = st.text_input("Email Address")

# -------------------------
# BOOK IDEA
# -------------------------
st.header("Book Idea")

idea_option = st.radio(
    "Do you have a book idea?",
    ["Yes, I have an idea", "No, find me a profitable niche"]
)

idea_description = ""
if idea_option == "Yes, I have an idea":
    idea_description = st.text_area("Describe your idea")

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

genre = st.selectbox(
    "Genre",
    [
        "Fantasy",
        "Sci-Fi",
        "Romance",
        "Thriller",
        "Mystery",
        "Horror",
        "Historical Fiction",
        "Self-Improvement",
        "Business Strategy",
        "Personal Finance",
        "Parenting",
        "Psychology",
        "Fitness",
        "Entrepreneurship"
    ]
)

word_count = st.selectbox(
    "Word Count",
    [
        "5000 words",
        "7000 words",
        "10000 words",
        "20000 words"
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

# -------------------------
# PRICE CALCULATION
# -------------------------

price_map = {
    "5000 words": 50,
    "7000 words": 60,
    "10000 words": 80,
    "20000 words": 150
}

price = price_map[word_count]

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:right; font-size:22px; font-weight:bold;'>
    Total Price: £{price}
    </div>
    """,
    unsafe_allow_html=True
)

terms = st.checkbox("I agree to the terms and understand delivery can take up to 7 days depending on complexity.")

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

            # -------- EMAIL TO YOU --------
            admin_message = f"""
NEW BOOK ORDER
====================

Order ID: {order_id}
Submitted: {timestamp}

Client Name: {client_name}
Client Email: {client_email}

Idea Option: {idea_option}
Idea Description: {idea_description}

Book Type: {book_type}
Genre: {genre}
Word Count: {word_count}
Tone: {tone}

Total Price: £{price}

====================
"""

            sender = st.secrets["EMAIL"]
            password = st.secrets["PASSWORD"]
            receiver = st.secrets["EMAIL"]

            msg_admin = MIMEText(admin_message)
            msg_admin["Subject"] = f"New Order - {order_id}"
            msg_admin["From"] = sender
            msg_admin["To"] = receiver
            msg_admin["Reply-To"] = client_email

            # -------- EMAIL TO CLIENT --------
            client_message = f"""
Hello {client_name},

Thank you for your order!

Order ID: {order_id}

Book Type: {book_type}
Genre: {genre}
Word Count: {word_count}
Tone: {tone}

Total Paid: £{price}

Your book will be delivered within a maximum of 7 days.
Delivery time may vary depending on complexity.

We will contact you if further clarification is needed.

Best regards,
AI Book Creation Service
"""

            msg_client = MIMEText(client_message)
            msg_client["Subject"] = f"Order Confirmation - {order_id}"
            msg_client["From"] = sender
            msg_client["To"] = client_email

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender, password)

            server.sendmail(sender, receiver, msg_admin.as_string())
            server.sendmail(sender, client_email, msg_client.as_string())

            server.quit()

            st.success("✅ Order submitted successfully!")
            st.info(f"Order ID: {order_id}")

        except Exception:
            st.error("Something went wrong while sending emails.")