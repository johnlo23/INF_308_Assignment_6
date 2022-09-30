# CINF 308 - Fall 2022 - Assignment 6
# Text adventure game
# John Logiudice

import random
import time

# global variable for inventory
inventory_list = []


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

    # print global options
    print()
    print("I. for inventory")
    print("Q. to quit game")

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
        elif response.lower() in ('i', 'inventory'):
            print_inventory()
        else:
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
            return f_feature_dict[f_feature]['item']
        else:
            print(f"You left the {f_feature_dict[f_feature]['item']} where it is.")
            return None
    # User already found this item
    else:
        print(f"There is nothing to see in the {f_feature}.")
        return None


# Change the state of or walk through a door
def door_state(f_feature, f_feature_dict, f_room):
    this_feature = f_feature_dict[f_feature]

    print(f"The {this_feature['title']} is currently {this_feature['state']}")

    # If door is currently closed
    if this_feature['state'] == 'closed':
        print()
        print(f"Would you like to open the {this_feature['title']}?")
        response = get_yn()

        if response == 'y':
            if this_feature['locked']:
                if unlock_door(this_feature):
                    print()
                    print(f"You unlock the {this_feature['title']} with the key.")
                    this_feature['state'] = 'open'
                    print(f"The {this_feature['title']} is now open")
                else:
                    print()
                    print(f"The {this_feature['title']} is locked. Do you have the key?")
            else:
                print()
                this_feature['state'] = 'open'
                print(f"The {this_feature['title']} is now open")

    # If door is currently open
    else:
        print()
        print(f"Would you like to close the {this_feature['title']}?")
        response = get_yn()

        if response == 'y':
            print()
            this_feature['state'] = 'closed'
            print(f"The {this_feature['title']} is now closed")

    # If the door is now in an open state, ask if user wants to walk through it
    if this_feature['state'] == 'open':
        print()
        print(f"Would you like to walk through the {this_feature['title']}?")
        response = get_yn()

        if response == 'y':
            # If reply is yes, call function to swap rooms
            f_room = leave_room(f_feature, f_feature_dict)

    # Return the current room
    return f_room


# Swap current room with next room according to the dictionary definition
def leave_room(f_feature, f_feature_dict):
    f_feature_dict[f_feature]['next_room'], f_feature_dict[f_feature]['curr_room'] = \
        f_feature_dict[f_feature]['curr_room'], f_feature_dict[f_feature]['next_room']
    return f_feature_dict[f_feature]['curr_room']


# Unlock a door if key in inventory
def unlock_door(f_this_feature):
    if 'key' in inventory_list:
        f_this_feature['locked'] = False
        return True
    else:
        return False


# Print the current inventory of items carried
def print_inventory():
    print()
    print("You are carrying: ", end="")
    if len(inventory_list) > 0:
        item_string = ""
        for item in inventory_list:
            item_string += item + ", "
        item_string = item_string.rstrip(" ").rstrip(",")
        print(item_string)
    else:
        print("nothing")


def feature_interact(f_feature, f_feature_dict):
    this_feature = f_feature_dict[f_feature]
    if this_feature['action'] == 'press autopilot':
        print(this_feature['action text'])
        print(f"Would you like to {this_feature['action']}?")
        response = get_yn()
        if response == 'y':
            start_engine(f_feature_dict)
    elif this_feature['action'] == 'insert a capacitor':
        if this_feature['equipped']:
            print("There is already a capacitor in the slot.")
        else:
            insert_capacitor(f_feature_dict)
    elif this_feature['action'] == 'call Earth':
        print(this_feature['action text'])
        print(f"Would you like to {this_feature['action']}?")
        response = get_yn()
        if response == 'y':
            if this_feature['fried']:
                print()
                print('Sorry, the radio appears to be out of commission.')
            else:
                aliens_invade = call_earth()
                this_feature['fried'] = True;
                if aliens_invade:
                    print()
                    print("You feel a strong vibration run through the ship.")
                    time.sleep(1)
                    print("The vibration grows stronger.")
                    time.sleep(1)
                    print("The sound of a metal tearing and a sudden jolt tells you something bad has happened.")
                    print("")
                    print("Ironically, with a damaged ship, you managed to complete your mission.")
                    print("Alien life forms from the planet Fligiborp orbiting Tau Ceti intercepted your radio call.")
                    print("It so happens that Fligiborp does have lifeforms and contains a perfect environment for Human life.")
                    print("Unfortunately for you and the ship's crew, the rest of your lives will be spent as forced labor")
                    print("in a Fligiborppian underground mining camp.")
                    print('I wish you better luck in future adventures')
                    quit_game()
        else:
            print("You can always try to call Earth later.")


def call_earth():
    print()
    print("You press the 911 button and wait for a response")
    time.sleep(2)
    print("You hear a crackle and then a voice:")
    print("  Earth here.")
    print("...crackle...")
    print("  We received telemetry that the ship hit an interstellar gas cloud.")
    print("  The engine hyperflux capacitor may have been damaged.")
    print("...hiss...")
    print("  Replace it if you can and try to restart the ship.")
    print()
    print("Before you can say anything, a small puff of white smoke rises from the radio.")

    # Calculate 50/50 chance that aliens invade the ship after using the radio
    chance = random.randint(0, 100)
    if chance > 60:
        return True
    else:
        return False


def start_engine(f_feature_dict):
    print()
    if f_feature_dict['engine']['equipped']:
        print("You press the Autopilot button.")
        time.sleep(2.0)
        print()
        if ship_explode(f_feature_dict):
            print('       !!!!!!! KABLAM !!!!!!!')
            print('The old capacitor must have been damaged.')
            print('The ship and its entire crew have perished.')
            print('I wish you better luck in future adventures')
            quit_game()
        else:
            print("The engines groan a little and then whir back to life!")
            print("Excellent job saving the crew and continuing the mission!")
            quit_game()
    else:
        print("Nothing happens. Maybe you should check the Engine Room.")


def insert_capacitor(f_feature_dict):
    print()
    if 'new capacitor' in inventory_list and 'old capacitor' in inventory_list:
        print("You are carrying the old capacitor and the new capacitor.")
        print()
        print("1. Old Capacitor")
        print("2. New Capacitor")
        # Loop until valid choice
        while True:
            response = input("Which would you like to insert? ")
            if is_int(response):
                response = int(response)
                if response == 1:
                    equip_capacitor(f_feature_dict, 'old capacitor')
                    break
                elif response == 2:
                    equip_capacitor(f_feature_dict, 'new capacitor')
                    break
            print("Please enter 1 or 2.")

    elif 'old capacitor' in inventory_list:
        print("You are carrying the old capacitor.")
        print("Would you like to insert it?")
        response = get_yn()
        if response == 'y':
            equip_capacitor(f_feature_dict, 'old capacitor')
        else:
            print("You are still carrying the old capacitor.")
    elif 'new capacitor' in inventory_list:
        print("You are carrying the new capacitor.")
        print("Would you like to insert it?")
        response = get_yn()
        if response == 'y':
            equip_capacitor(f_feature_dict, 'new capacitor')
        else:
            print("You are still carrying the old capacitor.")
    else:
        print('You are do not have a capacitor to insert.')


def equip_capacitor(f_feature_dict, capacitor_type):
    inventory_list.remove(capacitor_type)
    f_feature_dict['engine']['equipped'] = capacitor_type
    print()
    print(f"You are no longer carrying the {capacitor_type}.")


# Determine if the ship explodes
def ship_explode(f_feature_dict):
    this_feature = f_feature_dict['engine']
    # If new capacitor is used, there is no explosion
    if this_feature['equipped'] == 'new capacitor':
        return False
    else:
        # If old capacitor is used
        # Use random to select a number, where > 80 means ship explodes
        chance = random.randint(0,100)
        if chance >= 80:
            return True
        else:
            return False



# Main
#room = 'quarters'
room = 'helm'

room_dict = {}
room_dict['quarters'] = {'features': ('quarters', 'bed', 'table', 'grey door'),
                         'title': 'your quarters'}
room_dict['hall'] = {'features': ('hall', 'plant', 'grey door', 'blue door', 'red door'),
                     'title': 'the hall'}
room_dict['helm'] = {'features': ('helm', 'blue door', 'ship controls', 'radio'),
                     'title': 'the helm'}
room_dict['engine room'] = {'features': ('engine room', 'engine', 'cabinet', 'floor', 'red door'),
                            'title': 'the engine room'}

feature_dict = {}
feature_dict['quarters'] = {'type': 'room',
                            'description': "You are in your quarters, a tiny space with just enough room for a table and bed.\n"
                                           "The bed is a mess of ruffled sheets and a pillow.\n"
                                           "There is a grey door which is closed.\n"}
feature_dict['hall'] = {'type': 'room',
                        'description': "This is a sterile looking white hallway with a black and grey tiled floor.\n"
                                       "There are three doors colored grey, blue, and red.\n"
                                       "Oddly, there is a well cared for potted plant in the corner.\n"
                                       "Someone must have a green thumb."
                        }
feature_dict['helm'] = {'type': 'room',
                        'description': "The helm is where the captain and crew navigate and operate the ship.\n"
                                       "You see the captain and crew are lying unconscious on the floor.\n"
                                       "Maybe there was an impact or explosion?\n"
                                       "There is the blue door that you entered from.\n"
                                       "The ship control station is where the helmsman 'flies' the ship."}
feature_dict['engine room'] = {'type': 'room',
                               'description': "The engine room is lined with wires and pipes.\n"
                                              "While you are not an engineer, you have some rudimentary knowledge of the engine systems.\n"
                                              "Interstellar Drive is electrically powered by a sealed nuclear fusion battery.\n"
                                              "You can see the hyperflux capacitor is missing from the engine.\n"
                                              "You think to yourself, 'We are not moving without the capacitor in place...'\n"
                                              "'Can I fix this?'"}
feature_dict['plant'] = {'type': 'object',
                         'item': 'key',
                         'description': "The plant is a happy rubber tree in a wicker basket."}
feature_dict['bed'] = {'type': 'object',
                       'item': 'gloves',
                       'description': "The bed is a mess of ruffled sheets with a thin pillow."}
feature_dict['table'] = {'type': 'object',
                         'description': "This is a simple metal table."}
feature_dict['ship controls'] = {'type': 'interact',
                                 'action text': "The ship's control panel has a flashing button labeled 'Resume Autopilot'",
                                 'action': 'press autopilot',
                                 'requires': 'capacitor',
                                 'description': "This is where the helmsman 'flies' the ship."}
feature_dict['engine'] = {'type': 'interact',
                          'equipped': None,
                          'action text': "There is an empty capacitor slot.",
                          'action': 'insert a capacitor',
                          'description': "The engine appears to be in good shape except for the missing capacitor."}
feature_dict['radio'] = {'type': 'interact',
                         'action text': "You can try to call for help.",
                         'action': 'call Earth',
                         'fried': False,
                         'description': "The radio uses a subspace quantum tunnel to communicate with Earth at greater than lightspeed."}
feature_dict['cabinet'] = {'type': 'object',
                           'item': 'new capacitor',
                           'description': "This is spare parts cabinet"}
feature_dict['floor'] = {'type': 'object',
                         'item': 'old capacitor',
                         'description': "It's a floor."}
feature_dict['grey door'] = {'type': 'door',
                             'title': 'grey door',
                             'state': 'closed',
                             'locked': False,
                             'curr_room': 'quarters',
                             'next_room': 'hall',
                             'description': "The door is an ordinary door."}
feature_dict['blue door'] = {'type': 'door',
                             'title': 'blue door',
                             'state': 'closed',
                             'locked': False,
                             'curr_room': 'hall',
                             'next_room': 'helm',
                             'description': "The door is an ordinary door."}
feature_dict['red door'] = {'type': 'door',
                            'title': 'red door',
                            'state': 'closed',
                            'locked': True,
                            'curr_room': 'hall',
                            'next_room': 'engine room',
                            'description': "The door is an ordinary door."}

item_dict = {}
item_dict['key'] = {'taken': False,
                    'description': "There is a shiny piece of metal. It looks like a key."}
item_dict['gloves'] = {'taken': False,
                       'description': "There is a pair of heavy canvas gloves with a thick rubber coating."}
item_dict['old capacitor'] = {'taken': False,
                              'description': "There is the fallen capacitor. It looks alright. Maybe you should reinsert it in the engine?"}
item_dict['new capacitor'] = {'taken': False,
                              'description': "There is a capacitor that looks a lot like the one that fell from the engine."}

title = " * * * * * * * Space Adventure * * * * * * *"
welcome_message = "You are a crew member of a spaceship travelling to Tau Ceti, a star 12 light-years from Earth.\n" \
                  "The mission is to investigate the planets around Tau Ceti to determine if life exists there and\n" \
                  "if they are capable of supporting human life. After an evening spent in the ship’s tavern, you\n" \
                  "return to your quarters and immediately fall into a deep sleep.\n"\
                  "A sudden jolt wakes you up.\n" \
                  "You feel the vibration of the engines slow, then stop.\n" \
                  "You are alone in your dimly lit room."

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
        item = feature_menu(feature, feature_dict, item_dict)
        if item is not None:
            inventory_list.append(item)

    if feature_dict[feature]['type'] == 'interact':
        feature_interact(feature, feature_dict)

    # If this feature is a door
    if feature_dict[feature]['type'] == 'door':
        room = door_state(feature, feature_dict, room)
