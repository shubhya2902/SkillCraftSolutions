from flask import Flask, render_template, request, redirect, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

import os
from datetime import datetime
import resend

app = Flask(__name__)
app.secret_key = 'SkillCraft@2025'

# Config SQLite DB in same folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillcraft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Email Sending

# Configuration (you can also move this to a config file)
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
resend.api_key = RESEND_API_KEY

SENDER_EMAIL = os.environ.get(
    'SENDER_EMAIL',
    'contact@skillcraftsolutions.in'
)

# Model for Enquiry
class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(11), nullable=True)
    subject = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# Routes

@app.route('/google489be291c74d0570.html')
def google_verification():
    return send_from_directory('.', 'google489be291c74d0570.html')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Thesis_Research')
def ThesisResearch():
    return render_template('Thesis_Research.html')

@app.route('/about')
def about():
    return render_template('about.html')


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

def send_thank_you_email(user_email, user_name, number=None, subject_text=None, message=None):
    try:
        subject = "Thank You for Connecting with SkillCraft Solutions!"

        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color:#f8f9fa; padding:20px;">

        <div style="max-width:600px;margin:auto;background:white;border-radius:10px;
                    overflow:hidden;box-shadow:0 4px 8px rgba(0,0,0,0.1);">

            <div style="background:#343a40;padding:20px;text-align:center;">
                <img src="https://skillcraftsolutions.in/static/assets/images/new_logo.png"
                     style="max-width:200px;">
            </div>

            <div style="padding:30px;">

                <h2>Hello {user_name},</h2>

                <p>
                    Thank you for contacting <strong>SkillCraft Solutions</strong>.
                </p>

                <p>
                    We have successfully received your enquiry.
                    Our team will review your request and contact you soon.
                </p>

                <hr>

                <h3>Your Enquiry Details</h3>

                <p><strong>Name:</strong> {user_name}</p>
                <p><strong>Email:</strong> {user_email}</p>
                <p><strong>Mobile:</strong> {number or 'Not provided'}</p>
                <p><strong>Subject:</strong> {subject_text or 'Not provided'}</p>
                <p><strong>Message:</strong> {message or 'Not provided'}</p>

                <br>

                <p>
                    If you have any additional questions, feel free to contact us.
                </p>

                <br>

                <strong>SkillCraft Solutions Team</strong>

            </div>

            <div style="background:#f1f1f1;padding:20px;text-align:center;font-size:14px;">
                📞 +91-9158698218 <br>
                📧 skillcrafttsolutions@gmail.com
            </div>

        </div>

        </body>
        </html>
        """

        params = {
            "from": f"SkillCraft Solutions <{SENDER_EMAIL}>",
            "to": [user_email],
            "subject": subject,
            "html": content
        }

        email = resend.Emails.send(params)

        print("✅ Thank-you email sent successfully")
        print("Resend Email ID:", email)

        return True

    except Exception as e:
        print(f"❌ Failed to send thank-you email: {e}")
        return False

@app.route('/inquire-basic', methods=['POST'])
def save_name_email_only():

    name = request.form.get('name')
    email = request.form.get('email')

    if name and email:

        enquiry = Enquiry(
            name=name,
            email=email
        )

        db.session.add(enquiry)
        db.session.commit()

        # Send confirmation email to user
        send_thank_you_email(
            user_email=email,
            user_name=name
        )

        flash('Inquiry submitted successfully!', 'success')

    else:
        flash('Name and Email are required!', 'danger')

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

        # Send confirmation email to user
        send_thank_you_email(
            user_email=email,
            user_name=name,
            number=number,
            subject_text=subject_text,
            message=message
        )

        flash('Inquiry submitted successfully!', 'success')

    else:
        flash('Name and Email are required!', 'danger')

    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
