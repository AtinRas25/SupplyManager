from flask import Blueprint, render_template, redirect, url_for
from manager.models import Suppliers
from manager.forms import SupplierForm
from manager.extensions import db


supplier_bp = Blueprint('supplier', __name__, url_prefix='/suppliers',
                        template_folder='templates')


@supplier_bp.route('/add_supplier', methods=["GET", "POST"])
def add_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        name = form.supplier_name.data
        mobile = form.supplier_mobile.data
        new_supplier = Suppliers(
            supplier_name=name,
            supplier_mobile=mobile
        )
        db.session.add(new_supplier)
        db.session.commit()
        return redirect(url_for('supplier.add_supplier'))
    return render_template('add_supplier.html', form=form)


@supplier_bp.route('/list')
def supplier_list():
    suppliers = Suppliers.query.all()
    return render_template('supplier_list.html', list=suppliers)