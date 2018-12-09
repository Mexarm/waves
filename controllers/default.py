# -*- coding: utf-8 -*-
if False:
    from gluon import *
    #from 10db import *  #repeat for all models
    from menu import *
    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T

@auth.requires_login()
def index():
    redirect(URL('select_tenant',vars=dict(next=URL('grid'))))

@auth.requires_login()
def select_tenant():
    tenant_ids = get_tenant_ids()
    if not tenant_ids: 
        session.flash = "Your user is not associated to a valid tenant"
        redirect('error')
    if len(tenant_ids) == 1:
        session.tenant_id = tenant_ids[0]
        if request.vars.next:
            redirect(request.vars.next)
    form = SQLFORM.factory(Field('tenant', 'string',default = tenant_ids[0], 
                            requires=IS_IN_DB(db(get_tenants_query('tenant',auth.user_id)),db.tenant.id,db.tenant._format)))
    if form.process().accepted:
        session.tenant_id = form.vars.tenant
        if request.vars.next:
            redirect(request.vars.next)
    return dict(form=form)

@auth.requires_login()
@requires_tenant(URL('default','select_tenant', vars=dict(next=URL())))
def file_import_s1():
    tenant = db.tenant(session.tenant_id)
    db.tenant_dataset.tenant.default = session.tenant_id
    set_fld_rw(db.tenant_dataset.tenant,r=True)
    form = SQLFORM(db.tenant_dataset, upload=URL('download'), fields=['tenant','description','datafile'])
    form.vars.tenant = session.tenant_id
    if request.vars.datafile!=None:
        form.vars.original_filename = request.vars.datafile.filename
    if form.process().accepted:
        dataset = db.tenant_dataset(form.vars.id)
        dataset.filesize = os.path.getsize(os.path.join(request.folder, DATASET_UPLOAD_FOLDER, dataset.datafile))
        dataset.update_record()
        session.flash = 'Dataset %s Uploaded' % dataset.description
        redirect(URL('file_import_s2', args=[dataset.id],user_signature=True))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)

@auth.requires_signature()
def file_import_s2():
    from file_import import detect_encoding
    dataset = db.tenant_dataset(request.args[0])
    result = detect_encoding(os.path.join(request.folder,DATASET_UPLOAD_FOLDER,dataset.datafile))
    form = SQLFORM(db.tenant_dataset,dataset,fields=['tenant','has_header','encoding_', 'delimiter_','quotechar'])
    form.vars.encoding_ = result['encoding']
    if form.process().accepted:
        redirect(URL('filemap', args=[dataset.id],user_signature=True))
    return dict(form=form)
    
@auth.requires_signature()
def filemap():
    from file_import import get_lines, create_header
    dataset = db.tenant_dataset(request.args[0])
    filename = os.path.join(request.folder,DATASET_UPLOAD_FOLDER,dataset.datafile)
    table = db.tenant_individual
    ifields = [ table.email, 
                table.mobile_number,
                table.name,    
                table.lastname,
                table.fullname,
                table.birthday,
                table.gender,
                table.external_id,
                table.doc_id ]
    file_lines = get_lines(filename,delimiter=dataset.delimiter_,encoding=dataset.encoding_)
    field_count = len(file_lines[0])
    first_row = 0
    file_header = []
    if dataset.has_header:
        file_header = file_lines[0]
        first_row = 1
    else:
        file_header = create_header('var',field_count)
    data_rows = [ OrderedDict(zip(file_header,line)) for line in file_lines[first_row:] ]
    form_fields = [ Field(fld,requires=IS_EMPTY_OR(IS_IN_SET([('[field]:'+f.name,f.label) for f in ifields]+[('[remove]',T('DO NOT IMPORT THIS COLUMN'))]))) for fld in file_header]
    buttons = [TAG.button('Back',_class="btn btn-secondary",_type="button",_onClick = "parent.location='%s' " % URL('file_import_s2', args=[dataset.id],user_signature=True)),
             TAG.button('Next',_class="btn btn-primary",_type="submit")]
    form = SQLFORM.factory(*form_fields, buttons=buttons)
    email_set = False
    for k in data_rows[0].iterkeys():
        if not IS_EMAIL()(data_rows[0][k])[1] and not email_set:
            form.vars[k] = '[field]:'+table.email.name
            email_set = True
        else:
            form.vars[k]=k
    if form.process(onvalidation=validate_filemap).accepted:
        fieldmap = OrderedDict()
        do_not_import = []
        for key in form.vars.iterkeys():
            if not form.vars[key] is None:
                if '[field]:' in  form.vars[key]: #its a field
                    field_name = form.vars[key].split(':')[1]
                    fieldmap[field_name] = key
                elif '[remove]' in form.vars[key]:
                    do_not_import.append(key)
        fieldmap_id = mongodb.fieldmap.insert(fieldmap=fieldmap, parent=dataset.id) #, do_not_import=do_not_import
        dataset.fieldmap = fieldmap_id 
        dataset.field_list = file_header
        dataset.update_record()
        task_id = scheduler.queue_task('import_csv_task',
                                 pargs=[dataset.id],
                                 immediate=True,
                                 group_name=IMPORT_TASK_GROUP,
                                 #application_name=BACKEND,
                                 timeout= 60*60*3, # 3 horas
                                 output = True).id
        session.flash = "import task created with id=%d" % task_id
        redirect(URL('grid'))
    elif form.errors:
        response.flash = form.errors

    return dict(data_rows = data_rows, form=form, colnum_string=colnum_string)

def att():
    form = SQLFORM(db.tenant_attachment,1)
    if form.process().accepted:
        session.flash="accepted"
        redirect(URL())
    elif form.errors: 
        print form.errors
        response.flash="errors"
    
    

    return dict(form=form)

def api_tags():
    query = request.vars.q
    # return query
    if query:
        qry = db.tenant_tag.tag.like('%{}%'.format(query))
    else:
        qry = db.tenant_tag.id > 0 
    rows = db(qry).select(db.tenant_tag.id, db.tenant_tag.tag,limitby=(0,100), orderby=db.tenant_tag.tag)
    #response.headers['content-type'] = 'application/json'
    return response.json(rows)

def myonvalidation(form):
    if form.table._tablename == 'tenant_attachment' and request.vars.filename:
        # if request.vars.filename:
        form.vars.filename = request.vars.filename

@auth.requires_login()
@requires_tenant(URL('default','select_tenant', vars=dict(next=URL())))
def grid():
    auth_tables =[ auth.settings[t] for t in auth.settings.keys() if re.match(r'table_\w+_name',t)]
    app_tables = [ t for t in db.tables() if not t in auth_tables ]
    constraints = { t: get_tenants_query(t, auth.user_id) for t in app_tables }
    constraints.update( tenant =  (db.tenant.id == session.tenant_id) )
    for t in app_tables:
        set_requires(db[t])
    #print request.vars
    db.tenant_broadcast.domain_.requires = IS_IN_DB(db(constraints['tenant_domain'] & (db.tenant_domain.verified == True)),
                                                    'tenant_domain.id', db.tenant_domain._format)
    db.tenant_broadcast.sender.requires = IS_IN_DB(db(constraints['tenant_sender'] & (db.tenant_sender.verified == True)),
                                                   'tenant_sender.id', db.tenant_sender._format)
    #db.tenant_broadcast.body.requires = IS_IN_DB(db(constraints['tenant_body'] & (db.tenant_sender.verified == True)),
    #                                               'tenant_sender.id', db.tenant_sender._format)
    #return response.json(str(constraints))
    if not request.vars.attachment_file is None:
        if hasattr( request.vars.attachment_file, 'filename'):
            request.vars.filename = request.vars.attachment_file.filename
    grid = SQLFORM.smartgrid(db.tenant, constraints = constraints, onvalidation=myonvalidation)
    return dict(grid=grid)
    
# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def edit_body():
    tenant_body_id = int(request.args[0])
    # @TODO only allow the user to access bodies of his tenats
    form=SQLFORM(db.tenant_body,tenant_body_id)
    if form.process().accepted:
       response.flash = T('broadcast body saved')
    elif form.errors:
        response.flash = T('errors')
    return dict(form=form)

def edit_broadcast():
    tenant_broadcast_id = int(request.args[0])
    # @TODO only allow the user to access bodies of his tenats
    db.tenant_broadcast.body.widget = SQLFORM.widgets.autocomplete(
     request, db.tenant_body.description, id_field=db.tenant_body.id,limitby=(0,10), min_length=0)
    form=SQLFORM(db.tenant_broadcast,tenant_broadcast_id)
    if form.process().accepted:
       response.flash = T('broadcast saved')
    elif form.errors:
        response.flash = T('errors')
    return dict(form=form)

def autocomplete():
    form=FORM('Your name:',
              INPUT(_name='name', requires=IS_NOT_EMPTY()),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

def error():
    return dict()

@request.restful()

#http://127.0.0.1:8000/waves/default/api/tags/contains/di.json
#{"content": [{"tag": "dimex", "id": 5, "tenant": 1}, {"tag": "readers-digest", "id": 11, "tenant": 1}]}
#http://127.0.0.1:8000/waves/default/api/tag/11.json
#{"content": [{"tag": "readers-digest", "id": 11, "tenant": 1}]}

def api():
    response.view = 'generic.' + request.extension
    def GET(*args,**vars):
        patterns = [
            "/tags/contains/{tenant_tag.tag.contains}",
            "/tag/{tenant_tag.id}"
            ]
        limit = int(vars['limit']) if 'limit' in vars else None
        parser = db.parse_as_rest(patterns, args, vars)
        if parser.status == 200:
            return dict(content=parser.response if not limit else parser.response[:limit])
        else:
            raise HTTP(parser.status, parser.error)

    # def POST(table_name, **vars):
    #     if table_name == 'person':
    #         return dict(db.person.validate_and_insert(**vars))
    #     elif table_name == 'pet':
    #         return dict(db.pet.validate_and_insert(**vars))
    #     else:
    #         raise HTTP(400)
    return locals()