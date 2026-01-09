from app import app, db
from models import *

from datetime import datetime, timedelta

with app.app_context():
    db.drop_all()
    db.create_all()

    company = Company(name="Demo Company")
    db.session.add(company)

    warehouse = Warehouse(name="Main Warehouse", company_id=1)
    db.session.add(warehouse)

    product = Product(
        name="Widget A",
        sku="WID-001",
        price=100.00,
        low_stock_threshold=20
    )
    db.session.add(product)

    inventory = Inventory(
        product_id=1,
        warehouse_id=1,
        quantity=5
    )
    db.session.add(inventory)

    supplier = Supplier(
        name="Supplier Corp",
        contact_email="orders@supplier.com"
    )
    db.session.add(supplier)

    link = ProductSupplier(product_id=1, supplier_id=1)
    db.session.add(link)

    sale = Sales(
        product_id=1,
        warehouse_id=1,
        quantity=60,
        created_at=datetime.utcnow() - timedelta(days=10)
    )
    db.session.add(sale)

    db.session.commit()
    print("Database seeded successfully.")
