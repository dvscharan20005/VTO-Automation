import imaplib
import email
from email.header import decode_header
import time

def verify_email_received(username, app_password, subject_to_find, max_wait_time=60):
    """
    Logs into an IMAP email server and checks if an email with a specific subject exists.
    """
    # 1. Connect to the Gmail server (change if using Outlook/Yahoo)
    imap_server = "imap.gmail.com"
    
    try:
        # 2. Login
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, app_password)
        mail.select("inbox")
        
        print(f"Waiting for email with subject: '{subject_to_find}'...")
        
        # 3. Poll the inbox (check every 5 seconds until max_wait_time is reached)
        end_time = time.time() + max_wait_time
        while time.time() < end_time:
            # Search for all emails
            status, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()
            
            # Check the latest emails first
            for e_id in reversed(email_ids[-5:]): # Only check the 5 most recent to save time
                _, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode the subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                            
                        if subject_to_find in subject:
                            print("Success: Email found!")
                            mail.logout()
                            return True
                            
            time.sleep(5) # Wait 5 seconds before checking again
            
        print("Timeout: Email not found.")
        mail.logout()
        return False

    except Exception as e:
        print(f"Failed to check email: {e}")
        return False