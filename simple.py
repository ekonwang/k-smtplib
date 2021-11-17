import ksmtplib
from email.mime.text import MIMEText
from email.header import Header


mail_host = None # For instance : "smtp.qq.com".
mail_user = "yifouforum@qq.com" # Your acount, for instance, "1@qq.com".
mail_pass = "frgpfojetmifhjeg" # Your password.

content =  None # Content of email, for instance:
f'''
神秘博士：
    您好，这里是M78星云给您发来的问候。
此致
'''

receivers = None # A list of receiver, for instance : ['g1547246193@gmail.com']
message = MIMEText(content, 'plain', 'utf-8')
message['From'] = Header(mail_user, 'utf-8')
message['To'] = Header((', ').join(receivers), 'utf-8')
subject = None # Email subject: 'KSMTP Test' 
message['Subject'] = Header(subject, 'utf-8')

try:
    ksmtp = ksmtplib.KSMTP(1)
    port = None # A port.
    ksmtp.connect(mail_host, port)
    ksmtp.start_tls()
    ksmtp.login(mail_user, mail_pass)
    ksmtp.email(mail_user, receivers, message.as_string())
    ksmtp.close()
    print('Sent Successfully.')
except OSError as e:
    print('Failed to send.')
    raise e
    