from flask import Flask, render_template, request
from flask_mail import Mail, Message  # Import Flask-Mail
from smtplib import SMTPException
import smtplib
import re  # Import the 're' module

# Create a Flask application
app = Flask('Test app', template_folder='app/templates', static_folder='app/static')

# Configure Flask-Mail with your email server settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587  # or 465
app.config['MAIL_USERNAME'] = 'tamarandoni@gmail.com'
app.config['MAIL_PASSWORD'] = 'peter87@@'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEBUG'] = True

# Initialize Flask-Mail
mail = Mail(app)

# Route: Display a simple "Hello" message
@app.route('/project')
def hello():
    return "Hello"

# Route: Display the main page using an HTML template
@app.route('/')
def index():
    return render_template('portfolio/index.html')

# Route: Handle form submission for sending an email
@app.route('/send-email', methods=['POST'])
def send_email():
    username = request.form['user-name']
    email = request.form['user-email']
    user_msg = request.form['user-message']

    msg = ''

    # Input validation and error handling
    if not username:
        msg = 'Username must not be empty'
    elif not email:
        msg = 'Email must not be empty'
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        msg = 'Invalid email address'
    elif not user_msg:
        msg = 'User message must not be empty'
    else:
        # Send email using Flask-Mail
        message = Message('Portfolio Contact Form Submission',
                          sender='tamarandoni@gmail.com',
                          recipients=['tamarandoni@gmail.com'])
        message.body = f'Name: {username}\nEmail: {email}\nMessage: {user_msg}'
        # Render a response using an HTML template
        return render_template('portfolio/login.html', user=msg)

    try:
        mail.send(message)
        return "Email sent successfully."
    except SMTPException as e:
        print("An error occurred while sending the email:", e)
        # Log the error for debugging or provide a user-friendly message
        return "Failed to send the email. Please try again later"

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)