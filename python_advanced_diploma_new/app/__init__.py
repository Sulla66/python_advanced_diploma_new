from flask import Flask, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_clone.db'
    db.init_app(app)

    # Статические файлы
    static_path = os.path.join(os.path.dirname(__file__), 'static')

    def get_api_key():
        headers = request.headers

        # 1. Проверяем заголовки
        api_key = (
                headers.get('Api-Key') or
                headers.get('api-key') or
                headers.get('API-Key') or
                headers.get('app-key') or
                'test-key'  # Fallback
        )

        # 2. Если ключ "test" - автоматически исправляем на "test-key"
        if api_key == 'test':
            print("⚠️ Исправляем API key: 'test' → 'test-key'")
            api_key = 'test-key'

        return api_key

    # Главная страница
    @app.route('/')
    def index():
        return send_from_directory(static_path, 'index.html')

    # Статические файлы
    @app.route('/<path:path>')
    def static_files(path):
        return send_from_directory(static_path, path)

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        api_key = data.get('api_key') or data.get('apiKey') or 'test-key'

        if api_key == 'test':
            api_key = 'test-key'

        return jsonify({
            "result": True,
            "message": "Login successful",
            "user": {"id": 1, "name": "Test User"},
            "api_key": api_key
        })

    # Health check
    @app.route('/api/health')
    def health():
        return jsonify({"status": "ok", "message": "Server is working"})

    # /api/users/me
    @app.route('/api/users/me')
    def user_me():
        api_key = get_api_key()

        print(f"🔍 Received headers: {dict(request.headers)}")
        print(f"🔍 Using API key: {api_key}")

        return jsonify({
            "result": True,
            "user": {
                "id": 1,
                "name": "Test User",
                "followers": [],
                "following": []
            }
        })

    @app.route('/api/tweets', methods=['GET'])
    def get_tweets():
        api_key = get_api_key()

        # Простые тестовые твиты
        return jsonify({
            "result": True,
            "tweets": [
                {
                    "id": 1,
                    "content": "Добро пожаловать в микроблог! 🎉",
                    "attachments": [],
                    "author": {"id": 1, "name": "Test User"},
                    "likes": [{"user_id": 1, "name": "Test User"}]
                },
                {
                    "id": 2,
                    "content": "Это тестовый твит для демонстрации",
                    "attachments": [],
                    "author": {"id": 1, "name": "Test User"},
                    "likes": []
                },
                {
                    "id": 3,
                    "content": "API key исправлен автоматически! ✅",
                    "attachments": [],
                    "author": {"id": 1, "name": "Test User"},
                    "likes": [{"user_id": 1, "name": "Test User"}]
                }
            ]
        })

    @app.route('/api/tweets', methods=['POST'])
    def create_tweet():
        api_key = get_api_key()

        data = request.get_json() or {}
        tweet_data = data.get('tweet_data', 'Новый твит')

        return jsonify({
            "result": True,
            "tweet_id": 999,
            "message": f"Твит создан: {tweet_data}",
            "api_key_used": api_key
        })

    # Инициализация БД
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")

    print("✅ Server ready: http://127.0.0.1:8000")
    print("🔧 Автоисправление API key: 'test' → 'test-key'")
    return app