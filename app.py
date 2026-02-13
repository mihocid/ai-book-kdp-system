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
# STYLING (BUTTONS, TITLE, FORM FIELDS)
# -------------------------
st.markdown("""
<style>
h1 {
    text-align: center;
    color: #4B0082;
    font-size: 3rem;
    margin-bottom: 0.2em;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.stButton>button {
    background-color: #4B0082;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 600;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select, .stMultiselect select {
    background-color: rgba(255,255,255,0.9);
    margin-bottom: 0.5rem;
}
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

    # CONTACT DETAILS
    st.subheader("📇 Contact Details")
    client_name = st.text_input("Full Name")
    client_email = st.text_input("Email Address")

    # BOOK IDEA
    st.subheader("💡 Book Idea")
    idea_description = st.text_area("Describe your book idea")

    # BOOK DETAILS
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

    # SAMPLE ORDER
    st.subheader("📄 Order Your 2-Page Sample")
    terms = st.checkbox("I understand my 2-page sample will be delivered within 24 hours.")

    sample_price = 10
    st.markdown(f"**Price for 2-page sample: £{sample_price}**")

    if st.button("Order Sample"):

        if not client_name or not client_email:
            st.error("Please enter your name and email.")
        elif not idea_description:
            st.error("Please describe your book idea.")
        elif not terms:
            st.error("You must accept the terms.")
        else:
            try:
                order_id = str(uuid.uuid4())[:8]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # ADMIN EMAIL
                admin_message = f"""
NEW SAMPLE ORDER
Order ID: {order_id}
Date: {timestamp}

Client: {client_name}
Email: {client_email}

Book Idea:
{idea_description}

Book Type: {book_type}
Genre: {genre}
Word Count for Sample: {word_count}
Tone: {tone}
Atmosphere: {atmosphere}
Extras: {', '.join(extras)}

Sample Price: £{sample_price}
"""
                # CLIENT EMAIL
                client_message = f"""
Hi {client_name},

Thank you for submitting your book idea!

Your 2-page sample will be delivered within 24 hours. We will email you as soon as it’s ready.

Here is a summary of your submission:

Book Type: {book_type}
Genre: {genre}
Word Count for Sample: {word_count}
Tone: {tone}
Atmosphere: {atmosphere}
Extras: {', '.join(extras)}

Thank you for choosing EasyBook Pro!
"""

                # SMTP CONFIG
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                sender_email = "YOUR_GMAIL@gmail.com"       # replace with your Gmail
                sender_password = "YOUR_APP_PASSWORD"       # Gmail App Password

                # --- SEND TO ADMIN ---
                msg_admin = MIMEText(admin_message)
                msg_admin['Subject'] = f"New EasyBook Sample Order: {order_id}"
                msg_admin['From'] = sender_email
                msg_admin['To'] = sender_email

                # --- SEND TO CLIENT ---
                msg_client = MIMEText(client_message)
                msg_client['Subject'] = f"Your EasyBook 2-Page Sample Order: {order_id}"
                msg_client['From'] = sender_email
                msg_client['To'] = client_email

                # Connect SMTP server
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, sender_email, msg_admin.as_string())
                server.sendmail(sender_email, client_email, msg_client.as_string())
                server.quit()

                st.success(f"✅ Sample ordered! You will receive it within 24 hours.")
                st.info(f"Order ID: {order_id}")

            except Exception as e:
                st.error(f"Error sending emails: {e}")

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