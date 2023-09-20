from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from re import match
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# Initialize a default number of rows and page
rows = 5
page = 1

# Initialize a boolean to check if user is in 'All' contacts or 'Favorite' contacts only 
global is_favorite_page
is_favorite_page = False
is_searching = False

class Contact(db.Model):
    # Attributes of the Contact SQL Table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255))
    telephone_number = db.Column(db.String(255))
    favorite = db.Column(db.Boolean, default=False, nullable=False)
    creation_timestamp = db.Column(db.DateTime)

@app.route('/')
def test():
    return 'Hello World!'

@app.route('/api/add', methods=["POST"])
def add():
    # Initialize data provided into variables
    name = request.json['name']
    email = request.json['email']
    telephone_number = str(request.json['telephone_number'])
    
    telephone_number.replace(" ", "")
    favorite = request.json['favorite']
    
    # Check and validate the data
    error_message = dataValidation(name, email, telephone_number)
    if error_message: 
        return error_message
    existing_contact = Contact.query.filter_by(name=name).first()
    if existing_contact:
        return jsonify('Contact already exists'), 400
    
    # Add the new contact into the database
    new_contact = Contact(name=name, email=email, telephone_number=telephone_number, favorite=favorite, creation_timestamp=datetime.now())
    db.session.add(new_contact)
    db.session.commit()

    # Return a success message
    return jsonify('Added successfully'), 200

@app.route('/api/contacts', methods=["GET"])
def getContacts():
    # Retrieve contacts from the database
    contacts = Contact.query.order_by(Contact.name).paginate(page=page, per_page=rows).items
    if not contacts:
        return jsonify('Contacts don\'t exist'), 400
    
    # User is not in the 'favorite' contacts only page
    global is_favorite_page
    is_favorite_page = False

    global is_searching
    is_searching = False

    # Initialize an array where contacts will be appeneded to be returned to the user
    contacts_list = []

    # Append the contacts in the array and convert to json format
    for contact in contacts:
        contacts_list.append(sqltojson(contact))

    # Return the contacts list
    return jsonify(contacts_list), 200

@app.route('/api/favorites', methods=["GET"])
def getFavorites():
    # Retrieve favorite contacts only from the database
    favorites = Contact.query.filter(Contact.favorite == True).order_by(Contact.name).paginate(page=page, per_page=rows).items
    if not favorites:
        return jsonify('Favorites don\'t exist'), 400
    
    # User is in the favorite page
    global is_favorite_page
    is_favorite_page = True

    global is_searching
    is_searching = False

    # Initialize an array where contacts will be appeneded to be returned to the user
    favorites_list = []

    # Append the contacts in the array and convert to json format
    for favorite in favorites:
        favorites_list.append(sqltojson(favorite))

    # Return the favorites list
    return jsonify(favorites_list), 200

@app.route('/api/contact/<id>', methods=["GET"])
def getContact(id):
    # Retrieve a contact based on the id
    q = Contact.query.get(id)
    if not q:
        return jsonify('Contact doesn\'t exist'), 400
    
    # Convert contact to json format
    individual_contact = sqltojson(q)

    # Return the individual contact
    return jsonify(individual_contact), 200

@app.route('/api/update/<id>', methods=["PUT"])
def updateContact(id):
    # Retrieve a contact based on the id
    q = Contact.query.get(id)
    if not q:
        return jsonify('Contact doesn\'t exist'), 400
    
    # Initialize the updated values into a variable
    upd = request.get_json(force=True)

    # Check and validate the new data
    error_message = dataValidation(upd['name'], upd['email'], upd['telephone_number'].replace(" ", ""))
    if error_message:
        return error_message
    if q.name != upd['name']:
        existing_contact = Contact.query.filter_by(name=upd['name']).first()
        if existing_contact:
            return jsonify('Contact already exists'), 400
    
    # Update the contact in the database
    q.name = upd['name']
    q.email = upd['email']
    q.telephone_number = upd['telephone_number']
    q.favorite = upd['favorite'] == 'true'
    db.session.commit()
    
    # Convert contact to json format
    individual_contact = sqltojson(q)

    # Return the individual contact
    return jsonify(individual_contact), 200

@app.route('/api/delete/<id>', methods=["DELETE"])
def deleteContact(id):
    # Retrieve a contact based on the id
    q = Contact.query.filter(Contact.id == id)
    if not q:
        return jsonify('Contact doesn\'t exist'), 400
    
    # Delete contact from the database
    q.delete()
    db.session.commit()

    # Return a success message
    return jsonify("Deleted successfully"), 200

@app.route('/api/favorite/<id>', methods=["PUT"])
def favoriteContact(id):
    # Retrieve a contact based on the id
    q = Contact.query.get(id)
    if not q:
        return jsonify('Contact doesn\'t exist'), 400
    
    # Initialize value of favorite into a variable
    fave = request.get_json(force=True)

    # Change the value of favorite of contact in the database
    q.favorite = fave['favorite']
    db.session.commit()
    
    # Convert contact to json format
    individual_contact = sqltojson(q)

    # Return the individual contact
    return jsonify(individual_contact), 200

@app.route('/api/search/', methods=["GET"])
def searchContacts():
    # Retrieve contacts that contain the query substrings
    global query
    query = request.args.get('name')

    global is_searching
    is_searching = True

    if is_favorite_page:
        searched = Contact.query.filter(Contact.name.like('%{}%'.format(query))).filter(Contact.favorite == is_favorite_page).order_by(Contact.name).paginate(page=page, per_page=rows).items
    else:
        searched = Contact.query.filter(Contact.name.like('%{}%'.format(query))).order_by(Contact.name).paginate(page=page, per_page=rows).items
    
    if not searched:
        return jsonify('Searched contacts don\'t exist'), 400
    
    # Initialize an array where contacts will be appeneded to be returned to the user
    searched_list = []

    # Check what page the user is in and convert the contacts into json format
    for search in searched:
        searched_list.append(sqltojson(search))

    # Return the searched list
    return jsonify(searched_list), 200

@app.route('/api/paginate/', methods=["GET"])
def paginate():
    # Initialize number of rows and page into variables
    global rows
    rows = int(request.args.get('rows'))
    if not rows:
        return jsonify('Rows not found'), 400
    global page
    page = int(request.args.get('page'))
    if not page:
        return jsonify('Page not found'), 400
    
    # # Check what page the user is in and retrieve the appropriate contacts
    if is_searching:
        if is_favorite_page:
            paginated = Contact.query.filter(Contact.name.like('%{}%'.format(query))).filter(Contact.favorite == is_favorite_page).order_by(Contact.name).paginate(page=page, per_page=rows).items
        else:
            paginated = Contact.query.filter(Contact.name.like('%{}%'.format(query))).order_by(Contact.name).paginate(page=page, per_page=rows).items
    else: 
        if is_favorite_page:
            paginated = Contact.query.filter(Contact.favorite == True).order_by(Contact.name).paginate(page=page, per_page=rows).items
        else: 
            paginated = Contact.query.order_by(Contact.name).paginate(page=page, per_page=rows).items

    # Initialize an array where contacts will be appeneded to be returned to the user
    paginated_list = []

    # Append the contacts in the array and convert to json format
    for contact in paginated:
        paginated_list.append(sqltojson(contact))

    # Return the paginated list
    return jsonify(paginated_list)

def sqltojson(q):
    # Convert retrieved sql data into a json / dictionary format
    date_time = q.creation_timestamp.strftime("%d/%m/%Y %H:%M:%S")
    individual_contact = {
        'id': q.id,
        'name': q.name,
        'email': q.email,
        'telephone_number': q.telephone_number,
        'favorite': q.favorite,
        'creation_timestamp': date_time
    }
    return individual_contact

def dataValidation(name, email, telephone_number):
    # Validate if a name is provided
    if not name:
        return jsonify('Name missing'), 400
    
    # Validate if both email and telephone number are provided
    if not email and not telephone_number:
        return jsonify('Email or Telephone Number must be set'), 400
    
    # Validate if email is in correct format
    if email:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        if not match(email_regex, email):
            return jsonify('Email format incorrect'), 400
        
    # Validate if telephone number is in correct format
    if telephone_number:
        telephone_number_regex = r'^\+?[0-9]{1,15}$' 
        if not match(telephone_number_regex, telephone_number):
            return jsonify('Telephone Number format incorrect'), 400
        
    # No errors are found
    return None

# Run application
if __name__ == "__main__":
    app.run(debug=True)