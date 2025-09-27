from flask import Blueprint, request, jsonify
from app.models import Media
from app import db
import os
from werkzeug.utils import secure_filename

# ДОБАВЛЯЕМ Blueprint
bp = Blueprint('media', __name__)

# Конфигурация загрузки файлов
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ИЗМЕНЯЕМ ДЕКОРАТОРЫ НА @bp.route

@bp.route('/api/medias', methods=['POST'])
def upload_media():
    api_key = request.headers.get('api-key')
    # В реальном приложении здесь должна быть проверка пользователя

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Проверка размера файла
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large'}), 400

        filename = secure_filename(file.filename)

        # Создаем папку если не существует
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Сохраняем файл
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Сохраняем информацию в БД
        media = Media(
            filename=filename,
            file_path=file_path,
            mime_type=file.content_type,
            file_size=file_length
        )

        db.session.add(media)
        db.session.commit()

        return jsonify({
            'result': True,
            'media_id': media.id
        })

    return jsonify({'error': 'Invalid file type'}), 400


@bp.route('/api/medias/<int:media_id>', methods=['GET'])
def get_media(media_id):
    media = Media.query.get(media_id)
    if not media:
        return jsonify({'error': 'Media not found'}), 404

    return jsonify({
        'id': media.id,
        'filename': media.filename,
        'mime_type': media.mime_type,
        'file_size': media.file_size
    })