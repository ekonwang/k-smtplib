import ksmtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.qq.com"  
mail_user = "yifouforum@qq.com" 
mail_pass = "frgpfojetmifhjeg" 

receivers = ['1547246193@qq.com']
message = MIMEText('你好帅我好爱\r\n哈哈哈你好\r\n', 'plain', 'utf-8')
message['From'] = Header(mail_user, 'utf-8')
message['To'] = Header((', ').join(receivers), 'utf-8')
subject = 'KSMTP test'
message['Subject'] = Header(subject, 'utf-8')

try:
    ksmtp = ksmtplib.KSMTP(1)
    ksmtp.connect(mail_host, 587)
    ksmtp.start_tls()
    ksmtp.login(mail_user, mail_pass)
    ksmtp.email(mail_user, receivers, message.as_string())
    ksmtp.close()
    print('发送成功')
except OSError as e:
    print('发送失败')
    raise e
    