from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField, Form, FormField, FieldList
from wtforms_sqlalchemy.fields import QuerySelectField
from manager.models import *
from datetime import date
from wtforms.validators import DataRequired, ValidationError

#TODO: Create custom validation for mobile numbers
#TODO: Create custom validation for qty to not allow overdraft



class VoucherEntryForm(Form):
    item = QuerySelectField("Product:",
                            query_factory=lambda: Supply.query.filter(Supply.unwashed_qty > 0).all(),
                            allow_blank=True)
    item_qty = IntegerField("Quantity", default=0)


class SupplierForm(FlaskForm):
    supplier_name = StringField("Karigar name:", validators=[DataRequired()])
    supplier_mobile = StringField("Enter mobile:", validators=[DataRequired()])
    submit = SubmitField("Register Supplier")


class ItemForm(FlaskForm):
    name = StringField("Item name:", validators=[DataRequired()])
    supplier = QuerySelectField("Karigar", validators=[DataRequired()], query_factory=lambda: Suppliers.query.all(), allow_blank=True,
                                get_label="supplier_name"
                                )
    qty = IntegerField("Quantity:", validators=[DataRequired()])
    supply_date = DateField('Date of supply:', default=date.today, format='%Y-%m-%d')
    submit = SubmitField("Add Item")


class DhobiForm(FlaskForm):
    name = StringField("Dhobi name:", validators=[DataRequired()])
    #TODO: Change mobile field to StringField
    mobile = IntegerField("Mobile:", validators=[DataRequired()])
    submit = SubmitField("Add Dhobi")


class Dhobi_Voucher(FlaskForm):
    date = DateField("Date", default=date.today, format='%Y-%m-%d')
    dhobi = QuerySelectField("Select dhobi:",validators=[DataRequired()], query_factory=lambda: Dhobi.query.all(), allow_blank=True,
                             get_label="name"
                             )
    product = FieldList(FormField(VoucherEntryForm), min_entries=10)
    submit = SubmitField("Add entry")


class VoucherListForm(FlaskForm):
    dhobi = QuerySelectField('Select Dhobi', validators=[DataRequired()], query_factory=lambda: Dhobi.query.all(), allow_blank=True, get_label='name')
    vouchers = QuerySelectField('Select Voucher', validators=[DataRequired()], allow_blank=True)
    submit = SubmitField("Update Voucher")


class ProductForm(Form):
    item = StringField('Products')
    item_qty = IntegerField("Quantity", default=0)


class SupplierVoucherForm(FlaskForm):
    date = DateField("Select Date:", default=date.today, validators=[DataRequired()], format='%Y-%m-%d')
    supplier = QuerySelectField("Select Supplier:", query_factory=lambda:Suppliers.query.all(), allow_blank=True,
                                get_label='supplier_name')
    product = FieldList(FormField(ProductForm), min_entries=10)
    submit = SubmitField("Add Products")


class SupplierVoucherList(FlaskForm):
    supplier = QuerySelectField("Select Supplier", validators=[DataRequired()], query_factory=lambda:Suppliers.query.all(), allow_blank=True,
                                get_label='supplier_name')
    vouchers = QuerySelectField("Select Vouchers", validators=[DataRequired()], allow_blank=True)
