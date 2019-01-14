# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

response.menu += [
    (T('Services'), False, URL('default', 'list_services'), []),
    (T('Service Types'), False, URL('default', 'list_service_types'), []),
    (T('Members'), False, URL('default', 'list_members'), []),
    (T('Loans'), False, URL('default', 'list_loans'), []),
    (T('Design'), False, 'http://127.0.0.1:8000/admin/default/design/LoansManager', []),
    ]
