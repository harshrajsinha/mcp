import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import copy

from __init__ import RESPONSE_FORMAT


def send_email(
    receiver_email, 
    subject, 
    body,
    cc=None,
    bcc=None,
    attachments=None):
    """
    Send an email using SMTP server
    
    Parameters:
    -----------
    sender_email : str
        Email address of the sender
    receiver_email : str or list
        Email address(es) of the recipient(s)
    subject : str
        Subject of the email
    body : str
        Content of the email
    smtp_server : str, optional
        SMTP server address (default is "smtp.gmail.com")
    smtp_port : int, optional
        SMTP server port (default is 587 for TLS)
    username : str, optional
        Username for SMTP authentication (default is None, will use sender_email if not provided)
    password : str, optional
        Password for SMTP authentication
    cc : str or list, optional
        Email address(es) to be CC'd
    bcc : str or list, optional
        Email address(es) to be BCC'd
    attachments : str or list, optional
        Path(s) to file(s) to be attached
        
    Returns:
    --------
    bool
        True if email was sent successfully, False otherwise
    """

    result = copy.deepcopy(RESPONSE_FORMAT)


    sender_email="put sendder email here"
    smtp_server="smtp.office365.com"
    smtp_port=587
    username="put username here"
    password="put password here"    

    # If username not provided, use sender_email
    if username is None:
        username = sender_email
    
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    
    # Handle receiver email as string or list
    if isinstance(receiver_email, list):
        message["To"] = ", ".join(receiver_email)
    else:
        message["To"] = receiver_email
    
    message["Subject"] = subject
    
    # Add CC recipients if provided
    if cc:
        if isinstance(cc, list):
            message["Cc"] = ", ".join(cc)
        else:
            message["Cc"] = cc
    
    # Add BCC recipients for tracking (not visible in message headers)
    # BCC recipients are handled when sending, not in message headers
    
    # Attach the body of the message
    message.attach(MIMEText(body, "plain"))
    
    # Process attachments if any
    if attachments:
        if not isinstance(attachments, list):
            attachments = [attachments]
        
        for attachment in attachments:
            if os.path.isfile(attachment):
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                
                # Add header with filename
                part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment)}"'
                message.attach(part)
    
    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        
        # Login to the email server
        server.login(username, password)
        
        # Prepare the recipients list for sending
        all_recipients = []
        
        # Add direct recipients
        if isinstance(receiver_email, list):
            all_recipients.extend(receiver_email)
        else:
            all_recipients.append(receiver_email)
        
        # Add CC recipients
        if cc:
            if isinstance(cc, list):
                all_recipients.extend(cc)
            else:
                all_recipients.append(cc)
        
        # Add BCC recipients
        if bcc:
            if isinstance(bcc, list):
                all_recipients.extend(bcc)
            else:
                all_recipients.append(bcc)
        
        # Send the email
        server.sendmail(sender_email, all_recipients, message.as_string())
        
        # Close the connection
        server.quit()
        
        result["result"]["answer"] = "Email sent successfully."
   
    except Exception as e:
        print(f"Error sending email: {e}")
        result["result"]["error"] = str(e)
        result["result"]["answer"] = "Failed to send email."
        
        
    return result