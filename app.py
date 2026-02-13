import streamlit as st
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="EasyBook Pro", page_icon="📘", layout="wide")

# -------------------------
# CLEAN PROFESSIONAL CSS
# -------------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f5f6fa, #e8e9ff);
        background-attachment: fixed;
    }

    .card {
        background-color: rgba(255,255,255,0.95);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }

    .stButton>button {
        background-color: #4B0082;
        color: white;
        border-radius: 8px;
        padding: 8px 18px;
        font-size: 16px;
        font-weight: 600;
    }

    .price-box {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #4B0082;
        color: white;
        padding: 12px 18px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# HEADER WITH LOGO
# -------------------------
st.markdown(
    """
    <div style='text-align:center; padding:20px 0;'>
        <div style='display:flex; justify-content:center; align-items:center; gap:12px;'>
            <div style='background:#4B0082; color:white; 
                        font-size:20px; padding:8px 12px; 
                        border-radius:8px; font-weight:bold;'>
                📘
            </div>
            <h1 style='font-size:48px; 
                       background: linear-gradient(90deg, #4B0082, #7B3FE4);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       margin:0;'>
                EasyBook Pro
            </h1>
        </div>
        <h3 style='color:#555; font-weight:400; margin-top:8px;'>
            From idea to published book — effortlessly.
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
menu = st.sidebar.selectbox("Navigation", ["Place Order", "Admin Panel"])

# -------------------------
# PLACE ORDER
# -------------------------
if menu == "Place Order":

    # CLIENT INFO
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👤 Client Information")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Full Name")
    with col2:
        client_email = st.text_input("Email Address")
    st.markdown("</div>", unsafe_allow_html=True)

    # BOOK IDEA
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💡 Book Idea")
    idea_option = st.radio(
        "Do you have a book idea?",
        ["Yes, I have an idea", "No, find me a profitable niche"],
        horizontal=True
    )

    idea_description = ""
    if idea_option == "Yes, I have an idea":
        idea_description = st.text_area("Describe your idea")
    st.markdown("</div>", unsafe_allow_html=True)

    # BOOK DETAILS
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📖 Book Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        book_type = st.selectbox("Book Type",
            ["Fiction", "Non-Fiction", "Children", "Self-Help",
             "Business", "Health & Fitness", "Cookbook", "Workbook"])
    with col2:
        genre = st.selectbox("Genre",
            ["Fantasy", "Sci-Fi", "Romance", "Thriller", "Mystery",
             "Horror", "Historical Fiction", "Self-Improvement",
             "Business Strategy", "Personal Finance",
             "Parenting", "Psychology", "Fitness"])
    with col3:
        word_count = st.selectbox("Word Count",
            ["5000 words", "7000 words", "10000 words", "20000 words"])

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("Tone",
            ["Inspirational", "Dark", "Humorous", "Serious",
             "Emotional", "Professional"])
    with col2:
        atmosphere = st.selectbox("Atmosphere",
            ["Cozy", "Suspenseful", "Epic", "Realistic",
             "Futuristic", "Intense"])

    extras = st.multiselect("Optional Extras",
        ["Illustrations", "Workbook Exercises",
         "Case Studies", "References", "SEO Optimization"])
    st.markdown("</div>", unsafe_allow_html=True)

    # TERMS & PAYMENT
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💳 Terms & Payment")
    terms = st.checkbox("I agree to the terms and delivery time (max 7 days).")
    payment_confirmed = st.checkbox("I confirm payment has been completed (simulated)")
    st.markdown("</div>", unsafe_allow_html=True)

    # PRICE CALCULATION
    price_map = {
        "5000 words": 50,
        "7000 words": 60,
        "10000 words": 80,
        "20000 words": 150
    }

    price = price_map[word_count]

    st.markdown(
        f"<div class='price-box'>Total: £{price}</div>",
        unsafe_allow_html=True
    )

    # SUBMIT BUTTON
    if st.button("Submit Order"):

        if not client_name or not client_email:
            st.error("Please enter your name and email.")

        elif not terms:
            st.error("You must accept the terms.")

        elif not payment_confirmed:
            st.error("Payment confirmation required.")

        else:
            try:
                order_id = str(uuid.uuid4())[:8]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # ADMIN EMAIL
                admin_message = f"""
NEW ORDER
Order ID: {order_id}
Date: {timestamp}

Client: {client_name}
Email: {client_email}

Idea Option: {idea_option}
Idea Description: {idea_description}

Book Type: {book_type}
Genre: {genre}
Word Count: {word_count}
Tone: {tone}
Atmosphere: {atmosphere}
Extras: {', '.join(extras)}

Total: £{price}
"""

                sender = st.secrets["EMAIL"]
                password = st.secrets["PASSWORD"]

                msg_admin = MIMEText(admin_message)
                msg_admin["Subject"] = f"New Order - {order_id}"
                msg_admin["From"] = sender
                msg_admin["To"] = sender
                msg_admin["Reply-To"] = client_email

                # CLIENT EMAIL
                client_message = f"""
Hello {client_name},

Thank you for your order!

Order ID: {order_id}
Total Paid: £{price}

Your book will be delivered within 7 days depending on complexity.

Best regards,
EasyBook Pro
"""

                msg_client = MIMEText(client_message)
                msg_client["Subject"] = f"Order Confirmation - {order_id}"
                msg_client["From"] = sender
                msg_client["To"] = client_email

                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.login(sender, password)
                server.sendmail(sender, sender, msg_admin.as_string())
                server.sendmail(sender, client_email, msg_client.as_string())
                server.quit()

                st.success("✅ Order submitted successfully!")
                st.info(f"Order ID: {order_id}")

            except:
                st.error("Error sending email.")

# -------------------------
# ADMIN PANEL
# -------------------------
if menu == "Admin Panel":
    st.subheader("Admin Access")
    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":
        st.success("Access granted.")
        st.info("Check your email for incoming orders.")
    else:
        st.warning("Enter correct admin password.")