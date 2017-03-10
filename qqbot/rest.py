# -*- coding: utf-8 -*-

import sys
from flask import Flask, jsonify
from flask import abort
from flask import request

from qterm import query
from utf8logger import CRITICAL, ERROR, WARN, INFO, PRINT

URL = {
    'baseUrl': '/rest/v1',
    'send': 'send'
}

SUCCESS_RESPONSE = {
    'result': 'success'
}

FAILED_RESPONSE = {
    'result': 'failure'
}

DEFAULT_PORT = 8288

app = Flask(__name__)


@app.route("{bu}/{send}".format(bu=URL['baseUrl'], send=URL['send']), methods=['POST'])
def send_msg():
    if not request.json:
        abort(400)
    coding = sys.getfilesystemencoding()
    json = request.json
    print coding
    print json
    ctype = json['ctype']
    contact = json['contact']
    content = json['content'].encode('utf-8')
    cmd = 'send'
    try:
        para = [cmd, ctype, contact, content]
        command = ' '.join(para)
        # para = "{ctype} {contact} {content}"\
        #     .format(ctype=ctype, contact=contact, content=content)
        # command = "{cmd} {para}".format(cmd=cmd, para=para)
        print command
        response = query(DEFAULT_PORT, command.encode('utf8'))
        INFO("QTerm response: %s" % response)
        SUCCESS_RESPONSE['message'] = response.decode(coding).encode('utf8')
        return jsonify(SUCCESS_RESPONSE), 200
    except Exception as e:
        print e
        # ERROR('Failed to send content: {content} to {contact}'
        #       .format(content=content, contact=contact), e)
        return jsonify(FAILED_RESPONSE), 500


def Start():
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
