from manager.extensions import db
from sqlalchemy.orm import relationship

dhobi_association = db.Table('Dhobi_Association_Table',
                             db.Column('dhobi_id', db.Integer, db.ForeignKey("supply.id")),
                             db.Column('supply_id', db.Integer, db.ForeignKey('dhobi.id'))
                             )


class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    supplier_mobile = db.Column(db.String(15), nullable=False)
    products = db.relationship('Supply', backref='suppliers')


class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    supply_date = db.Column(db.Date, nullable=False)
    unwashed_qty = db.Column(db.Integer, nullable=False)
    washing_qty = db.Column(db.Integer, default=0)
    received_qty = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    dhobi_list = db.relationship('Dhobi', secondary=dhobi_association, backref='items')

    def __repr__(self):
        return f"{self.name} -- {self.unwashed_qty}"






class Dhobi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    vouchers = db.relationship('DhobiVoucher', backref='dhobi')


class DhobiVoucher(db.Model):
    id = db.Column("Voucher Id", db.Integer, primary_key=True)
    voucher_date = db.Column(db.Date, nullable=False)
    voucher_details = db.Column(db.JSON, default='{}')
    dhobi_id = db.Column(db.Integer, db.ForeignKey('dhobi.id'))

    def __repr__(self):
        return f"Voucher {self.id}"


class SupplierVoucher(db.Model):
    id = db.Column("Voucher Id", db.Integer, primary_key=True)
    voucher_date = db.Column(db.Date, nullable=False)
    voucher_details = db.Column(db.JSON, default='{}')
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))

    def __repr__(self):
        return f"Voucher {self.id}"
