# -*- coding: utf-8 -*-

BROADCAST_STATE_DRAFT = 'draft'
BROADCAST_STATE_ENDED = 'ended'

CHANNEL_TYPES = ['email','SMS']
CREDIT_ENTITIES = ['broadcast', 'purchase', 'send']

ATTACHMENT_TEMP_FOLDER = 'temp'
ATTACH_FROM_URL = 'Attach from URL'
ATTACH_FROM_S3_OBJECT_KEY = 'Attach from S3 object key'
CUSTOM_FIELD_TYPES_ATTACHMENTS = [ATTACH_FROM_URL, ATTACH_FROM_S3_OBJECT_KEY]
ATTACHMENT_NAME_FROM_URL_PARAM = 'from url'
ATTACHMENT_NAME_FROM_URL_CONTENT_DISPOSITION = 'from CONTENT-DISPOSITION'
ATTACHMENT_NAME_SPECIFIED = 'specified'
ATTACHMENT_NAME_FROM_URL = [ATTACHMENT_NAME_FROM_URL_PARAM,
                            ATTACHMENT_NAME_FROM_URL_CONTENT_DISPOSITION, 
                            ATTACHMENT_NAME_SPECIFIED]

CUSTOM_FIELD_TYPES = ['Text', 'Decimal Number', 'Integer Number', 'True/False', 'Fecha']
ADMIN_ROLE = 'admin'
TENANT_ADMIN = 'tenant_admin'
DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STORAGE_TYPE_SUPPORTED = ['AWS S3', 'URL WITH BASIC AUTH']

DATASET_UPLOAD_FOLDER = 'datasets'

IMPORT_TASK_GROUP = 'import_task'

DATETIME_UTC = configuration.get('app.datetime_utc')
NOW_UTC = request.utcnow.replace(tzinfo=pytz.utc)
# auth.signature UTC based
def utc_signature():
    auth.signature.created_on.default = NOW_UTC
    auth.signature.modified_on.default = NOW_UTC
    auth.signature.modified_on.update = NOW_UTC

REPR_DATETIME = lambda value,row: value.strftime(DEFAULT_DATETIME_FORMAT) if value else ''

TABLE_FILTERS = {}

DATA_IMPORT_PARAMS = dict( delimiters =  [',', '\t', '|', ';'], quotechars= ['"',"'"], encodings=['ascii','utf-8','UTF-8-SIG','ISO-8859-1'])
