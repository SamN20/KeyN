from flask_mail import Message
from flask import url_for, render_template
import jwt
import datetime

def send_verification_email(user, app, mail):
    print("Sending verification email to", user.email)

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    link = url_for("auth.verify_email", token=token, _external=True)

    html_body = render_template("email/verify_email.html", username=user.username, link=link)

    msg = Message(
        subject="Verify Your Email",
        recipients=[user.email],
        html=html_body
    )
    try:
        mail.send(msg)
        print(f"[✓] Verification email sent to {user.email}")
    except Exception as e:
        print(f"[X] Failed to send email: {e}")
