# SDEV220-final-project

[Final Project Launch document](https://docs.google.com/document/d/1Z90PjYnpw-Ow5EOVVITlBRNZac2CWHlNpFsoIt7qHpE/edit).


For our project, we will be creating an inventory system for Open-air Gardens. This is a small plant nursery franchise that sells plants. The inventory system we create will provide the user with a graphic interface where they can list all of the items they keep in stock, along with how many of each item they currently have in stock, where that item is stored, a general description of the item, the supplier and more. The user will also be able to add or remove stock of each item individually. Additionally, we will manage orders in our system. These orders will have basic client information, a status, and the items that are required for the order.

## Tech
This project will use Flask for the back end, sqlite3 for data storage, and Javascript/html for the front end.

## Features
Users will be able to add items, customers, and orders to the inventory system. Once items are added to the system you can change the quantity of each item individually for instances where items are found or destroyed, or you can process a shipment of items for when you recieve stock. Simmilarly when you make a sale you are able to add an order to the system, and then once that order is ready to be sent out you will have the option to process the order. This will fail if there are not enough items in stock. 

The user will be able to view information from all tables inside of the system aswell. This allows them to view orders, customers, or items in the system. 

## Details of project

### Api Routes
GET:: /api/<category>
accepts a search term inside of the json, and this will either be a category, or an item ID. Then the api will return a list of items that meet the criteria. suppliers and customers wont have a category so we can use the phone number

GET:: /api/<category>
only accepts an id, and will return only one record that is an exact match

POST:: /api/<category>/add
accepts a json object that containst all the items to create a record for that table, and returns a success or failure response

DELETE:: /api/<category>/remove
accepts a json object that containst an id, and returns a success or failure response

###Front end design
Because the front end pages are all going to be reading, updating, and deleting records they will have very simmilar format. The design below is for the items page. It is not the finalized design, but it will be used to design the other pages. 

![image](https://user-images.githubusercontent.com/81537476/235364087-398e41da-23ef-42ba-a3bf-3f8f131fcb10.png)

This will allow users to create items, search items, remove items, and adjust item quantities. 



