import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import uuid

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="EasyBook Pro", layout="centered")

# -------------------------
# BACKGROUND IMAGE
# -------------------------
background_url = "PASTE_YOUR_RAW_GITHUB_IMAGE_LINK_HERE"  # replace with your uploaded image link

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                url("{background_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.main-card {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}}

h1 {{
    text-align: center;
    color: white;
    font-size: 3rem;
    margin-bottom: 0.2em;
}}

.subtitle {{
    text-align: center;
    color: #f1f1f1;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}}

.stButton>button {{
    background-color: #4B0082;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 600;
}}

.stTextInput input, .stTextArea textarea, .stSelectbox select {{
    background-color: rgba(255,255,255,0.9);
}}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("<h1>EasyBook Pro</h1>", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tell me your idea and I will make it come to life</div>', unsafe_allow_html=True)

# -------------------------
# SIDEBAR MENU
# -------------------------
menu = st.sidebar.selectbox("Navigation", ["Order Sample", "Admin Panel"])

# -------------------------
# ORDER SAMPLE
# -------------------------
if menu == "Order Sample":

    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.subheader("👤 Client Information")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Full Name")
    with col2:
        client_email = st.text_input("Email Address")

    st.subheader("💡 Book Idea")
    idea_option = st.radio(
        "Do you have a book idea?",
        ["Yes, I have an idea", "No, find me a profitable niche"],
        horizontal=True
    )
    idea_description = ""
    if idea_option == "Yes, I have an idea":
        idea_description = st.text_area("Describe your idea")

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
        word_count = st.selectbox("Word Count for Sample", ["500", "700", "1000"])

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
        ["Illustrations", "Workbook Exercises", "Case Studies", "References", "SEO Optimization"])

    st.markdown('<div style="margin-top:15px;"></div>', unsafe_allow_html=True)

    st.subheader("📄 Order Your 2-Page Sample")
    terms = st.checkbox("I understand my 2-page sample will be delivered within 24 hours.")

    sample_price = 10
    st.markdown(f"**Price for 2-page sample: £{sample_price}**")

    if st.button("Order Sample"):

        if not client_name or not client_email:
            st.error("Please enter your name and email.")
        elif not terms:
            st.error("You must accept the terms.")
        else:
            try:
                order_id = str(uuid.uuid4())[:8]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # ADMIN EMAIL TEMPLATE
                admin_message = f"""
NEW SAMPLE ORDER
Order ID: {order_id}
Date: {timestamp}

Client: {client_name}
Email: {client_email}

Idea Option: {idea_option}
Idea Description: {idea_description}

Book Type: {book_type}
Genre: {genre}
Word Count for Sample: {word_count}
Tone: {tone}
Atmosphere: {atmosphere}
Extras: {', '.join(extras)}

Sample Price: £{sample_price}
"""
                # Here you would send this email to yourself manually or via SMTP
                # You can keep using the Gmail method you already have

                st.success(f"✅ Sample ordered! You will receive it within 24 hours.")
                st.info(f"Order ID: {order_id}")

            except:
                st.error("Error processing your order. Please try again.")

    st.markdown('</div>', unsafe_allow_html=True)

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