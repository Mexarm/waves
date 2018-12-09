# -*- coding: utf-8 -*-

def update_groups():
    rows = db.executesql("""SELECT tenant 
                      FROM   tenant t 
                      WHERE  NOT EXISTS (
                      SELECT 1 
                      FROM   auth_group g
                      WHERE  t.tenant = g.role
                      );""")
    for description, in rows:
        auth.add_group(description, 'auto created group for tenant %s'% description)
        db.commit()
    
def get_tenant(tenant_name):
    return db(db.tenant.tenant==tenant_name).select(limitby=(0,1)).first()

def get_tenant_ids():
    user_id = auth.user_id
    if not user_id: redirect(URL('user', args=['login'],vars=dict(next = URL())))
    groups = auth.user_groups
    ids = []
    for key in groups.keys():
        tenant = get_tenant(groups[key])
        if tenant:
            ids.append(tenant.id)
    return ids

def get_tenants_query(table, user_id):
    fld = None
    if isinstance(table, str) and table in db.tables():
        table = db[table]
    if table._tablename == 'tenant':
        fld = table.id
    elif hasattr(table, 'tenant'):
        fld = table.tenant
    else:
        return table.id>0 # no filter
    t = get_tenant_ids()
    if len(t)>0:
        return ((fld == t[0]) if len(t)==1 else fld.belongs(t))
    return table.id==-1 # not allowed
        #'%s.%s'%(table._tablename,fld._raw_rname)
    #session.flash = T("No Tenant is associated with your account (user_id=%d), please contact your system administrator"%user_id)

# def apply_table_filters():
#     for t in db.tables():
#         if  hasattr(db[t],'apply_filters'):
#             db[t].apply_filters()

def only_tenant_records(table,user_id=None):
    from pydal.objects import Set, Query
    if not user_id:
        user_id = auth.user_id
    if isinstance(table, str) and table in auth.db.tables():
        table = auth.db[table]
        return get_tenants_query(table,user_id)
    elif isinstance(table, (Set, Query)):
        if isinstance(table, Set):
            cquery = table.query
        else:
            cquery = table
        tablenames = auth.db._adapter.tables(cquery)
        for tablename in tablenames:
            cquery &= get_tenants_query(tablename, user_id)
        return cquery
        # if not isinstance(table, str) and \
        #         self.has_permission(name, table, 0, user_id):
        #     return table.id > 0
    
    return get_tenants_query(table,user_id)

def set_requires(table):
    for f in table.fields():
        fld = table[f]
        if fld.type.startswith('reference'):
            rtable = fld.type.split(' ')[1]
            qry = get_tenants_query(rtable,auth.user_id)
            is_in_db = IS_IN_DB(db(qry),db[rtable]._id,db[rtable]._format)
            fld.requires = is_in_db if fld.notnull else IS_EMPTY_OR(is_in_db)

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def validate_filemap(form):
    #print form.vars.file_lines
    # for v in form.vars.iterkeys():
    #     if form.vars[v] == "":
    #         form.vars[v] = v
    #@TODO: do other validations 
    pass

def requires_tenant(redirect_url):
    def requires_tenant_(func):
        def wrapper():
            if not session.tenant_id: redirect(redirect_url)
            return func()
        return wrapper
    return requires_tenant_

def set_fld_rw(fld,r=False,w=False):
    fld.readable = r
    fld.writable = w

def import_csv_task(dataset_id):
    from file_import import import_csv, get_lines
    dataset = db.tenant_dataset(dataset_id)
    fieldmap = mongodb.fieldmap(dataset.fieldmap).fieldmap
    filename=os.path.join(request.folder,DATASET_UPLOAD_FOLDER,dataset.datafile)
    header = get_lines(filename, linecount=1, encoding=dataset.encoding_, delimiter=dataset.delimiter_, quotechar=dataset.quotechar)[0] if dataset.has_header else 'var'
    import_csv(db,mongodb,dataset.id,filename,field_map=fieldmap,encoding=dataset.encoding_,header=header, delimiter=dataset.delimiter_, quotechar=dataset.quotechar)
    #import_csv(db, mongodb, tenant_id, filename, field_map=None, encoding='utf-8', header='var', delimiter=',', quotechar='"'):

def send_email_range(broadcast_id, dataset_id, from_seq, to_seq):
    from Queue import Queue
    import MTRequests

    tb = db.tenant_broadcast
    tds = db.tenant_dataset
    ti = db.tenant_individual
    broadcast = tb(broadcast_id)
    dataset= tds(dataset_id)
    rows = db((ti.dataset == dataset_id) & (ti.seq>=from_seq) & (ti.seq<=to_seq)).select()
    q = Queue()
    for row in rows:
        q.put((row.id,['GET', 'https://httpbin.org/anything/v3/domain/messages'],{ "data" : {"to":row.email,"from":"test@test.com"}}))
    mt_requests = MTRequests.MTRequests(q)
    out_queue = mt_requests.run()
    for i in range(out_queue.qsize()):
        params, response, duration = out_queue.get()
        mongodb.tenant_event.insert(tenant=broadcast.tenant,individual=params[0],event_type="send",event_data=response.json())
        # db(ti.id == params[0]).update(status='sent')
        # db.commit()
        mongodb.commit()

# def recursive_list_files(pth):
#     from os import path, mkdir, system, remove, walk, listdir
#     files=list()
#     for root, directories, filenames in walk(pth):
#         for filename in filenames:
#             files.append(path.join(root,filename))
#     return files

# # def download_file(url,filename):
# #     import urllib2
# #     res=urllib2.urlopen(url.replace(' ','%20'))
# #     f=open(filename,'wb')
# #     f.write(res.read())
# #     f.close()


# def is_downloadable(url):
#     import requests
#     """
#     Does the url contain a downloadable resource
#     """
#     h = requests.head(url, allow_redirects=True)
#     header = h.headers
#     content_type = header.get('content-type')
#     if 'text' in content_type.lower():
#         return False
#     if 'html' in content_type.lower():
#         return False
#     return True

# #print is_downloadable('https://www.youtube.com/watch?v=9bZkp7q19f0')
# # >> False
# #print is_downloadable('http://google.com/favicon.ico')
# # >> True

# def get_filename_from_cd(cd):
#     import requests
#     import re
#     """
#     Get filename from content-disposition
#     """
#     if not cd:
#         return None
#     fname = re.findall('filename=(.+)', cd)
#     if len(fname) == 0:
#         return None
#     return fname[0]

# class FileNameError(Exception):
#     """ Could not determine filename from URL or content-disposition
#     """
#     pass
    
# def download_file_from_url(url, path, name_source=ATTACHMENT_NAME_SOURCE_FROM_URL_CONTENT_DISPOSITION, auth=None):

#     import os
#     kwargs = dict(auth=auth) if auth else dict()
#     kwargs.update(allow_redirects=True)
#     r = request.get(url,**kwargs)
#     r.raise_for_status()
#     filename=None
#     if name_source == ATTACHMENT_NAME_SOURCE_FROM_URL_CONTENT_DISPOSITION:
#         filename = get_filename_from_cd(r.headers.get('content-disposition'))
#     elif name_source == ATTACHMENT_NAME_SOURCE_FROM_URL_PARAM:
#         if url.find('/'):
#             filename = url.rsplit('/', 1)[1]
#     if not filename:
#         raise FileNameError("could not determine file name for download url {}".format(url))
#     fullname = os.path.join(path,filename)
#     open(fullname,'wb').write(r.content)
#     return fullname


# def unzip_file(filename):
#     import zipfile
#     zip_ref = zipfile.ZipFile(filename, 'r')
#     unzip_path = prepare_subfolder(filename+'.unzip')
#     zip_ref.extractall(unzip_path)
#     zip_ref.close()
#     return recursive_list_files(unzip_path)


# def save_attachment_from_url(url, path, name_source=ATTACHMENT_NAME_SOURCE_FROM_URL_CONTENT_DISPOSITION, auth=False, uncompress_attachment=False):
#     pth=prepare_subfolder('attach_temp/')
#     pth=prepare_subfolder('attach_temp/{}'.format(b64encode(url))

#     fullname = path.join(pth, filename)
#     if not path.isfile(fullname):
#         download_file(url,fullname)
#     #@TODO howto verify checksum ??? verify_checksum(doc.checksum,fullname)
#     if filename.lower() == '.zip' and uncompress_attachment:
#         return unzip_file(fullname)
#     return [fullname]

