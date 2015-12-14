import smtplib, ConfigParser

config_path = "email.ini"

config = ConfigParser.ConfigParser()
print("Reading email config: %s" % config_path)
config.read(config_path)

from_address = config.get('credentials','username')
to_address_list  = config.get('adresses','to').split(",")
username = config.get('credentials','username')
password = config.get('credentials','password')

class EmailNotification(object):
    def __init__(self, subject, message):
        self.subject = subject
        self.message = message

    def __format_message():
        message_with_header = "\r\n".join([
          "From: %s" % from_address,
          "To: %s" % ",".join(to_address_list),
          "Subject: [Pamur] %s" % self.subject,
          "",
          "%s" % self.message
          ])
        return message_with_header

    def send():
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        msg = __format_message()
        server.sendmail(from_address, to_address_list, msg)
        server.quit()
