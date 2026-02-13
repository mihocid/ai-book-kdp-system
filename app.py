import streamlit as st
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText

# Uncomment when Google Sheets + OpenAI are ready
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from openai import OpenAI

st.set_page_config(page_title="AI Book Creation SaaS", page_icon="📚", layout="wide")

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
menu = st.sidebar.selectbox("Navigation", ["Place Order", "Admin Panel"])

# -------------------------
# PLACE ORDER FORM
# -------------------------
if menu == "Place Order":
    st.markdown("<h1 style='text-align:center;color:#4B0082;'>📚 AI Book Creation SaaS</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # -------------------------
    # CLIENT INFO
    # -------------------------
    st.subheader("Client Information")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Full Name")
    with col2:
        client_email = st.text_input("Email Address")
    
    st.markdown("---")
    
    # -------------------------
    # BOOK IDEA
    # -------------------------
    st.subheader("Book Idea")
    idea_option = st.radio(
        "Do you have a book idea?",
        ["Yes, I have an idea", "No, find me a profitable niche"],
        horizontal=True
    )
    idea_description = ""
    if idea_option == "Yes, I have an idea":
        idea_description = st.text_area("Describe your idea (2-3 sentences)")
    
    st.markdown("---")
    
    # -------------------------
    # BOOK DETAILS
    # -------------------------
    st.subheader("Book Details")
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
    
    st.markdown("---")
    
    # -------------------------
    # TERMS & PAYMENT
    # -------------------------
    st.subheader("Terms & Payment")
    terms = st.checkbox("I agree to the terms and understand delivery can take up to 7 days depending on complexity.")
    
    # ---------- Stripe Placeholder ----------
    st.info("💳 Stripe placeholder: Payment is simulated. Real Stripe Checkout will replace this in the future.")
    payment_confirmed = st.checkbox("I confirm payment has been completed (simulated)")
    
    # -------------------------
    # PRICE CALCULATION
    # -------------------------
    price_map = {"5000 words":50, "7000 words":60, "10000 words":80, "20000 words":150}
    price = price_map[word_count]
    
    st.markdown(
        f"<div style='position:fixed; bottom:20px; right:20px; background-color:#4B0082; color:white; padding:15px; border-radius:10px; font-size:18px;'>Price: £{price}</div>",
        unsafe_allow_html=True
    )
    
    # -------------------------
    # SUBMIT ORDER BUTTON
    # -------------------------
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
                
                # -------- ADMIN EMAIL --------
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

                # -------- CLIENT EMAIL --------
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

                # Send emails
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.login(sender, password)
                server.sendmail(sender, receiver, msg_admin.as_string())
                server.sendmail(sender, client_email, msg_client.as_string())
                server.quit()
                
                st.success("✅ Order submitted successfully!")
                st.info(f"Order ID: {order_id}")

                # -------- GOOGLE SHEETS BACKUP --------
                """
                # Uncomment when ready
                scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
                gs_client = gspread.authorize(credentials)
                sheet = gs_client.open("AI Book Orders").sheet1
                sheet.append_row([order_id, timestamp, client_name, client_email, book_type, genre, word_count, tone, atmosphere, ', '.join(extras), price])
                """

                # -------- OPENAI OUTLINE GENERATION --------
                """
                # Uncomment when ready
                client_ai = OpenAI(api_key=st.secrets["OPENAI_KEY"])
                outline_prompt = f"Create a detailed book outline for: {book_type}, Genre: {genre}, Word Count: {word_count}, Tone: {tone}, Atmosphere: {atmosphere}"
                response = client_ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": outline_prompt}]
                )
                outline = response.choices[0].message.content
                st.subheader("Generated Book Outline")
                st.write(outline)
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