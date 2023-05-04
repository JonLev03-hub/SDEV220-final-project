from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///OpenAirGardens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50))
    item_supplier_id = db.Column(db.String(50))
    item_price = db.Column(db.Float(precision=2))
    item_description = db.Column(db.String(50))
    item_count = db.Column(db.Integer)

    def __init__(self, item_name, item_supplier_id, item_price, item_description, item_count):
        self.item_name = item_name
        self.item_supplier_id = item_supplier_id
        self.item_price = item_price
        self.item_description = item_description
        self.item_count = item_count

# Allow searching of items using different features
@app.route('/items', methods=['GET'])
def get_all_items():
    search_query = request.args.get('q')
    if search_query:
        items = Item.query.filter(or_(Item.item_name.contains(search_query), Item.item_supplier_id.contains(search_query))).all()
    else:
        items = Item.query.all()
    result = []
    for item in items:
        item_data = {}
        item_data['id'] = item.id
        item_data['item_name'] = item.item_name
        item_data['item_supplier_id'] = item.item_supplier_id
        item_data['price'] = item.item_price
        item_data['item_description'] = item.item_description
        item_data['item_count'] = item.item_count
        result.append(item_data)
    return jsonify(result)


@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'})
    item_data = {}
    item_data['id'] = item.id
    item_data['item_name'] = item.item_name
    item_data['item_supplier_id'] = item.item_supplier_id
    item_data['price'] = item.item_price
    item_data['item_description'] = item.item_description
    item_data['item_count'] = item.item_count
    return jsonify(item_data)

@app.route('/items', methods=['POST'])
def add_item():
    item_name = request.json['item_name']
    item_supplier_id = request.json['item_supplier_id']
    price = request.json['price']
    item_description = request.json['item_description']
    item_count = request.json['item_count']
    item = Item(item_name=item_name, item_supplier_id=item_supplier_id, item_price=price, item_description=item_description, item_count=item_count)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'})

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'})
    item_name = request.json['item_name']
    item_supplier_id = request.json['item_supplier_id']
    price = request.json['price']
    item_description = request.json['item_description']
    item_count = request.json['item_count']
    item.item_name = item_name
    item.item_supplier_id = item_supplier_id
    item.item_price = price
    item.item_description = item_description
    item.item_count = item_count
    db.session.commit()
    return jsonify({'message':
