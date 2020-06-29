from flask import Blueprint, current_app, session, url_for, request, Response
from jinja2 import Template

from geonature.utils.utilssqlalchemy import json_resp
from geonature.utils.env import DB

# import des fonctions utiles depuis le sous-module d'authentification
from geonature.core.gn_permissions import decorators as permissions
from geonature.core.gn_permissions.tools import get_or_fetch_user_cruved

import importlib
import sys
from os.path import join, dirname
from datetime import datetime
import email.utils
sys.path.append(dirname(__file__))

import customs_query

blueprint = Blueprint('myapi', __name__)

@blueprint.route('/', methods=['GET'])
def info():
    return 'Hello world !'

@blueprint.route('/<string:query_name>/', methods=['GET'])
@json_resp
def qr_route(query_name):
    try :
        mod = importlib.import_module('.'+query_name,'customs_query')
        qr = mod._qr()
    except ImportError:
        return dict(error='Not found'), 404
    except SyntaxError:
        return dict(error='Server error (syntaxe)'), 500
    args = qr.args_default
    args.update(request.args.to_dict())
    qr.set_args(args)
    if not qr.is_allowed(request.args.get('token', None)):
        return dict(error='wrong token'), 401
    
    result = qr.execute()
    return result

@blueprint.route('/rss/<string:query_name>/', methods=['GET'])
def qr_route_rss(query_name):
    try :
        mod = importlib.import_module('.'+query_name,'customs_query')
        qr = mod._qr()
    except ImportError:
        return dict(error='Not found'), 404
    except SyntaxError as err:
        return dict(error='Server error : {}'.format(err)), 500
    args = qr.args_default
    args.update(request.args.to_dict())
    qr.set_args(args)
    if not qr.is_allowed(request.args.get('token', None)):
        return dict(error='wrong token'), 401
    
    result = qr.execute()

    xml_items=[ dict(title=e.get('title','Sans titre'), pub_date=email.utils.format_datetime(e['pub_date']), description=e.get('description','Pas de description'), link=e.get('link','https://clicnat.fr')) for e in result ]

    template = Template(
    """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Clicnat Flux</title>
            <description>Beta, flux clicnat</description>
            <lastBuildDate>{{ lbd }}</lastBuildDate>
            <link>http://www.example.org</link>
                {% for xml_item in xml_items %}
                <item>
                    <title><![CDATA[ {{ xml_item.title }} ]]></title>
                    <description><![CDATA[ {{ xml_item.description }} ]]></description>
                    <pubDate>{{ xml_item.pub_date }}</pubDate>
                    <link>{{ xml_item.link }}</link>
                </item>
                {% endfor %}
        </channel>
    </rss>
    """)

    out=template.render(
        lbd=email.utils.format_datetime(datetime.now()),
        xml_items=xml_items 
    )

    return Response(out,mimetype="application/xml")

