import requests
import json

baseurl = 'https://g8y8j.api.infobip.com/'
user = 'HerzuMx'
passw = '$UseR2704'
files = {
    'from': (None, 'HZD <contacto@info.herzudigital.com>'),
    #'to': (None, 'armando.hernandez.marin@gmail.com'),
    'to': (None, json.dumps({
        'to':'armando.hernandez.marin@gmail.com',
        'placeholders': {
            'firstName': 'ARMANDO'
        }})),
     'to': (None,'mexarm@me.com'),
     'defaultPlaceholders': json.dumps(dict(firstName='Cliente')),  
    'subject': (None, 'support confirmation'),
    #'text': (None, 'support confirmation body'),
    #'html' : open('/Users/armandohm/Projects/email_samples/bbvab1.html', 'rb').read(),
    'track' : True,
    'templateId': 52330,

    #'attachment': ('/Users/armandohm/Downloads/guias bodegon 2018-10-25 impresion.pdf', open('/Users/armandohm/Downloads/guias bodegon 2018-10-25 impresion.pdf', 'rb')),
    #'attachment': ('miadjunto.pdf', open('/Users/armandohm/Downloads/guias bodegon 2018-10-25 impresion.pdf', 'rb')),
}

response = requests.post('{}email/1/send'.format(baseurl), files=files, auth=(user, passw))

data = {
    'to': '525543961110',
    'text': 'Estimado Armando, esto es una prueba de HERZU Digital, https://www.herzudigital.com'
}

#response2 = requests.post('{}sms/1/text/single'.format(baseurl), data=data, auth=(user, passw))
