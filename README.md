# Contacts - Full Stack Web App

Contacts is a full stack web app that allows users to manage their contacts. Users can add, edit, delete, and mark contacts as favorites. The app also provides a search function to help users find contacts quickly and easily.

## Tech Stack
- **Frontend**: Angular
- **Backend**: Flask
- **Database**: SQLite3

## Functionalities
- **Manage Contacts**: Users should be able to add, edit, delete, and mark contacts as favorites.
- **List Contacts**: Users should be able to list all contacts, sorted alphabetically. The list should show contacts in tabular form, with a different shade for favorite contacts. Users should also be able to switch between viewing all contacts and only viewing favorite contacts. The list should be paginated, with users able to specify the page size.
- **Search for Contacts**: Users should be able to search for contacts by name.
- **Data Validation**: Before a contact is saved, the data received by the app should meet the following requirements: 
    - Contact name: The contact name must be set and unique.
    - Email: The email address must follow a typical email address format.
    - Telephone Number: The telephone number must contain only numeric characters and an optional "+" prefix.
    - At least one of Email or Telephone Number: At least one of either email or telephone number must be set.

## How to Run

To run the front end of web application, run the following commands:

```
npm install
npm start
```

and for the Flask backend, navigate to the folder that contains the code and run:

```
python app.py
``` 

In your web browser, navigate to `http://localhost:4200/` to access the web application.
