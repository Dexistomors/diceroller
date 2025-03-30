# Diceroller
Diceroller is a multi-user dice rolling web application for use in tabletop games. Users are able to join rooms with other users and roll digital dice on  a web-based interface. This should allow players to transparently share their dice rolls with each other and to keep a record of the results. A server/client design reduces the opportunity for cheating.

This is an in-progress self-guided project to learn web design. The intention is to learn the following concepts:
- Server/client web application design
- Programming for web applications
- Front-end UI
- Back-end API design and usage

And the following technologies:
- Backend logic and API via Python/Django
- Relational database via Django/SQL
- Frontend via HTML/CSS/Grid and JavaScript/jQuery

## Usage

Examples are using /home/dexistomors/git/diceroller as the repository root. These steps assume a Linux operating system with Python 3 and Django installed.

**Note**: The intent for the project is eventually to automate deployment via Docker, but while in-progress the project can be tested with the following steps:

1. The location of the diceroller module must be included in PYTHONPATH
  - `export PYTHONPATH=/home/dexistomors/git/diceroller/:$PYTHONPATH`
2. Use the Django test server from the Django project directory
  - `cd /home/dexistomors/git/diceroller/site/project`
3. Migrate the database for the Django test server
  - `python3 manage.py migrate`
4. Create a Django test server superuser
  - `python3 manage.py createsuperuser`
5. Run the Django test server
     `python3 manage.py runserver`
6. Navigate to the server using your preferred web browser. From here you can login with the superuser account you just created to explore the basic functionality of the app.
7. You can create additional users using the Django administration interface at /admin to test multi-user functionality.


To roll some dice:

1. Enter a room code to create a room (if that room code does not exist) or join a room (if the room code already exists).
2. Enter the die faces, modifiers, and advantage in the left panel.
3. Save the roll configuration (or load a roll configuration) and roll the dice from the center panel.
4. Results for the room are shown in the right panel.

## Code Explanation

The dice-roller web application consists of 4 major parts: the UI, API, the database, and the diceroller module. Once a user has created and/or joined a room, the flow is as follows:
1. Users interact with the UI to create roll configurations, which are sent to the API.
2. The API sends those roll configurations to the diceroller module, which returns roll results to the API.
3. The API then stores results in the database, and returns success or an error to the UI.
4. The UI periodically queries the API for up-to-date information on the current room, which includes roll results from other users.

The repo is split into two parts: the diceroller Python module in /diceroller and the Django project in /site/project. The Django project includes the UI, API, and database. 

I chose to implement the dice rolling logic as the diceroller Python module to teach myself basic Python and object-oriented programming. The module can deserialize RollConfig objects from a JSON string. That's used to create Roll objects which contain dice, modifiers, and various other settings. Then it creates a RollResult object that is used to serialize the results as a JSON string for handing back to the API. The module also features some basic unit testing. 

The UI was used to learn HTML/CSS and Grid for the layout. Queries to the API from the UI were done with JavaScript and jQuery, and loading results into the UI from the API was done with Ajax requests and long polling. There is also some login functionality via Django, which taught me some of the basics of authentication and session management. 

I used the design of the API to teach myself about REST APIs in general. While it's not strictly compliant, it uses Django views to implement a basic interface for the front-end. The /api/roll endpoint receives roll configuration JSONs (via a POST) and returns JSON results after they've been processed by the diceroller module. The /api/room endpoint receives a particular room code (via a GET) and returns JSON results with the users and roll results, or it can create new rooms or add users to rooms (via a POST). The /api/roll_config endpoint is still in progress, but will be able to return roll configurations for the current user (via a GET), save roll configurations (via a POST), or delete them (via a DELETE). 

The database is managed by Django, and contains users, passwords, rooms, roll configurations, and roll results. Roll configurations and roll results are currently stored as serialized JSON but will eventually be implemented using Django's database model.

## Roadmap

- To Do: Finish roll_config endpoint: Add functionality for updating and deleting individual configs.
- To Do: UI updates roll_config list upon save and during long polling.
- To Do: Add new user registration to the UI.
- To Do: Use Django's database model for storing diceroller data.
- To Do: Package and version the Python module.
- To Do: Create a Docker container.
- To Do: Create deployment and testing scripts using the container image.
