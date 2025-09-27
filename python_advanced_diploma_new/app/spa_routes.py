from flask import send_from_directory
import os


def init_spa_routes(app):
    """
    Initialize SPA routing for the app
    """

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        if path.startswith('static/') or path.startswith(
                'js/') or path.startswith('css/'):
            try:
                return send_from_directory(app.static_folder, path)
            except:
                return "File not found", 404

        try:
            return send_from_directory(app.static_folder, 'index.html')
        except:
            return "SPA routing error", 404