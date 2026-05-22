from app import create_app
from app.extensions import db

app = create_app()


@app.shell_context_processor
def shell_context():
    from app.models import User, Record, Order, OrderItem
    return {"db": db, "User": User, "Record": Record, "Order": Order, "OrderItem": OrderItem}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
