from flask import Blueprint, request, jsonify
from app.models import User
from app import db

# ДОБАВИТЬ ЭТУ СТРОКУ:
bp = Blueprint('auth', __name__)


# ИЗМЕНИТЬ ДЕКОРАТОРЫ (добавить @bp.)
@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {'message': 'User created successfully', 'user_id': user.id})