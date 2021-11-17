from datetime import datetime
import ksmtplib
from email.mime.text import MIMEText
from email.header import Header

current_time_stamp = str(datetime.now())

mail_host = "smtp.qq.com"  
mail_user = "yifouforum@qq.com" 
mail_pass = "frgpfojetmifhjeg" 

content = f'''
神秘博士：
    您好，这里是M78星云给您发来的问候。
此致
'''

receivers = ['g1547246193@gmail.com']
message = MIMEText(content, 'plain', 'utf-8')
message['From'] = Header(mail_user, 'utf-8')
message['To'] = Header((', ').join(receivers), 'utf-8')
subject = 'KSMTP Test %s' %current_time_stamp
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
    