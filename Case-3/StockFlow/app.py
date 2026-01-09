from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func

from models import (
    db, Company, Warehouse, Product,
    Inventory, Supplier, ProductSupplier, Sales
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stockflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []
    last_30_days = datetime.utcnow() - timedelta(days=30)

    inventory_items = (
        db.session.query(Inventory)
        .join(Warehouse)
        .filter(Warehouse.company_id == company_id)
        .all()
    )

    for item in inventory_items:
        product = item.product
        warehouse = item.warehouse

        recent_sales = (
            db.session.query(func.sum(Sales.quantity))
            .filter(
                Sales.product_id == product.id,
                Sales.warehouse_id == warehouse.id,
                Sales.created_at >= last_30_days
            )
            .scalar()
        )

        if not recent_sales or recent_sales <= 0:
            continue

        avg_daily_sales = recent_sales / 30

        if item.quantity >= product.low_stock_threshold:
            continue

        days_until_stockout = int(item.quantity / avg_daily_sales)

        supplier = (
            db.session.query(Supplier)
            .join(ProductSupplier)
            .filter(ProductSupplier.product_id == product.id)
            .first()
        )

        alerts.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "current_stock": item.quantity,
            "threshold": product.low_stock_threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": {
                "id": supplier.id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            } if supplier else None
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
