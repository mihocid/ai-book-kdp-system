import streamlit as st
import smtplib
from email.mime.text import MIMEText

st.title("📚 AI Book Creation Intake Form")

idea_option = st.radio(
    "Do you have a book idea?",
    ["Yes", "No, find me a niche"]
)

idea_description = ""
if idea_option == "Yes":
    idea_description = st.text_area("Describe your idea")

book_type = st.selectbox(
    "Book Type",
    ["Fiction", "Non-Fiction", "Children", "Self-Help", "Business", "Low Content"]
)

genre = st.text_input("Genre")

length = st.selectbox(
    "Length",
    ["Short", "Medium", "Long"]
)

tone = st.selectbox(
    "Tone",
    ["Dark", "Inspirational", "Humorous", "Serious", "Emotional"]
)

if st.button("Submit"):

    prompt = f"""
    Book Idea: {idea_description}
    Type: {book_type}
    Genre: {genre}
    Length: {length}
    Tone: {tone}
    """

    sender = st.secrets["EMAIL"]
    password = st.secrets["PASSWORD"]
    receiver = st.secrets["EMAIL"]

    msg = MIMEText(prompt)
    msg["Subject"] = "New Book Order"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

    st.success("Submitted successfully!")
