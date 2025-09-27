from flask import Blueprint, request, jsonify
from app.models import User, Follow
from app import db

# ДОБАВИТЬ:
bp = Blueprint('users', __name__)


# ИЗМЕНИТЬ ДЕКОРАТОРЫ
@bp.route('/api/users/me', methods=['GET'])
def get_current_user():
    api_key = request.headers.get('api-key')
    user = User.query.filter_by(api_key=api_key).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'result': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'followers': [{'id': f.follower_id, 'name': f.follower.name} for f
                          in user.followers],
            'following': [{'id': f.followed_id, 'name': f.followed.name} for f
                          in user.following]
        }
    })


@bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'result': True,
        'user': {
            'id': user.id,
            'name': user.name,
            'followers': [{'id': f.follower_id, 'name': f.follower.name} for f
                          in user.followers],
            'following': [{'id': f.followed_id, 'name': f.followed.name} for f
                          in user.following]
        }
    })


@bp.route('/api/users/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    api_key = request.headers.get('api-key')
    current_user = User.query.filter_by(api_key=api_key).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    user_to_follow = User.query.get(user_id)
    if not user_to_follow:
        return jsonify({'error': 'User to follow not found'}), 404

    if current_user.id == user_to_follow.id:
        return jsonify({'error': 'Cannot follow yourself'}), 400

    existing_follow = Follow.query.filter_by(follower_id=current_user.id,
                                             followed_id=user_to_follow.id).first()
    if existing_follow:
        return jsonify({'error': 'Already following this user'}), 400

    follow = Follow(follower_id=current_user.id, followed_id=user_to_follow.id)
    db.session.add(follow)
    db.session.commit()

    return jsonify({'result': True})


@bp.route('/api/users/<int:user_id>/follow', methods=['DELETE'])
def unfollow_user(user_id):
    api_key = request.headers.get('api-key')
    current_user = User.query.filter_by(api_key=api_key).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    follow = Follow.query.filter_by(follower_id=current_user.id,
                                    followed_id=user_id).first()
    if not follow:
        return jsonify({'error': 'Not following this user'}), 400

    db.session.delete(follow)
    db.session.commit()

    return jsonify({'result': True})