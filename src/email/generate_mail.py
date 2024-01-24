import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email_with_attachment(to_email, subject, message, attachment_path, username, password):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject

    body = MIMEText(message)
    msg.attach(body)

    with open(attachment_path, 'rb') as attachment:
        attachment_part = MIMEApplication(attachment.read(), Name='resume.pdf')
        attachment_part['Content-Disposition'] = f'attachment; filename=resume.pdf'
        msg.attach(attachment_part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, to_email, msg.as_string())
        server.quit()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

# Example usage:
name = "John Doe"
job_description = "Your long job description text here..."
co_founder_first_name = "Jane"
api_key = 'your_openai_api_key'  # Replace with your actual OpenAI API key
to_email = 'recipient@example.com'  # Replace with the recipient's email address
subject = 'Job Application'
attachment_path = 'path/to/resume.pdf'  # Replace with the actual path to the resume file
username = 'your_gmail_username@gmail.com'  # Replace with your actual Gmail username
password = 'your_gmail_password'  # Replace with your actual Gmail password

# cold_email = generate_cold_email(name, job_description, co_founder_first_name, api_key)
send_email_with_attachment(to_email, subject, cold_email, attachment_path, username, password)
      
