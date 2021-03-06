# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

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

# actions
# List of services

SERVICE_TYPE = ''

def ondelete_service_type(service_type_table, service_type_id):
    count = db(db.services.service_type == service_type_id).count()
    if count > 0:        
        response.flash = T('Cant delete %s.', (db.service_type.type_name))
        raise HTTP(403)
    else:
        pass
    return locals()

def list_service_types():
    grid = SQLFORM.smartgrid(db.service_types
        , fields = [db.service_types.type_name, db.services.service_name]
        , ondelete = ondelete_service_type
        )
    return locals()

def create_service_type():
    form = SQLFORM(db.service_types).process()
    return locals()

def list_services():
    grid = SQLFORM.smartgrid(db.services
        , fields = [db.services.service_name,db.services.service_type]
        , linked_tables = []
        )
    return locals()
    
def loan_services():
    loan_type_id = db(db.service_types.type_name=='Loan').select().first()
    rows = db(db.services.service_type==loan_type_id).select()
    return locals()

   
def create_service():
    form = SQLFORM(db.services).process()
    return locals()
    
    
def list_members():
    grid = SQLFORM.smartgrid(db.members
        , fields = [db.members.member_name]
        )
    return locals()

def create_member():
    return locals()

def list_loans():
    rows = db((db.loan.service==db.services.id) & (db.loan.member_id==db.members.id)).select(
      db.services.service_name,
      db.members.member_name,
      db.loan.amount,
      db.loan.interest_rate,
      )
    return locals()

def create_loan():
    return locals()

from decimal import *
    
def file_loan():
    service_id = request.args(0)
    db.loan.service.writable = False
    db.loan.interest_rate.writable = False
    #db.loan.interest.writable = False
    db.loan.service.default = service_id
    interest_r = Decimal(db(db.services.id==service_id).select(db.services.interest_rate).first().interest_rate)
    db.loan.interest_rate.default = interest_r
    db.loan.interest.default = round(Decimal('0.01') * db.loan.amount.default * interest_r, 2)
    interest = Decimal(db.loan.interest.default)
    amount = Decimal(db.loan.amount.default)
    form = SQLFORM(db.loan,fields=['service','member_id','amount','interest_rate','interest']).process()
    return locals()
