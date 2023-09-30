from flask import Blueprint, render_template, redirect, url_for
from manager.models import Supply
from manager.forms import ItemForm
from manager.extensions import db
from datetime import date


supply_bp = Blueprint('supply', __name__, url_prefix='/supply', template_folder='templates')


@supply_bp.route('/add_supply', methods=["GET", "POST"])
def add_supply():
    form = ItemForm()
    if form.validate_on_submit():
        supplier = form.supplier.data
        supplier_id = supplier.id
        name = form.name.data
        qty = form.qty.data
        supply_date = form.supply_date.data
        new_supply = Supply(
            name=name,
            qty=qty,
            unwashed_qty=qty,
            supply_date=supply_date,
            supplier_id=supplier_id
        )
        db.session.add(new_supply)
        db.session.commit()
        return redirect(url_for('supply.add_supply'))
    return render_template('add_item.html', form=form)


@supply_bp.route('/list')
def supply_list():
    supplies = Supply.query.all()
    return render_template("item_list.html", items=supplies)