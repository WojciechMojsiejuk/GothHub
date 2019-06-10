import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='wojciechmojsiejuk@gmail.com',
    to_emails='pawel.bak98@gmail.com',
    subject='GothHub activation token',
    html_content='<strong>hejka</strong>')
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
