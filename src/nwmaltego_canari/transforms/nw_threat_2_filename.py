#!/usr/bin/env python

import json

from common.entities import NWFilename, NWThreat
from canari.framework import configure
from common import nwmodule

__author__ = 'bostonlink'
__copyright__ = 'Copyright 2012, Netwitness Maltego Integration Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'bostonlink'
__email__ = 'bostonlink@pentest-labs.org'
__status__ = 'Development'

__all__ = [
    'dotransform'
]

@configure(
    label='Threat To Filename [Netwitness]',
    description='Returns filenames associated with the specified threat from Netwitness.',
    uuids=[ 'netwitness.v2.NetwitnessThreattoFileName_Netwitness' ],
    inputs=[ ( 'Netwitness', NWThreat ) ],
    debug=True
)

def dotransform(request, response):

    nwmodule.nw_http_auth()

    # NW REST API Query and results

    risk_name = request.value

    if 'ip' in request.fields:
        ip = request.fields['ip']
        where_clause = 'risk.warning="%s" && ip.src=%s || ip.dst=%s' % (risk_name, ip, ip)
    else:
        where_clause = 'risk.warning="%s"' % risk_name

    field_name = 'filename'
    json_data = json.loads(nwmodule.nwValue(0, 0, 25, field_name, 'application/json', where_clause))
    file_list = []

    for d in json_data['results']['fields']:
        if d['value'] not in file_list:
            response += NWFilename(
                d['value'].decode('ascii'),
                riskname = risk_name,
                metaid1=d['id1'],
                metaid2=d['id2'],
                type_=d['type'],
                count=d['count']
            )
            file_list.append(d['value'])

    return response