# -*- coding: utf-8 -*-

if DATETIME_UTC:
    utc_signature()

def tenant_field():
    # return Field('tenant', 'string', length=128, unique=True, notnull=True, requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db,'tenant.tenant')])
    return Field('tenant', 'reference tenant', notnull=True)

db.define_table('tenant',
                Field('tenant', 'string', length=128, unique=True, notnull=True, requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db,'tenant.tenant')]),
                Field('description', 'string', length=256),
                auth.signature, 
                format='%(tenant)s',
                singular=T('Company'), 
                plural=T('Companies') )
# def tenant():
#     t = db.tenant
#     qry,fld = get_tenants_query(db.tenant)
#     t.tenant.requires=IS_IN_DB(db(qry),fld,'%(tenant)s')
#     t.tenant.default = get_tenant_ids()[0]

# db.tenant.apply_filters = tenant

#db(auth.accessible_query('read', db.mytable)).select(db.mytable.ALL)

db.define_table('balance_entry',
                tenant_field(),
                Field('channel_type', 'string', requires=IS_IN_SET(CHANNEL_TYPES)),
                Field('qty', 'float', notnull=True),
                Field('balance', 'float', notnull=True),
                Field('origin_type', 'string', notnull=True, requires=IS_IN_SET(CREDIT_ENTITIES)), #type of entity that generated this entry
                Field('origin_id', 'string', notnull=True), #id of the entity that generated this entry
                Field('datetime_applied', notnull=True, default=NOW_UTC),
                auth.signature)

db.define_table('tenant_tag',
                tenant_field(),
                Field('tag','string',length=32,notnull=True, requires=[IS_SLUG()]),
                auth.signature,
                format='%(tag)s',
                singular=T('tag'), 
                plural=T('tags'))

db.define_table('tenant_storage_credential',
                tenant_field(),
                Field('storage_friendly_name','string', notnull=True, unique=True,label=T('Storage or endpoint friendly name')),
                Field('storage_type', 'string', length=20,notnull=True, requires=IS_IN_SET(STORAGE_TYPE_SUPPORTED)),
                Field('access_key_id','password', notnull=True, unique=True, readable=False, label = 'Access key id or username'),
                Field('secret_access_key', 'password', notnull=True,readable=False, label='Secret access key or password'),
                #Field('url', 'string'),
                auth.signature,
                format='%(storage_friendly_name)s',
                singular=T('storage credentials'), 
                plural=T('storage credentials'))

db.define_table('tenant_sender',
                tenant_field(),
                Field('name', 'string'),
                Field('address', 'string', requires=IS_EMAIL(), unique=True, notnull=True),
                Field.Virtual('formatted', lambda row: '{} <{}>'.format(row.tenant_sender.name,row.tenant_sender.address) if row.tenant_sender.name else '{}'.format(row.tenant_sender.address)),
                Field('verified', 'boolean'),
                Field('verification_key','string', length=36, default=web2py_uuid()),
                auth.signature,
                format='%(address)s',
                singular=T('sender'), 
                plural=T('senders'))

db.define_table('tenant_domain',
                tenant_field(),
                Field('domain_'),
                Field('verified','boolean'),
                auth.signature,
                format=lambda r: '%(domain_)s[VERIFIED]'%r if r.verified else '%(domain_)s[NOT VERIFIED]'%r,
                singular=T('domain'), 
                plural=T('domains')
                )

db.define_table('tenant_body',
                tenant_field(),
                Field('description'),
                Field('channel_type', 'string', requires=IS_IN_SET(CHANNEL_TYPES)),
                Field('is_template','boolean'),
                Field('body', 'text'),
                auth.signature,
                format='%(channel_type)s:%(description)s',
                singular=T('message body'), 
                plural=T('message bodies'))


db.define_table('tenant_attachment',
                tenant_field(),
                Field('description'),
                Field('upload', 'boolean', label='upload attachment'),
                Field('filename', 'string', writable = False),
                Field('attachment_file','upload', uploadfolder=os.path.join(request.folder,DATASET_UPLOAD_FOLDER), 
                                       autodelete=True),
                Field('attachment_field','string'),
                Field('attachment_type','string', requires=IS_EMPTY_OR(IS_IN_SET(CUSTOM_FIELD_TYPES_ATTACHMENTS))),
                Field('name_source_from_url', 'string', requires=IS_EMPTY_OR(IS_IN_SET(ATTACHMENT_NAME_FROM_URL))),
                Field('bucket_name', 'string', comment='required for S3'),
                Field('key_field', 'string', comment='required for S3'),
                Field('requires_auth','boolean'),
                Field('lista','list:reference tenant_tag', widget = SelectMultiple.widget),
                # Field('lista','list:string'),
                Field('headers','json'),
                Field('unzip', 'boolean', default = False, label='unzip downloaded file before attach'),
                Field('http_method', 'string', default='GET', requires=IS_EMPTY_OR(IS_IN_SET(['GET','POST']))),
                Field('data_params', 'json'), #user can say { 'account': '{{MyField}}' }
                Field('static_name',comment='rename the attachment to this name, you can use variables {{MyField}}.pdf'),
                Field('credentials', 'reference tenant_storage_credential'),
                auth.signature,
                format='%(description)s',
                singular=T('attachment'), 
                plural=T('attachments'))

def tenant_attachment_show_if():
    #db.tenant_attachment.filename.show_if= (db.tenant_attachment.upload==True) 
    db.tenant_attachment.attachment_file.show_if=(db.tenant_attachment.upload==True)
    db.tenant_attachment.attachment_field.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.attachment_type.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.name_source_from_url.show_if=(db.tenant_attachment.upload==False) 
    db.tenant_attachment.bucket_name.show_if=(db.tenant_attachment.upload==False) 
    db.tenant_attachment.key_field.show_if=(db.tenant_attachment.upload==False) 
    db.tenant_attachment.requires_auth.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.headers.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.unzip.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.http_method.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.data_params.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.static_name.show_if=(db.tenant_attachment.upload==False)
    db.tenant_attachment.credentials.show_if=(db.tenant_attachment.requires_auth==True)
    
tenant_attachment_show_if()

db.define_table('tenant_broadcast',
                tenant_field(),
                Field('uuid','string',length=36, default=web2py_uuid()),
                Field('description','string', notnull=True, length=384),
                Field('channel_type','string', notnull=True,requires=IS_IN_SET(CHANNEL_TYPES)),
                Field('domain_','reference tenant_domain'),
                Field('sender', 'reference tenant_sender'),
                Field('subject', 'string'),
                Field('status', 'string', length=20,notnull=True, default=BROADCAST_STATE_DRAFT),
                Field('tags','list:reference tenant_tag'),
                Field('associated_storage', 'reference tenant_storage_credential'),
                Field('body', 'reference tenant_body'),
                Field('attachments','list:reference tenant_attachment'),
                auth.signature,
                format='%(channel_type)s:%(description)s',
                singular=T('broadcast'), 
                plural=T('broadcasts'))



# def tenant_broadcast():
#     t = db.tenant_broadcast
#     qry,fld = get_tenants_query(db.tenant)
#     t.tenant.requires = IS_IN_DB(db(qry),fld,'%(tenant)s')
#     qry,fld = get_tenants_query(db.tenant_storage_credential)
#     t.associated_storage.requires = IS_NULL_OR(IS_IN_DB(db(qry),fld,'%(storage_friendly_name)s'))


# db.tenant_broadcast.apply_filters = tenant_broadcast



# def tenant_body():
#     t = db.tenant_body
#     qry,fld = get_tenants_query(db.tenant)
#     t.tenant.requires = IS_IN_DB(db(qry),fld,'%(tenant)s')

# db.tenant_body.apply_filters = tenant_body
db.define_table('tenant_dataset',
                tenant_field(),
                Field('original_filename', notnull=True),
                Field('datafile','upload', 
                        requires=IS_UPLOAD_FILENAME(extension="^txt$|^csv$"), 
                        uploadfolder=os.path.join(request.folder,DATASET_UPLOAD_FOLDER), 
                        autodelete=True),
                Field('filesize','integer'),
                Field('description'),
                Field('system_tag'),
                Field('encoding_', requires= IS_IN_SET(DATA_IMPORT_PARAMS['encodings'])),
                Field('has_header', 'boolean'),
                Field('field_list','list:string'),
                Field('delimiter_', requires= IS_IN_SET(DATA_IMPORT_PARAMS['delimiters'])),
                Field('quotechar', requires= IS_IN_SET(DATA_IMPORT_PARAMS['quotechars'])),
                Field('status'),
                Field('fieldmap', 'string'),
                auth.signature,
                format='%(description)s',
                singular=T('Data Set'), 
                plural=T('Data Sets')
                )

db.define_table('tenant_custom_field',
                tenant_field(),
                Field('name','string',length=64,notnull=True),
                Field('field_type', 'string',notnull=True,requires=IS_IN_SET(CUSTOM_FIELD_TYPES)),
                auth.signature)

db.define_table('tenant_individual',
                tenant_field(),
                Field('dataset', 'reference tenant_dataset'),
                Field('email', 'string', length=128),
                Field('mobile_number', 'string', length= 20, label=T('Mobile Number')),
                Field('name', 'string', length=80),    
                Field('lastname', 'string', length=80),
                Field('fullname', 'string'),
                Field('birthday','datetime', label=T('Birthday')),
                Field('gender', 'string'),
                Field('external_id','string', length=256),
                Field('seq', 'integer'),
                Field('doc_id', 'string'), 
                auth.signature,
                )
                #custom data, example: 
                #"""
                #{ "rfc": "xxxx0909091a2",
                #   "nss": "12192181811",
                #   "credit": 123.99
                #}
                #each key (rfc,nss,credit) has an entry on table tenant_custom field
                #"""

db.define_table('broadcast_target',
                Field('parent_type'), #parent table name or direct, in case of direct target should be an email or a mobile number. 
                Field('parent_id', 'integer'),
                Field('target', 'string', requires=IS_EMPTY_OR(IS_EMAIL())))
                #@TODO requires IS_EMPTY_OR(IS_MOBILE_NUMBER())

# db.define_table('broadcast_sender',
#                 Field('broadcast', 'reference tenant_broadcast', requires=IS_IN_DB(db, 'tenant.id', '%(tenant)s')),
#                 Field('tenant_sender', 'reference tenant_sender', requires=IS_IN_DB(db, 'tenant_sender.id', '"%(name)s" <%(address)s>')))

# db.define_table('broadcast_body',
#                 Field('broadcast','reference tenant_broadcast', requires=IS_IN_DB(db, 'tenant.id', '%(tenant)s')),
#                 Field('tenant_body', 'reference tenant_body', requires=IS_IN_DB(db, 'tenant_body.id', '%(description)s')))

# --- mongo db -----

mongodb.define_table('email_verification',
                Field('email'),
                Field('verification_result'),
                Field('verified_on', 'datetime'),
                Field('raw_api_response', 'json'))

mongodb.define_table('custom_data',
                Field('custom_data','json'),
                Field('parent','integer'))

mongodb.define_table('fieldmap',
                Field('fieldmap','json'),
                Field('parent','integer'))

mongodb.define_table('tenant_event',
                #tenant_field(),
                Field('tenant', 'integer'),
                Field('individual','integer'),
                Field('event_type'),
                Field('event_data','json'))