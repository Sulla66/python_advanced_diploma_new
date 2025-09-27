from flask import Blueprint, request, jsonify
from app.models import Tweet, Like, User, Follow
from app import db
from datetime import datetime

# ДОБАВЛЯЕМ Blueprint
bp = Blueprint('tweets', __name__)


# ИЗМЕНЯЕМ ДЕКОРАТОРЫ НА @bp.route

@bp.route('/api/tweets', methods=['GET'])
def get_tweets():
    api_key = request.headers.get('api-key')
    current_user = User.query.filter_by(api_key=api_key).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    # Получаем ID пользователей, на которых подписан текущий пользователь
    following_ids = [f.followed_id for f in current_user.following]
    following_ids.append(current_user.id)  # Добавляем свои твиты

    # Получаем твиты от пользователей, на которых подписан
    tweets = Tweet.query.filter(Tweet.user_id.in_(following_ids)).order_by(
        Tweet.created_at.desc()).all()

    tweets_data = []
    for tweet in tweets:
        tweet_data = {
            'id': tweet.id,
            'content': tweet.content,
            'attachments': [media.filename for media in
                            tweet.media_files] if hasattr(tweet,
                                                          'media_files') else [],
            'author': {
                'id': tweet.author.id,
                'name': tweet.author.name
            },
            'likes': [
                {
                    'user_id': like.user.id,
                    'name': like.user.name
                }
                for like in tweet.likes
            ]
        }
        tweets_data.append(tweet_data)

    return jsonify({
        'result': True,
        'tweets': tweets_data
    })


@bp.route('/api/tweets', methods=['POST'])
def create_tweet():
    api_key = request.headers.get('api-key')
    current_user = User.query.filter_by(api_key=api_key).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    tweet_data = data.get('tweet_data')
    media_ids = data.get('tweet_media_ids', [])

    if not tweet_data:
        return jsonify({'error': 'Tweet data is required'}), 400

    tweet = Tweet(
        content=tweet_data,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.session.add(tweet)
    db.session.commit()

    # Здесь можно добавить логику для привязки media_ids к твиту
    # if media_ids:
    #     for media_id in media_ids:
    #         media = Media.query.get(media_id)
    #         if media:
    #             media.tweet_id = tweet.id

    db.session.commit()

    return jsonify({
        'result': True,
        'tweet_id': tweet.id
    })


@bp.route('/api/tweets/<int:tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id):
    api_key = request.headers.get('api-key')
    current_user = User.query.filter_by(api_key=api_key).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return jsonify({'error': 'Tweet not found'}), 404

    # ПРОВЕРКА АВТОРСТВА - ВАЖНО!
    if tweet.user_id != current_user.id:
        return jsonify({'error': 'Can only delete your own tweets'}), 403

    # Удаляем лайки твита
    Like.query.filter_by(tweet_id=tweet_id).delete()

    # Удаляем твит
    db.session.delete(tweet)
    db.session.commit()

    return jsonify({'result': True})


@bp.route('/api/tweets/<int:tweet_id>/likes', methods=['POST'])
def like_tweet(tweet_id):
    api_key = request.headers.get('api-key')
    current_user = User.query.filter_by(api_key=api_key).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        return jsonify({'error': 'Tweet not found'}), 404

    # Проверяем, не лайкал ли уже
    existing_like = Like.query.filter_by(user_id=current_user.id,
                                         tweet_id=tweet_id).first()
    if existing_like:
        return jsonify({'error': 'Already liked this tweet'}), 400

    like = Like(user_id=current_user.id, tweet_id=tweet_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({'result': True})


@bp.route('/api/tweets/<int:tweet_id>/likes', methods=['DELETE'])
def unlike_tweet(tweet_id):
    api_key = request.headers.get('api-key')
    current_user = User.query.filter_by(api_key=api_key).first()

    if not current_user:
        return jsonify({'error': 'User not found'}), 404

    like = Like.query.filter_by(user_id=current_user.id,
                                tweet_id=tweet_id).first()
    if not like:
        return jsonify({'error': 'Like not found'}), 404

    db.session.delete(like)
    db.session.commit()

    return jsonify({'result': True})