import asyncio
import tornado.ioloop, tornado.web
from email.mime.text import MIMEText
import smtplib
import time


def sendEmail(recipient_emails, name, start_time): 
    sender_email = "sender_email_id"
    app_password = "create_&_use_app_password"
    # SMTP config
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    duration_minutes = round((time.time() - start_time)/60)
    
    subject = "Hello, I'm %s" % name
    body = '''<p>You can write your html content in this</p>
              <br>
              <p>MIME will convert your html code to email content.
              <h3>%s has created this script which runs in % minutes.</h3>
              <br>
              <ul>
                  <li>WhatsApp: <a href="https://wa.me/+919794371985" style="text-decoration:none;">+91-9794371985</a></li>
                  <li>Email: <a href="mailto:anupeshkverma121@gmail.com" style="text-decoration:none;">anupeshkverma121@gmail.com</a></li>
              </ul>
              ''' % (name, duration_minutes)
    
    # Create a MIMEText object with HTML content
    message = MIMEText(body, 'html')
    message['Subject'] = subject
    message['From'] = sender_email
    recipients_str = ", ".join(recipient_emails)
    message['To'] = recipients_str
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        print("Email sent successfully")
        email_sent = True
    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Authentication Error: %s" % e)
    except Exception as e:
        print("Error: %s", e)

  # Raise exception for outer try except
    if not email_sent:
        raise Exception("Email sending failed.")


# main function
async def main():
    # start_time = time.time()
    start_time = 1724493360.3464098
    try:         
        
        recipient_emails = ["Anupesh.verma@edugorilla.org", "anupeshkverma121@gmail.com", "anupesh.20205039@mnnit.ac.in"]
        app_name = "myApp"
        tornado.ioloop.IOLoop.current().run_in_executor(None, sendEmail, recipient_emails, name, start_time)
    except Exception as e:
        print(e)      

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
