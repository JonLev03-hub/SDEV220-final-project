from flask import Flask, render_template
from flask import request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

items = [{
        "id": 123,
        "name": "testItem",
        "supplier_id": 123,
        "price": 123,
        "desc": "item desc",
        "count": 123,
        "category": "misc_category"
    },
    {
        "id": 123,
        "name": "testItem",
        "supplier_id": 123,
        "price": 123,
        "desc": "item desc",
        "count": 123,
        "category": "misc_category"
    },
    {
        "id": 123,
        "name": "testItem",
        "supplier_id": 123,
        "price": 123,
        "desc": "item desc",
        "count": 123,
        "category": "misc_category"
    }]

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
    # Add the code to remove an item from the database and if it was successful with a success or fail message along with error code
    # example body 
    # {
    #     "id": 123,
    # }
    # return {"msg":"failed"}, 400
    return {"msg":"item removed"}, 200

# add a single item
@app.route('/api/item/add', methods=["POST"])
def addItem():
    data = request.get_json(force=True)
    print(data)
    # Add the code to add an item from the database and if it was successful with a success or fail message along with error code
    # example body
    # {
    #     "id": 123,
    #     "name": "testItem",
    #     "supplier_id": 123,
    #     "price": 123,
    #     "desc": "item desc",
    #     "count": 123,
    #     "category": "misc_category"
    # }
    # return {"msg":"failed"}, 400
    return {"msg":"item added"}, 200

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
    return {"msg":"item quantity updated"}, 200

# return all items
@app.route('/api/items/', methods=["GET"])
@app.route('/api/items/<string:category>', methods=["GET"])
def getItems(category = "all"):
    print(category)
    # return all items with the exact same category. If the category is all return all items. return in a list.
    return jsonify(items)

if __name__ == "__main__":
    app.run()