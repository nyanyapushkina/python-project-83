from flask import Flask
from page_analyzer.routes.main import main_bp
from page_analyzer.routes.urls import urls_bp
from page_analyzer.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(urls_bp, url_prefix='/urls')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
