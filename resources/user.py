from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from models.userModel import UserModel

user = Blueprint('user', __name__, url_prefix='/users')


@user.post('/signup')
def signup():

    email = request.json['email']
    username = request.json['username']
    password = generate_password_hash(request.json['password'])
    password_confirm = request.json['password_confirm']

    if (request.json['password'] != password_confirm):
        return jsonify({'message': 'Passwords do not match'}), 400

    if (UserModel.find_by_username(username)):
        return jsonify({'message': 'Username already exists'}), 400

    if (UserModel.find_by_email(email)):
        return jsonify({'message': 'Email already exists'}), 400

    user = UserModel(email=email, username=username, password=password)

    user.save_to_db()

    return jsonify({
        "message": "Sign up successful",
        "user": user.serialize()
    })


@user.post('/login')
def login():

    email = request.json['email']
    password = request.json['password']

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    if not password:
        return jsonify({'message': 'Password is required'}), 400

    user = UserModel.find_by_email(email)

    if not user:
        return jsonify({'message': 'User does not exist'}), 400

    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Password is incorrect'}), 400

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    })


@user.put('/edit/profile')
@jwt_required()
def edit_profile():

    user_id = get_jwt_identity()

    new_username = request.json.get('username')

    user = UserModel.query.filter_by(id=user_id).first()

    user.username = new_username

    user.save_to_db()

    return jsonify({"message": "Username changed succesfuly"})
