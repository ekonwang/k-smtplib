import test
from email.mime.text import MIMEText
from email.header import Header
# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "yifouforum@qq.com" # 用户名
mail_pass = "frgpfojetmifhjeg" # 口令
# receivers = ['21210240375@m.fudan.edu.cn'] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
receivers = ['1547246193@qq.com']
message = MIMEText('你好帅我好爱\r\n哈哈哈你好\r\n', 'plain', 'utf-8')
message['From'] = Header(mail_user, 'utf-8')
message['To'] = Header((', ').join(receivers), 'utf-8')
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
try:
    smtp = test.SMTP()
    smtp.debuglevel = 1
    smtp.connect(mail_host, 587)
    smtp.login(mail_user, mail_pass)
    smtp.sendmail(mail_user, receivers, message.as_string())
    # print(message.as_string())
    print('发送成功')
except test.SMTPException as e:
    print('发送失败')
    raise e
