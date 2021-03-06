from flask import Flask, abort, request, jsonify


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def check_for_required_fields(jsn, rqd_fields):
    if jsn is not None:
        for field in rqd_fields:
            if field not in jsn:
                raise InvalidUsage(f"Missing data field: {field}", status_code=400)
    else:
        raise InvalidUsage(f"Missing these data fields: {rqd_fields}", status_code=400)