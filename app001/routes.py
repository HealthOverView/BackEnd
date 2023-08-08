from flask import request, jsonify
from app001 import app
from app001.views import upload


@app.route('/test')
def test():
    return jsonify(result='testing now!')


@app.route('/diagnosis', methods=['GET'])
def diag():
    if 'image' not in request.files:
        return {
            'status': 404,
            'message': 'err',
            'description': 'File is missing'
        }
    image = request.files['image']
    if image.filename == '':
        return {
            'status': 404,
            'message': 'err',
            'description': 'File is missing'
        }

    res_list = ['비가임기', '과도기', '가임기']
    result = upload(image)
    return {
        'status': 200,
        'message': 'success',
        'description': res_list[result]
    }
