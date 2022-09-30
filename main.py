# CINF 308 - Fall 2022 - Assignment 6
# Text adventure game
# John Logiudice

import random


# Check if string can be converted to an integer
def is_int(f_string):
    try:
        int(f_string)
        return True
    except ValueError:
        return False


# Get and confirm a Y of N answer
def get_yn():
    while True:
        response = input("Please enter (Y)es or (N)o: ").lower()

        # Only check first letter in case user types Yes or No
        if response[0] in ('y', 'n'):
            return response


def quit_game():
    print()
    print('Thanks for playing!')
    quit()


# Print the room menu and get response
def room_menu(f_room, f_room_dict):
    this_room_feature = f_room_dict[f_room]['features']

    # iterate over and print each feature in the room to the menu
    for i in range(0, len(this_room_feature)):
        print(f"{i + 1}. {this_room_feature[i]}")

    # loop until user chooses valid menu response
    while True:
        response = input("What would you like to look at (enter the number)? ")
        # Check that integer was entered
        if is_int(response):
            # Subtract 1 to match tuple index
            response = int(response) - 1
            # Return feature value
            if int(response) in range(0, len(this_room_feature)):
                return f_room_dict[f_room]['features'][response]
        elif response.lower() in ('q', 'quit'):
            quit_game()

        print('Please enter a valid menu choice')


# Print item found in feature and ask if user wants to take it
def feature_menu(f_feature, f_feature_dict, f_item_dict):
    this_feature_item = f_item_dict[f_feature_dict[f_feature]['item']]

    # If item is not already found, ask user Y/N to take it
    if not this_feature_item['taken']:
        print(this_feature_item['description'])
        print(f"Would you like to take the {f_feature_dict[f_feature]['item']}?")
        response = get_yn()
        print()

        if response == 'y':
            this_feature_item['taken'] = 'True'
            print(f"You took the {f_feature_dict[f_feature]['item']}.")

    # User already found this item
    else:
        print(f"There is noting to see in the {f_feature}.")


# Change the state of or walk through a door
def door_state(f_feature, f_feature_dict, f_room):
    this_feature = f_feature_dict[f_feature]

    print(f"It is currently {this_feature['state']}")

    if this_feature['state'] == 'closed':
        print()
        print("Would you like to open it?")
        response = get_yn()

        if response == 'y':
            print()
            this_feature['state'] = 'open'
            print('It is now open')

    elif this_feature['state'] == 'open':
        print()
        print("Would you like to close it?")
        response = get_yn()

        if response == 'y':
            print()
            this_feature['state'] = 'closed'
            print('It is now closed')

    if this_feature['state'] == 'open':
        print()
        print('Would you like to walk through it?')
        response = get_yn()

        if response == 'y':
            f_room = leave_room(f_feature, f_feature_dict)
    return f_room


def leave_room(f_feature, f_feature_dict):
    f_feature_dict[f_feature]['next_room'], f_feature_dict[f_feature]['curr_room'] = f_feature_dict[f_feature][
                                                                                         'curr_room'], \
                                                                                     f_feature_dict[f_feature][
                                                                                         'next_room']
    return f_feature_dict[f_feature]['curr_room']


# Main

room = 'quarters'
inventory_list = []

room_tuple = ('quarters', 'hall', 'helm', 'engine room')

room_dict = {}
room_dict['quarters'] = {'features': ('quarters', 'plant', 'bed', 'grey door'),
                         'title': 'your quarters'}
room_dict['hall'] = {'features': ('hall', 'grey door', 'blue door', 'red door'),
                     'title': 'the hall'}
room_dict['helm'] = {'features': ('blue door',),
                     'title': 'the helm'}
room_dict['engine room'] = {'features': ('red door',),
                            'title': 'the engine room'}

feature_dict = {}
feature_dict['quarters'] = {'type': 'room',
                            'description': "You are in your quarters, a tiny space with just enough room for a table and bed.\n" \
                                           "The bed is a mess of ruffled sheets and a pillow.\n" \
                                           "There is a grey door which is closed.\n" \
                                           "Oddly, there is a well cared for potted plant in the corner.\n" \
                                           "You must have a green thumb."}
feature_dict['hall'] = {'type': 'room',
                        'description': "This is a sterile looking white hallway with a black and grey tiled floor.\n" \
                                       "There are three doors colored grey, blue, and red."}
feature_dict['helm'] = {'type': 'room',
                        'description': ""}
feature_dict['engine room'] = {'type': 'room',
                               'description': ""}
feature_dict['plant'] = {'type': 'object',
                         'item': 'key',
                         'description': "The plant is a happy rubber tree in a wicker basket."}
feature_dict['bed'] = {'type': 'object',
                       'item': 'gloves',
                       'description': "The bed is a mess of ruffled sheets with a thin pillow."}
feature_dict['grey door'] = {'type': 'door',
                             'state': 'closed',
                             'curr_room': 'quarters',
                             'next_room': 'hall',
                             'description': "The door is an ordinary door."}
feature_dict['blue door'] = {'type': 'door',
                             'state': 'closed',
                             'curr_room': 'hall',
                             'next_room': 'helm',
                             'description': "The door is an ordinary door."}
feature_dict['red door'] = {'type': 'door',
                            'state': 'closed',
                            'curr_room': 'hall',
                            'next_room': 'engine room',
                            'description': "The door is an ordinary door."}

item_dict = {}
item_dict['key'] = {'taken': False,
                    'description': "There is a shiny piece of metal. It looks like a key."}
item_dict['gloves'] = {'taken': False,
                       'description': "These are heavy canvas gloves with a thick rubber coating."}

title = " * * * * * * * Space Adventure * * * * * * *"
welcome_message = ""

print(title)
print(welcome_message)
print(" -" * 23)

while True:
    print()
    print(f"You are in {room_dict[room]['title']}.")
    print()
    print('- - - - MENU - - - -')
    feature = room_menu(room, room_dict)

    print()
    print(feature_dict[feature]['description'])
    print()
    # If this feature has items to find
    if 'item' in list(feature_dict[feature]):
        feature_menu(feature, feature_dict, item_dict)

    # If this feature is a door
    if feature_dict[feature]['type'] == 'door':
        room = door_state(feature, feature_dict, room)
