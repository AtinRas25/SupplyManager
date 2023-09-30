from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint('main', __name__, url_prefix='/main', template_folder='templates')


@main_bp.route('/')
def dashboard():
    return render_template('dashboard.html')