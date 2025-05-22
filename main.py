import base64
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Scope for modifying Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Authenticate and build Gmail API
def gmail_authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("oauth.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

# Create email draft with optional PDF attachment
def create_draft(service, user_id, message_body, to, subject, attachment_path=None):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject

    # Attach plain text body
    message.attach(MIMEText(message_body, 'plain'))

    # Attach PDF file if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            pdf = MIMEApplication(f.read(), _subtype='pdf')
            pdf.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
            message.attach(pdf)

    # Encode and create draft
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft_body = {'message': {'raw': raw}}

    draft = service.users().drafts().create(userId=user_id, body=draft_body).execute()
    print(f"✅ Draft created for {to}")
    return draft

# Read recipients from CSV
def read_recipients_from_csv(file_path):
    recipients = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipients.append({
                "name": row.get("name", "").strip(),
                "email": row.get("email", "").strip(),
                "company": row.get("company", "").strip()
            })
    return recipients

# Main
if __name__ == "__main__":
    service = gmail_authenticate()
    recipients = read_recipients_from_csv("data.csv")

    attachment_path = "CUC_Sports_Meet_2025_Sponsorship_Proposal.pdf"  # Replace with your actual file name

    for r in recipients:
        name = r['name']
        email = r['email']
        company = r['company']
        if not email:
            print(f"⚠️ Skipping row due to missing email: {r}")
            continue

        subject = f"Exciting Opportunity at {company or 'your company'}"
        body = f"""Hi {name or 'there'},

I hope you're doing well! I wanted to reach out to you at {company or 'your organization'} with an exciting opportunity.

Please find attached a brochure with more details.

Best regards,  
Yasiru
"""
        create_draft(service, "me", body, email, subject, attachment_path)
    print("✅ All drafts created successfully.")
