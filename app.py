import streamlit as st
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText

# Uncomment when ready
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from openai import OpenAI

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Book Creation SaaS", page_icon="📚", layout="wide")

# -------------------------
# STYLISH CSS
# -------------------------
st.markdown(
    """
    <style>
    /* Full-page gradient background */
    body {
        background: linear-gradient(135deg, #f0f0f5, #e6e6ff);
        background-attachment: fixed;
    }

    /* Style headers */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #4B0082;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #e6e6ff !important;
    }

    /* Style checkboxes, radio buttons */
    .stCheckbox, .stRadio {
        color: #4B0082;
        font-weight: bold;
    }

    /* Style submit button */
    .stButton>button {
        background-color: #4B0082;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
    }

    /* Live price box */
    div[style*="position:fixed"] {
        background: #4B0082;
        color: white;
        font-weight: bold;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.3);
    }

    /* Card sections */
    .card {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
menu = st.sidebar.selectbox("Navigation", ["Place Order", "Admin Panel"])

st.markdown(
    """
    <div style='text-align:center; padding:20px 0;'>
        <h1 style='font-size:55px; color:#4B0082; margin-bottom:5px;'>
            EasyBook Pro
        </h1>
        <h3 style='color:gray; font-weight:400; margin-top:0;'>
            From idea to published book — effortlessly.
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# PLACE ORDER FORM
# -------------------------
if menu == "Place Order":
    st.markdown("<h1 style='text-align:center;'>📚 AI Book Creation SaaS</h1>", unsafe_allow_html=True)
    
    # ---------- CLIENT INFO CARD ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👤 Client Information")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Full Name")
    with col2:
        client_email = st.text_input("Email Address")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- BOOK IDEA CARD ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💡 Book Idea")
    idea_option = st.radio("Do you have a book idea?", ["Yes, I have an idea", "No, find me a profitable niche"], horizontal=True)
    idea_description = ""
    if idea_option == "Yes, I have an idea":
        idea_description = st.text_area("Describe your idea (2-3 sentences)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- BOOK DETAILS CARD ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📖 Book Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        book_type = st.selectbox("Book Type", ["Fiction", "Non-Fiction", "Children", "Self-Help", "Business", "Health & Fitness", "Cookbook", "Workbook", "Low Content"])
    with col2:
        genre = st.selectbox("Genre", ["Fantasy", "Sci-Fi", "Romance", "Thriller", "Mystery", "Horror", "Historical Fiction", "Self-Improvement", "Business Strategy", "Personal Finance", "Parenting", "Psychology", "Fitness", "Entrepreneurship"])
    with col3:
        word_count = st.selectbox("Word Count", ["5000 words", "7000 words", "10000 words", "20000 words"])
    
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("Tone", ["Dark", "Inspirational", "Humorous", "Serious", "Emotional", "Academic"])
    with col2:
        atmosphere = st.selectbox("Atmosphere", ["Cozy", "Suspenseful", "Epic", "Realistic", "Futuristic", "Intense"])
    
    st.subheader("Extras (Optional)")
    extras = st.multiselect("Select extras", ["Illustrations", "Workbook Exercises", "Case Studies", "Dialogue Heavy", "Fast Paced", "References", "SEO Optimization"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- TERMS & PAYMENT CARD ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💳 Terms & Payment")
    terms = st.checkbox("I agree to the terms and understand delivery can take up to 7 days depending on complexity.")
    st.info("Stripe placeholder: Payment is simulated. Real Stripe Checkout will replace this in the future.")
    payment_confirmed = st.checkbox("I confirm payment has been completed (simulated)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- PRICE CALCULATION ----------
    price_map = {"5000 words":50, "7000 words":60, "10000 words":80, "20000 words":150}
    price = price_map[word_count]
    st.markdown(
        f"<div style='position:fixed; bottom:20px; right:20px; background-color:#4B0082; color:white; padding:15px; border-radius:10px; font-size:18px;'>Price: £{price}</div>",
        unsafe_allow_html=True
    )
    
    # ---------- SUBMIT ORDER BUTTON ----------
    if st.button("Submit Order"):
        if not client_name or not client_email:
            st.error("Please enter your name and email.")
        elif not terms:
            st.error("You must accept the terms to continue.")
        elif not payment_confirmed:
            st.error("Payment confirmation required.")
        else:
            try:
                order_id = str(uuid.uuid4())[:8]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # ---------- EMAILS ----------
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
Atmosphere: {atmosphere}

Extras: {', '.join(extras)}
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

                client_message = f"""
Hello {client_name},

Thank you for your order!

Order ID: {order_id}

Book Type: {book_type}
Genre: {genre}
Word Count: {word_count}
Tone: {tone}
Atmosphere: {atmosphere}

Extras: {', '.join(extras)}
Total Paid: £{price}

Your book will be delivered within a maximum of 7 days depending on complexity.

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

                # ---------- GOOGLE SHEETS + OPENAI ----------
                """
                # Uncomment when ready
                # Google Sheets backup + OpenAI outline generation
                """
                
            except Exception:
                st.error("Something went wrong while sending emails.")

# -------------------------
# ADMIN PANEL
# -------------------------
if menu == "Admin Panel":
    st.subheader("Admin Panel")
    admin_password = st.text_input("Enter Admin Password", type="password")
    if admin_password == "youradminpass":
        st.success("Access granted")
        st.info("Check Google Sheet for all orders or wait for email notifications.")
    else:
        st.warning("Enter the correct admin password.")