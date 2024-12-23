from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Saint'
app.config['MAIL_PASSWORD'] = 'ilovebrownies<3'
app.config['MAIL_DEFAULT_SENDER'] = 'sigasaint@gmail.com'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        email = request.form['email']
        message = request.form['message']
    except KeyError:
        return "Missing form data, 400"


    msg = Message('New Contact Form Submission', recipients=['sigasaint@gmail.com'])
    msg.body = f"From: {email}\n\n{message}"

    try:
        mail.send(msg)
        return redirect(url_for('index'))
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)