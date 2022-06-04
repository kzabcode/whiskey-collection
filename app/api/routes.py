from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import Whiskey, db, User, contact_schema, contacts_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/whiskey', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    distiller = request.json['distiller']
    age = request.json['age']
    percent = request.json['percent']
    color = request.json['color']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey(distiller,age,percent,color,user_token=user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = contact_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_user = current_user_token.token
    whiskey = Whiskey.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(whiskey)
    return jsonify(response)

# Get single contact
@api.route('/whiskey/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = contact_schema.dump(whiskey)
    return jsonify(response)


@api.route('/whiskey/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.distiller = request.json['distiller']
    whiskey.age = request.json['age']
    whiskey.percent = request.json['percent']
    whiskey.color = request.json['color']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = contact_schema.dump(whiskey)
    return jsonify(response)