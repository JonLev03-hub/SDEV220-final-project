from flask import Flask, render_template
from flask import request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# add all of the database table models here
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    supplier_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    desc = db.Column(db.String)
    count = db.Column(db.Integer)
    category = db.Column(db.String)

# add all of the database table models here
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    # add all of the database table models here
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer)
    date = db.Column(db.Date)
    items = db.Column(db.String)

with app.app_context():
    db.create_all()

@app.route("/")
def itemsPage():
    return render_template("items.html")

#delete a single item
@app.route('/api/item/delete',methods=["DELETE","POST"])
def deleteItem():
    data = request.get_json(force=True)
    print(data)
    item = Item.query.get(data["id"])
    if item is None:
        return {"msg": "Item has not been found"}
    db.session.delete(item)
    db.session.commit()
    return {"msg":"item removed"}, 200

# add a single item
@app.route('/api/item/add', methods=["POST"])
def addItem():
    try:
        data = request.get_json(force=True)
        print(data)
        item = Item(
            id = data["id"],
            name = data["name"],
            supplier_id = data["supplier_id"],
            price = data["price"],
            desc = data["desc"],
            count = data["count"],
            category = data["category"]
        )
        db.session.add(item)
        db.session.commit()
    except Exception as E:
        if(data["id"] == ""):
            return {"msg":"Please enter all fields"}, 400
        return {"msg":str(E.args)}, 400
    return {"msg":"item added"}, 200

# update item quantity
@app.route('/api/item/update', methods=["PUT"])
def updateItem():
    data = request.get_json(force=True)
    print(data)

    item = Item.query.get(data["id"])
    if item is None:
        return {"msg": "Item has not been found"}, 400
    if data["subtract"]:
        if item.count < int(data["quantity"]): 
            return {"msg": "Cant have quantity less than 0"} ,400
        item.count -= int(data["quantity"])
        print("Here")
    else:
        item.count += int(data["quantity"])
        print("Here else")

    db.session.commit()
    return {"msg":"item quantity updated"}, 200

# return all items
@app.route('/api/items/', methods=["GET"])
@app.route('/api/items/<string:category>', methods=["GET"])
def getItems(category = "all"):
    items = []
    if category == "all":
        query  = Item.query.all()
    else:
        query  = Item.query.filter(Item.category == category)
    for item in query:
        items.append({
                    "id": item.id,
                    "name": item.name,
                    "supplier_id": item.supplier_id,
                    "price": item.price,
                    "desc": item.desc,
                    "count": item.count,
                    "category": item.category
        })
    print(items)
    return jsonify(items)

# add a single customer
@app.route('/api/customer/add', methods=["POST"])
def addCustomer():
    data = request.get_json(force=True)
    try:
        data = request.get_json(force=True)
        print(data)
        customer = Customer(
        id = data["id"],
        name = data["name"],
        phone = data["phone"],
        email = data["email"],
        )
        db.session.add(customer)
        db.session.commit()
    except Exception as E:
        if data["id"] == "":
            return {"msg": "Please Enter All Fields"}, 400
        return {"msg":str(E.args)}, 400
    return {"msg":"item added"}, 200

# return all items
@app.route('/api/customers/', methods=["GET"])
@app.route('/api/customers/<string:phone>', methods=["GET"])
def getCustomers(phone = 0):
    customers = []
    if phone == 0:
        query  = Customer.query.all()
    else:
        query  = Customer.query.filter(Customer.phone == phone)
    for customer in query:
        customers.append({
                    "id": customer.id,
                    "name": customer.name,
                    "phone":customer.phone,
                    "email" : customer.email
        })

    return jsonify(customers)

#delete a single customer
@app.route('/api/customer/delete',methods=["DELETE","POST"])
def deleteCustomer():
    data = request.get_json(force=True)
    print(data)
    customer = Customer.query.get(data["id"])
    if customer is None:
        return {"msg": "Customer has not been found"}
    db.session.delete(customer)
    db.session.commit()
    return {"msg":"Customer removed"}, 200

# add a single supplier
@app.route('/api/supplier/add', methods=["POST"])
def addSupplier():
    data = request.get_json(force=True)
    try:
        data = request.get_json(force=True)
        print(data)
        supplier = Supplier(
        id = data["id"],
        name = data["name"],
        phone = data["phone"],
        email = data["email"],
        )
        db.session.add(supplier)
        db.session.commit()
    except Exception as E:
        if data["id"] == "":
            return {"msg": "Please Enter All Fields"}, 400
        return {"msg":str(E.args)}, 400
    return {"msg":"supplier added"}, 200

# return all items
@app.route('/api/suppliers/', methods=["GET"])
@app.route('/api/suppliers/<string:phone>', methods=["GET"])
def getSupplier(phone = 0):
    suppliers = []
    if phone == 0:
        query  = Supplier.query.all()
    else:
        query  = Supplier.query.filter(Supplier.phone == phone)
    for supplier in query:
        suppliers.append({
                    "id": supplier.id,
                    "name": supplier.name,
                    "phone":supplier.phone,
                    "email" : supplier.email
        })

    return jsonify(suppliers)

#delete a single item
@app.route('/api/supplier/delete',methods=["DELETE","POST"])
def deleteSupplier():
    data = request.get_json(force=True)
    print(data)
    supplier = Supplier.query.get(data["id"])
    if supplier is None:
        return {"msg": "Supplier has not been found"}
    db.session.delete(supplier)
    db.session.commit()
    return {"msg":"Supplier removed"}, 200

# add a single item
@app.route('/api/order/add', methods=["POST"])
def addOrder():
    data = request.get_json(force=True)
    try:
        data = request.get_json(force=True)
        print(data)
        order = Order(
        id = data["id"],
        customerid = data["customer"],
        items = str(data["items"]),
        date = dt.now()
        )
        db.session.add(order)
        db.session.commit()
    except Exception as E:
        if data["id"] == "":
            return {"msg": "Please Enter All Fields"}, 400
        return {"msg":str(E.args)}, 400
    return {"msg":"order added"}, 200

# return all items
@app.route('/api/orders/', methods=["GET"])
def getOrders():
    orders = []

    query  = Order.query.all()
    
    for item in query:
        orders.append({
                    "id": item.id,
                    "customer": item.customerid,
                    "date":str(item.date),
        })
    print(orders)
    return jsonify(orders)

# return a order by id
@app.route('/api/order/<string:id>', methods=["GET"])
def getOrder(id = 0):
    # data = request.get_json(force=True)
    # print(data)
    order = Order.query.get(id)
    if order is None:
        return {"msg": "order has not been found"}
    order = {
                    "orderId": order.id,
                    "customerId": order.customerid,
                    "date":str(order.date),
                    "items" :eval(order.items)
        }
    return order, 200

#delete a single item
@app.route('/api/order/delete',methods=["DELETE","POST"])
def deleteOrder():
    data = request.get_json(force=True)
    print(data)
    order = Order.query.get(data["id"])
    if order is None:
        return {"msg": "order has not been found"}
    db.session.delete(order)
    db.session.commit()
    return {"msg":"order removed"}, 200

if __name__ == "__main__":
    app.run()