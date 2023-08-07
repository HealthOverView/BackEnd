from flask import request, jsonify
from app001 import app

@app.route('/test')
def test():
	return jsonify(result='testing now!')
