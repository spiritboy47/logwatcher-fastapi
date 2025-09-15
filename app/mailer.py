import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "devops@gmail.com"
SMTP_PASSWORD = "gmail-app-password"
FROM_ADDRESS = "devops@gmail.com"

def send_summary_email(project_name, error_list, recipients):
    if not error_list:
        return

    subject = f"🚨 {project_name.upper()} Logs - Summary of Errors"
    body = f"Hi Team,\n\nHere is the summary of errors for project **{project_name}**:\n\n"

    for filename, errors in error_list.items():
        body += f"\nFile: {filename}\n"
        for err in errors:
            body += f"- {err.strip()}\n"

    body += f"\nDirectory: {project_name}\n"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_ADDRESS
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_ADDRESS, recipients, msg.as_string())
        print(f"Email sent for project {project_name}")
    except Exception as e:
        print("Failed to send email:", e)
