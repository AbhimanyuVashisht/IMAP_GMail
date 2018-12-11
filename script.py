import imaplib
import email

ORG_EMAIL = "@xane.ai"
FROM_EMAIL = "xane" + ORG_EMAIL
FROM_PWD = "<Enter your password here>"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

mail = imaplib.IMAP4_SSL(SMTP_SERVER)


def process_mailbox(M):
    rv, data = M.search(None, 'ALL')
    if rv != 'OK':
        print("No message found!")
        return
    for num in data[0].split():
        f = open('email/email' + num.decode('utf-8') + '.txt', 'a+')
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERR: ", num)
            return
        x = data[0][1].decode('utf-8')
        msg = email.message_from_string(x)
        f.write(msg['from'] + '\n\n\n')
        f.write(msg['Subject'] + '\n\n\n')
        f.write(msg['Date'] + '\n\n\n')
        print(msg['from'], msg['Subject'], msg['Date'])
        # if msg.is_multipart():
        #     for payload in msg.get_payload():
        #         if type(payload) is not list:
        #             f.write(payload.get_payload())
        #         else:
        #             print(payload.get_payload())
        # else:
        #     if type(msg) is not list:
        #         f.write(msg.get_payload())
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)
        else:
            body = msg.get_payload(decode=True)

        # print(body.decode)
        if type(body) is bytes:
            f.write(body.decode('utf-8', errors='ignore'))
        else:
            f.write(body)
        f.close()


def read_email():
    try:
        mail.login(FROM_EMAIL, FROM_PWD)
        rv, mailboxes = mail.list()
        if rv == 'OK':
            print('OK')
        rv, data = mail.select('INBOX')
        if rv == 'OK':
            process_mailbox(mail)
            mail.close()
        mail.logout()

    except Exception as e:
        print(e)


read_email()
