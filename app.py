from flask import Flask, request, render_template, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Load environment variables from .env file
load_dotenv()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

@app.route('/')
def index():
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).limit(3).all()
    return render_template('index.html', feedbacks=feedbacks)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        email = request.form['email']
        message = request.form['message']
    except KeyError:
        return "Missing form data", 400

    subject = "New Contact Form Submission"
    sender_email = SMTP_USERNAME
    recipient_email = 'sigasaint@gmail.com'

    # Create the email content
    text = f"From: {email}\n\n{message}"
    html = f"""
    <html>
    <body>
        <h2>New Contact Form Submission</h2>
        <p><strong>From:</strong> {email}</p>
        <p><strong>Message:</strong></p>
        <p>{message}</p>
    </body>
    </html>
    """

    # Create the email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        flash('Your message has been sent successfully. I will get back to you soon!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash('An error occurred while sending your message. Please try again later.', 'danger')
        return redirect(url_for('index'))
    
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    if not name or not email or not message:
        flash('All fields are required!', 'danger')
        return redirect(url_for('index'))

    feedback = Feedback(name=name, email=email, message=message)
    db.session.add(feedback)
    db.session.commit()

    flash('Your feedback has been submitted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, )