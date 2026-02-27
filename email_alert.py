import yagmail

def send_alert(to_email, subject, content):
    yag = yagmail.SMTP(
        "kandula.jayati@gmail.com",
        "yvasveplgqokszed"
    )
    yag.send(
        to=to_email,
        subject=subject,
        contents=content
    )