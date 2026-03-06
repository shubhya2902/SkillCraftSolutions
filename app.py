from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'SkillCraft@2025'

# Config SQLite DB in same folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillcraft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Email Sending
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration (you can also move this to a config file)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# to our email
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECEIVER_EMAILS = os.environ.get('RECEIVER_EMAILS')

# to user
sender_email_to_user = os.environ.get('SENDER_EMAIL_TO_USER')
sender_password_to_user = os.environ.get('SENDER_PASSWORD_TO_USER')

# Model for Enquiry
class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(11), nullable=True)
    subject = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=True)


# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Thesis_Research')
def ThesisResearch():
    return render_template('Thesis_Research.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/base')
def base():
    return render_template('base.html')

# Individual service detail pages
@app.route('/technologies')
def technologies():
    return render_template('portfolio.html')


def send_enquiry_email(subject, content):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ', '.join(RECEIVER_EMAILS)
        msg['Subject'] = subject

        msg.attach(MIMEText(content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def send_thank_you_email(user_email, user_name):
    try:
        subject = "Thank You for Connecting with SkillCraft Solutions!"

        # HTML content with logo and contact info
        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

                <div style="background-color: #343a40; padding: 20px; text-align: center;">
                    <img src="https://yourdomain.com/static/assets/images/skillcraft.jpg" alt="SkillCraft Solutions" style="max-width: 200px; height: auto;" />
                </div>

                <div style="padding: 30px;">
                    <h2 style="color: #333;">Hello {user_name},</h2>
                    <p style="font-size: 16px; color: #555;">
                        Thank you for contacting <strong>SkillCraft Solutions</strong>. We’ve received your inquiry and our team will get back to you shortly.
                    </p>
                    <p style="font-size: 16px; color: #555;">
                        If you have any further questions, feel free to reach out.
                    </p>
                    <p style="margin-top: 30px; font-size: 16px; color: #333;">
                        Best regards,<br>
                        <strong>SkillCraft Solutions Team</strong>
                    </p>
                </div>

                <div style="background-color: #f1f1f1; padding: 20px; text-align: center; font-size: 14px; color: #666;">
                    📞 +91-9158698218<br>
                    📧 skillcrafttsolutions@gmail.com<br>
                </div>
            </div>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email_to_user
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email_to_user, sender_password_to_user)
        server.sendmail(sender_email_to_user, user_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"❌ Failed to send thank-you email: {e}")

@app.route('/inquire-basic', methods=['POST'])
def save_name_email_only():
    name = request.form.get('name')
    email = request.form.get('email')

    if name and email:
        enquiry = Enquiry(name=name, email=email)
        db.session.add(enquiry)
        db.session.commit()

        # Email content
        subject = "📩 New Basic Inquiry Received"
        content = f"""
        <h2>New Basic Inquiry</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        """

        flash('✅ Inquiry saved successfully!', 'success')
        send_thank_you_email(email, name)
        send_enquiry_email(subject, content)
    else:
        flash('❌ Name and Email are required!', 'danger')

    return redirect('/')

@app.route('/inquire-full', methods=['POST'])
def save_full_enquiry():
    name = request.form.get('name')
    number = request.form.get('number')
    email = request.form.get('email')
    subject_text = request.form.get('subject')
    message = request.form.get('message')

    if name and email:
        enquiry = Enquiry(
            name=name,
            number=number,
            email=email,
            subject=subject_text,
            message=message
        )
        db.session.add(enquiry)
        db.session.commit()

        # Email content
        subject = "📩 New Full Inquiry Received"
        content = f"""
        <h2>New Full Inquiry</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Number:</strong> {number}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Subject:</strong> {subject_text}</p>
        <p><strong>Message:</strong> {message}</p>
        """

        flash('✅ Inquiry submitted successfully!', 'success')
        send_enquiry_email(subject, content)
        send_thank_you_email(email, name)
    else:
        flash('❌ Name and Email are required!', 'danger')

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
