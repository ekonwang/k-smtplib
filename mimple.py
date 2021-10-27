import smtplib
from email.mime.text import MIMEText
from email.header import Header
# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "yifouforum@qq.com" # 用户名
mail_pass = "frgpfojetmifhjeg" # 口令
sender = "yifouforum@qq.com"
# receivers = ['21210240375@m.fudan.edu.cn'] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
receivers = ['19307110217@fudan.edu.cn']
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("python robot", 'utf-8')
message['To'] = Header("google mail receiver", 'utf-8')
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
try:
    smtp = smtplib.SMTP()
    smtp.connect(mail_host, 587)
    smtp.login(mail_user, mail_pass)
    smtp.sendmail(sender, receivers, message.as_string())
    print(message.as_string())
    print('发送成功')
except smtplib.SMTPException as e:
    print('发送失败')
    raise e
