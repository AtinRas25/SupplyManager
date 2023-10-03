from flask import Blueprint, render_template, redirect, url_for, request
from manager.forms import Dhobi_Voucher, VoucherListForm, SupplierVoucherForm, SupplierVoucherList
from manager.extensions import *
from manager.models import DhobiVoucher, Dhobi, Suppliers, Supply, SupplierVoucher
from datetime import date
import json
vouchers_bp = Blueprint("voucher", __name__, url_prefix='/voucher', template_folder='templates')


@vouchers_bp.route('/create_voucher', methods=["GET", "POST"])
def createVoucher():
    form = Dhobi_Voucher()
    if form.validate_on_submit():
        dhobi_id = form.dhobi.data.id
        voucher_date = form.date.data
        voucher = {}
        total_qty = 0
        iterator = 1
        for field in form.product.data:
            product = field['item']
            if product is not None:
                qty = field['item_qty']
                product.unwashed_qty -= qty
                product.washing_qty += qty
                supplier = Suppliers.query.get_or_404(product.supplier_id)

                voucher[f'{iterator}'] = {'item_id': product.id, 'item_name': product.name, 'item_supplier': supplier.supplier_name,
                                          'item_qty': qty, 'item_received': 0, 'item_remaining': qty}
                iterator += 1
                total_qty += qty

        # qty = form.qty.data
        # item = form.entry.data
        # entry = item.name
        # item.unwashed_qty = item.unwashed_qty - qty
        # item.washing_qty += qty
        #
        # voucher = {
        #     f"{entry}": qty
        # }
        voucher['Total_qty'] = total_qty
        new_voucher = DhobiVoucher(
            voucher_date=voucher_date,
            voucher_details=json.dumps(voucher),
            dhobi_id=dhobi_id
        )
        db.session.add(new_voucher)
        db.session.commit()
        return redirect(url_for("voucher.createVoucher"))
    return render_template("create_Voucher.html", form=form)


@vouchers_bp.route('/dhobi_vouchers', methods=['GET', 'POST'])
def dhobi_voucher_list():
    form = VoucherListForm()
    form.vouchers.query = DhobiVoucher.query.filter(None).all()
    if request.method == 'POST':
        voucher_id = request.form.get('vouchers', type=int)
        voucher = DhobiVoucher.query.get_or_404(voucher_id)
        details = json.loads(voucher.voucher_details)
        qty_received = request.form.getlist('qty', type=int)
        iterator = 0
        for key in details.keys():
            if key != 'Total_qty':
                quantity = qty_received[iterator]
                item_id = details[key]['item_id']
                item = Supply.query.get_or_404(item_id)
                item.washing_qty -= quantity
                item.received_qty += quantity
                details[key]['item_received'] += quantity
                details[key]['item_remaining'] -= quantity
                voucher.voucher_details = json.dumps(details)
                db.session.commit()
                iterator += 1

        return redirect(url_for('voucher.dhobi_voucher_list'))

    return render_template('voucher_details.html', form=form)


@vouchers_bp.route('/get_vouchers')
def get_vouchers():
    dhobi_id = request.args.get("dhobi", type=int)
    vouchers = DhobiVoucher.query.filter_by(dhobi_id=dhobi_id).all()
    return render_template("get_vouchers.html", vouchers=vouchers)


@vouchers_bp.route('/get_details')
def get_voucher_details():
    voucher_id = request.args.get('vouchers', type=int)
    voucher = DhobiVoucher.query.get(voucher_id)
    return render_template('get_voucher_details.html', voucher=json.loads(voucher.voucher_details))


@vouchers_bp.route('/supplier_voucher', methods=["GET", "POST"])
def supplier_voucher():
    form = SupplierVoucherForm()
    if form.validate_on_submit():
        voucher_date = form.date.data
        supplier_id = form.supplier.data.id
        supplier_name = form.supplier.data.supplier_name
        voucher = {}
        iterator = 1
        total_price = 0
        for field in form.product.data:
            product = field['item']
            if product != '':
                qty = field['item_qty']
                price = field['item_price']
                new_item = Supply(
                    name=product,
                    qty=qty,
                    unwashed_qty=qty,
                    supply_date=voucher_date,
                    supplier_id=supplier_id,
                    supplier_name=supplier_name,
                    price=price
                )
                total_price += price*qty
                db.session.add(new_item)
                db.session.commit()
                voucher[f"{iterator}"] = field
                iterator += 1

        voucher["Total Price"] = total_price
        new_voucher = SupplierVoucher(
            voucher_date=voucher_date,
            voucher_details=json.dumps(voucher),
            supplier_id=supplier_id,
            voucher_total=total_price
        )
        db.session.add(new_voucher)
        db.session.commit()
        print(voucher)
        return redirect(url_for('voucher.supplier_voucher'))
    return render_template('supplier_voucher.html', form=form)


@vouchers_bp.route('/supplier_voucher_list')
def supp_voucher_list():
    form = SupplierVoucherList()
    form.vouchers.query = SupplierVoucher.query.filter(None).all()
    return render_template("supplier_voucher_list.html", form=form)


@vouchers_bp.route('/get_supplier_voucher')
def get_supplier_voucher():
    supplier_id = request.args.get('supplier', type=int)
    vouchers = SupplierVoucher.query.filter_by(supplier_id=supplier_id).all()
    return render_template("get_supplier_voucher.html", vouchers=vouchers)


@vouchers_bp.route('/get_supp_vouch_details')
def get_supp_details():
    voucher_id = request.args.get('vouchers', type=int)
    voucher = SupplierVoucher.query.get(voucher_id)
    date_voucher = voucher.voucher_date
    return render_template('get_supp_vouch_details.html', voucher=json.loads(voucher.voucher_details),
                           date=date_voucher)
