from flask import Flask, redirect, url_for
from manager.extensions import db, bootstrap
from manager.models import *
from manager.register.dhobi import dhobi_bp
from manager.voucher.voucher import vouchers_bp
from manager.register.supplier import supplier_bp
from manager.register.supply import supply_bp
from manager.register.mainpage import main_bp
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URI', 'sqlite:///inventory.db')
    app.config["DATABASE_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bootstrap.init_app(app)

    app.register_blueprint(dhobi_bp)
    app.register_blueprint(vouchers_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(supply_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def hello():
        return redirect(url_for('main.dashboard'))

    return app








