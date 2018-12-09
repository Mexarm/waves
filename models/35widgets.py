# -*- coding: utf-8 -*-
from gluon.sqlhtml import FormWidget  # , IntegerWidget, StringWidget


class SelectMultiple(FormWidget):
    @staticmethod
    def widget(field, value):
        default = dict(
            value=[{'id': _id, 'represent': field.represent(
                [_id])} for _id in value],
            _url=URL('default', 'api', args=['tags','contains','__query__.json'], vars=dict(limit=25)),
            
            _filterby='tag'
        )
        default['_@selected'] = 'itemSelected($event)'
        attr = FormWidget._attributes(field, default)
        attr.update(default)
        wautocomplete = TAG['w-autocomplete'](**attr)
        attr2 = {'_:items': 'items', '_display_prop': 'tag',
                 '_@deleted': "itemDeleted"}
        wchiplist = TAG['w-chip-list'](**attr2)
        options = [OPTION(field.represent([id_]),_value=id_,_selected=True) for id_ in value  ]
        sattr=FormWidget._attributes(field,dict(_multiple=True,_hidden=""))
        #sattr.update(dict(_multiple=True))
        select = SELECT(*options, **sattr)
        
        return DIV(wautocomplete, wchiplist,select)
