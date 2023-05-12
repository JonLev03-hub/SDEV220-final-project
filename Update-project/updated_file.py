from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import or_

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
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
        
@app.route('/')
def get_all_items():
    items = []
    return render_template("items.html", items=items)
@app.route('/add', methods = ['POST'])
def add():
    if request.method=='POST':
        name=request.form['name']
        supplier_id=request.form['supplier_id']
        item_price=request.form['item_price']
        item_description=request.form['item_description']
        item_count=request.form['item_count']
        
        my_data = Item(name, supplier_id, item_price, item_description, item_count)
        db.session.add(my_data)
        db.session.commit()
        
        return redirect(url_for('items'))
    
 
  

if not os.path.exists('crud.db'):
    with app.app_context():
        db.create_all()

@app.route('/items/', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'})
    item_data = {}
    item_data['id'] = item.id
    item_data['item_name'] = item.item_name
    item_data['item_supplier_id'] = item.item_supplier_id
    item_data['price'] = item.price
    item_data['item_description'] = item.item_description
    item_data['item_count'] = item.item_count
    return jsonify(item_data)

@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.json['item_name']
    item_supplier_id = request.json['item_supplier_id']
    price = request.json['price']
    item_description = request.json['item_description']
    item_count = request.json['item_count']
    item = Item(item_name=item_name, item_supplier_id=item_supplier_id, price=price, item_description=item_description, item_count=item_count)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'})

@app.route('/update', methods=['PUT'])
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
    item.price = price
    item.item_description = item_description
    item.item_count = item_count
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})

@app.route('/delete', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({'error': 'Item not found'})
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    
    
    
    
