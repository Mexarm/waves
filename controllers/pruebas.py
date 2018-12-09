# -*- coding: utf-8 -*-

#https://web2py.readthedocs.io/en/latest/tools.html#gluon.tools.Auth.jwt
@auth.allows_jwt()
@auth.requires_login()
def myapi(): return 'hello %s' % auth.user.email

def manage_tokens():
    return auth.manage_tokens()