import ksmtplib

mail_host = "smtp.qq.com"  
mail_user = "yifouforum@qq.com" 
mail_pass = "frgpfojetmifhjeg" 
sender = "yifouforum@qq.com"

try:
    smtp = ksmtplib.SMTP(1)
    smtp.connect(mail_host, 587)
    smtp.login(mail_user, mail_pass)
except OSError as e:
    print('发送失败')
    raise e