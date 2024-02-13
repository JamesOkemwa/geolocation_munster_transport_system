# Münster Public Transport App

This project is a web application for exploring public transport information in Münster. It allows users to view bus stop locations, find the nearest bus stop based on their location, view details of the next bus and search for addresses or places on the map.

### Prerequisites

Before running the application, ensure you have the following installed:

- [Python](https://www.python.org/) (version 3.x.x)
- [Pip](https://pypi.org/project/pip/)
- Any tool for creating a virtual environment.

### Installation and running the application
- Create a directory on your computer and copy the zipped file.
- Create a virtual environment and activate it.
```
python -m venv venv
source venv/bin/activate
```
- Install the required dependencies using the command `pip install requirements.txt`
- Run the application using the command `python app.py`
- Open your browser to view the application `http://localhost:5000`

### Using the map
- The map displays bus stop locations in Münster city.
- Click on a bus stop marker to view its details.
- Allow access to your location from the browser, to extract and view the details of the nearest bus stop.
- Click the search icon on the upper right corner, to search for a place name or an address in Münster.


### Features
- Displays bus stop locations on an interactive map.
- Finds the nearest bus stop based on the user location.
- Finds the details of the next bus at the identified nearest bus stop.
- Finds and displays the route followed by the next bus.
- Search for locations or addresses using the geocoding search bar, and find the nearest bus stop to the searched address.