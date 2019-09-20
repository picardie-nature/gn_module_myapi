from flask import Blueprint, current_app, session, url_for, request

from geonature.utils.utilssqlalchemy import json_resp
from geonature.utils.env import DB

# import des fonctions utiles depuis le sous-module d'authentification
from geonature.core.gn_permissions import decorators as permissions
from geonature.core.gn_permissions.tools import get_or_fetch_user_cruved


import sys
from os.path import join, dirname
sys.path.append(dirname(__file__))
import customs_query
from customs_query import *

blueprint = Blueprint('myapi', __name__)

@blueprint.route('/', methods=['GET'])
def info():
    return 'Hello world !'

@blueprint.route('/test/', methods=['GET'])
@json_resp
def bp_test():
    ctx=count.ctx
    ctx.set_args(request.args)
    if not ctx.is_allowed(request.args.get('token', None)):
        return dict(error='wrong token')
    
    result = ctx.execute()
    return result


@blueprint.route('/<string:query_name>/', methods=['GET'])
@json_resp
def qr_route(query_name):
    try :
        mod = getattr(customs_query,query_name)
        qr = mod._qr
    except AttributeError:
        return dict(error='Not found'), 404
    args = qr.args_default
    args.update(request.args)
    qr.set_args(args)
    if not qr.is_allowed(request.args.get('token', None)):
        return dict(error='wrong token'), 401
    
    result = qr.execute()
    return result


