from flask import jsonify


def resp_json(message="", code=200, data=None):
    return jsonify({
        "meta": {
            "message": message,
            "code": code
        },
        "data": data
    }), code
