from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'saintsiga@gmail.com'
SMTP_PASSWORD = 'ilovebrownies<33'  # Use an app password if 2-Step Verification is enabled

@app.route('/')
def index():
    return render_template('index.html')

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
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)