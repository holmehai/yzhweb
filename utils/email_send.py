# -*- coding: utf-8 -*-
__author__ = 'yzh'
__date__ = '2018/4/7/007 19:39'
from random import Random
from django.core.mail import send_mail

from  users.models import EmailVerifyRecord
from yzhweb.settings import EMAIL_FROM


def generate_random_str(randomlength=8):
    str=''
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str=str+chars[random.randint(0,length)]
    return str


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code=code
    email_record.email = email
    email_record.send_type=send_type
    email_record.save()

    email_title=''
    email_body=''

    if send_type=='register':
        email_title='yzhlab注册激活链接'
        email_body='请点击下面的链接激活账号：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])

    elif send_type == 'forget':
        email_title = 'yzhlab密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])