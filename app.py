from flask import Flask, render_template
from flask import request, jsonify
from flask_cors import CORS
# Fixed a typo in the line below
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
# Sample testing data
items = [{
        "id": 123,
        "itemname": "testItem",
        "supplierId": 123,
        "price": 123,
        "desc": "item desc",
        "quantity": 123,
        "category": "misc_category"
    },
    {
        "id": 456,
        "itemname": "testItem",
        "supplierId": 123,
        "price": 123,
        "desc": "item desc",
        "quantity": 123,
        "category": "misc_category"
    },
    {
        "id": 789,
        "itemname": "testItem",
        "supplierId": 123,
        "price": 123,
        "desc": "item desc",
        "quantity": 123,
        "category": "misc_category"
    }]
customers =[
        {
        "customerId": 123,
        "customername": "testItem",
        "customerphone":1231231231,
        "customeremail":"someEmail@test.com"
    },
    {
        "customerId": 456,
        "customername": "testItem",
        "customerphone":1231231231,
        "customeremail":"someEmail@test.com"
    },
    {
        "customerId": 789,
        "customername": "testItem",
        "customerphone":1231231231,
        "customeremail":"someEmail@test.com"
    }
]
suppliers =[
        {
        "supplierId": 123,
        "suppliername": "testItem",
        "supplierphone":1231231231,
        "supplieremail":"someEmail@test.com"
    },
    {
        "supplierId": 456,
        "suppliername": "testItem",
        "supplierphone":1231231231,
        "supplieremail":"someEmail@test.com"
    },
    {
        "supplierId": 789,
        "suppliername": "testItem",
        "supplierphone":1231231231,
        "supplieremail":"someEmail@test.com"
    }
]
orders=[
{
    "orderId":123,
    "customerId": 123,
    "items":[
                {"id":123,"quantity":1},
                {"id":123,"quantity":1}
            ],
    "price":123,
    "date":"12-12-2012"
},
{
    "orderId":456,
    "customerId": 123,
    "items":[
                {"itemid":123,"quantity":1},
                {"itemid":123,"quantity":1}
            ],
    "price":123,
    "date":"12-12-2012",
}]


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# add all of the database table models here
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String)
    supplierId = db.Column(db.Integer)
    price = db.Column(db.Integer)
    desc = db.Column(db.String)
    quantity = db.Column(db.Integer)
    category = db.Column(db.String)
    

class Customer(db.Model):
    customerId = db.Column(db.Integer, primary_key=True)
    customername = db.Column(db.String)
    customerphone = db.Column(db.Integer)
    customeremail = db.Column(db.String)

class Supplier(db.Model):
    supplierId = db.Column(db.Integer, primary_key=True)
    suppliername = db.Column(db.String)
    supplierphone = db.Column(db.Integer)
    supplieremail = db.Column(db.String)


class Order(db.Model):
    orderId = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customer.customerId'))
    itemId = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    date = db.Column(db.DateTime)

with app.app_context():
    db.create_all()

# ----- this route may not be used -------
# # find a single item 
# @app.route('/api/item/<int :id>',method = "GET")
# def item(id):
#     data = request.get_json(force=True)
#     print(data)
#     # change this to return a single item from the database that matches the item id or return an error
#     return items[0]

#delete a single item
@app.route('/api/item/delete',methods=["DELETE","POST"])
def deleteItem():
    data = request.get_json(force=True)
    print(data)
    item = Item.query.get(data["id"])
    if item is None:
        return {"error": "Item has not been found"}
    db.session.delete(item)
    db.session.commit()
    return {"msg":"item removed"}, 200

# add a single item
@app.route('/api/item/add', methods=["POST"])
def addItem():
    data = request.get_json(force=True)
    # Checks if all required fields are present in the request
    if not all(key in data for key in ('id', 'itemname', 'supplierId', 'price', 'desc', 'quantity', 'category')):
        return {'error': 'Missing required fields'}, 400
    # Checks if item with given id already exists in the database
    if Item.query.filter_by(id=data['id']).first():
        return {'error': 'Item with given id already exists'}, 400
    # Creates new item object from the request data
    new_item = Item.from_dict(data)
    # Adds new item to the session then saves changes.
    db.session.add(new_item)
    db.session.commit()
    return {'msg': 'Item added successfully'}, 201


# update item quantity
@app.route('/api/item/update', methods=["PUT"])
def updateItem():
    data = request.get_json(force=True)
    print(data)
    # Add the code to add an item from the database and if it was successful with a success or fail message along with error code
    # {
    # 'id': '', 
    # 'subtract': True,
    # 'quantity': ''
    # }
    # return {"msg":"failed"}, 400
    item = Item.query.get(data["id"])
    if item is None:
        return {"msg": "Item has not been found"}, 400
    if data["subtract"]:
        if item.quantity < int(data["quantity"]): 
            return {"msg": "Cant have quantity less than 0"} ,400
        item.quantity -= int(data["quantity"])
        print("Here")
    else:
        item.quantity += int(data["quantity"])
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
                    "quantity": item.quantity,
                    "category": item.category
        })

    return jsonify(items)

# add a single customer
@app.route('/api/customer/add', methods=["POST"])
def addCustomer():
    data = request.get_json(force=True)
    print(data)
    # Add the code to add an customer from the database and if it was successful with a success or fail message along with error code
    # example body
    # {
    #     "id": 123,
    #     "name": "testItem",
    #     "phone":1231231231,
    #     "email":"someEmail@test.com"
    # }
    # return {"msg":"failed"}, 400
    return {"msg":"customer added"}, 200

# return all items
@app.route('/api/customers/', methods=["GET"])
@app.route('/api/customers/<string:category>', methods=["GET"])
def getCustomers(phone = 0):
    print(phone)
    # return all customers if phone number = 0, or return the customer that has a matching phone number.
    # this can be done with phone number, or if its easier I can change it to id, I assumed phone number is more practical
    return jsonify(customers)

#delete a single item
@app.route('/api/customer/delete',methods=["DELETE","POST"])
def deleteCustomer():
    data = request.get_json(force=True)
    print(data)
    # Add the code to remove an customer from the database and if it was successful with a success or fail message along with error code
    # this can be done with phone number, or if its easier I can change it to id, I assumed phone number is more practical
    # example body 
    # {
    #     "phone": 123,
    # }
    # return {"msg":"failed"}, 400
    return {"msg":"customer removed"}, 200

# add a single item
@app.route('/api/supplier/add', methods=["POST"])
def addSupplier():
    data = request.get_json(force=True)
    print(data)
    # Add the code to add an supplier from the database and if it was successful with a success or fail message along with error code
    # example body
    # {
    #     "id": 123,
    #     "name": "testItem",
    #     "phone":1231231231,
    #     "email":"someEmail@test.com"
    # }
    # return {"msg":"failed"}, 400
    return {"msg":"supplier added"}, 200

# return all items
@app.route('/api/suppliers/', methods=["GET"])
@app.route('/api/suppliers/<string:phone>', methods=["GET"])
def getSupplier(phone = 0):
    print(phone)
    # return all supplier if phone number = 0, or return the supplier that has a matching phone number.
    # this can be done with phone number, or if its easier I can change it to id, I assumed phone number is more practical
    return jsonify(suppliers)

#delete a single item
@app.route('/api/supplier/delete',methods=["DELETE","POST"])
def deleteSupplier():
    data = request.get_json(force=True)
    print(data)
    # Add the code to remove an supplier from the database and if it was successful with a success or fail message along with error code
    # this can be done with phone number, or if its easier I can change it to id, I assumed phone number is more practical
    # example body 
    # {
    #     "phone": 123,
    # }
    # return {"msg":"failed"}, 400
    return {"msg":"supplier removed"}, 200

# add a single item
@app.route('/api/order/add', methods=["POST"])
def addOrder():
    data = request.get_json(force=True)
    print(data)
    # Add the code to add an supplier from the database and if it was successful with a success or fail message along with error code
    # example body
    # {
#     "customerId": 123,
#     "items":[
#                 {"id":123,"quantity":1},
#                 {"id":123,"quantity":1}
#             ],
#     "orderDate":"12-12-2012",
#     "totalCost":123,
#       }
    # return {"msg":"failed"}, 400
    return {"msg":"order added"}, 200

# return all items
@app.route('/api/orders/', methods=["GET"])
@app.route('/api/orders/<string:id>', methods=["GET"])
def getOrders(id = 0):
    print(id)
    # return all supplier if phone number = 0, or return the supplier that has a matching phone number.
    # this can be done with phone number, or if its easier I can change it to id, I assumed phone number is more practical
    return jsonify(orders)

# return a order by id
@app.route('/api/order/<string:id>', methods=["GET"])
def getOrder(id = 0):
    print(id)
    # return all supplier if phone number = 0, or return the supplier that has a matching phone number.
    # this can be done with phone number, or if its easier I can change it to id, I assumed phone number is more practical
    return jsonify(orders[0])

#delete a single item
@app.route('/api/order/delete',methods=["DELETE","POST"])
def deleteOrder():
    data = request.get_json(force=True)
    print(data)
    # Add the code to remove an supplier from the database and if it was successful with a success or fail message along with error code
    # this can be done with phone number, or if its easier I can change it to id, I assumed phone number is more practical
    # example body 
    # {
    #     "phone": 123,
    # }
    # return {"msg":"failed"}, 400
    return {"msg":"order removed"}, 200

if __name__ == "__main__":
    app.run()