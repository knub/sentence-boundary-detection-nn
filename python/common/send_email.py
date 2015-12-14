import smtplib, ConfigParser, argparse

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

    def __format_message(self):
        message_with_header = "\r\n".join([
          "From: %s" % from_address,
          "To: %s" % ",".join(to_address_list),
          "Subject: [Pamur] %s" % self.subject,
          "",
          "%s" % self.message
          ])
        return message_with_header

    def send(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        msg = self.__format_message()
        server.sendmail(from_address, to_address_list, msg)
        server.quit()

    def attach_files(self, files):
        for filename in files:
            self.message += "\r\n\r\n========== %s ==========\r\n" % filename
            with open(filename, "r") as file_:
                for line in file_:
                    self.message += "> %s" % line
            self.message += "\r\n\r\n========== %s ==========\r\n" % filename

def main(args):
    e = EmailNotification(args.subject, args.message)
    e.attach_files(args.files)
    # print e.message
    e.send()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a notification email')
    parser.add_argument('subject', help='subject of the email')
    parser.add_argument('message', help='message of the email')
    parser.add_argument('files', help='files which are appended after the text', nargs='*')
    args = parser.parse_args()
    main(args)
