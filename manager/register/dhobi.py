from flask import Blueprint, render_template, redirect, url_for
from manager.forms import DhobiForm
from manager.models import Dhobi
from manager.extensions import db

dhobi_bp = Blueprint("dhobi",__name__, url_prefix="/dhobi", template_folder='templates')


@dhobi_bp.route('/add_dhobi', methods=["GET", "POST"])
def addDhobi():
    form = DhobiForm()
    if form.validate_on_submit():
        name=form.name.data
        mobile=form.mobile.data
        new_dhobi = Dhobi(
            name=name,
            mobile=mobile
        )
        db.session.add(new_dhobi)
        db.session.commit()
        return redirect(url_for('dhobi.addDhobi'))
    return render_template("add_Dhobi.html", form=form)


@dhobi_bp.route('/list')
def dhobi_list():
    list = Dhobi.query.all()
    return render_template("dhobi_list.html", list=list)
