import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def build_and_send_email_with_new_stuff(email_config, allNewProducts):
    sender_email = email_config['sender_email']
    receiver_email = email_config['receiver_email']
    if not email_config['sender_email_password']:
        password = input("Type your password and press enter:")
    else:
        password = email_config['sender_email_password']

    message = MIMEMultipart("alternative")
    message["Subject"] = "I spotted some new items!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hello,
    How are you?
    Here is all the new stuff you are curious about:
    """
    for newProduct in allNewProducts:
        text += f"""\
        {newProduct[1]} - {newProduct[4]}
        {newProduct[2]}
        """
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           Here is all the new stuff you were curious about: <br>
        </p>
        <table>
        <tr>
            <th>Product Name</th>
            <th>Product Price</th>
            <th>Status</th>
            <th>Sold Out</th>
        </tr>
    """

    for newProduct in allNewProducts:
        html += f"""\
        <tr>
            <td><a href="{newProduct[2]}">{newProduct[1]}</a>
            <td>{newProduct[4]}</td>
            <td>{newProduct[5]}</td>
            <td>{newProduct[6]}</td>
        </tr>
        """

    html += """\
    </table>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(email_config['smtp_server'], email_config['smtp_port'], context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
