# -*- coding: utf-8 -*-

def get_email_data(broadcast_id):
    broadcast = db.tenant_broadcast(broadcast_id)
    domain_ = broadcast.domain_
    from_ = tenant_broadcast.sender.formatted
    subject_ = broadcast.subject
    tags_ = broadcast.tags
    body_ = db.tenant_body(broadcast.body)
    attachments_ = db(db.tenant_attachment.id.belongs(broadcast.attachments)).select()
    return {
        'broadcast': broadcast,
        'domain': domain_,
        'from': from_,
        'subject': subject_,
        'tags': tags_,
        'body': body_,
        'attachments': attachments_
    }
