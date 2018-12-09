# -*- coding: utf-8 -*-

import requests
from gluon import current
from gluon.template import render
import re
from os import path, mkdir, walk
from gluon.fileutils import abspath


def download_file_from_s3(bucket_name, key, save_path, credentials):
    import boto3
    import botocore

    aws_access_key_id, aws_secret_access_key = credentials
    s3 = boto3.resource('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
    downloaded_file = path.join(save_path, key)
    try:
        s3.meta.client.download_file(bucket_name, key, downloaded_file)
        return downloaded_file
    except botocore.exceptions.ClientError as e:
        # print(e.response['Error'])
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def prepare_subfolder(subfolder):
    pth = path.join(abspath(request.folder), subfolder)
    if not path.isdir(pth):
        mkdir(pth)
    return pth


def get_api_key():
    return current.configuration.get('mailgun.api_key')


def api_send_message(domain, params):
    """ send a message 
        params = { data : ...,
                   files : ... }
    """
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(domain),
        auth=("api", get_api_key()),
        **params)

# def get_send_message_tuple(domain, params):
#     args = ['POST', 'https://api.mailgun.net/v3/{}/messages'.format(domain)]
#     kwargs = dict(
#         auth=("api", get_api_key()),
#         **params
#     )
#     return (args,kwargs


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def download_file(url, params={}, data={}, auth=None, method='GET', headers=None, filename=None, folder='/tmp'):
    # NOTE the stream=True parameter
    if method == 'GET':
        f = requests.get
    elif method == 'POST':
        f = requests.post
        #headers = {'Content-Type':'application/json'}
        #print headers
    r = f(url, allow_redirects=True, stream=True, headers=headers,
          data=data, params=params, auth=auth)  # timeout=0.1
    r.raise_for_status()
    if not filename:
        filename_cd = get_filename_from_cd(
            r.headers.get('Content-Disposition'))
        filename_url = url.split('/')[-1]
        filename = filename_cd or filename_url
    fullname = path.join(folder, filename)
    with open(fullname, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return fullname


def recursive_list_files(pth):
    files = list()
    for root, directories, filenames in walk(pth):
        for filename in filenames:
            files.append(path.join(root, filename))
    return files


def unzip_file(filename):
    import zipfile
    zip_ref = zipfile.ZipFile(filename, 'r')
    unzip_path = prepare_subfolder(filename+'.unzip')
    zip_ref.extractall(unzip_path)
    zip_ref.close()
    return recursive_list_files(unzip_path)
    # must return the list of filenames decompressed


def get_files(attachments, attach_temp_folder, context):
    import ntpath
    files = []
    for attach in attachments:
        downloaded_filename = None
        credentials = (attach.credentials.access_key_id, attach.credentials.secret_access_key) if attach.requires_auth or (
            attach.attachment_type == ATTACH_FROM_S3_OBJECT_KEY) else None
        if attach.upload:
            files.append(
                ('attachment', (attach.filename, open(attach.file, 'rb').read())))
        elif attach.attachment_type == ATTACH_FROM_URL:
            url = context[attach.attachment_field]
            headers = attach.headers
            method = attach.method or 'GET'
            static_name = attach.static_name
            downloaded_filename = download_file(
                url, auth=credentials, headers=headers, method=method,filename=static_name, folder=attach_temp_folder) 
                #data = ..., params= ... 
        elif attach.attachment_type == ATTACH_FROM_S3_OBJECT_KEY:
            downloaded_filename = download_file_from_s3(
                attach.bucket_name, context[attach.key_field], attach_temp_folder, credentials)
        if downloaded_filename:
            if attach.unzip and downloaded_filename[-4:].lower() == '.zip':
                for f in unzip_file(downloaded_filename):
                    files.append(
                        ('attachment', (ntpath.basename(f), open(f, 'rb').read())))
            else:
                files.append(('attachment', (ntpath.basename(
                    downloaded_filename), open(downloaded_filename, 'rb').read())))
    return files


def send(send_item):
    from html2text import html2text
    from requests.exceptions import HTTPError
    permanent_errors = [401, 404]
    broadcast, individual, custom_data, attach_temp_folder = send_item
    
    # [[xxx.yyy]] -> {{=xxx.yy}}
    raw_html_body = sub(r'(\[\[)(\w+\.\w+)(\]\])', r'{{=\2}}', broadcast.body.body)
    # [[xxx.yyy]] -> {{=xxx.yy}}
    raw_subject = sub(r'(\[\[)(\w+\.\w+)(\]\])', r'{{=\2}}', broadcast.subject)
    context = dict(custom_data.custom_data)
    # @TODO: filter individual properties before asign to data
    context.update(data=individual)
    subject = render(raw_subject, context=context)
    html_body = render(raw_html_body, context=context)
    text_body = html2text(html_body.decode('utf-8'))
    domain = broadcast.domain_
    data = {
        'from': broadcast.sender.from_line,
        'to': individual.send_email,
        'subject': subject,
        'html': html_body,
        'text': text_body
    }
    files = get_files(broadcast.attachments, attach_temp_folder, context)
    try:
        r = api_send_message(domain, dict(data=data, files=files))
        r.raise_for_status()
    except HTTPError as err:
        if not r.status_code in permanent_errors:
            raise HTTPError(err.message)
    return (individual.id, r.json())
