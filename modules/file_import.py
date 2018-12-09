# -*- coding: utf-8 -*-

import csv
import codecs
import json
from collections import OrderedDict

def csv_unireader(f, encoding="utf-8",delimiter=',', quotechar='"'):
    for row in csv.reader(codecs.iterencode(codecs.iterdecode(f, encoding), "utf-8"),delimiter=delimiter,quotechar=quotechar):
        yield [e.decode("utf-8") for e in row]

def get_lines(filename, linecount=10, encoding='utf-8', delimiter=',', quotechar='"'):
    with open(filename,'rb') as handle:
        csv_reader = csv_unireader(handle,encoding=encoding, delimiter=delimiter, quotechar=quotechar)
        lines = []
        for i,line in enumerate(csv_reader):
            if i>=linecount: break
            lines.append(line)
        return lines

def create_header(header_prefix, col_count):
    if not '%d' in header_prefix:
        header_prefix = header_prefix + "%d"
    return [ header_prefix%i for i in range(1,col_count+1) ]

def import_csv(db, mongodb, dataset_id, filename, field_map=None, encoding='utf-8', header='var', delimiter=',', quotechar='"'):
    # if header is a string it is the prefix for header names ex. var1, var2, etc, else pass a list with the header names
    dataset = db.tenant_dataset(dataset_id)
    tenant_id = dataset.tenant
    with open(filename,'rb') as handle:
        csv_reader = csv_unireader(handle,encoding=encoding, delimiter=delimiter, quotechar=quotechar)
        col_count = 0
        #header = []
        if isinstance(header,list):
            csv_reader.next()
        for lineno,line in enumerate(csv_reader):
            #line=[ f.decode(encoding).encode('utf-8') for f in line] #converts to utf-8
            if col_count == 0: 
                col_count = len(line)
                #print header
                if isinstance(header, str):
                    header = create_header(header,col_count)
            elif not col_count==len(line) or not len(header)==len(line):
                raise ValueError('numero de columnas inconsistente en linea: %s'%line)
                #@TODO do not make the import process fail, instead add error rows to a list and report to the user at the end of the process
            
            #print header,line
            file_record = OrderedDict(zip(header,line))
            #print file_record
            record = { f:file_record[field_map[f]] for f in field_map}
            # record.update(dict(custom_data=file_record,tenant=tenant_id))
            record.update(dict(dataset=dataset.id, seq=lineno+1,tenant=tenant_id))
            res =  db.tenant_individual.validate_and_insert(**record)
            custom_data_id =  mongodb.custom_data.insert(custom_data=file_record)
            db.tenant_individual(res.id).update_record(doc_id=custom_data_id)
            if lineno%1000==0:
                db.commit()
        db.commit()

def detect_encoding(filename):
    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()
    with open(filename,'rb') as handle:
        for index,line in enumerate(handle.readlines()):
            detector.feed(line)
            if detector.done or index>1000 : break
    detector.close()
    return detector.result

                      
    
