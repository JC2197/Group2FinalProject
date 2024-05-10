Central Connecticut Sate University 
CS-416-02 
Fall 2023

The functionality of our project is the full Ticketmaster app mock web app, meaning the ability to search for events and see them displayed on the page, as well as the ability to create an account and sign in. 
When signed out, users have limited access to the page until they are authenticated and signed in. Signing up for an account requires a username and password, and two usernames cannot match. 
Users are prompted with alert messages if their sign up form is invalid. A user must sign in with a valid username and password present in the database. 
Each user can save events to view on a separate page, and then on that page, they can favorite events or remove them from their saved events. 
The project is deployed via PythonAnywhere so that it can be accessed on any internet browser. 
The core functionality was developed by Joseph in Javascript and translated to the Django format by Emilio. 
It takes the keyword in one text input, and the city in another, and uses those to perform a search in the Ticketmaster API using requests in views.py file. 
It then programmatically loops through the response and uses Django template language to render Bootstrap cards with the information coming from the API onto the HTML page. 
The accounts functionality was developed by Joseph. Signup extends the UserCreation classes in Django. 
It saves a username and password (hashed automatically) to the database and authorizes that combination to log in to the page. Both the Signup and Signin pages are styled with Bootstrap. 
The CRUD requirement was developed by Emilio. 
C - Allow users to add saved events to the database 
R - Users can view their saved events. 
U - Users can update their saved events to mark them as favorited or remove them from their favorites. 
D -Users can delete events they no longer want to be saved from their saved event list. 
Riley was responsible for deploying and updating the site via PythonAnywhere, as well as helping input code snippets, such as bug fixing/error handling for the sign up, saved events, and favoriting.
