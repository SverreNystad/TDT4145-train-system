# README

## Train App

Train App is a command line based application that allows users to interact with a train ticketing system. Users can check train routes, trips, and available tickets, as well as register, log in, and buy tickets if they are a customer. This application uses a local SQLite database to store data. This application was made in one of our subjects TDT4145 as a semester project to show that we both understand databases but can also make use of them in our applications.

```
  _______     _______     _______     _______     ___       
 /       \   /       \   /       \   /       \   /  |\_     
|   NORD  | |  LANDS  | |  BANEN  | |   S J   | |   |____\_ 
|_________|_|_________|_|_________|_|_________|_|_  |______|
  O     O     O     O     O     O     O     O    O\/_|      
```
### Features

1. Register as a customer
2. Log in as a customer
3. View all stations
4. View all train routes for a specific station on a specific weekday
5. View all train trips for a specific date and start and end station
6. View all available tickets between a start station and an end station for a given route
7. Buy tickets (for logged in customers only)
8. View future tickets (for logged in customers only)
9. Visualization of train wagons for choosing placement.

### Usage

Run the `train_app.py` Python file to start the application. Upon starting, you will be greeted with a list of commands. Type a command and press Enter to execute it. To exit the application, type 'exit' and press Enter.

### Commands

* `help` - displays a list of commands
* `exit` - exits the app
* `stations` - lists all stations
* `train routes, <weekday>, <station>` - lists all train routes for a specific station on a specific weekday
* `train trips, <DD.MM.YYYY>, <HH:MM>, <start station>, <end station>` - lists all train trips for a specific date and start and end station
* `register` - registers as a Customer
* `login` - logs in as a Customer
* `tickets, <trip ID>, <start station>, <end station>` - lists all available tickets between a start station and an end station for a given route
* `buy tickets, <trip ID>, <start station>, <end station>, [(<wagon number>,<seat/bed number>)]` - reserve a seat/bed in a specific wagon between a start station and an end station for a given route (logged in customers only)
* `my tickets` - lists all future tickets for the logged in Customer

### ER diagram
![ER diagram of train app](https://user-images.githubusercontent.com/89105607/236075048-20557b51-a4c3-4096-b4e3-fc0b424e2f12.PNG)


### Dependencies

* Python 3.6 or higher

### License

This project is released under the MIT License.
